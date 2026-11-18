"""Hidden settings encode/decode (no Home Assistant needed)."""

import unittest

from _load import load

settings = load("settings")


class TestSettings(unittest.TestCase):
    def test_dnd_matches_app_capture(self):
        # Captured while the app showed Do Not Disturb on, 00:00-01:00
        self.assertEqual(settings.decode_dnd("AAABAAE="), {"start": "00:00", "end": "01:00", "enabled": True})
        self.assertEqual(settings.encode_dnd("00:00", "01:00", True), "AAABAAE=")
        self.assertEqual(settings.decode_dnd(settings.encode_dnd("22:30", "7:05", False)),
                         {"start": "22:30", "end": "07:05", "enabled": False})

    def test_clean_schedule_matches_app_capture(self):
        # App: cleaning schedule 04:00 on, then off
        self.assertEqual(settings.decode_clean_schedule("BAAB"), [{"time": "04:00", "enabled": True}])
        self.assertEqual(settings.decode_clean_schedule("BAAA"), [{"time": "04:00", "enabled": False}])
        self.assertEqual(settings.encode_clean_schedule([{"time": "04:00", "enabled": True}]), "BAAB")
        two = [{"time": "04:00", "enabled": True}, {"time": "16:30", "enabled": False}]
        self.assertEqual(settings.decode_clean_schedule(settings.encode_clean_schedule(two)), two)
        self.assertEqual(settings.decode_clean_schedule(""), [])

    def test_sterilize_schedule_matches_app_capture(self):
        # App: sterilization 02:00 for 5 minutes, on then off
        on = settings.decode_sterilize_schedule("AgAABQE=")
        self.assertEqual(on, [{"time": "02:00", "minutes": 5, "enabled": True}])
        self.assertEqual(settings.encode_sterilize_schedule(on), "AgAABQE=")
        # Thing model example: 0A00 0020 01 = 10:00 for 32 minutes, enabled
        self.assertEqual(settings.decode_sterilize_schedule("CgAAIAE="), [{"time": "10:00", "minutes": 32, "enabled": True}])
        self.assertEqual(settings.encode_sterilize_schedule([{"time": "10:00", "minutes": 32}]), "CgAAIAE=")
        self.assertFalse(settings.decode_sterilize_schedule("AgAABQA=")[0]["enabled"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            settings.encode_dnd("24:00", "01:00", True)
        with self.assertRaises(ValueError):
            settings.encode_sterilize_schedule([{"time": "02:00", "minutes": 0}])
        with self.assertRaises(ValueError):
            settings.encode_clean_schedule([{"time": "01:00"}] * 9)
        self.assertIsNone(settings.decode_dnd("not base64!"))

    def test_decode_settings_merges_sources(self):
        local = {"1": False, "103": True, "109": 7}
        raw = {"105": {"value": "AAABAAE="}, "107": {"value": "BAAA"}, "103": {"value": False}}
        out = settings.decode_settings(local, raw)
        self.assertTrue(out["child_lock"])  # LAN value wins
        self.assertEqual(out["deodorizer_days"], 7)
        self.assertTrue(out["dnd"]["enabled"])
        self.assertEqual(out["clean_schedule"], [{"time": "04:00", "enabled": False}])
        self.assertIsNone(out["sterilize_schedule"])
        self.assertFalse(out["sterilizing"])


if __name__ == "__main__":
    unittest.main()
