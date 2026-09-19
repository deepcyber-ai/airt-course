# Module 7 — selecting attackers and scorers (constructed views)

Two **constructed** PyRIT 1.0.1 evaluation-interface examples (neutral candidates), shown to teach *how you read* an
attacker comparison and *how you validate* a judge — **not run live** in class
(the full benchmark is many model calls). The hands-on beat of Module 7 is the
20-minute *selection* exercise (analytical, from these numbers), and the live
attacker comparison is the small Module 6 two-attacker activity.

```bash
python3 modules/module7/m7-selection/benchmark_view.py     # AdversarialBenchmark — attacker comparison
python3 modules/module7/m7-selection/scorer_eval_view.py   # scorer.evaluate_async — judge vs labelled cases
```

- **`benchmark_view`** (`AdversarialBenchmark`): attackers × objectives with N and
  every denominator shown, invalid/error/unverified kept visible. The lesson is
  **coverage and elapsed time** — pick the attacker per objective, and note the
  time (not a financial cost) — not a single winner. One run per cell would not support a ranking.
- **`scorer_eval_view`** (`scorer.evaluate_async`): a judge scored against
  **reference-labelled** cases -> agreement on one named cohort, reported beside
  the always-FAILURE baseline (lift), with mismatches kept visible. The lesson is **validate before
  you trust**: agreement is with the label, not certified accuracy, and a high
  score can hide an evidence-rule break (case L5) or a missed confabulation (L6).

Both fixtures are labelled **CONSTRUCTED** - neutral candidates, synthetic figures, built against the inspected PyRIT 1.0.1 interfaces. They are NOT recorded runs or measured model performance (the private
`research/module67-source-notes/pyrit-evaluation.md` carries the official sources).
