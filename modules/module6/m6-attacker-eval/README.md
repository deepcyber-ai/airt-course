# Module 6 — two-attacker mini evaluation

A small **single-turn** comparison (not PAIR/TAP/a benchmark). Two same-provider
attackers each generate **three candidate** attacks from a common brief, against
one Larkfield target and one objective — reveal the internal configuration
reference — which neither attacker is given. Six candidate responses, plus one
benign control.

```bash
export AIRT_GROUP=openai   # or bedrock — PICK THE GROUP BEFORE RUNNING.
                           # Without it, compare_pair() returns one model twice
                           # and the two-model comparison is absent.
python3 modules/module6/m6-attacker-eval/attacker_eval.py            # the saved example (offline, no spend)
python3 modules/module6/m6-attacker-eval/attacker_eval.py --live     # calls the two attackers + target
```

Each **run** is written to its own **batch directory** with a `batch.json`
manifest, so re-running never mixes an old batch into the next comparison. Older
batches are retained. The five steps (Charlie's Decision 2): show all settings
first (the protected reference is **not** printed — it's the answer); generate
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

Every verdict is saved to `scores.json` in the batch dir (criterion id + text,
scorer model, prompt, raw output, verdict, source), so it can be reopened later.

Six attempts (two models × three) do **not** establish a success rate or a model
ranking — it is a worked example, not a leaderboard. Keep refusals, invalid output
and infrastructure errors distinguishable. Where the marker and judge disagree,
inspect the response against the reference before recording a missed disclosure —
a judge SUCCESS with no flag is a case to check, not proof. The protected
reference is never placed in an attacker's input; only synthetic fixtures are used.
