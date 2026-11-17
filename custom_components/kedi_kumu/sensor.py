"""Sensors for Kedi Kumu."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfMass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.util import dt as dt_util

from .const import BOX_STATES, DOMAIN, SIGNAL_CAT_ADDED, SIGNAL_CAT_REMOVED
from .entity import KediKumuEntity
from .tracker import LitterTracker


def _ts(value: str | None):
    return dt_util.parse_datetime(value) if value else None


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    tracker: LitterTracker = hass.data[DOMAIN]

    def cat_entities(cat_id: str) -> list[SensorEntity]:
        return [CatWeight(tracker, cat_id), CatLastVisit(tracker, cat_id), CatVisitsToday(tracker, cat_id)]

    entities: list[SensorEntity] = [
        BoxStatus(tracker),
        LastCat(tracker),
        PendingVisits(tracker),
        VisitsToday(tracker),
        LastClean(tracker),
    ]
    for cat in tracker.cats:
        entities.extend(cat_entities(cat["id"]))
    async_add_entities(entities)

    @callback
    def cat_added(cat_id: str) -> None:
        async_add_entities(cat_entities(cat_id))

    @callback
    def cat_removed(cat_id: str) -> None:
        dev_reg = dr.async_get(hass)
        device = dev_reg.async_get_device_by_identifier((DOMAIN, f"{entry.entry_id}_{cat_id}"), entry.entry_id)
        ent_reg = er.async_get(hass)
        if device is not None:
            for ent in er.async_entries_for_device(ent_reg, device.id, include_disabled_entities=True):
                ent_reg.async_remove(ent.entity_id)
            dev_reg.async_remove_device(device.id)

    entry.async_on_unload(async_dispatcher_connect(hass, f"{SIGNAL_CAT_ADDED}_{entry.entry_id}", cat_added))
    entry.async_on_unload(async_dispatcher_connect(hass, f"{SIGNAL_CAT_REMOVED}_{entry.entry_id}", cat_removed))


# ---------------------------------------------------------------- box level
class BoxStatus(KediKumuEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = BOX_STATES

    def __init__(self, tracker: LitterTracker) -> None:
        super().__init__(tracker, "status")

    @property
    def native_value(self) -> str:
        return self.tracker.status

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        cur = self.tracker.current
        cat = self.tracker.get_cat(cur.get("cat_id") or cur.get("suggestion")) if cur else None
        return {
            "kedi": cat["name"] if cat else None,
            "kedi_kesin": bool(cur and cur.get("cat_id")),
            "agirlik_kg": round(cur["weight"] / 1000, 2) if cur and cur.get("weight") else None,
            "baglanti": self.tracker.hooked,
        }


class LastCat(KediKumuEntity, SensorEntity):
    def __init__(self, tracker: LitterTracker) -> None:
        super().__init__(tracker, "last_cat")

    @property
    def _visit(self) -> dict | None:
        return self.tracker.last_visit()

    @property
    def native_value(self) -> str | None:
        visit = self._visit
        if visit is None:
            return None
        cat = self.tracker.get_cat(visit.get("cat_id"))
        return cat["name"] if cat else "Bilinmiyor"

    @property
    def entity_picture(self) -> str | None:
        visit = self._visit
        cat = self.tracker.get_cat(visit.get("cat_id")) if visit else None
        return self.tracker.photo_url(cat) if cat else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        visit = self._visit
        if visit is None:
            return {}
        return {
            "agirlik_kg": round(visit["weight"] / 1000, 2) if visit.get("weight") else None,
            "sure_sn": visit.get("duration"),
            "zaman": visit.get("start"),
            "durum": visit.get("status"),
            "guven": visit.get("confidence"),
            "ziyaret_id": visit.get("id"),
        }


class PendingVisits(KediKumuEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, tracker: LitterTracker) -> None:
        super().__init__(tracker, "pending")

    @property
    def native_value(self) -> int:
        return len(self.tracker.pending())


class VisitsToday(KediKumuEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, tracker: LitterTracker) -> None:
        super().__init__(tracker, "visits_today")

    @property
    def native_value(self) -> int:
        return self.tracker.visits_today()


class LastClean(KediKumuEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, tracker: LitterTracker) -> None:
        super().__init__(tracker, "last_clean")

    @property
    def native_value(self):
        return _ts(self.tracker.last_clean)


# ---------------------------------------------------------------- per cat
class CatWeight(KediKumuEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.WEIGHT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_suggested_display_precision = 2

    def __init__(self, tracker: LitterTracker, cat_id: str) -> None:
        super().__init__(tracker, "cat_weight", cat_id)

    @property
    def native_value(self) -> float | None:
        visits = [v for v in self.tracker.cat_visits(self.cat_id) if v.get("weight") and v.get("learned")]
        if visits:
            return round(visits[-1]["weight"] / 1000, 3)
        cat = self.cat
        if cat and cat.get("hint"):
            return round(cat["hint"] / 1000, 3)
        return None

    @property
    def entity_picture(self) -> str | None:
        cat = self.cat
        return self.tracker.photo_url(cat) if cat else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        cat = self.cat
        if cat is None:
            return {}
        info = self.tracker.cat_info(cat)
        return {
            "ortalama_kg": round(info["center"] / 1000, 2) if info["center"] else None,
            "taniyor": info["trained"],
            "etiket_sayisi": info["manual_count"],
        }


class CatLastVisit(KediKumuEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, tracker: LitterTracker, cat_id: str) -> None:
        super().__init__(tracker, "cat_last_visit", cat_id)

    @property
    def native_value(self):
        visit = self.tracker.last_visit(self.cat_id)
        return _ts(visit["start"]) if visit else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        visit = self.tracker.last_visit(self.cat_id)
        if visit is None:
            return {}
        return {"sure_sn": visit.get("duration"), "agirlik_kg": round(visit["weight"] / 1000, 2) if visit.get("weight") else None}


class CatVisitsToday(KediKumuEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, tracker: LitterTracker, cat_id: str) -> None:
        super().__init__(tracker, "cat_visits_today", cat_id)

    @property
    def native_value(self) -> int:
        return self.tracker.visits_today(self.cat_id)

