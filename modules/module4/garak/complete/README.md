# Lab 2 — garak · COMPLETE

```bash
bash modules/module4/garak/complete/run.sh quick     # ~1 min, proves the plumbing
bash modules/module4/garak/complete/run.sh           # both postures, five probe families
```

The runner calls the VM's `garak` launcher (its own environment), writes a full
log per run, and **stops if a scan fails** rather than printing "reports" over a
crash. Reports are written to `out/` as `.jsonl` and `.html`. Target is the Larkfield
level ladder — neutral `:8081`, hardened `:8083`.

## The finding to look for

Run the full set against both postures and read the reports **per probe**, not by
the aggregate. You may see the aggregate fall from neutral to hardened, so the
hardening looks like a win — or you may not; that is for your reports to say. The
point of the lab holds either way: an **aggregate score can hide a per-objective
result that did not move**, so look for one and name it, from your own reports.
(Record your own numbers as the evidence; do not carry numbers measured on a
different target onto this one.)

## What `latentinjection` here actually tests (read carefully)

It is tempting to call this "the retrieval attack that hardening can't reach." In
this configuration that is **not** what happens, on two counts:

1. **Larkfield's hardened prompt does address retrieved instructions.** Rule 5
   tells the model to treat tool/document/knowledge-base content as untrusted
   data and to reject instructions found in it (`system_prompt_hardened.txt`).
   That rule may fail, but it is present — so do not claim hardening "says nothing
   about" retrieval.
2. **This probe does not use Larkfield's retrieval channel.** `latentinjection.
   LatentInjectionReport` combines its synthetic document and instruction into one
   prompt, and this REST adapter sends that prompt through the application's **user
   `input`**. Nothing is planted in the knowledge base and retrieved later. So its
   detector firing is about how the model handles a document-shaped *user message*
   — it is not evidence that Larkfield's configured retrieve-then-consume flow was
   compromised, and it is not the same event as an `OWASP{...}` flag.

So: describe it as an **inline/simulated document-context probe**, inspect its
actual prompt and detector criterion, and record the result without predicting a
hit or an unchanged score. Contrast that scope with the real retrieve-then-consume
Larkfield flow — the multi-turn indirect-injection route the single-turn labs
cannot reach.

## Notes worth keeping

**Garak needs no attacker or judge model.** Prompts are static, detectors are
rules or small classifiers. No attacker/judge-model charge beyond the target's
own inference — so it works for attendees with no credentials.

**An empty prompt can abort the entire scan.** `test.Test` opens with `""`. A
target that returns HTTP 400 raises `ConnectionError` inside garak and the run
dies on its first prompt. Our harness answers empty prompts for exactly this
reason.

**`atkgen` is the exception** — it is the one family that uses an attacker model
(`red_team_model_type` / `red_team_model_name`). Everything else here is free.

**Reply field is `output`.** Get `response_json_field` wrong and every reply
reads as empty, which looks exactly like a target that refuses everything.

## Exercises

1. **Run both postures and diff the aggregates.** Write down whatever the headline
   move is — improvement, no change, or worse — before you look at the per-probe
   numbers.
2. **Then read each probe's result per objective.** Which moved and which did not?
3. **Compare with promptfoo (lab 1).** Promptfoo's single-turn probes cannot enter
   the retrieve-then-consume flow; garak's `latentinjection` does not enter it
   either — it sends a document-shaped *user prompt*. Neither reaches Larkfield's
   real retrieval channel single-turn; that is the multi-turn route in later labs.
   Say precisely what each tool tested, rather than "one blind spot, one hit."
4. **Add `dan` and `leakreplay`** to the probe list in `run.sh` and see whether
   either finds anything the configured flags do not cover.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
