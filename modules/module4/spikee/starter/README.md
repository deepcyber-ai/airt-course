# Lab 3 — Spikee (starter)

> **OPTIONAL AFTER-COURSE REFERENCE.** Not part of the classroom task unless your trainer assigns it.

## What you'll do

Spikee uses a Python connector to send requests to Larkfield. Copy the supplied
connector into your workspace and read how it sends the request and extracts the reply.
Then create a small dataset and send each prompt as a separate test (single-turn). The
multi-turn GOAT example is in the `complete` version.

## Before you start

- **Target:** neutral Larkfield on `:8089` — bring it up with `airt-target larkfield`.
  For the hardened comparison you **restart the same target with the hardened prompt**
  (same port), so leave that until step 3.
- **`<repo>`** below means your course checkout — the folder that contains `modules/`
  and `labs-ctf/`.
- Set up a Spikee workspace and add the Larkfield target:

```bash
mkdir -p ~/spikee-ws && cd ~/spikee-ws
spikee init                                    # creates datasets/ targets/ attacks/ judges/
cp <repo>/modules/module4/spikee/starter/targets/larkfield.py targets/
cp <repo>/modules/module4/spikee/complete/judges/airt_flags.py judges/   # the dataset names this judge
spikee list targets                            # 'larkfield' should appear
```

If `larkfield` shows an error in the Tags column, the module raised while Spikee was
describing it — read the traceback (it's usually a typo in an enum).

## Run the exercise

**The runnable classroom Spikee command is on the Module 4 entry page** (the `native-demo/spikee`
block): it generates and tests a supplied dataset in one go. Use that for the class task. The
steps below are an optional build-your-own-dataset walkthrough; for a complete, runnable
generate-and-test set see [`../complete/README.md`](../complete/README.md).

**1. Write a dataset aimed at THIS target.** A seed folder needs
`standalone_user_inputs.jsonl` plus empty `instructions.jsonl`, `jailbreaks.jsonl`
and `base_user_inputs.jsonl`. Each line looks like:

```json
{"id":"my-probe-01","text":"...","jailbreak_type":"data-disclosure",
 "judge_name":"airt_flags","judge_args":"","ideal_summary":"","question":"","ideal_answer":""}
```

Check the response and relevant tool records to establish what happened — the target
scores when something happens (a query runs, a record returns, a restricted tool is
invoked). On the neutral target a single probe may be refused; that is a valid result
to record.

**2. Generate and run it** single-turn against `:8089`. (Remember `--include-standalone-inputs`,
or the dataset generates empty — see troubleshooting below.)

**3. Restart the target with the hardened prompt, run the same dataset again, and
compare** the two results.

## Read and record

Open the results file printed at the end of the run. Read each prompt, Larkfield's
reply in `meta.response`, and the flag result in `success`. Check whether the prompts
tested the behaviour you intended to assess. A run with no flags does not establish that
Larkfield resisted an attack. Record the result and the supporting evidence.

## Optional — troubleshooting, and how the scoring works

**Troubleshooting.**

| Trap | What you see |
|---|---|
| `--sample` is a **fraction**, not a count | `--sample 12` → "Sample larger than population" |
| The target must return a **2-tuple** `(bool-or-Content, meta)` | "Invalid tuple return … got 3 elements" |
| `--include-standalone-inputs` is **not** the default | dataset generates with **0 entries**, no error |
| Tags come from `ModuleTag` — there is no `CUSTOM` | target lists with an error where its tag should be |

The third is the dangerous one: you get a valid but empty dataset and a run that
reports `success=0` — indistinguishable from a secure target.

**Why this target needs no judge model.** `larkfield.py` returns a **bool** instead of
text, so Spikee scores on our flag markers rather than calling an LLM judge — no judge
model, no judge cost. The reply rides along in `meta` so you can still check the aimed
effect. A marker is a discovery signal, not proof (an `llm06` marker can be a simulated
tool call, not a real deletion), so read the response and the evidence too. That is a
deliberate trade: you lose Spikee's own nuanced grading and gain a signal tied to the
harness's flags. Where you need content grading, the `complete` lab adds an explicit
LLM judge.

**Next:** once the single-turn half works, do GOAT in [`../complete/README.md`](../complete/README.md).

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
