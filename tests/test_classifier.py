"""Weight based cat recognition (no Home Assistant needed)."""

import unittest

from _load import load

classifier = load("classifier")
const = load("const")


def cat(cid, weights=(), manual=0, hint=None):
    return {"id": cid, "name": cid, "samples": [{"w": w, "src": "manual"} for w in weights], "manual_count": manual, "hint": hint}


TRAINED = [cat("a", [3780, 3800, 3760], 3), cat("b", [4600, 4650, 4580], 3), cat("c", [5500, 5450, 5520], 3)]


class TestClassifier(unittest.TestCase):
    def test_untrained_asks(self):
        res = classifier.classify(3780, [cat("a"), cat("b")], 3)
        self.assertEqual(res.status, const.ST_PENDING)

    def test_not_a_cat(self):
        self.assertEqual(classifier.classify(200, TRAINED, 3).status, const.ST_NOT_CAT)
        self.assertEqual(classifier.classify(20000, TRAINED, 3).status, const.ST_NOT_CAT)

    def test_learning_phase_suggests(self):
        cats = [cat("a", [3780, 3800], 2), cat("b", hint=4600), cat("c", hint=5500)]
        res = classifier.classify(3790, cats, 3)
        self.assertEqual((res.status, res.suggestion), (const.ST_PENDING, "a"))

    def test_trained_auto(self):
        res = classifier.classify(3820, TRAINED, 3)
        self.assertEqual((res.status, res.cat_id), (const.ST_AUTO, "a"))
        self.assertGreater(res.confidence, 0.5)
        self.assertEqual(classifier.classify(5480, TRAINED, 3).cat_id, "c")

    def test_between_cats_asks(self):
        self.assertEqual(classifier.classify(4200, TRAINED, 3).status, const.ST_PENDING)

    def test_similar_cats_are_ambiguous(self):
        close = [cat("a", [4000, 4020, 3990], 3), cat("b", [4100, 4080, 4120], 3)]
        res = classifier.classify(4050, close, 3)
        self.assertEqual((res.status, res.reason), (const.ST_PENDING, "ambiguous"))

    def test_anomaly_flags_scale(self):
        res = classifier.classify(7800, TRAINED, 3)
        self.assertEqual(res.status, const.ST_PENDING)
        self.assertTrue(res.anomaly)

    def test_outliers_not_learned(self):
        self.assertFalse(classifier.should_learn(6000, TRAINED[0], 3))
        self.assertTrue(classifier.should_learn(3900, TRAINED[0], 3))


if __name__ == "__main__":
    unittest.main()
