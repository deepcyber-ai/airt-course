# Prepared HumanBound run — Larkfield (Module 4 inspect-track)

A real, recorded HumanBound single-turn (unit) run against neutral Larkfield, saved so a
group can inspect it without spending their own allowance. See `provenance.json` for the
exact command, models, target and hashes.

**Inspect it:**
```bash
python3 modules/module4/native-demo/humanbound/prepared-run/read-results.py
```
It reports the totals, the findings by category, and — for the Module 4 objective — how
many of HumanBound's generated tests disclosed the internal configuration reference
`LARKFIELD-CFG-7Q2X` (8 of 304 in this run), with one example.

**Your task for this track:** inspect the saved run and identify only the tests aimed at
internal-configuration disclosure. Count those as your denominator. HumanBound generates
its own single-turn tests, so this is a different workflow from the other three tracks —
compare the exposure it found, not a matched success rate. `logs.jsonl` holds every
conversation with its verdict, category and explanation; `meta.json` holds the summary.
