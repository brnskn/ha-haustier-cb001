"""Base entities for Kedi Kumu."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, SIGNAL_UPDATE, VERSION
from .tracker import LitterTracker


class KediKumuEntity(Entity):
    """Entity bound to the tracker; refreshes on every tracker change."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, tracker: LitterTracker, key: str, cat_id: str | None = None) -> None:
        self.tracker = tracker
        self.cat_id = cat_id
        entry_id = tracker.entry.entry_id
        self._attr_translation_key = key
        if cat_id is None:
            self._attr_unique_id = f"{entry_id}_{key}"
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, entry_id)},
                name="Kedi Kumu",
                manufacturer="Haustier",
                model="CB001 kedi takibi",
                sw_version=VERSION,
                via_device_id=tracker.tuya_registry_device_id(),
            )
        else:
            cat = tracker.get_cat(cat_id) or {"name": "Kedi"}
            self._attr_unique_id = f"{entry_id}_{cat_id}_{key}"
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, f"{entry_id}_{cat_id}")},
                name=cat["name"],
                manufacturer="Kedi Kumu",
                model="Kedi",
                via_device_id=tracker.box_registry_device_id(),
            )

    @property
    def cat(self) -> dict | None:
        return self.tracker.get_cat(self.cat_id) if self.cat_id else None

    @property
    def available(self) -> bool:
        return self.cat_id is None or self.cat is not None

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, f"{SIGNAL_UPDATE}_{self.tracker.entry.entry_id}", self.async_write_ha_state
            )
        )
