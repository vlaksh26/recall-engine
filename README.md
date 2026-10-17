# recall-engine

Tiny, dependency-free building blocks for **spaced repetition** and
**teach-back scoring** (checking that someone can explain an idea in their own
words). Pure Python, no packages to install, MIT licensed.

It was extracted from [Recall](https://github.com/vlaksh26/recall-alexa-mcp), a
voice study tutor built as an MCP server for Alexa+, so other voice and MCP
projects can reuse the same logic.

## What's inside
| Function | What it does |
|---|---|
| `sm2(quality, repetitions, interval, ease)` | One step of the SM-2 spaced-repetition algorithm. Returns the new `(repetitions, interval_days, ease)` |
| `RATINGS` | Maps `again`, `hard`, `good`, `easy` to SM-2 quality scores, which are easier for a voice assistant to pick than 0-5 |
| `score_explanation(text, key_points)` | Checks which key points a spoken explanation covered. Returns `(covered, missed, ratio)` |
| `rating_for(ratio)` | Turns coverage into a rating word: `good` (85% or more), `hard` (50% or more), else `again` |

Keywords match at the **start of a word**, so `"photosynthes"` matches
"photosynthesis", while `"light"` does not match "delightful".

## Example
```python
from recall_engine import sm2, score_explanation, rating_for, RATINGS

# Schedule a card: first successful review
reps, interval, ease = sm2(RATINGS["good"], 0, 0, 2.5)
print(reps, interval, round(ease, 2))   # 1 1 2.5  -> due again in 1 day

# Score a spoken explanation
points = [
    {"point": "uses sunlight", "keywords": ["sunlight"]},
    {"point": "makes sugar", "keywords": ["sugar", "glucose"]},
]
covered, missed, ratio = score_explanation("Plants use sunlight", points)
print(covered, missed, ratio, rating_for(ratio))
# ['uses sunlight'] ['makes sugar'] 0.5 hard
```

## Install
```
pip install git+https://github.com/vlaksh26/recall-engine
```
Requires Python 3.9 or newer.

## Test
```
python tests/test_engine.py
```

## License
MIT
