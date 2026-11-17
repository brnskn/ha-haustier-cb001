"""Core of Kedi Kumu: visit assembly, cat profiles, learning and storage."""

from __future__ import annotations

import base64
import binascii
from collections import deque
from collections.abc import Callable
from datetime import datetime, timedelta
import logging
from pathlib import Path
import secrets
from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .classifier import build_model, classify, should_learn
from .const import (
    BOX_STATES,
    CONF_MIN_MANUAL,
    CONF_NOTIFY,
    CONF_TUYA_DEVICE_ID,
    DEFAULT_MIN_MANUAL,
    DOMAIN,
    DP_DURATION_DAY,
    DP_RECORD,
    DP_STATUS,
    EVENT_ANOMALY,
    EVENT_VISIT,
    MAX_SAMPLES,
    MAX_VISITS,
    NOT_CAT,
    NOTIFY_ACTION_PREFIX,
    SIGNAL_CAT_ADDED,
    SIGNAL_CAT_REMOVED,
    SIGNAL_UPDATE,
    ST_AUTO,
    ST_MANUAL,
    ST_NOT_CAT,
    ST_PENDING,
    URL_PHOTOS,
    VISIT_TIMEOUT,
)
from .protocol import (
    REC_CLEAN_DONE,
    REC_DURATION,
    REC_OUT,
    REC_WEIGHT,
    parse_record,
)

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
CAT_COLORS = ["#f4a261", "#2a9d8f", "#e76f51", "#8e7dbe", "#e9c46a", "#4ea8de"]
MAX_PHOTO_BYTES = 4 * 1024 * 1024
PHOTO_TYPES = {b"\xff\xd8\xff": "jpg", b"\x89PNG": "png", b"RIFF": "webp"}


