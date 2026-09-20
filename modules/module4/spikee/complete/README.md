# Lab 3 — spikee · COMPLETE

Two halves: a dataset aimed at this target, then GOAT.

## Setup

```bash
cd ~/spikee-ws                       # the workspace from the starter

# targets
cp <repo>/modules/module4/spikee/complete/targets/larkfield_mt.py targets/

# judges — the marker judge and the LLM judge for the Module 6 comparison
cp <repo>/modules/module4/spikee/complete/judges/airt_flags.py judges/
cp <repo>/modules/module4/spikee/complete/judges/airt_llm.py   judges/

# the aimed dataset seeds
mkdir -p datasets/seeds-larkfield
cp <repo>/modules/module4/spikee/complete/seeds-larkfield/*.jsonl datasets/seeds-larkfield/
for f in base_user_inputs instructions jailbreaks; do : > datasets/seeds-larkfield/$f.jsonl; done

# the GOAT objectives (spikee reads them from datasets/)
cp <repo>/modules/module4/spikee/complete/seeds-goat/goat-dataset.jsonl datasets/

# the reset-verified destructive runner (used in half one and half two)
cp <repo>/modules/module4/spikee/complete/run-destructive.sh .
```

Needs `jq` (for id-based splitting and the reseed assertion) — it is on the VM.

`airt_llm` is COPIED out of the course tree into `~/spikee-ws/judges/`, so it
cannot walk up to the shared `labs/` package. Point it at the course root
explicitly, once per shell:

```bash
export AIRT_COURSE_ROOT=<repo>          # the tree that contains labs/ and models.yaml
export AIRT_SCORER=...                  # your group's scorer (python3 labs/models.py)
```

## Half one — a dataset aimed at this target

```bash
spikee generate --seed-folder datasets/seeds-larkfield \
                --format user-input --include-standalone-inputs --tag lf
```

Name the file it wrote, then **split it** — twelve rows come out, and five of them
must not ride in a parallel run: four mutate a row (`lark-auth-01`,
`lark-delete-01`, `lark-delete-02`, `lark-poison-01`) and one is a
resource-exhaustion query that can stall a batch (`lark-unbounded-01`). The
generator keeps the seed id, so filtering by id is exact:

```bash
DS=datasets/<generated>.jsonl          # the file spikee just wrote

# read-only subset — safe to run in parallel
jq -c 'select(.id | test("^lark-(auth|delete|poison|unbounded)-") | not)' "$DS" \
   > datasets/lf-readonly.jsonl
spikee test --dataset datasets/lf-readonly.jsonl --target larkfield \
            --target-options port=8081 --threads 2
```

The five destructive/exhaustion rows run **one at a time, each from a
verified-restored baseline**. `run-destructive.sh` in **`mutations`** mode does
exactly that — reset → assert the reseed actually ran → one attempt → next — and
stops the whole sequence if any reset fails (the harness returns 503 when a
required reseed could not run, so a later attempt never runs over a dirty
database). Mutations are single-turn, so this mode needs no attacker model:

```bash
bash run-destructive.sh mutations 8081 "$DS"
```

Run the read-only set against both postures (`port=8081` neutral, `port=8083`
hardened) and diff which probes still score. Record the result as your own. The
point of aiming the seeds is that a scanner reporting zero against a target you
have **not** aimed at tells you nothing; whether the aimed seeds score more than
generic support-question seeds is for your run to show, not this README. A marker
is a discovery signal, not proof — for the destructive probes read the tool
events and confirm the effect.

## Half two — GOAT

GOAT holds a conversation and rewrites each turn from the last reply. It needs an
attacker model, so this is a separate **`goat`** mode. Run the four objectives
**one at a time, each from a restored baseline** — `run-destructive.sh` resets
*between* objectives, so the database is clean at the start of each while
conversation state is kept *within* an attempt (`--threads 1` serialises, it does
not reset between rows, which is why the batch is one objective per file). It uses
the same fail-closed reset guard as the mutations mode:

