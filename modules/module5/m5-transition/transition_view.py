"""Module 5 closer — the recorded trace view (Charlie's Decision 1).

    python3 modules/module5/m5-transition/transition_view.py

Module 5 ran the attacks with prepared settings and did NOT dwell on the
components. This is the five-minute closing reveal: open one SAVED trace and
name the three things that were quietly at work — the attacker, the technique,
and the scoring function — then hand off to Module 6, where the scorer becomes
the subject.

The point to land: the scorer here was a deterministic RULE (a marker match),
not a model. A selected model name in a config does not establish that an LLM
scorer was ever called.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
"""
import json
from pathlib import Path

t = json.loads((Path(__file__).resolve().parent / "fixtures" / "saved-trace.json").read_text())

print(f"\n=== Module 5 closer — what was quietly at work  [{t['_label'].split(' - ')[0]}] ===")
print(f"  target    : {t['target']['profile']}  ({t['target']['posture']})")
print(f"  objective : {t['objective']}\n")
print("  Three components, unremarked during the run:\n")
print(f"  1. ATTACKER  — {t['attacker']['name']}")
print(f"       {t['attacker']['note']}")
print(f"  2. TECHNIQUE — {t['technique']['name']}")
print(f"       {t['technique']['note']}")
print(f"  3. SCORER    — {t['scorer']['kind']}: {t['scorer']['rule']}")
print(f"       {t['scorer']['note']}\n")
print("  The trace (2 turns):")
for turn in t["turns"]:
    hit = f"  FLAG {turn['flag']}" if turn["flag"] else ""
    print(f"    turn {turn['n']}: att> {turn['attacker_msg'][:60]}...")
    print(f"            tgt> {turn['target_reply'][:60]}...{hit}")
print(f"\n  note on AUTH-9902: {t['authorisation_note']}")
o = t["outcome"]
print(f"\n  this trace DEMONSTRATES: {o['demonstrates']}")
print(f"  it does NOT prove   : {o['does_not_prove']}")
print(f"  decided by          : {o['decided_by']}")
print(f"  calls: attacker {o['attacker_calls']}, target {o['target_calls']}, "
      f"scorer {o['scorer_calls']} (the rule is free; no judge model was called).")
print("\n  -> Module 6: now we make the SCORER the subject. Was a marker match")
print("     enough? What does a model judge see that it doesn't — and miss?")
