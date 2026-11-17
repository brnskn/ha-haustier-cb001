"""Waste bag fill estimate (no Home Assistant needed)."""

from datetime import datetime, timedelta, timezone
import unittest

from _load import load

waste = load("waste")
T0 = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)


class TestWasteBin(unittest.TestCase):
    def test_counts_cleans_against_default_capacity(self):
        b = waste.WasteBin()
        for _ in range(10):
            b.on_clean()
        self.assertEqual(b.count, 10)
        self.assertFalse(b.learned)
        self.assertEqual(b.percent, round(10 / waste.DEFAULT_CAPACITY * 100))

    def test_full_event_learns_capacity_and_shows_100(self):
        b = waste.WasteBin()
        for _ in range(28):
            b.on_clean()
        b.on_full(True)
        self.assertEqual(b.percent, 100)
        self.assertTrue(b.learned)
        self.assertEqual(b.capacity, 28)
        b.on_full(True)  # repeated report does not add a second sample
        self.assertEqual(b.samples, [28])

    def test_bag_change_needs_drawer_out_long_enough(self):
        b = waste.WasteBin()
        for _ in range(12):
            b.on_clean()
        b.on_drawer(True, T0)
        self.assertFalse(b.on_drawer(False, T0 + timedelta(seconds=8)))  # quick peek
        self.assertEqual(b.count, 12)
        b.on_drawer(True, T0 + timedelta(minutes=1))
        self.assertTrue(b.on_drawer(False, T0 + timedelta(minutes=2)))
        self.assertEqual(b.count, 0)
        self.assertEqual(b.since, (T0 + timedelta(minutes=2)).isoformat())

    def test_change_clears_full_and_relearns(self):
        b = waste.WasteBin()
        for size in (30, 34, 32):
            for _ in range(size):
                b.on_clean()
            b.on_full(True)
            b.reset(T0)
        self.assertEqual(b.samples, [30, 34, 32])
        self.assertEqual(b.capacity, 32)
        self.assertFalse(b.full)
        self.assertEqual(b.percent, 0)

    def test_tiny_counts_are_not_capacity_samples(self):
        b = waste.WasteBin()
        b.on_clean()
        b.on_full(True)  # e.g. a stale fault right after a reset
        self.assertFalse(b.learned)

    def test_roundtrip(self):
        b = waste.WasteBin()
        for _ in range(7):
            b.on_clean()
        b.on_drawer(True, T0)
        c = waste.WasteBin(b.to_dict())
        self.assertEqual(c.to_dict(), b.to_dict())
        self.assertTrue(c.info()["drawer_out"])
        self.assertLess(c.percent, 100)


if __name__ == "__main__":
    unittest.main()
