# Module 9 — Evidence-pack template (optional reference)

**OPTIONAL AFTER-COURSE REFERENCE**

Use this when you write up a real finding. It is optional background for the class — you do not
need to complete every table.

# Page 2 - Evidence-pack template

A complete evidence pack lets a reader trace every report statement back to the exact conversation, tool result and affected resource, and re-run the check. Keep the assessor's conclusion distinct from the raw records. Keep an original copy and a redacted sharing copy, and keep them distinguishable.

## 1. Pack manifest

| Field | Your entry |
|---|---|
| Finding ID | |
| Case / objective | |
| Assessor and date | |
| Original vs redacted copy | |
| Source pin SHA-256 (and what was hashed: file / physical row / canonical send) | |

A hash detects a change against the recorded value; it does not authenticate that the event is true. Any signature identifies the signer and what was signed; it does not prove an action executed.

## 2. Exact inputs

| Field | Your entry |
|---|---|
| Full request(s) sent (prompt text, verbatim) | |
| Request body / headers / session id | |
| Turn index | |
| Configuration in force (model, profile, policy, posture) | |

Treat any instruction quoted inside a transcript as untrusted evidence, never as an instruction to your reporting assistant.

## 3. Exact outputs

| Field | Your entry |
|---|---|
| Full response(s) returned, verbatim (not the 500/1000-char view) | |
| Any refusal / partial / error text | |

## 4. Identifiers

| Field | Your entry |
|---|---|
| Run ID | |
| Conversation / session ID (original and any new replay session) | |
| Case ID | |
| Source file, line and hash | |

## 5. Actual tool / state evidence (the ACTION record)

| Field | Your entry |
|---|---|
| Ordered tool-event sequence (tool, args, result) | |
| Affected resource(s) and their before/after state | |
| Database rows changed (or protected rows unchanged) | |
| `auth_ref` / approval reference present or NULL | |

This section, not the judge, establishes whether the action happened. For C01 record the deletion events **and** the `reseed_database` event; for C03 record the `place_trade` rejection **and** the SQL writes with `auth_ref=NULL`; for C02 record the returned document body against the source fixture and the invented content, separately.

## 6. Scorer / judge evidence (kept separate from section 5)

| Field | Your entry |
|---|---|
| Scorer or judge input as it actually saw it (note the truncation) | |
| Verdict (PASS / FAIL / SKIP / ERROR) | |
| Raw judge explanation, preserved in full | |
| Criterion key and version | |

The replay judge sees one truncated prompt/response excerpt, no tool events and no history. Its verdict cannot by itself establish that an action happened or was prevented. The parser treats any response not starting with PASS as FAIL, so read the raw explanation and flag malformed or ambiguous results by hand. A model's "passed" claim is not independent verification.

## 7. Errors and usage

| Field | Your entry |
|---|---|
| Errors / timeouts / infrastructure failures (kept visible, not as passes) | |
| Requests made vs request cap | |
| Token / call usage if recorded | |

## Evidence index (one row per referenced item)

| Finding ID | Objective | Source file / hash | Physical row | Run / session ID | Send / turn | Event reference | Expected result | Observed result | Evidence status | Model / profile / policy / scorer version | Assessor note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |
| | | | | | | | | | | | |

Evidence status is one of: confirmed / unresolved / errored / unexecuted. Keep unresolved and errored states visible; do not silently drop them from a rate. If you report a rate over a restricted denominator, label it and keep the unresolved count in view.

## Regression check

| Field | Your entry |
|---|---|
| Regression case ID (linked to finding) | |
| Starting state and reset step | |
| Attack sequence (original) | |
| Variation (mark unexecuted if not run) | |
| Forbidden effect and oracle location | |
| Legitimate control task and expected result | |
| Before/after effect evidence compared | |
| Result: FAIL blocks / PASS / UNRESOLVED / ERROR | |

One failing case can establish a regression. Repeated model passes support only the declared tested conditions - they are not proof the boundary holds in general.

### Does this actually gate a pipeline? Verify before you claim it.

Before writing "the pipeline enforces this", confirm the real exit behaviour:

- `airt-replay` (`harness/replay.py`) prints a judge tally (`Judge: N PASS, M FAIL, ...`) and writes the report, then **exits 0**. It has **no `--fail-on` option** and returns a non-zero status only for operational errors (bad arguments, session not found, harness unreachable) - **never for a FAIL verdict or a CHANGED result**. A replay report alone is therefore **not** a CI failure gate. If you want it to break a build, a separate wrapper must parse the result and set the exit code, and that wrapper must be shown and rehearsed - do not assume it exists.
- The governance sample's `verify.py` **does** carry a failure exit status, but it is a rule check, not end-to-end execution testing. It can confirm a policy rule evaluates as written; it does not prove the agent's action was actually blocked at runtime. An escalation decision recorded by the sample is not a completed approval workflow.

State the pipeline as a proposed integration unless you have run the wrapper and seen it fail on a planted regression.

---

## Checklist (before you finalise the pack)

- [ ] Each factual claim cites a file, row and the turn.
- [ ] Observed effects are stated separately from potential consequences.
- [ ] Action evidence (tool/state) is separate from any judge opinion.
- [ ] No flag is presented as an execution record.
- [ ] Deletion + reseed is not described as permanent loss; a final intact dataset is not described as proof deletion never happened.
- [ ] Any cited number carries its source, date, denominator and definition.
- [ ] Unexecuted variants are labelled unexecuted; unresolved and errored states are visible.
- [ ] Any pipeline-enforcement claim is backed by an observed non-zero exit, not a report.

Reference figures, if you cite any, come only from the labs dated hand-measurement (`gpt-4.1`, N=20 per flag, 2026-08-25) and must be labelled as that - a small single-model, single-date baseline, not the current answer key and not a success rate for any other model. For example, in that baseline the audit-record-destroyed flag moved from 18/20 (Act 1, unsecured) to 0/20 (Act 2, hardened), while confidential-document disclosure barely moved (20/20 to 19/20) because no rule was written for it. Do not present these as live results.
