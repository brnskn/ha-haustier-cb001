"""Haustier CB001 settings that live outside the Tuya cloud schema.

From the device's Tuya thing model (product nietgqxmysgyf988), confirmed by
toggling each setting in the Tuya app and watching the device:

    DP 1    switch            UV sterilize + deodorize, bool; runs until off
    DP 101  pour_sand         empty the litter into the bag, bool trigger
                              (status becomes "clear_sand"; the app calls it "Kum Ekle")
    DP 102  smooth_sand       level the litter, bool trigger (status "smooth")
    DP 103  child_lock        bool
    DP 105  sleep_onoff_time  do not disturb, raw: start_h start_m end_h end_m enabled
    DP 106  uv_onoff_time     sterilization schedule, raw, 5 bytes per entry:
                              hour minute minutes(uint16 BE) enabled
    DP 107  clean_onoff_time  cleaning schedule, raw, 3 bytes per entry: hour minute enabled
    DP 108  filter_reset      deodorizer filter replaced, bool trigger
    DP 109  filter_days       deodorizer filter days left, 0-30

Raw values travel base64 encoded, as in the Tuya app.
"""

from __future__ import annotations

import base64
import binascii
import re
from typing import Any

DP_STERILIZE = 1
DP_POUR_SAND = 101
DP_LEVEL = 102
DP_CHILD_LOCK = 103
DP_DND = 105
DP_STERILIZE_SCHEDULE = 106
DP_CLEAN_SCHEDULE = 107
DP_FILTER_RESET = 108
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
            "minutes": int.from_bytes(data[i + 2 : i + 4], "big"),
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
        if not 1 <= minutes <= 120:
            raise ValueError("minutes must be 1-120")
        out += bytes([h, m]) + minutes.to_bytes(2, "big") + bytes([1 if entry.get("enabled", True) else 0])
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
