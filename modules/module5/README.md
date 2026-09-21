# Module 5 — Multi-Turn Techniques

In this module, you will see how an attack changes over several requests. We will work
through PAIR, TAP, GOAT and Crescendo, then practise using the supplied examples. Follow
the tool route assigned to you. You do not need to run every implementation. You use your
own model key.

## The technique examples (PyRIT)

The PyRIT folder contains one short example for each method. The starter version asks you
to set the objective; the complete version shows a worked example. Each run records its
requests and saves the conversation for inspection.

- `pyrit/` — `single`, `crescendo`, `goat`, `tap`, `pair`, each with a **starter** (you
  set the objective) and a **complete** (worked).

## Optional — one tool set, not all

Each student or pair runs **one** of these, on your own model key. Same target, same
read-only objective (cross-customer PII), for configuration study — not a ranked
comparison:

- `promptfoo/` — the same methods as promptfoo redteam strategies (two runnable local
  strategies; two hosted ones are method notes, not run here).
- `spikee/` — the same methods via spikee `--attack`. **Not yet rehearsed end to end** —
  treat it as a post-course reference, not a dependable classroom fallback.

## Capstone — two approaches, then compare (~20 min)

The assigned close. Split the room: **Half A** drives a named multi-turn technique with a
larger budget (PyRIT); **Half B** declares a scope and inspects a prepared HumanBound run.
The recording did **not** test Half A's contact-details objective. Compare how the two
approaches work, the requests used and the evidence recorded, and explain that coverage
gap rather than ranking their success rates. Label the HumanBound run as a recorded
example — a declared scope does not show that every objective was tested.

## Also here

- `m5-transition/` — the closing reveal (an illustrative saved trace, labelled).
- `m5-attempt/` — **reference only, superseded by the capstone as the close.**

## Cost

You use your own key and run one tool set. The approximate **£2** figure belongs to the
particular automated route and model assumptions (varies by model, provider, retries and
exchange rate); it is not a universal cap or a price guarantee. Watch each run's target
request count and keep an emergency stop (Ctrl+C).
