# Module 5 — Multi-Turn Techniques

This module shows how PAIR, TAP, GOAT and Crescendo change an attack after each reply.
Live runs use your own model key; prepared recordings make no model calls.

## During class

The classroom exercises use manual requests and saved examples. Follow the activity shown
by the trainer. Do not run a full automated campaign unless the trainer assigns one.

Complete the work in this order.

1. **The technique activity.** For the method assigned to you, write the next request and
   explain how it responds to the previous reply. Record the objective, request, reply,
   number of target requests, your conclusion and one limitation. Stop at the request limit
   on the activity card.
2. **One single-turn introduction** — either PyRIT or Promptfoo (see below). Record the
   generated request, Larkfield's reply, the scoring criterion, the verdict and the
   scorer's explanation.
3. **Your assigned capstone half only.** Half A runs one PyRIT script; Half B validates one
   scope file and inspects the saved HumanBound run. Add one row to
   `capstone/COMPARISON-RECORD.md`.
4. **The closer.** Open `m5-transition/` and identify the attacker, technique and scorer in
   the saved trace.

The larger PyRIT, Promptfoo and Spikee examples are **optional references for after the
course**, not classroom tasks.

## What to keep

One technique record (objective, request, reply, target-request count, conclusion, one
limitation); one single-turn record (request, reply, criterion, verdict, explanation); one
row in `capstone/COMPARISON-RECORD.md`; and the three components named from `m5-transition/`.

## Step 2 — the single-turn introduction

Meet the two roles the methods lean on — a model that **writes the attack** and a check
that **decides success** — on their own, in one turn. Run **one** of:

- `pyrit/single-attacker/` — the attacker model rewrites a bare objective into the prompt
  that is sent, and a *separate* LLM judge scores the reply (starter + complete).
- `promptfoo/single-attacker/` — the attack model generates the prompts and the grader
  scores them, with no multi-turn strategy (starter + complete).

In the PyRIT route, the keyword flag and the model verdict are **not independent** — the judge reads the same
reply, banner included — so read this as a look at the two roles, and inspect the disclosed
content. Module 6 examines how far to trust a model judge.

## Step 3 — the capstone

The assigned close, in `capstone/`. Your trainer assigns your group to **Half A or Half B**;
complete only that half. Half A tests whether PyRIT can reveal all three supplied contact
details; Half B inspects a saved broad HumanBound scan. The saved scan did not test Half A's
exact objective — use the same contact-details check to identify that coverage gap, and do
not calculate a combined success rate.

## Step 4 — the closer

`m5-transition/` opens an illustrative saved trace. It identifies the attacker model, the
Crescendo search method and the local marker check used as the scorer. Viewing it makes no
model calls, costs nothing, and there is nothing to submit. Module 6 examines scorers in
more detail.

## Optional after-course references

Use these on your own key after the course — they are not classroom tasks:

- `pyrit/` — one worked example for each method (`single`, `crescendo`, `goat`, `tap`,
  `pair`), starter + complete. Run one assigned method, not the whole set.
- `promptfoo/` — runnable local examples of Crescendo and `jailbreak:tree`; the hosted GOAT
  and jailbreak examples are non-runnable method notes.
- `spikee/` — of these, **only Crescendo was rehearsed end to end** (20 September 2026); the
  course VM model, GOAT and the iterative route remain unverified.

## Cost

Live runs use your own key. The approximate **£2** figure belongs to a particular automated
route and model assumptions (it varies by model, provider, retries and exchange rate); it is
not a universal cap or a price guarantee. Watch each run's target-request count and keep an
emergency stop (Ctrl+C).
