# Module 7 — Selecting Attackers & Scorers

The Module 7 exercise is a hands-on comparison: run one short attack, score what it produced,
then change only the attacker model and do it again. It makes the selection question concrete
— which attacker was more effective here, and which scoring criterion fits the objective. It
is an individual exercise on your own key.

Everything except the attacker is fixed: the target (neutral Larkfield on `:8089`), the
objective, the broad scorer model, both criteria and the five-turn limit.

## During class

1. Run the first attack, then score it:
   ```bash
   python3 modules/module7/attacker-scorer/attack.py --attacker gpt-4.1
   python3 modules/module7/attacker-scorer/score.py --run course-runs/module7/<first-trace>.json --scorer gpt-4o-mini
   ```
2. Change only the attacker model and run the second pair:
   ```bash
   python3 modules/module7/attacker-scorer/attack.py --attacker gpt-4o-mini
   python3 modules/module7/attacker-scorer/score.py --run course-runs/module7/<second-trace>.json --scorer gpt-4o-mini
   ```
3. Read both conversations and both score files, fill the two-attacker comparison table in
   `attacker-scorer/README.md`, and answer its two questions.
4. Now change the **scorer** instead: score **one** of your saved traces with a second scorer
   model under the same criterion, and fill the two-scorer table:
   ```bash
   python3 modules/module7/attacker-scorer/score.py --run course-runs/module7/<a-trace>.json --scorer gpt-4.1
   ```

`attack.py` creates the evidence; `score.py` assesses the saved evidence afterwards. The score
file name includes the scorer model, so the second score does not overwrite the first.

## What to keep

The two completed tables (two attackers; then two scorers on one trace) and the answers: which
attacker was more effective for this objective, and whether the two scorers agreed on the same
reply. Two runs illustrate this
case; they do not rank either model in general.

**In this folder**
- `attacker-scorer/` — the runnable exercise (`attack.py` then `score.py`; change only
  `--attacker` to compare). Start here.
- `MODULE7-SELECTION-HANDOUT.md` — measured attacker results and scorer-agreement figures.
  Optional; the trainer may use it in the debrief. It is not a second required exercise.
- `m7-selection/` — two constructed examples of evaluation interfaces (`benchmark_view.py`,
  `scorer_eval_view.py`). Optional; invented figures, for reading practice only.
- `m7-archetype/` — attack conversation cards with model names hidden (`archetype_view.py`).
  Optional; read them to practise describing an attacker's style.

The lab scripts locate the shared `labs/` folder automatically. If they cannot find it, set
`AIRT_COURSE_ROOT` to the course folder.