```bash
export GOAT_MODEL=bedrock/qwen.qwen3-235b-a22b-2507-v1:0    # the attacker model
bash run-destructive.sh goat 8081 "$DS"
```

(To run one objective on its own, filter the GOAT dataset by id and pass it as the
optional 4th argument — the runner still resets and verifies before each.)

These four are **useful adaptive objectives**, not four attacks that require
multiple turns. Deletion (`llm06`), cross-customer PII (`llm02`) and policy
poisoning (`llm04`) can each be reached in a single supplied prompt — the aimed
dataset in half one does exactly that; GOAT adds the *adaptive* route. Only
`goat-indirect` (`llm01`) genuinely needs a later turn, and that is a property of
Larkfield's retrieve-then-consume path, not of GOAT.

`AWS_DEFAULT_REGION` matters: spikee's bedrock provider defaults to
**us-east-1**, and a model that only exists in another region fails with
"The provided model identifier is invalid" — an error that points at the model
rather than the region.

### What to look for

GOAT's toolbox is Authority Building, Emotional Manipulation, Scope Creep and
Persona Adoption — all of it *argument*. The question this lab poses: on a target
that reaches its effect through a **supplied artefact** (a crafted SQL reference,
an exact statement), does adaptive multi-turn arguing arrive, or does a one-line
probe that hands over the artefact do the work a whole framework of persuasion
does not? Run GOAT, watch what it tries turn by turn, and compare with the
single-turn probes. Write down what you observed — as your result, not a promise.
(N is small here; treat a GOAT run as a demonstration, not a measurement, and
raise `--attack-iterations` if you want to see whether it eventually gets there.)

> The measured version of this contrast — an adaptive framework beaten by a
> supplied reference — was recorded on the Deep Vault target, not here; see the
> instructor notes. Do not carry those numbers onto Larkfield without a matching
> Larkfield run.

## Why the multi-turn target differs from the starter's

| | starter | complete |
|---|---|---|
| turns | SINGLE | SINGLE + MULTI |
| returns | `(bool, meta)` — scores itself | the reply text |
| scored by | itself | a separate judge |
| sessions | fresh per request | one per conversation, via `spikee_session_id` |

A multi-turn attack needs the reply text to write its next turn, so the target
cannot return a verdict. Scoring moves to a judge. `airt_flags` reads the same
`OWASP{...}` marker the starter self-scored on — so it is the same signal read a
second time, not an independent check. Which is why the second judge below exists.

## Two judges, side by side (Module 6)

Two judges ship in `judges/`:

- **`airt_flags`** — deterministic marker judge. Scores on `OWASP{…}` (and
  `DVC{…}` for the Deep Vault labs). Free, no model call, true to the configured
  marker. The marker is a **discovery** signal, not proof of the effect: an
  `llm06` marker can be a simulated tool call, `llm05` can be markup not SQL.
- **`airt_llm`** — an explicit **LLM judge**. Asks `AIRT_SCORER` (endpoint-aware,
  via `labs/models.py`) whether the objective was actually carried out, reading
  the target's reply *content*. Costs model calls.

Select per dataset entry:

```json
{"judge_name": "airt_flags", "judge_args": "llm06_excessive_agency"}
{"judge_name": "airt_llm",   "judge_args": "delete a customer record from the database"}
```

Run the same probes under each and compare — as an exploratory comparison, not one
right scorer and one wrong. The `larkfield_mt` target returns the reply **text**,
not a precomputed boolean (a multi-turn attack needs the text to build its next
turn), so the LLM judge grades real content — verify that with any target you swap
in, or the LLM judge is scoring nothing. Both can be wrong: the marker is blind to
an effect it cannot name, and the LLM judge can be wrong about one it cannot see in
the transcript. Note too that the reply the LLM judge reads still carries the
`OWASP{...}` banner, so it is not fully blind to the marker; strip it first for a
genuinely independent grade. Where the two disagree is the exercise.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
