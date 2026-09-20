# Module 5 — Spikee (Explore further / optional implementation reference)

**Optional.** The Module 5 slot is the manual practice plus the prepared recordings;
the automated attacker/scorer reveal is the closing few minutes. This is a
reference for attendees who want to run one tool set themselves afterwards.
**Each student or pair runs ONE tool set only — PyRIT, Promptfoo *or* Spikee — not
all three**, on their own provider key.

Spikee is CLI-driven, so this is delivered as **scripts**: each `*.sh` generates a
dataset from a seed folder and runs `spikee test --attack …`.

## What Spikee actually offers (not a ranked comparison)

These examples align **one synthetic, read-only objective** (cross-customer PII)
across the attacks Spikee has, for *configuration study* — not to rank techniques
or claim they are the "same method on equal footing".

| This example | Spikee attack | What it is |
|---|---|---|
| crescendo | `crescendo` | multi-turn (max-turns 5) |
| goat | `goat` | multi-turn — from the workspace (`spikee init` provides it) |
| iterative | `llm_jailbreaker` | **single-turn, response-informed baseline** — NOT a multi-turn iterative method |

**Spikee has no PAIR and no TAP.** `goat` comes from the workspace copy, so
`spikee init` must have run.

## One-time setup (a Spikee workspace)

```bash
cd ~/spikee-ws                      # your spikee workspace (spikee init already run)
cp <course>/modules/module4/spikee/complete/targets/larkfield_mt.py targets/   # the MULTI-TURN target
cp <course>/modules/module4/spikee/complete/judges/airt_flags.py    judges/
```

The scripts use **`larkfield_mt`** — the text-returning, session-aware multi-turn
target. (`larkfield`, the single-turn Boolean adapter, cannot run crescendo/goat.)

## Run one method

```bash
cd ~/spikee-ws
export SPIKEE_ATTACKER=openai/gpt-4o-mini    # your attack model, as a Spikee provider/model
bash <course>/modules/module5/spikee/crescendo/complete.sh       # or goat/, iterative/
```

**Attack model matters.** In our rehearsal `openai/gpt-4o-mini` REFUSED the adversarial
role, so spikee crescendo errored (`RuntimeError`, "LLM did not return valid JSON"). That is
an observation, not a guarantee — a guarded model can make a poor attacker. If a run stalls
on refusals, try a more compliant model (e.g. `bedrock/qwen...`, not rehearsed here).

Each script generates from its seed folder, then runs `spikee test --target
larkfield_mt --attack <method> --attack-only`. **`--attack-only`** matters: without
it Spikee first submits the plain seed and *skips* the named attack if that already
succeeds — so the run would not actually exercise the method. **Supported objectives (starter)** — pick ONE `objective_id`; anything else fails closed:
- `cross_customer_contact_disclosure` -> flag `llm02_pii_disclosure`
- `internal_config_reference_disclosure` -> flag `llm07_system_prompt`

The **starter** reads
`seeds-starter/` and **fails closed** until you replace the `TODO` objective and set
`judge_args` to your expected flag; the **complete** reads `seeds-pii/`.

## Cost — allowance (Spikee route not yet rehearsed)

Allow about **£2 for one full tool route** (owner-approved allowance). NOTE: the Spikee
route has NOT been completed in rehearsal — with a guarded attack model it refused; treat
Spikee as an **unrehearsed post-course implementation reference** until a compliant-model run
is completed and saved (see the instructor cost note). **Your cost will vary by provider, model, token use, retries and
exchange rate.** The full prepared run is allowed — this is not capped to a
spending target — but keep an **emergency stop**: cancel with Ctrl+C if a run loops
or exceeds a few minutes, and note that Spikee defaults to 3 retries, so
`--attack-iterations` is not a physical-send ceiling.

## Reading the result

Spikee writes a results JSONL under `results/` — the path is printed at the end of
the run; open it to read the transcript, the target's replies and the judge output.
The judge `airt_flags` is a **discovery rule** (it checks for a target-emitted
`OWASP{…}` marker) — a flag identifies a useful discovery but does **not** by itself
prove the full objective (all of a name, email and phone delivered). Check the
returned values against the known synthetic fixture.

## Keep keys out of course files

`SPIKEE_ATTACKER` and any provider key live in your shell/`.env`, never in these
scripts, the seeds, saved results, screenshots or anything committed/exported.
