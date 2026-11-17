"""Binary sensors for Kedi Kumu."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .entity import KediKumuEntity
from .tracker import LitterTracker


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    tracker: LitterTracker = hass.data[DOMAIN]
    async_add_entities([ScaleSuspect(tracker), Occupied(tracker)])


class ScaleSuspect(KediKumuEntity, BinarySensorEntity):
    """On when a weight matched no cat: the scale probably needs a power cycle."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, tracker: LitterTracker) -> None:
        super().__init__(tracker, "scale_suspect")

    @property
    def is_on(self) -> bool:
        return self.tracker.scale_suspect


class Occupied(KediKumuEntity, BinarySensorEntity):
    """On while a cat is in the box."""

    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    def __init__(self, tracker: LitterTracker) -> None:
        super().__init__(tracker, "occupied")

    @property
    def is_on(self) -> bool:
        return self.tracker.current is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        cur = self.tracker.current
        if not cur:
            return {}
        cat = self.tracker.get_cat(cur.get("cat_id") or cur.get("suggestion"))
        return {"kedi": cat["name"] if cat else None, "agirlik_kg": round(cur["weight"] / 1000, 2)}
