"""Estimated waste bag fill level.

The Haustier CB001 only says "bag full" (fault bit) and "drawer out"; it has
no fill level. We count finished cleaning cycles since the bag was last
changed and learn how many cycles fill a bag from the "bag full" events.

- A cleaning cycle (DP 104 kind 5) adds one portion.
- The drawer out for at least ``CHANGE_MIN_SECONDS`` and back in means the
  bag was changed: the counter resets. A quick peek does not.
- When the box reports "bag full", the current count is stored as a
  capacity sample; the capacity is the median of the latest samples.
"""

from __future__ import annotations

from datetime import datetime
from statistics import median
from typing import Any

DEFAULT_CAPACITY = 40
CHANGE_MIN_SECONDS = 30
MIN_SAMPLE = 5
MAX_SAMPLES = 6


class WasteBin:
    """Serializable bag fill estimator."""

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        data = data or {}
        self.count: int = int(data.get("count", 0))
        self.since: str | None = data.get("since")
        self.samples: list[int] = [int(x) for x in data.get("samples", [])][-MAX_SAMPLES:]
        self.out_since: str | None = data.get("out_since")
        self.full: bool = bool(data.get("full", False))

    def to_dict(self) -> dict[str, Any]:
        return {
            "count": self.count,
            "since": self.since,
            "samples": self.samples,
            "out_since": self.out_since,
            "full": self.full,
        }

    # ---------------------------------------------------------------- model
    @property
    def learned(self) -> bool:
        return bool(self.samples)

    @property
    def capacity(self) -> int:
        return int(round(median(self.samples))) if self.samples else DEFAULT_CAPACITY

    @property
    def percent(self) -> int:
        if self.full:
            return 100
        return min(99, round(self.count / max(1, self.capacity) * 100))

    def info(self) -> dict[str, Any]:
        return {
            "percent": self.percent,
            "count": self.count,
            "capacity": self.capacity,
            "learned": self.learned,
            "since": self.since,
            "full": self.full,
            "drawer_out": self.out_since is not None,
        }

    # ---------------------------------------------------------------- events
    def on_clean(self) -> None:
        self.count += 1

    def on_full(self, full: bool) -> None:
        if full and not self.full and self.count >= MIN_SAMPLE:
            self.samples = (self.samples + [self.count])[-MAX_SAMPLES:]
        self.full = full

    def on_drawer(self, out: bool, now: datetime) -> bool:
        """Track the drawer; returns True when this counts as a bag change."""
        if out:
            if self.out_since is None:
                self.out_since = now.isoformat()
            return False
        if self.out_since is None:
            return False
        started = datetime.fromisoformat(self.out_since)
        self.out_since = None
        if (now - started).total_seconds() >= CHANGE_MIN_SECONDS:
            self.reset(now)
            return True
        return False

    def reset(self, now: datetime) -> None:
        self.count = 0
        self.full = False
        self.since = now.isoformat()
