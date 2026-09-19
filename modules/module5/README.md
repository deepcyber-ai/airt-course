# Module 5 — Multi-Turn Techniques (entry point)

Multi-turn / adaptive attacks. Start here, then open each lab's own README.

**Labs in this folder**
- `pyrit/` — the technique stages (single / crescendo / goat / tap / pair), with a
  transport ledger and read-only evidence (starter + complete)
- `m5-transition/` — the closing reveal (illustrative saved trace, labelled)
- `m5-attempt/` — the deeper PAIR attempt with the dual request cap ENFORCED
  (`deeper_attempt.py --self-test` proves the cap offline, no model calls)

**Shared helpers** are in the sibling `labs/` folder (`labs/CHOOSING-MODELS.md`,
`labs/models.py`, `labs/budget.py`, `labs/reset.sh`). Every lab finds `labs/`
automatically (or set `AIRT_COURSE_ROOT`). Keep to the per-pair request allowance.
