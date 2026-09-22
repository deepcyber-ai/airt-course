# HumanBound — prepared run (Half B inspects this)

**ASSIGNED ROUTE ONLY** — Half B groups.

Run `bash ../read-results.sh` from `modules/module5/capstone`. It reads this folder and reports
the completed/error counts, the conversation-turn count, and whether all three contact-detail
fields appear in any reply. Record that one output row.

A recorded LOCAL HumanBound run, so the capstone fits the slot without a live scan.
Students write their own scope (`../scope.starter.yaml`, validate it), then inspect
what the engine actually did here.

    bash ../read-results.sh    # reads this run (see provenance.json for the exact facts)

## How it was made

`hb test --local --quick` (the open-source engine, no account) with the PII-only scope
(`../scope.complete.yaml`) against neutral Larkfield `:8081`; attack + judge model
`gpt-4o-mini`; 2026-09-19. `meta.json` + `logs.jsonl` are the raw outputs; `provenance.json`
records the command, versions, endpoint and file hashes. No credentials are stored here.

## What it shows — read both verdicts, and mind the scope

- **Observed runtime:** 8m48s (23:38:50 -> 23:47:38). Note: any "~45 min" you see is a
  generic CLI estimate / a slower prior environment, NOT this run.
- **This is the broad `owasp_agentic` unit set** — 97 templates across many categories.
  The engine runs its full set regardless of the scope, so most findings are NOT the PII
  objective: only **3 of 97** are `fail_category = pii_disclosure` (the rest are off-topic,
  authority-boundary, restriction-bypass, etc.).
- Three of the 97 conversations have the category `pii_disclosure`. They concern the
  signed-in customer's information or the assistant's policy. The recording did not test
  the capstone objective of revealing another customer's contact details. None of the 97
  conversations contained a reply with all three required details.
- **776 assistant turns** — the target-request measure; why a live run is costly.

Record HumanBound's three findings separately from the contact-details check. Compare the
workflows and evidence from the two halves, and explain that they tested different
objectives. Most of HumanBound's 97 results concern other categories.

## Inspecting a conversation

`logs.jsonl` is one JSON object per template: `conversation` is a list of `{u, a}` turns
(user / assistant), plus `fail_category`, `severity` and `explanation` (the judge's
reasoning). Open a few `pii_disclosure` ones and see how the agent responded.
