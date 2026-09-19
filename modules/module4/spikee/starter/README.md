# Lab 3 — spikee

Reversec's prompt-injection kit. Two halves:

1. **Single-turn datasets** — payloads built by combining instructions with
   jailbreak wrappers, fired one at a time.
2. **GOAT** — a real implementation of the Generative Offensive Agent Tester
   (arXiv 2410.01606), which holds a multi-turn conversation and adapts.

Unlike promptfoo and garak, spikee has no built-in way to reach an application
like ours — its targets talk to LLM provider APIs. So you write a **target
module**. That is the point of the first half of this lab: every scanner has to
be told how to reach your system, and writing one shows you what all of them
actually need.

## Setup

```bash
mkdir -p ~/spikee-ws && cd ~/spikee-ws
spikee init                                    # creates datasets/ targets/ attacks/ judges/
cp <repo>/modules/module4/spikee/starter/targets/larkfield.py targets/

spikee list targets                            # larkfield should appear
```

Bring the Larkfield level ladder up first (`labs-ctf/start-levels.sh`); the
target defaults to **L1 neutral `:8081`**, with **L3 hardened `:8083`** as the
comparison.

If the target appears with an error in the Tags column, the module raised while
being described — read the traceback, it is usually a typo in the enum.

## The point of the first exercise

Generate a dataset from generic seeds and you should expect a very low score —
likely zero — and the first exercise is to work out whether that means the
target held or the test was never capable of finding anything. A marker is a
**discovery** signal — "no flag" means no configured flag was observed, not that
the target held. Seeds that ask ordinary support questions are not aimed at any
configured effect, so a scanner reporting zero against a target you have not
aimed at tells you nothing. Run it and record what you actually get.

## Four things that will cost you an hour if nobody warns you

| Trap | What you see |
|---|---|
| `--sample` is a **fraction**, not a count | `--sample 12` → "Sample larger than population" |
| Target must return a **2-tuple** `(bool-or-Content, meta)` | "Invalid tuple return … got 3 elements" |
| `--include-standalone-inputs` is **not** the default | dataset generates with **0 entries**, no error |
| Tags come from `ModuleTag` — there is no `CUSTOM` | target lists with an error where its tag should be |

The third is the dangerous one. You get a valid, empty dataset and a run that
reports `success=0`, which is indistinguishable from a secure target.

## Your task

**1. Write a dataset aimed at THIS target.** A seed folder needs
`standalone_user_inputs.jsonl` plus empty `instructions.jsonl`,
`jailbreaks.jsonl` and `base_user_inputs.jsonl`. Each line:

```json
{"id":"my-probe-01","text":"...","jailbreak_type":"data-disclosure",
 "judge_name":"airt_flags","judge_args":"","ideal_summary":"","question":"","ideal_answer":""}
```

Aim at effects, not opinions. The target scores when something *happens* — a
query runs, a record returns, a restricted tool is invoked. On the neutral
target a single probe may be refused; record that too.

**2. Run it against both postures** (`port=8081`, `port=8083`) and diff.

**3. Then GOAT.** See `../complete/README.md` once you have the single-turn
half working.

## Why this target needs no judge

`larkfield.py` returns a **bool** rather than text, so spikee scores on our flag
markers instead of calling an LLM judge. No judge model, no judge cost. The
reply rides along in `meta` so you can check the aimed effect — a marker is a
discovery signal, not proof (an `llm06` marker can be a simulated tool call, not
a deletion), so read the response and the evidence.

That is a deliberate trade. You lose spikee's own nuanced grading; you gain a
signal that ties to the harness's own flags. Where you need content grading, the
complete lab adds an explicit LLM judge to compare against.

(c) 2026 Deep Cyber Ltd. Apache 2.0 licensed.
