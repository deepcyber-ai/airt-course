# Module 6 — Attackers & Scorers (entry point)

Compare attackers, and compare a marker scorer against an LLM judge. Start here, then
open each lab's own README.

**Labs in this folder**
- `m6-attacker-eval/` — two attackers × three objectives, batched, on the 6/7/12
  persisted ledger
- `scorer-exercise/` — marker vs LLM scoring, the criterion FLIP, and the run-input
  path (`score_exercise.py --offline` uses saved labels, no calls)

**Shared helpers** are in the sibling `labs/` folder (`labs/CHOOSING-MODELS.md`,
`labs/models.py`, `labs/budget.py`). Every lab finds `labs/` automatically (or set
`AIRT_COURSE_ROOT`).
