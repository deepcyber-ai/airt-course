"""Module 6 - score one reply with the model scorer.

    python3 modules/module6/scorer-exercise/score.py --run examples/2-disclosed-no-flag.json
    python3 modules/module6/scorer-exercise/score.py --run <a JSON your Module 5 lab saved>

Reads the assistant reply from a JSON file and asks the group's scorer model whether the
objective was met. This introduces the scorer: a model reading the reply, not a keyword rule.
Needs a scorer model (AIRT_GROUP=openai -> gpt-4o-mini).
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _score import reply_from, model_scorer, marker, CRITERION   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="a JSON file with an assistant reply")
    a = ap.parse_args()
    reply, objective, case = reply_from(a.run)
    verdict, raw, model = model_scorer(reply, objective)
    print(f"  case      : {case}")
    print(f"  reply     : {reply.strip()[:300]}")
    print(f"  scorer    : {model}  ->  {verdict}   (raw: {raw!r})")
    print(f"  criterion : {CRITERION}")
    print("\n  The scorer read the whole reply and judged it against the criterion - not a "
          "keyword\n  match. See compare.py for how that differs from the deterministic marker.")


if __name__ == "__main__":
    main()
