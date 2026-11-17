"""Haustier CB001 settings that live outside the Tuya cloud schema.

Mapped by toggling each setting in the Tuya app and watching the device:

    DP 1    manual UV sterilization, bool; runs until switched off
            (in the cloud schema as "switch")
    DP 102  level litter, bool trigger                 (status becomes "smooth")
    DP 103  child lock, bool
    DP 105  do not disturb, raw: start_h start_m end_h end_m enabled
    DP 106  sterilization schedule, raw: 5 bytes per entry
            hour minute flags minutes enabled
    DP 107  cleaning schedule, raw: 3 bytes per entry: hour minute enabled
    DP 109  deodorizer days left, int

Raw values travel base64 encoded, as in the Tuya app.
"""

from __future__ import annotations

import base64
import binascii
import re
from typing import Any

DP_STERILIZE = 1
DP_LEVEL = 102
DP_CHILD_LOCK = 103
DP_DND = 105
DP_STERILIZE_SCHEDULE = 106
DP_CLEAN_SCHEDULE = 107
DP_DEODORIZER_DAYS = 109

MAX_SCHEDULE_ENTRIES = 8
_TIME_RE = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")


def _b64(value: Any) -> bytes | None:
    if not isinstance(value, str):
        return None
    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError):
        return None


def _enc(data: bytes) -> str:
    return base64.b64encode(data).decode()


def _hm(h: int, m: int) -> str:
    return f"{h:02d}:{m:02d}"


def parse_time(value: str) -> tuple[int, int]:
    match = _TIME_RE.match(str(value).strip())
    if not match:
        raise ValueError(f"invalid time {value!r}")
    return int(match.group(1)), int(match.group(2))


# ---------------------------------------------------------------- DND
def decode_dnd(value: Any) -> dict[str, Any] | None:
    data = _b64(value)
    if not data or len(data) < 5:
        return None
    return {"start": _hm(data[0], data[1]), "end": _hm(data[2], data[3]), "enabled": bool(data[4])}


def encode_dnd(start: str, end: str, enabled: bool) -> str:
    sh, sm = parse_time(start)
    eh, em = parse_time(end)
    return _enc(bytes([sh, sm, eh, em, 1 if enabled else 0]))


# ---------------------------------------------------------------- schedules
def decode_clean_schedule(value: Any) -> list[dict[str, Any]] | None:
    data = _b64(value)
    if data is None:
        return None
    return [
        {"time": _hm(data[i], data[i + 1]), "enabled": bool(data[i + 2])}
        for i in range(0, len(data) - len(data) % 3, 3)
    ]


def encode_clean_schedule(entries: list[dict[str, Any]]) -> str:
    if len(entries) > MAX_SCHEDULE_ENTRIES:
        raise ValueError("too many entries")
    out = bytearray()
    for entry in entries:
        h, m = parse_time(entry["time"])
        out += bytes([h, m, 1 if entry.get("enabled", True) else 0])
    return _enc(bytes(out))


def decode_sterilize_schedule(value: Any) -> list[dict[str, Any]] | None:
    data = _b64(value)
    if data is None:
        return None
    return [
        {
            "time": _hm(data[i], data[i + 1]),
            "flags": data[i + 2],
            "minutes": data[i + 3],
            "enabled": bool(data[i + 4]),
        }
        for i in range(0, len(data) - len(data) % 5, 5)
    ]


def encode_sterilize_schedule(entries: list[dict[str, Any]]) -> str:
    if len(entries) > MAX_SCHEDULE_ENTRIES:
        raise ValueError("too many entries")
    out = bytearray()
    for entry in entries:
        h, m = parse_time(entry["time"])
        minutes = int(entry.get("minutes", 5))
        if not 1 <= minutes <= 60:
            raise ValueError("minutes must be 1-60")
        flags = int(entry.get("flags", 0)) & 0xFF
        out += bytes([h, m, flags, minutes, 1 if entry.get("enabled", True) else 0])
    return _enc(bytes(out))


# ---------------------------------------------------------------- summary
def decode_settings(local_dps: dict[str, Any], raw_dps: dict[str, Any]) -> dict[str, Any]:
    """Merge LAN status and the last pushed raw values into readable settings."""

    def get(dp: int) -> Any:
        key = str(dp)
        if key in local_dps:
            return local_dps[key]
        item = raw_dps.get(key)
        return item.get("value") if isinstance(item, dict) else None

    days = get(DP_DEODORIZER_DAYS)
    return {
        "sterilizing": bool(get(DP_STERILIZE)) if get(DP_STERILIZE) is not None else None,
        "child_lock": get(DP_CHILD_LOCK) if isinstance(get(DP_CHILD_LOCK), bool) else None,
        "deodorizer_days": days if isinstance(days, int) else None,
        "dnd": decode_dnd(get(DP_DND)),
        "clean_schedule": decode_clean_schedule(get(DP_CLEAN_SCHEDULE)),
        "sterilize_schedule": decode_sterilize_schedule(get(DP_STERILIZE_SCHEDULE)),
    }
