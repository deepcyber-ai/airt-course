# Module 7 — Selecting Attackers & Scorers

First, read the selected attack conversations and describe what the attacker does. Then
use the supplied comparison results (`MODULE7-SELECTION-HANDOUT.md`) to choose two
attackers, a primary scorer and a fallback for the assigned objectives. Explain what the
second attacker adds and what evidence supports your scorer choice.

The conversation cards illustrate behaviour in individual runs. They do not establish a
model's overall success rate. The constructed PyRIT examples in `m7-selection/` show how
an evaluation can be presented; their invented numbers are not evidence of actual model
performance — use the measured results in the selection handout for the decision.

**In this folder**
- `m7-archetype/` — the attack conversation cards (model identities masked; the viewer
  makes no calls). `archetype_view.py` shows them.
- `m7-selection/` — two constructed examples of the evaluation interface
  (`benchmark_view.py`, `scorer_eval_view.py`), for reading a comparison — not the
  measured evidence.
- `MODULE7-SELECTION-HANDOUT.md` — the **measured** attacker and scorer comparisons for
  the selection decision.

Shared helpers are in the sibling `labs/` folder; every lab finds `labs/` automatically
(or set `AIRT_COURSE_ROOT`).
