"""Run with `python tests/test_engine.py` (no dependencies) or `pytest`."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from recall_engine import RATINGS, rating_for, score_explanation, sm2  # noqa: E402

PHOTO = [
    {"point": "plants use sunlight", "keywords": ["sunlight", "light"]},
    {"point": "chlorophyll captures the light", "keywords": ["chlorophyll"]},
    {"point": "carbon dioxide and water go in", "keywords": ["carbon dioxide", "co2"]},
    {"point": "glucose and oxygen come out", "keywords": ["glucose", "sugar"]},
]


def test_sm2_interval_progression():
    reps, interval, ease = 0, 0, 2.5
    reps, interval, ease = sm2(RATINGS["good"], reps, interval, ease)
    assert (reps, interval) == (1, 1)
    reps, interval, ease = sm2(RATINGS["good"], reps, interval, ease)
    assert (reps, interval) == (2, 6)
    reps, interval, ease = sm2(RATINGS["good"], reps, interval, ease)
    assert reps == 3 and interval == round(6 * 2.5)


def test_sm2_failure_resets_and_ease_has_floor():
    reps, interval, ease = sm2(RATINGS["again"], 5, 30, 2.5)
    assert (reps, interval) == (0, 1)
    for _ in range(20):
        reps, interval, ease = sm2(RATINGS["again"], reps, interval, ease)
    assert ease == 1.3


def test_score_explanation():
    covered, missed, ratio = score_explanation(
        "Plants take in Sunlight and CO2, and chlorophyll helps.", PHOTO
    )
    assert len(covered) == 3 and missed == ["glucose and oxygen come out"]
    assert ratio == 0.75


def test_keywords_match_word_starts_only():
    kp = [{"point": "p", "keywords": ["photosynthes"]}]
    assert score_explanation("photosynthesis", kp)[0] == ["p"]
    assert score_explanation("delightful", [{"point": "p", "keywords": ["light"]}])[0] == []


def test_empty_inputs_are_safe():
    assert score_explanation("anything", []) == ([], [], 0.0)
    assert score_explanation("", PHOTO)[2] == 0.0


def test_rating_for_thresholds():
    assert rating_for(1.0) == "good"
    assert rating_for(0.85) == "good"
    assert rating_for(0.6) == "hard"
    assert rating_for(0.49) == "again"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print(f"{len(tests)} passed")