def _new_id(length: int = 8) -> str:
    return secrets.token_hex(length // 2)


def _ms_to_iso(ms: int | None) -> str:
    if ms:
        return dt_util.utc_from_timestamp(ms / 1000).isoformat()
    return dt_util.utcnow().isoformat()


class LitterTracker:
    """Keeps cats and visits, listens to the Tuya litter box."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self.device_id: str = entry.data[CONF_TUYA_DEVICE_ID]
        self._store: Store = Store(hass, STORAGE_VERSION, f"{DOMAIN}.{entry.entry_id}")
        self.cats: list[dict] = []
        self.visits: list[dict] = []
        self.last_clean: str | None = None
        self.scale_suspect = False
        self.status = "standby"
        self.current: dict | None = None
        self._seen: deque = deque(maxlen=300)
        self._timeout_unsub: CALLBACK_TYPE | None = None
        self._subscribers: set[Callable[[], None]] = set()
        self._hooked_manager: Any = None
        self.photo_dir = Path(hass.config.path(DOMAIN, "photos"))

    # ------------------------------------------------------------------ setup
    @property
    def min_manual(self) -> int:
        return int(self.entry.options.get(CONF_MIN_MANUAL, DEFAULT_MIN_MANUAL))

    @property
    def notify_services(self) -> list[str]:
        return list(self.entry.options.get(CONF_NOTIFY, []))

    async def async_load(self) -> None:
        data = await self._store.async_load() or {}
        self.cats = data.get("cats", [])
        self.visits = data.get("visits", [])
        self.last_clean = data.get("last_clean")
        self.scale_suspect = data.get("scale_suspect", False)
        await self.hass.async_add_executor_job(
            lambda: self.photo_dir.mkdir(parents=True, exist_ok=True)
        )

    def _data_to_save(self) -> dict:
        return {
            "cats": self.cats,
            "visits": self.visits[-MAX_VISITS:],
            "last_clean": self.last_clean,
            "scale_suspect": self.scale_suspect,
        }

    def _save(self) -> None:
        self._store.async_delay_save(self._data_to_save, 3)

    async def async_flush(self) -> None:
        await self._store.async_save(self._data_to_save())

    # ------------------------------------------------------------- tuya hook
    @callback
    def async_ensure_hook(self, *_: Any) -> None:
        """Attach to the Tuya manager that owns our device (idempotent)."""
        for entry in self.hass.config_entries.async_entries("tuya"):
            if entry.state is not ConfigEntryState.LOADED:
                continue
            manager = getattr(getattr(entry, "runtime_data", None), "manager", None)
            if manager is None or self.device_id not in getattr(manager, "device_map", {}):
                continue
            current = manager.__dict__.get("_on_device_report")
            if current is not None and getattr(current, "_kedi_kumu", False):
                self._hooked_manager = manager
                return
            original = manager._on_device_report  # bound method of the class
            loop = self.hass.loop
            device_id = self.device_id
            handler = self._handle_report

            def _on_device_report(dev_id: str, status: list, _orig=original):
                if dev_id == device_id:
                    try:
                        loop.call_soon_threadsafe(handler, [dict(i) for i in status])
                    except RuntimeError:
                        pass
                return _orig(dev_id, status)

            _on_device_report._kedi_kumu = True  # type: ignore[attr-defined]
            manager._on_device_report = _on_device_report
            self._hooked_manager = manager
            _LOGGER.info("Attached to Tuya device %s", device_id)
            return

    @callback
    def async_unhook(self) -> None:
        manager = self._hooked_manager
        if manager is not None and "_on_device_report" in manager.__dict__:
            del manager.__dict__["_on_device_report"]
        self._hooked_manager = None

    def tuya_registry_device_id(self) -> str | None:
        registry = dr.async_get(self.hass)
        for device in registry.devices.values():
            if ("tuya", self.device_id) in device.identifiers:
                return device.id
        return None

    def box_registry_device_id(self) -> str | None:
        device = dr.async_get(self.hass).async_get_device_by_identifier(
            (DOMAIN, self.entry.entry_id), self.entry.entry_id
        )
        return device.id if device else None

    @callback
    def async_ensure_box_device(self) -> None:
        dr.async_get(self.hass).async_get_or_create(
            config_entry_id=self.entry.entry_id,
            identifiers={(DOMAIN, self.entry.entry_id)},
            name="Kedi Kumu",
            manufacturer="Haustier",
            model="CB001 kedi takibi",
            via_device_id=self.tuya_registry_device_id(),
        )

    @property
    def hooked(self) -> bool:
        return self._hooked_manager is not None

    # ------------------------------------------------------------ messages
    @callback
    def _handle_report(self, status: list[dict]) -> None:
        changed = False
        for item in sorted(status, key=lambda i: (i.get("t") or 0)):
            key = (item.get("dpId"), item.get("t"), str(item.get("value")))
            if key in self._seen:
                continue
            self._seen.append(key)
            dp = item.get("dpId")
            value = item.get("value")
            t = item.get("t")
            if dp == DP_STATUS and isinstance(value, str):
                new = value if value in BOX_STATES else "other"
                if new != self.status:
                    self.status = new
                    changed = True
            elif dp == DP_DURATION_DAY and self.current and isinstance(value, int):
                self.current.setdefault("duration", value)
            elif dp == DP_RECORD:
                rec = parse_record(value)
                if rec is None:
                    continue
                _LOGGER.debug("Record %s", rec)
                changed |= self._on_record(rec.kind, rec.value, t)
        if changed:
            self._notify_change()

    def _on_record(self, kind: int, value: int, t: int | None) -> bool:
        if kind == REC_WEIGHT:
            if self.current is not None:
                self._finish_visit(t)
            self._start_visit(value, t)
            return True
        if kind == REC_DURATION and self.current is not None:
            self.current["duration"] = value
            return True
        if kind == REC_OUT and self.current is not None:
            self._finish_visit(t)
            return True
        if kind == REC_CLEAN_DONE:
            self.last_clean = _ms_to_iso(t)
            self._save()
            return True
        return False

    def _start_visit(self, weight: int, t: int | None) -> None:
        result = classify(weight, self.cats, self.min_manual)
        self.current = {
            "id": _new_id(10),
            "start": _ms_to_iso(t),
            "end": None,
            "weight": weight,
            "duration": None,
            "cat_id": result.cat_id,
            "status": result.status,
            "suggestion": result.suggestion,
            "confidence": result.confidence,
            "reason": result.reason,
            "anomaly": result.anomaly,
            "learned": False,
        }
        if self._timeout_unsub:
            self._timeout_unsub()
        self._timeout_unsub = async_call_later(
            self.hass, VISIT_TIMEOUT, self._timeout_visit
        )

    @callback
    def _timeout_visit(self, _now: datetime) -> None:
        self._timeout_unsub = None
        if self.current is not None:
            self._finish_visit(None)
            self._notify_change()

    def _finish_visit(self, t: int | None) -> None:
        visit = self.current
        if visit is None:
            return
        self.current = None
        if self._timeout_unsub:
            self._timeout_unsub()
            self._timeout_unsub = None
        visit["end"] = _ms_to_iso(t)
        if visit.get("duration") is None:
            start = dt_util.parse_datetime(visit["start"])
            end = dt_util.parse_datetime(visit["end"])
            if start and end:
                visit["duration"] = max(0, int((end - start).total_seconds()))
        self._store_visit(visit)

    def _store_visit(self, visit: dict) -> None:
        self.visits.append(visit)
        if len(self.visits) > MAX_VISITS:
            del self.visits[: len(self.visits) - MAX_VISITS]

        if visit["status"] == ST_AUTO and visit["cat_id"]:
            cat = self.get_cat(visit["cat_id"])
            if cat is not None:
                self._learn(cat, visit, manual=False)
            if self.scale_suspect and visit["confidence"] >= 0.6:
                self.scale_suspect = False
        if visit.get("anomaly"):
            self.scale_suspect = True
            self.hass.bus.async_fire(
                EVENT_ANOMALY,
                {"visit_id": visit["id"], "weight": visit["weight"], "reason": visit["reason"]},
            )
        self._fire_visit_event(visit)
        if visit["status"] == ST_PENDING:
            self.hass.async_create_task(self._async_send_question(visit))
        self._save()

    def _fire_visit_event(self, visit: dict) -> None:
        cat = self.get_cat(visit["cat_id"]) if visit.get("cat_id") else None
        self.hass.bus.async_fire(
            EVENT_VISIT,
            {
                "visit_id": visit["id"],
                "cat_id": visit.get("cat_id"),
                "cat_name": cat["name"] if cat else None,
                "status": visit["status"],
                "weight_kg": round(visit["weight"] / 1000, 2) if visit.get("weight") else None,
                "duration": visit.get("duration"),
                "start": visit["start"],
            },
        )

    # ------------------------------------------------------------ learning
    def _learn(self, cat: dict, visit: dict, manual: bool) -> None:
        weight = visit.get("weight")
        if not weight:
            visit["learned"] = False
            return
        if not manual or cat.get("manual_count", 0) >= self.min_manual:
            if not should_learn(weight, cat, self.min_manual):
                visit["learned"] = False
                return
        cat.setdefault("samples", []).append(
            {"w": weight, "t": visit["start"], "v": visit["id"], "src": "manual" if manual else "auto"}
        )
        cat["samples"] = cat["samples"][-MAX_SAMPLES:]
        if manual:
            cat["manual_count"] = cat.get("manual_count", 0) + 1
        visit["learned"] = True

    def _unlearn(self, visit_id: str) -> None:
        for cat in self.cats:
            samples = cat.get("samples", [])
            for s in samples:
                if s.get("v") == visit_id:
                    samples.remove(s)
                    if s.get("src") == "manual":
                        cat["manual_count"] = max(0, cat.get("manual_count", 0) - 1)
                    break

    def _reclassify_pending(self) -> None:
        """Re-run recognition on still-open questions after the model changed."""
        for visit in self.visits:
            if visit["status"] != ST_PENDING:
                continue
            result = classify(visit.get("weight"), self.cats, self.min_manual)
            visit["suggestion"] = result.suggestion
            visit["confidence"] = result.confidence
            visit["reason"] = result.reason

    # ------------------------------------------------------------ queries
    def get_cat(self, cat_id: str | None) -> dict | None:
        return next((c for c in self.cats if c["id"] == cat_id), None)

    def get_visit(self, visit_id: str) -> dict | None:
        return next((v for v in reversed(self.visits) if v["id"] == visit_id), None)

    def photo_url(self, cat: dict) -> str | None:
        if cat.get("photo"):
            return f"{URL_PHOTOS}/{cat['photo']}"
        return None

    def cat_visits(self, cat_id: str) -> list[dict]:
        return [v for v in self.visits if v.get("cat_id") == cat_id and v["status"] in (ST_AUTO, ST_MANUAL)]

    def visits_today(self, cat_id: str | None = None) -> int:
        today = dt_util.now().date()
        count = 0
        for v in reversed(self.visits):
            start = dt_util.parse_datetime(v["start"])
            if start is None:
                continue
            local = dt_util.as_local(start).date()
            if local < today - timedelta(days=1):
                break
            if local != today or v["status"] == ST_NOT_CAT:
                continue
            if cat_id is None or v.get("cat_id") == cat_id:
                count += 1
        return count

    def last_visit(self, cat_id: str | None = None) -> dict | None:
        for v in reversed(self.visits):
            if v["status"] == ST_NOT_CAT:
                continue
            if cat_id is None or v.get("cat_id") == cat_id:
                return v
        return None

    def pending(self) -> list[dict]:
        return [v for v in self.visits if v["status"] == ST_PENDING]

    def cat_info(self, cat: dict) -> dict:
        model = build_model(cat, self.min_manual)
        last = self.last_visit(cat["id"])
        return {
            "id": cat["id"],
            "name": cat["name"],
            "color": cat.get("color"),
            "photo": self.photo_url(cat),
            "hint": cat.get("hint"),
            "center": round(model.center) if model.center else None,
            "spread": round(model.spread),
            "manual_count": model.manual,
            "samples": model.samples,
            "trained": model.trained,
            "last_weight": last.get("weight") if last else None,
            "last_visit": last.get("start") if last else None,
            "today": self.visits_today(cat["id"]),
            "created": cat.get("created"),
        }

    def controls(self) -> dict:
        """Entity ids of the Tuya litter box entities, for the card."""
        out: dict[str, str] = {}
        registry = er.async_get(self.hass)
        prefix = f"tuya.{self.device_id}"
        wanted = {
            "manual_clean": "clean",
            "light": "light",
            "fault_full_fault": "bag_full",
            "fault_box_out": "lid",
            "auto_clean": "auto_clean",
            "status": "tuya_status",
            "delay_clean_time": "clean_delay",
        }
        for ent in registry.entities.values():
            if ent.platform != "tuya" or not ent.unique_id.startswith(prefix):
                continue
            code = ent.unique_id[len(prefix):]
            if code in wanted:
                out[wanted[code]] = ent.entity_id
        mine = {
            ent.unique_id.removeprefix(f"{self.entry.entry_id}_"): ent.entity_id
            for ent in er.async_entries_for_config_entry(registry, self.entry.entry_id)
        }
        out["entities"] = mine  # type: ignore[assignment]
        return out

    def snapshot(self, visit_limit: int = 600) -> dict:
        return {
            "cats": [self.cat_info(c) for c in self.cats],
            "visits": self.visits[-visit_limit:],
            "current": self.current,
            "status": self.status,
            "last_clean": self.last_clean,
            "scale_suspect": self.scale_suspect,
            "min_manual": self.min_manual,
            "hooked": self.hooked,
            "controls": self.controls(),
            "notify": bool(self.notify_services),
        }

    # ------------------------------------------------------------ changes
    def subscribe(self, cb: Callable[[], None]) -> Callable[[], None]:
        self._subscribers.add(cb)
        return lambda: self._subscribers.discard(cb)

    @callback
    def _notify_change(self) -> None:
        async_dispatcher_send(self.hass, f"{SIGNAL_UPDATE}_{self.entry.entry_id}")
        for cb in list(self._subscribers):
            cb()

    @callback
    def async_day_changed(self, *_: Any) -> None:
        self._notify_change()

    # --------------------------------------------------------- cat editing
    async def async_save_cat(
        self,
        cat_id: str | None,
        name: str | None = None,
        color: str | None = None,
        hint_kg: float | None = None,
        photo: str | None = None,
        remove_photo: bool = False,
    ) -> dict:
        new = cat_id is None
        if new:
            if not name:
                raise ValueError("name_required")
            used = {c.get("color") for c in self.cats}
            cat = {
                "id": _new_id(8),
                "name": name.strip()[:40],
                "color": color or next((c for c in CAT_COLORS if c not in used), CAT_COLORS[0]),
                "samples": [],
                "manual_count": 0,
                "created": dt_util.utcnow().isoformat(),
            }
        else:
            cat = self.get_cat(cat_id)
            if cat is None:
                raise ValueError("unknown_cat")
            if name:
                cat["name"] = name.strip()[:40]
            if color:
                cat["color"] = color
        if hint_kg is not None:
            cat["hint"] = round(hint_kg * 1000) if hint_kg > 0 else None
        if remove_photo and cat.get("photo"):
            await self._async_delete_photo(cat["photo"])
            cat["photo"] = None
        if photo:
            old = cat.get("photo")
            cat["photo"] = await self._async_write_photo(photo)
            if old:
                await self._async_delete_photo(old)
        if new:
            self.cats.append(cat)
            async_dispatcher_send(self.hass, f"{SIGNAL_CAT_ADDED}_{self.entry.entry_id}", cat["id"])
        else:
            self._update_cat_device(cat)
        self._reclassify_pending()
        self._save()
        self._notify_change()
        return self.cat_info(cat)

    async def async_delete_cat(self, cat_id: str) -> None:
        cat = self.get_cat(cat_id)
        if cat is None:
            raise ValueError("unknown_cat")
        self.cats.remove(cat)
        if cat.get("photo"):
            await self._async_delete_photo(cat["photo"])
        for v in self.visits:
            if v.get("cat_id") == cat_id:
                v["cat_id"] = None
                v["status"] = ST_PENDING
            if v.get("suggestion") == cat_id:
                v["suggestion"] = None
        # Old history of a removed cat should not flood the question list.
        cutoff = dt_util.utcnow() - timedelta(days=2)
        for v in self.visits:
            if v["status"] == ST_PENDING and v.get("cat_id") is None:
                start = dt_util.parse_datetime(v["start"])
                if start and start < cutoff and not v.get("suggestion"):
                    v["status"] = ST_NOT_CAT
                    v["reason"] = "cat_deleted"
        async_dispatcher_send(self.hass, f"{SIGNAL_CAT_REMOVED}_{self.entry.entry_id}", cat_id)
        self._reclassify_pending()
        self._save()
        self._notify_change()

    def _update_cat_device(self, cat: dict) -> None:
        registry = dr.async_get(self.hass)
        device = registry.async_get_device_by_identifier((DOMAIN, f"{self.entry.entry_id}_{cat['id']}"), self.entry.entry_id)
        if device is not None and device.name != cat["name"]:
            registry.async_update_device(device.id, name=cat["name"])

    async def _async_write_photo(self, data_url: str) -> str:
        payload = data_url.split(",", 1)[1] if data_url.startswith("data:") else data_url
        try:
            raw = base64.b64decode(payload, validate=True)
        except (binascii.Error, ValueError) as err:
            raise ValueError("bad_photo") from err
        if len(raw) > MAX_PHOTO_BYTES:
            raise ValueError("photo_too_large")
        ext = next((e for magic, e in PHOTO_TYPES.items() if raw.startswith(magic)), None)
        if ext is None:
            raise ValueError("bad_photo")
        name = f"{secrets.token_hex(12)}.{ext}"
        path = self.photo_dir / name
        await self.hass.async_add_executor_job(path.write_bytes, raw)
        return name

    async def _async_delete_photo(self, name: str) -> None:
        path = self.photo_dir / Path(name).name

        def _rm() -> None:
            if path.is_file():
                path.unlink()

        await self.hass.async_add_executor_job(_rm)

    # ------------------------------------------------------- visit editing
    def assign(self, visit_id: str, cat_id: str | None) -> dict:
        """Label a visit. cat_id None/'none' means "not a cat"."""
        visit = self.get_visit(visit_id)
        if visit is None:
            raise ValueError("unknown_visit")
        self._unlearn(visit_id)
        if cat_id in (None, NOT_CAT):
            visit["cat_id"] = None
            visit["status"] = ST_NOT_CAT
            visit["learned"] = False
        else:
            cat = self.get_cat(cat_id)
            if cat is None:
                raise ValueError("unknown_cat")
            visit["cat_id"] = cat_id
            visit["status"] = ST_MANUAL
            self._learn(cat, visit, manual=True)
        visit["anomaly"] = False
        self._reclassify_pending()
        self._save()
        self._notify_change()
        self.hass.async_create_task(self._async_clear_question(visit_id))
        return visit

    def delete_visit(self, visit_id: str) -> None:
        visit = self.get_visit(visit_id)
        if visit is None:
            raise ValueError("unknown_visit")
        self._unlearn(visit_id)
        self.visits.remove(visit)
        self._reclassify_pending()
        self._save()
        self._notify_change()
        self.hass.async_create_task(self._async_clear_question(visit_id))

    def add_manual_visit(self, weight: int, start: datetime | None, duration: int | None) -> dict:
        start_dt = start or dt_util.utcnow()
        result = classify(weight, self.cats, self.min_manual)
        visit = {
            "id": _new_id(10),
            "start": dt_util.as_utc(start_dt).isoformat(),
            "end": dt_util.as_utc(start_dt + timedelta(seconds=duration or 0)).isoformat(),
            "weight": weight,
            "duration": duration,
            "cat_id": result.cat_id,
            "status": result.status,
            "suggestion": result.suggestion,
            "confidence": result.confidence,
            "reason": result.reason,
            "anomaly": result.anomaly,
            "learned": False,
            "source": "manual_entry",
        }
        self._store_visit(visit)
        self.visits.sort(key=lambda v: v["start"])
        self._notify_change()
        return visit

    def reset_scale_warning(self) -> None:
        self.scale_suspect = False
        self._save()
        self._notify_change()

    # ------------------------------------------------------- notifications
    async def _async_send_question(self, visit: dict) -> None:
        services = self.notify_services
        if not services or not self.cats:
            return
        local = dt_util.as_local(dt_util.parse_datetime(visit["start"]))
        weight = f"{visit['weight'] / 1000:.2f}".replace(".", ",") if visit.get("weight") else "?"
        parts = [f"{weight} kg", local.strftime("%H:%M")]
        if visit.get("duration"):
            parts.insert(1, f"{visit['duration']} sn")
        suggestion = self.get_cat(visit.get("suggestion"))
        message = " · ".join(parts)
        if suggestion:
            message += f"\nTahminim: {suggestion['name']}"
        if visit.get("anomaly"):
            message += "\nBu ağırlık hiçbir kediye uymuyor; tartı kaymış olabilir."
        actions = [
            {"action": f"{NOTIFY_ACTION_PREFIX}_{visit['id']}_{c['id']}", "title": c["name"]}
            for c in self.cats[:8]
        ]
        actions.append(
            {"action": f"{NOTIFY_ACTION_PREFIX}_{visit['id']}_{NOT_CAT}", "title": "Kedi değil", "destructive": True}
        )
        data = {
            "tag": f"kedi_kumu_{visit['id']}",
            "group": "kedi_kumu",
            "actions": actions,
            "push": {"interruption-level": "passive"},
        }
        for service in services:
            try:
                await self.hass.services.async_call(
                    "notify",
                    service,
                    {"title": "🐾 Kumu kim kullandı?", "message": message, "data": data},
                    blocking=False,
                )
            except Exception as err:  # noqa: BLE001
                _LOGGER.warning("Notification via %s failed: %s", service, err)

    async def _async_clear_question(self, visit_id: str) -> None:
        for service in self.notify_services:
            try:
                await self.hass.services.async_call(
                    "notify",
                    service,
                    {"message": "clear_notification", "data": {"tag": f"kedi_kumu_{visit_id}"}},
                    blocking=False,
                )
            except Exception:  # noqa: BLE001
                pass

    @callback
    def async_handle_notification_action(self, event: Event) -> None:
        action = str(event.data.get("action", ""))
        if not action.startswith(f"{NOTIFY_ACTION_PREFIX}_"):
            return
        try:
            _, visit_id, cat_id = action.split("_", 2)
            self.assign(visit_id, cat_id)
        except ValueError as err:
            _LOGGER.debug("Ignoring notification action %s: %s", action, err)
