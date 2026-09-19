# Module 7 — Selection & Archetypes (entry point)

Identify attacker behaviour, then make a model-selection decision. Start here, then
open each lab's own README.

**Labs in this folder**
- `m7-archetype/` — the behaviour-identification cards (model identities masked; the
  viewer makes no calls). `archetype_view.py` shows them; `--full` shows the sends.
- `m7-selection/` — the constructed coverage benchmark for the selection decision
  (`benchmark_view.py`)

The archetype cards are heterogeneous single runs — describe the STYLE; they are NOT
a coverage grid or a ranking (use `m7-selection` for the decision). **Shared helpers**
are in the sibling `labs/` folder. Every lab finds `labs/` automatically (or set
`AIRT_COURSE_ROOT`).
