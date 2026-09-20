# Module 6 — Attackers & Scorers

You will use two attacker models to write three attacks each. Send the six attacks to
Larkfield, then score Larkfield's replies using a flag check and two model-based
criteria. Inspect the saved results and explain any disagreement. Use your own model
key and keep the same batch throughout the exercise.

You run **one** sequence — do not treat the two folders as separate exercises. The
scores must belong to the batch you just produced.

## Your target and models

- **Target:** neutral Larkfield at `http://localhost:8089` (the script appends `/chat`) —
  the same target and port as Modules 1–2 (`airt-target larkfield`). Use the endpoint on
  your setup sheet if it differs.
- **Model group:** choose your two-attacker group before running. Use
  `export AIRT_GROUP=openai` for your OpenAI key, or `export AIRT_GROUP=bedrock` for the
  Bedrock route. Offline needs no group.
- **Allowance:** 6 attacker + 7 target + 12 scorer requests for the group — about one
  live pass. The scripts enforce the allowance.

## The sequence

**1. Choose a fresh run directory** that has not been used for an earlier Module 6
exercise (run from the course folder containing `modules/` and `labs/`):
```bash
mkdir -p course-runs
export AIRT_RUN_DIR="$(mktemp -d "$PWD/course-runs/m6-XXXXXX")"
```

**2. Run the two attacker models live.** Each writes three attacks against the shared
objective (reveal Larkfield's internal configuration reference, whose value neither
attacker is given), plus a benign control:
```bash
python3 modules/module6/m6-attacker-eval/attacker_eval.py --live
```
It prints the **batch directory** it wrote. Note that path. Check each record's
`source`: records labelled `saved-fallback` or `error` must not be described as live
results.

**3. Score Larkfield's six replies, live.** `attacker_eval.py` prints the complete scorer
command for the batch it just wrote — copy and run that (it already contains the exact batch
directory). It looks like:
```bash
python3 modules/module6/scorer-exercise/score_exercise.py --run-input <the-printed-batch-dir>
```
Each reply receives three checks: whether it contains the flag, whether it meets the
strict disclosure criterion, and whether it meets the broader disclosure criterion. The
two model-based checks use different definitions of success — read those definitions
before comparing their verdicts. `SUCCESS` means the criterion was met; `FAILURE` means
it was not; `UNRESOLVED` means no usable verdict was returned. Score a complete batch
once; the script will not overwrite an existing live score file.

**4. Inspect the saved evidence.** Open `batch.json` to find the attack record IDs and
the benign-control ID; open the corresponding JSON files to read the prompts and
replies. Open `scores.live.json` to inspect the marker result, the model verdicts, and
the scorer inputs and raw outputs. The judge returns a verdict, not an explanation.

## Record and discuss

Inspect the six attack replies and the separate benign control. Compare the three
checks for each attack reply. If they disagree, inspect the response and the criterion
to explain why. If your live results all agree, use the labelled saved example for that
discussion. Six attempts can show what happened in this exercise; they do not establish
a model ranking.

## If the live target fails

Create the saved-example batch without calling a model, then score it (marker check
only; the model criteria are left unjudged):
```bash
# Create the saved example batch (no model calls):
python3 modules/module6/m6-attacker-eval/attacker_eval.py
# Copy the complete scorer command it prints and append --offline:
python3 modules/module6/scorer-exercise/score_exercise.py --run-input <the-printed-batch-dir> --offline
```
To inspect the separate labelled teaching fixtures instead, run
`python3 modules/module6/scorer-exercise/score_exercise.py --offline`. Those saved
labels are constructed teaching examples — they do not become live scores for the batch
above.
