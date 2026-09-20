# Module 6 — two-attacker mini evaluation

A small **single-turn** comparison (not PAIR/TAP/a benchmark). Two same-provider
attackers each generate **three candidate** attacks from a common brief, against
one Larkfield target and one objective — reveal the internal configuration
reference — which neither attacker is given. Six candidate responses, plus one
benign control.

```bash
# OFFLINE (default) — the saved example, no spend, NO GROUP REQUIRED
# (it replays the saved run's own two distinct attackers):
python3 modules/module6/m6-attacker-eval/attacker_eval.py

# LIVE only — pick the two-model group FIRST, or you get one model twice:
export AIRT_GROUP=openai   # or bedrock  (required for --live)
python3 modules/module6/m6-attacker-eval/attacker_eval.py --live     # calls the two attackers + target
```

Each **run** is written to its own **batch directory** with a `batch.json`
manifest, so re-running never mixes an old batch into the next comparison. Older
batches are retained. The five steps (Charlie's Decision 2): show all settings
first (the reference value is **withheld from the attack model** — the experimental control — so its prompts are genuine, not templated around the answer; the value IS in the saved fixture, so it is not hidden from attendees); generate
three prompts per attacker and preserve each exactly; run a benign control plus
the six attacks **each in its own `x-session-id` session**; save every response;
write the batch manifest.

**Budget is enforced and PERSISTED at module/group scope** — `6 attacker /
7 target / 12 scorer` per group across the whole module (`labs/budget.py`,
`AIRT_RUN_DIR/m6-budget.json`). This activity spends the 6 attacker (2×3) +
7 target (6 attacks + 1 benign); the scorer exercise spends the 12 scorer. The
ledger counts across both scripts and across batches/re-runs, and refuses to
overspend. When the allowance can't complete a candidate live it falls back to
the saved example **for that candidate and says so** — it never silently swaps
saved text in for a failed live call.

## Cost — the whole Module 6 exercise (measured)

Module 6 is a **small, fixed single-turn** exercise: per group, **6 attacker + 7 target +
12 scorer = 25 calls**, no branching (unlike Module 5's tree methods), so the cost is tiny
and predictable. The **scorer leg is measured** from a live rehearsal (qwen, 2026-09-20 —
12 calls, 1252 tokens, $0.00029); the attacker and target legs are estimated from the
**prompt and reply text stored in the constructed fixture** (~115/30 attacker in/out,
~165/33 target in/out including the 135-token Larkfield system prompt) at each model's list
price. FX assumption: **$1 = £0.79**.

This is a **same-model cost illustration** (one model on all three legs). The shipped groups
use different attacker/scorer models and the target is configured separately, so a real
group's figure is a mix of the rows below — use them as an order-of-magnitude guide.

| Model (illustrative, all three legs) | Per group (USD) | Per group (GBP) |
|---|--:|--:|
| gpt-4.1 | ~$0.0096 | ~£0.0076 |
| gpt-4o-mini | ~$0.0007 | ~£0.0006 |
| qwen (scorer leg measured) | ~$0.00106 | ~£0.00084 |

On gpt-4.1 the whole Module 6 exercise is **about one US cent per group** (≈$0.0096 at the
stored fixture lengths; live output lengths vary, so treat this as an estimate, not a cap).
For a **15-attendee room** each independently making the 12 scorer calls, the whole-room
**scorer** spend is about **$0.040 on gpt-4.1**, **$0.003 on gpt-4o-mini**, or **$0.004 on
qwen**. Negligible beside Module 5's ~£2/learner (which is the TAP/PAIR branching); any model
is fine on cost — the 12-scorer / 8-fixtures caps are a discipline limit, not a spend concern.
Live-rehearsal evidence and the full calculation are frozen in
`reviews/review2/module6-live-rehearsal-20260920/`; the aggregate token/cost record is a
budgeting estimate, not provider-receipt/audit-grade cost.

Each record separates **what was requested from where the bytes came from**:

| field | meaning |
|-------|---------|
| `requested_model` | the group attacker this slot would use live |
| `source_model` | where the text actually came from — a live model, or the saved fixture's origin (so a Bedrock run never mislabels saved gpt-4.1 text as qwen) |
| `constructed` | `true` when the text is saved/fallback, not a live measurement |
| `source` | `live` / `error` / `saved` / `saved-fallback` — `error` is infra, **not** a target refusal |
| `session_id` | a real live session, or `null` (saved text has no original session) |

The scorer reads **one batch** and scores exactly its six responses under **that
run's two criteria** (original + alternative, from `batch.json`) — the command is
printed at the end of the run:

```bash
python3 modules/module6/scorer-exercise/score_exercise.py --run-input <batch-dir>
python3 modules/module6/scorer-exercise/score_exercise.py            # or the labelled fixtures (slide reveal)
```

Every verdict is saved to `scores.live.json` (live) or `scores.offline.json` (offline) in
the batch dir (criterion id + text, scorer model, prompt, raw output, verdict,
`judgement_source` and `response_source`), so it can be reopened later.

Six attempts (two models × three) do **not** establish a success rate or a model
ranking — it is a worked example, not a leaderboard. Keep refusals, invalid output
and infrastructure errors distinguishable. Where the marker and judge disagree,
inspect the response against the reference before recording a missed disclosure —
a judge SUCCESS with no flag is a case to check, not proof. The protected
reference is never placed in an attacker's input; only synthetic fixtures are used.
