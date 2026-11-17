"""Websocket API used by the Kedi Kumu card."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN


def _tracker(hass: HomeAssistant):
    return hass.data.get(DOMAIN)


@callback
def async_register_websocket(hass: HomeAssistant) -> None:
    for handler in (ws_data, ws_subscribe, ws_save_cat, ws_delete_cat, ws_assign, ws_delete_visit, ws_reset_scale):
        websocket_api.async_register_command(hass, handler)


def _not_ready(connection, msg) -> None:
    connection.send_error(msg["id"], "not_ready", "Kedi Kumu kurulu değil")


@websocket_api.websocket_command({vol.Required("type"): "kedi_kumu/data", vol.Optional("limit", default=600): int})
@callback
def ws_data(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    tracker = _tracker(hass)
    if tracker is None:
        _not_ready(connection, msg)
        return
    connection.send_result(msg["id"], tracker.snapshot(min(max(msg["limit"], 10), 3000)))


@websocket_api.websocket_command({vol.Required("type"): "kedi_kumu/subscribe"})
@callback
def ws_subscribe(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    tracker = _tracker(hass)
    if tracker is None:
        _not_ready(connection, msg)
        return

    @callback
    def changed() -> None:
        connection.send_message(websocket_api.event_message(msg["id"], {"changed": True}))

    connection.subscriptions[msg["id"]] = tracker.subscribe(changed)
    connection.send_result(msg["id"])


@websocket_api.websocket_command(
    {
        vol.Required("type"): "kedi_kumu/cat/save",
        vol.Optional("cat_id"): vol.Any(None, str),
        vol.Optional("name"): vol.All(str, vol.Length(min=1, max=40)),
        vol.Optional("color"): vol.Match(r"^#[0-9a-fA-F]{6}$"),
        vol.Optional("hint_kg"): vol.Any(None, vol.All(vol.Coerce(float), vol.Range(min=0, max=20))),
        vol.Optional("photo"): str,
        vol.Optional("remove_photo", default=False): bool,
    }
)
@websocket_api.async_response
async def ws_save_cat(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    tracker = _tracker(hass)
    if tracker is None:
        _not_ready(connection, msg)
        return
    try:
        cat = await tracker.async_save_cat(
            msg.get("cat_id"),
            name=msg.get("name"),
            color=msg.get("color"),
            hint_kg=msg.get("hint_kg") if "hint_kg" in msg else None,
            photo=msg.get("photo"),
            remove_photo=msg["remove_photo"],
        )
    except ValueError as err:
        connection.send_error(msg["id"], "invalid", str(err))
        return
    connection.send_result(msg["id"], cat)


@websocket_api.websocket_command({vol.Required("type"): "kedi_kumu/cat/delete", vol.Required("cat_id"): str})
@websocket_api.async_response
async def ws_delete_cat(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    tracker = _tracker(hass)
    if tracker is None:
        _not_ready(connection, msg)
        return
    try:
        await tracker.async_delete_cat(msg["cat_id"])
    except ValueError as err:
        connection.send_error(msg["id"], "invalid", str(err))
        return
    connection.send_result(msg["id"])


@websocket_api.websocket_command(
    {vol.Required("type"): "kedi_kumu/visit/assign", vol.Required("visit_id"): str, vol.Required("cat_id"): vol.Any(None, str)}
)
@callback
def ws_assign(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    tracker = _tracker(hass)
    if tracker is None:
        _not_ready(connection, msg)
        return
    try:
        visit = tracker.assign(msg["visit_id"], msg["cat_id"])
    except ValueError as err:
        connection.send_error(msg["id"], "invalid", str(err))
        return
    connection.send_result(msg["id"], visit)


@websocket_api.websocket_command({vol.Required("type"): "kedi_kumu/visit/delete", vol.Required("visit_id"): str})
@callback
def ws_delete_visit(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    tracker = _tracker(hass)
    if tracker is None:
        _not_ready(connection, msg)
        return
    try:
        tracker.delete_visit(msg["visit_id"])
    except ValueError as err:
        connection.send_error(msg["id"], "invalid", str(err))
        return
    connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): "kedi_kumu/reset_scale"})
@callback
def ws_reset_scale(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None:
    tracker = _tracker(hass)
    if tracker is None:
        _not_ready(connection, msg)
        return
    tracker.reset_scale_warning()
    connection.send_result(msg["id"])
