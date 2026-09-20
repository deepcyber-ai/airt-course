"""Module 7 — CONSTRUCTED view: AdversarialBenchmark (attacker comparison).

    python3 modules/module7/m7-selection/benchmark_view.py

A CONSTRUCTED PyRIT AdversarialBenchmark interface example with NEUTRAL candidates
(attacker-A/B/C), shown to teach how you READ an attacker comparison — coverage
and elapsed time, which attacker for which objective. It is NOT a recorded run and
NOT measured model performance; the figures are synthetic and illustrate the
method, not any named vendor's strength.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
"""
import json
from collections import defaultdict
from pathlib import Path

b = json.loads((Path(__file__).resolve().parent / "fixtures" / "adversarial-benchmark.json").read_text())
n = b["n_per_cell"]
objs = sorted({c["objective"] for c in b["cells"]})
by = {(c["attacker"], c["objective"]): c for c in b["cells"]}
cost = defaultdict(lambda: [0, 0])
for c in b["cells"]:
    cost[c["attacker"]][0] += c["attacker_calls"]
    cost[c["attacker"]][1] += c["elapsed_s"]


def cell_str(c):
    # show the COUNT of each non-aimed outcome, not just its presence
    extra = " ".join(f"{lbl}{c[k]}" for lbl, k in (("i", "invalid"), ("e", "error"), ("u", "unverified")) if c[k])
    return f"{c['aimed']}/{n}" + (f"·{extra}" if extra else "")


print("\n=== Module 7 · AdversarialBenchmark — CONSTRUCTED example (not a live run) ===")
print(f"  interface: {b['pyrit_interface']}")
print(f"  target: {b['target']}   technique: {b['technique']}   N per cell: {n}\n")
head = "  attacker".ljust(16) + "".join(f"{o.split(' ')[0]:>16}" for o in objs) + f"{'calls/elapsed s':>18}"
print(head)
print("  " + "-" * (len(head) - 2))
for a in b["attackers"]:
    row = f"  {a:14}"
    for o in objs:
        row += f"{cell_str(by[(a, o)]):>16}"
    row += f"{f'{cost[a][0]}/{cost[a][1]}s':>18}"
    print(row)
print("\n  Legend: x/5 = aimed-category positives of N=5.  ·i/e/u = invalid / error /")
print("  unverified counts kept VISIBLE (never folded into the rate).")
print("\n  How to read it (this is the selection lesson):")
print("   - COVERAGE, not a single winner: attacker-C owns destructive (5/5), attacker-A")
print("     owns config-reference (4/5); attacker-B is the thinnest. Pick per objective.")
print("   - TIME is part of the choice: attacker-C's coverage takes about 5x (630s vs 120s)")
print("     attacker-B's elapsed seconds. Request counts and elapsed time are NOT a")
print("     financial cost figure.")
print("   - One run per cell would NOT support a ranking; N and denominators must be shown.")
print("   - Candidates are NEUTRAL placeholders; this is a constructed method example.")
