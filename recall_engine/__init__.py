"""recall-engine: tiny, dependency-free building blocks for spaced repetition
and "teach-back" (explain it in your own words) scoring.

    from recall_engine import sm2, score_explanation, rating_for
"""
import re

__version__ = "0.1.0"
__all__ = ["RATINGS", "sm2", "score_explanation", "rating_for"]

# Anki-style ratings are easier for a voice assistant to choose than SM-2's 0-5.
RATINGS = {"again": 1, "hard": 3, "good": 4, "easy": 5}


def sm2(quality, repetitions, interval, ease):
    """One SM-2 step.

    quality: 0-5 (use RATINGS to map from a word). Returns the new
    (repetitions, interval_days, ease). Failing a card (quality < 3) resets it
    to a 1-day interval; ease never drops below 1.3.
    """
    if quality < 3:
        repetitions, interval = 0, 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = round(interval * ease)
        repetitions += 1
    ease = max(1.3, ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    return repetitions, interval, ease


def score_explanation(explanation, key_points):
    """Check which key points a spoken explanation covered.

    key_points is a list of {"point": "...", "keywords": ["...", ...]}. A point
    counts as covered if ANY keyword appears at the START of a word, so the
    keyword "photosynthes" matches "photosynthesis" but "light" does not match
    "delightful". Returns (covered_points, missed_points, ratio).
    """
    text = re.sub(r"[^a-z0-9\s]", " ", explanation.lower())
    covered, missed = [], []
    for kp in key_points:
        hit = any(
            re.search(r"\b" + re.escape(kw.lower().strip()), text)
            for kw in kp.get("keywords", [])
            if kw.strip()
        )
        (covered if hit else missed).append(kp["point"])
    ratio = len(covered) / len(key_points) if key_points else 0.0
    return covered, missed, ratio


def rating_for(ratio):
    """Turn explanation coverage (0.0-1.0) into a review rating word."""
    if ratio >= 0.85:
        return "good"
    if ratio >= 0.5:
        return "hard"
    return "again"
