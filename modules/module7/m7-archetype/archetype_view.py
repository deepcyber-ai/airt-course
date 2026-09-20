"""Module 7 archetype exercise - a NO-CALL viewer for the trace cards.

    python3 modules/module7/m7-archetype/archetype_view.py            # show the cards
    python3 modules/module7/m7-archetype/archetype_view.py --full     # show the full sends (untruncated)

Shows the trace cards for the BEHAVIOUR-IDENTIFICATION half of the archetype
exercise: each card's relevant send(s) - the attacker prompt and the target's actual
reply - and the REVIEWED outcome. Model identities are masked here (revealed from the instructor
key at the debrief). No model or target calls are made.

These are MEASURED reviewed runs across DIFFERENT objectives/postures - they are a
set for identifying attacker BEHAVIOUR, NOT a common-objective coverage comparison.
For the selection decision, use the constructed coverage in
`modules/module7/m7-selection/benchmark_view.py` (attackers x objectives, with counts), not
one episode per objective. Do not read these cards as a model ranking.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
"""
import argparse
import glob
import json
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_cards():
    return [json.load(open(f)) for f in sorted(glob.glob(str(HERE / "cards" / "*.json")))]


def _wrap(label, text, width, full):
    text = text if full else (text[:width] + (" ..." if len(text) > width else ""))
    lines = textwrap.wrap(text, 92) or [""]
    print(f"    {label:20}: {lines[0]}")
    for ln in lines[1:]:
        print(f"    {'':20}  {ln}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="show the full attacker/response excerpts")
    a = ap.parse_args()
    cards = load_cards()
    print("\n=== Module 7 archetype cards - BEHAVIOUR IDENTIFICATION (model identities MASKED) ===")
    print("    These span different objectives/postures on purpose; describe the STYLE.\n")
    for c in cards:
        print(f"  {c['card_id']}   model: {c['model']}   target: {c['target']} [{c['posture']}]"
              f"   objective: {c['intended_objective']}")
        for sno, snd in c["relevant_sends"].items():
            print(f"    -- relevant send {sno} --")
            _wrap("attacker prompt", snd["prompt"], 200, a.full)
            _wrap("target response", snd["response"], 200, a.full)
        print(f"    {'physical calls':20}: {c['physical_calls']}   turns: {c['turns']}")
        print(f"    {'top-level flags':20}: {c['top_level_flags'] or '[]'}   collateral: {c['collateral_flags'] or '[]'}")
        _wrap("reviewed outcome", c["reviewed_outcome"], 400, True)
        print(f"    ({c['measured_or_constructed']}; source {c['source']['source_sha256'][:12]})\n")

    print("  Step 1 (behaviour): describe each card's actual behaviour, then label its")
    print("  archetype(s). A style is an observation about the transcript, not a permanent")
    print("  vendor trait; a model can show more than one, and change mid-attack.")
    print("  Keep the behavioural description SEPARATE from the objective verdict, and read")
    print("  the reviewed outcome (incl. CARD-3, where an EMPTY top-level flag hides a real")
    print("  disclosure in the send ledger, and CARD-4, a SIMULATED receipt, not a deletion).")
    print("\n  Steps 2-4 (selection): use the constructed coverage table -")
    print("    python3 modules/module7/m7-selection/benchmark_view.py")
    print("  which compares attackers x objectives with counts; these single episodes cannot.")


if __name__ == "__main__":
    main()
