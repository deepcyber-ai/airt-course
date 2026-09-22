# Module 7 — selecting attackers and scorers (constructed views)

**OPTIONAL AFTER-COURSE REFERENCE**

These two constructed examples show how to read an attacker comparison and how to test a
scorer against labelled reference cases. The viewers make no model calls. All figures are
invented for teaching, so do not use them to rank real models or make the classroom
selection. Base that decision on the measured course results in
`MODULE7-SELECTION-HANDOUT.md`. Technical interface names such as `AdversarialBenchmark` are
explained below as reference material; you do not need them before the exercise.

```bash
python3 modules/module7/m7-selection/benchmark_view.py     # AdversarialBenchmark — attacker comparison
python3 modules/module7/m7-selection/scorer_eval_view.py   # scorer.evaluate_async — judge vs labelled cases
```

- **`benchmark_view`** (`AdversarialBenchmark`) shows attacker results by objective. It gives
  the sample size and denominator for every cell and keeps invalid, error and unverified
  outcomes visible. Use it to practise choosing an attacker for each objective and considering
  elapsed time. Elapsed time is not a financial cost, and one run per cell cannot support a
  ranking.
- **`scorer_eval_view`** (`scorer.evaluate_async`) compares a judge with cases that have
  reference labels. It reports agreement for one named group of cases beside an
  always-`FAILURE` baseline, with mismatches kept visible. Use it to see why a scorer must be
  validated before use. Agreement with a label is not proof of accuracy, and a high figure can
  hide an unsupported verdict in case L5 or a missed fabrication in case L6.

Both fixtures are marked **CONSTRUCTED**. They use neutral candidate names and synthetic
figures based on the inspected PyRIT 1.0.1 interfaces. They are not recorded runs or measured
model performance. Technical source details are kept in the private
`research/module67-source-notes/pyrit-evaluation.md`.
