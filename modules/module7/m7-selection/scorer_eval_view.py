"""Module 7 — CONSTRUCTED view: scorer.evaluate_async (judge vs labelled cases).

    python3 modules/module7/m7-selection/scorer_eval_view.py

A CONSTRUCTED PyRIT scorer-evaluation interface example with a NEUTRAL judge
placeholder, shown to teach how you VALIDATE a judge against cases with
independently supported reference labels — before trusting it. It is NOT a
recorded run and NOT a measured model result. The hands-on beat is the 20-minute
selection exercise.

(c) 2026 Deep Cyber Ltd. Apache 2.0 licensed.
"""
import json
from pathlib import Path

e = json.loads((Path(__file__).resolve().parent / "fixtures" / "scorer-evaluation.json").read_text())
m = e["metrics"]
print("\n=== Module 7 · scorer.evaluate_async — CONSTRUCTED example (not a live run) ===")
print(f"  interface: {e['pyrit_interface']}")
print(f"  scorer: {e['scorer']}   trials: {e['num_scorer_trials']}")
print(f"  objective: {e['objective']}")
print(f"  cohort: {m['cohort']}\n")
print(f"  {'case':6} {'reference':14} {'judge verdict':14} {'agree'}")
for c in e["cases"]:
    mark = "ok" if c["agree"] else "MISMATCH"
    print(f"  {c['id']:6} {c['reference_label']:14} {c['scorer_verdict']:14} {mark}   ({c['reply_summary']})")
print(f"\n  agreement {m['agreements']}/{m['n']} = {m['agreement_pct']}%  |  "
      f"always-FAILURE baseline {m['always_failure_baseline_pct']}%  |  lift {m['lift_points']:+} pts")
print(f"  ({m['alt_cohort_note']})")
print("\n  How to read it (the validation lesson):")
print("   - Agreement is with the reference LABEL, not certified accuracy. Report it beside")
print("     the always-FAILURE baseline (lift), on ONE named cohort, mismatches visible.")
print("   - L5: judge said SUCCESS on a claim with NO evidence — it broke the evidence")
print("     rule; UNVERIFIED was the right label. A high score can hide that.")
print("   - L6: judge missed a confabulation the label counts as success. Two errors, two")
print("     causes — validate on labelled cases before trusting a judge on unlabelled ones.")
