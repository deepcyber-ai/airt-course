# Lab 2 — garak · COMPLETE

```bash
bash modules/module4/garak/complete/run.sh quick     # ~1 min, proves the plumbing
bash modules/module4/garak/complete/run.sh           # full set against the CURRENT posture (neutral)
# then restart the target hardened (same :8089, same model — see the starter README) and:
POSTURE=hardened bash modules/module4/garak/complete/run.sh
```

**A quiet console is normal.** garak's own output goes to the log file, so after
`=== neutral (:8089) ===` the terminal stays silent until the run finishes (the full
set is a few minutes). It is not stuck — watch progress with
`tail -f modules/module4/garak/complete/out/<tag>-<posture>.log` (e.g.
`…/out/full-neutral.log`) in another terminal, or run
`bash modules/module4/garak/complete/run.sh quick`
first for a ~1 min plumbing check. When it finishes it prints the `garak run complete`
summary and the report locations.

The runner calls the VM's `garak` launcher (its own environment), writes a full
log per run, and **stops if a scan fails** rather than printing "reports" over a
crash. Each run writes to `out/<tag>-<posture>*` (`.jsonl` + `.html`), so the
neutral and hardened runs are kept **side by side, not overwritten**. Target is the
one Larkfield on `:8089`; the hardened posture is the **same target restarted with
the hardened prompt** (no new port).

## Finding the details

The `.html` is the **summary**. garak's percentage is **resilience** (higher = the
target resisted more) and DC-5 is its **best** grade — so a low score is the
interesting one. The raw evidence is in `out/`:

- **`<tag>-<posture>.hitlog.jsonl`** — only the **failures**: each prompt that got
  through, with the model's reply. Read this for a low-scoring probe.
- **`<tag>-<posture>.report.jsonl`** — **every** attempt (pass or fail): its `prompt`
  and `outputs`.

```bash
cd modules/module4/garak/complete/out
# what got through, with the reply (empty for a 100% probe — nothing got through):
jq -c '{probe, prompt, output}' full-neutral.hitlog.jsonl
# every prompt + reply for one probe:
jq -c 'select(.entry_type=="attempt" and (.probe_classname|test("encoding"))) | {prompt, outputs}' full-neutral.report.jsonl
```
Read the per-probe evidence, not just the aggregate — the transcript is the finding.

## The finding to look for

Run the full set against each posture (neutral, then hardened) and read the reports
**per probe**, not by the aggregate. You may see the aggregate fall from neutral to
hardened, so the
hardening looks like a win — or you may not; that is for your reports to say. The
point of the lab holds either way: an **aggregate score can hide a per-objective
result that did not move**, so look for one and name it, from your own reports.
(Record your own numbers as the evidence; do not carry numbers measured on a
different target onto this one.)

## What `latentinjection` here actually tests

Don't call this "the retrieval attack hardening can't reach." It isn't:

- **It sends everything as one user message.** `latentinjection.LatentInjectionReport`
  puts its synthetic document *and* its instruction into a single prompt, which this
  REST adapter sends through the app's user `input`. Nothing is planted in the
  knowledge base and fetched later. So a hit means the model obeyed an instruction
  hidden in a **message you sent** — not that Larkfield's retrieval was subverted (and
  it's not the same event as an `OWASP{...}` flag).
- **Hardening does cover retrieval.** Rule 5 of the hardened prompt tells the model to
  treat document/knowledge-base content as untrusted and reject instructions in it. It
  may fail, but it's there — so don't say hardening "ignores" retrieval.

Larkfield's real **retrieve-then-act** flow — content planted in the knowledge base
that the assistant acts on when it *retrieves* it — is the **multi-turn** indirect-injection
route in a later lab, not this one. Inspect this probe's actual prompt and detector, and
record what you saw; don't predict a hit or an unchanged score.

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
3. **Compare with promptfoo (lab 1) — write down precisely what each tool tested.**
   Both are single-turn, and neither reached Larkfield's retrieve-then-act channel:
   promptfoo sent your crafted prompts as user input; garak's `latentinjection` sent a
   document *and* its instruction as one user message. So each answered "does the model
   obey an instruction in the message I sent it?" — not "was the knowledge-base retrieval
   subverted?" State that per tool, rather than a vague "one tool missed, one hit".
4. **Add a probe the batch isn't already running.** The full set already includes
   `dan.DanInTheWild` and `leakreplay.GuardianComplete`, so pick a *different* probe (or a
   whole family) and see whether it finds anything the configured flags don't cover.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
