"""Decoder for the Haustier CB001 event record (Tuya DP 104).

The device reports every litter box event as a 9 byte raw value:

    YY MM DD hh mm ss  KIND  VALUE(uint16, big endian)

Observed kinds:
    0  cat near the box (presence sensor)
    1  cat left the box
    2  visit finished, VALUE = time spent in seconds
    3  cat entered the box, VALUE = cat weight in grams
    5  cleaning cycle finished
"""

from __future__ import annotations

import base64
import binascii
from dataclasses import dataclass

REC_PRESENCE = 0
REC_OUT = 1
REC_DURATION = 2
REC_WEIGHT = 3
REC_CLEAN_DONE = 5


@dataclass(frozen=True)
class Record:
    """A decoded DP 104 record."""

    kind: int
    value: int
    device_time: str  # "2026-11-17 19:21:55" in the device's local time
    raw: str


def parse_record(value: str) -> Record | None:
    """Decode a base64 DP 104 value. Returns None when it is not a record."""
    if not isinstance(value, str):
        return None
    try:
        data = base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError):
        return None
    if len(data) < 9:
        return None
    yy, mm, dd, hh, mi, ss, kind = data[:7]
    val = int.from_bytes(data[7:9], "big")
    stamp = f"{2000 + yy:04d}-{mm:02d}-{dd:02d} {hh:02d}:{mi:02d}:{ss:02d}"
    return Record(kind=kind, value=val, device_time=stamp, raw=value)
