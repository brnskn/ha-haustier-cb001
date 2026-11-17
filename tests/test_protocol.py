"""DP 104 record decoding (no Home Assistant needed)."""

import base64
import unittest

from _load import load

protocol = load("protocol")


class TestProtocol(unittest.TestCase):
    def test_weight_record(self):
        rec = protocol.parse_record("GgsRExU3Aw7E")
        self.assertEqual(rec.kind, protocol.REC_WEIGHT)
        self.assertEqual(rec.value, 3780)
        self.assertEqual(rec.device_time, "2026-11-17 19:21:55")

    def test_duration_out_clean(self):
        self.assertEqual(protocol.parse_record("GgsRExYlAgAq").value, 42)
        self.assertEqual(protocol.parse_record("GgsRExYlAQAA").kind, protocol.REC_OUT)
        self.assertEqual(protocol.parse_record("GgsRExg1BQAA").kind, protocol.REC_CLEAN_DONE)
        self.assertEqual(protocol.parse_record("GgsREDMMAAAA").kind, protocol.REC_PRESENCE)

    def test_rejects_garbage(self):
        self.assertIsNone(protocol.parse_record("standby"))
        self.assertIsNone(protocol.parse_record(123))
        self.assertIsNone(protocol.parse_record(base64.b64encode(b"\x01\x02").decode()))


if __name__ == "__main__":
    unittest.main()
