"""Weight based cat recognition.

Each cat keeps its recent weight samples. A cat's model is the median of its
samples and a robust spread (MAD). A visit is assigned automatically only when
the nearest cat is trained (has enough manual labels), the weight is close to
it and clearly closer to it than to any other cat. Everything else is left for
the household to pick, with a suggestion.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median

from .const import ST_AUTO, ST_NOT_CAT, ST_PENDING

MIN_CAT_WEIGHT = 500  # g, anything lighter is not a cat (empty scale, litter dust)
MAX_CAT_WEIGHT = 15000  # g
MIN_SPREAD = 60  # g
DEFAULT_SPREAD = 150  # g, used until a cat has 3 samples
HINT_SPREAD = 250  # g, used when only the owner's estimate is known
AUTO_MAX_Z = 3.0
AUTO_MAX_DIFF = 450  # g
AUTO_MIN_GAP_Z = 1.5
AUTO_MIN_GAP_G = 120  # g
SUGGEST_MAX_Z = 4.5
LEARN_MAX_Z = 4.0
LEARN_MAX_DIFF = 600  # g
WINDOW = 15


@dataclass
class CatModel:
    """Weight model of one cat."""

    cat_id: str
    center: float | None
    spread: float
    samples: int
    manual: int
    trained: bool


@dataclass
class Result:
    """Outcome of classifying a weight."""

    status: str
    cat_id: str | None = None
    suggestion: str | None = None
    confidence: float = 0.0
    anomaly: bool = False
    reason: str = ""


def build_model(cat: dict, min_manual: int) -> CatModel:
    """Build the weight model of a cat."""
    weights = [s["w"] for s in cat.get("samples", [])][-WINDOW:]
    manual = int(cat.get("manual_count", 0))
    if weights:
        center = float(median(weights))
        if len(weights) >= 3:
            mad = median(abs(w - center) for w in weights) * 1.4826
            spread = max(mad, MIN_SPREAD)
        else:
            spread = DEFAULT_SPREAD
    elif cat.get("hint"):
        center = float(cat["hint"])
        spread = HINT_SPREAD
    else:
        center = None
        spread = DEFAULT_SPREAD
    return CatModel(
        cat_id=cat["id"],
        center=center,
        spread=spread,
        samples=len(weights),
        manual=manual,
        trained=manual >= min_manual,
    )


def classify(weight: float | None, cats: list[dict], min_manual: int) -> Result:
    """Decide which cat a weight belongs to."""
    if weight is None:
        return Result(ST_PENDING, reason="no_weight")
    if weight < MIN_CAT_WEIGHT or weight > MAX_CAT_WEIGHT:
        return Result(ST_NOT_CAT, anomaly=True, reason="out_of_range")
    if not cats:
        return Result(ST_PENDING, reason="no_cats")

    models = [build_model(c, min_manual) for c in cats]
    known = [m for m in models if m.center is not None]
    if not known:
        return Result(ST_PENDING, reason="untrained")

    ranked = sorted(
        ((abs(weight - m.center) / m.spread, abs(weight - m.center), m) for m in known),
        key=lambda x: x[0],
    )
    z1, d1, best = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None

    suggestion = best.cat_id if (z1 <= SUGGEST_MAX_Z or d1 <= 500) else None
    gap_ok = True
    if second is not None:
        z2, d2, _ = second
        gap_ok = (z2 - z1) >= AUTO_MIN_GAP_Z and (d2 - d1) >= AUTO_MIN_GAP_G

    # Confidence: closeness to the best cat, scaled by separation from the next.
    closeness = max(0.0, 1.0 - z1 / (AUTO_MAX_Z * 2))
    if second is not None:
        sep = min(1.0, (second[0] - z1) / (AUTO_MIN_GAP_Z * 2))
    else:
        sep = 1.0
    confidence = round(max(0.0, min(0.99, closeness * (0.5 + 0.5 * sep))), 2)

    all_known = len(known) == len(models)
    all_trained = all(m.trained for m in models)
    if (
        best.trained
        and all_known
        and z1 <= AUTO_MAX_Z
        and d1 <= AUTO_MAX_DIFF
        and gap_ok
    ):
        return Result(
            ST_AUTO,
            cat_id=best.cat_id,
            suggestion=best.cat_id,
            confidence=confidence,
            reason="match",
        )

    anomaly = all_trained and z1 > SUGGEST_MAX_Z and d1 > 400
    reason = "no_match" if anomaly else ("ambiguous" if not gap_ok else "learning")
    return Result(
        ST_PENDING,
        suggestion=suggestion,
        confidence=confidence,
        anomaly=anomaly,
        reason=reason,
    )


def should_learn(weight: float, cat: dict, min_manual: int) -> bool:
    """Whether a weight assigned to a cat should become a training sample.

    A trained cat ignores weights far from its model, so a mis-weighed visit
    (e.g. after the scale drifted) does not poison the model.
    """
    model = build_model(cat, min_manual)
    if not model.trained or model.center is None:
        return True
    diff = abs(weight - model.center)
    return diff / model.spread <= LEARN_MAX_Z or diff <= LEARN_MAX_DIFF
