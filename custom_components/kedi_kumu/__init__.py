"""Kedi Kumu: cat recognition and visit tracking for the Haustier CB001 litter box."""

from __future__ import annotations

from datetime import timedelta
import hashlib
import logging
from pathlib import Path

import voluptuous as vol

from homeassistant.components.frontend import add_extra_js_url
from aiohttp import web

from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.event import async_track_time_change, async_track_time_interval
from homeassistant.helpers.start import async_at_started
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, URL_CARD, URL_PHOTOS, VERSION
from .tracker import LitterTracker
from .websocket import async_register_websocket

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

ADD_VISIT_SCHEMA = vol.Schema(
    {
        vol.Required("weight_kg"): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=20)),
        vol.Optional("start"): cv.datetime,
        vol.Optional("duration"): vol.All(vol.Coerce(int), vol.Range(min=0, max=3600)),
    }
)


def _card_url() -> str:
    path = Path(__file__).parent / "frontend" / "kedi-kumu-card.js"
    digest = hashlib.sha1(path.read_bytes()).hexdigest()[:8]
    return f"{URL_CARD}?v={VERSION}-{digest}"


class CardView(HomeAssistantView):
    """Serve the card with "no-cache" so browsers revalidate (ETag) on every load.

    Without it, a card updated while Home Assistant keeps running stays stale in
    browsers and the companion apps until the URL's version changes at restart.
    """

    url = URL_CARD
    name = "kedi_kumu:card"
    requires_auth = False

    def __init__(self, path: Path) -> None:
        self.path = path

    async def get(self, request: web.Request) -> web.FileResponse:
        return web.FileResponse(
            self.path,
            headers={"Cache-Control": "no-cache", "Content-Type": "text/javascript; charset=utf-8"},
        )


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register the card, static paths, websocket commands and services."""
    photo_dir = Path(hass.config.path(DOMAIN, "photos"))
    await hass.async_add_executor_job(lambda: photo_dir.mkdir(parents=True, exist_ok=True))
    card = Path(__file__).parent / "frontend" / "kedi-kumu-card.js"
    await hass.http.async_register_static_paths([StaticPathConfig(URL_PHOTOS, str(photo_dir), True)])
    hass.http.register_view(CardView(card))
    add_extra_js_url(hass, await hass.async_add_executor_job(_card_url))
    async_register_websocket(hass)

    def _tracker() -> LitterTracker:
        tracker = hass.data.get(DOMAIN)
        if tracker is None:
            raise ServiceValidationError("Kedi Kumu kurulu değil")
        return tracker

    async def add_visit(call: ServiceCall) -> None:
        _tracker().add_manual_visit(
            round(call.data["weight_kg"] * 1000),
            call.data.get("start"),
            call.data.get("duration"),
        )

    async def reset_scale(call: ServiceCall) -> None:
        _tracker().reset_scale_warning()

    async def reset_bin(call: ServiceCall) -> None:
        _tracker().reset_bin()

    hass.services.async_register(DOMAIN, "add_visit", add_visit, schema=ADD_VISIT_SCHEMA)
    hass.services.async_register(DOMAIN, "reset_scale_warning", reset_scale)
    hass.services.async_register(DOMAIN, "reset_waste_bin", reset_bin)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the tracker for a litter box."""
    tracker = LitterTracker(hass, entry)
    await tracker.async_load()
    hass.data[DOMAIN] = tracker
    tracker.async_ensure_box_device()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    tracker.async_ensure_hook()
    # The Tuya entry can load after us or be reloaded; keep re-attaching.
    entry.async_on_unload(
        async_track_time_interval(hass, tracker.async_ensure_hook, timedelta(seconds=30))
    )
    entry.async_on_unload(async_at_started(hass, tracker.async_ensure_hook))
    entry.async_on_unload(
        async_track_time_change(hass, tracker.async_day_changed, hour=0, minute=0, second=5)
    )
    entry.async_on_unload(
        hass.bus.async_listen("mobile_app_notification_action", tracker.async_handle_notification_action)
    )
    async def _refresh_local(*_):
        await tracker.async_local_status()

    entry.async_on_unload(async_track_time_interval(hass, _refresh_local, timedelta(minutes=10)))
    # Runs right away on a reload (e.g. after changing options), or once HA has started.
    entry.async_on_unload(async_at_started(hass, _refresh_local))
    entry.async_on_unload(entry.add_update_listener(_async_reload))
    return True


async def _async_reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload."""
    tracker: LitterTracker | None = hass.data.get(DOMAIN)
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok and tracker is not None:
        tracker.async_unhook()
        await tracker.async_flush()
        hass.data.pop(DOMAIN, None)
    return ok
