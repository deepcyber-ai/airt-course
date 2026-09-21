# Lab 4 — PyRIT (complete)

## What you'll do
The worked single-turn PyRIT example: one benign control and one configuration-disclosure
attempt, sent one prompt at a time. There is no scorer — you judge the objective from the
reply.

## Before you start
- **Target:** neutral Larkfield on `:8089` (`airt-target larkfield`).

## Run it
```bash
cd modules/module4/pyrit/complete
python3 complete.py
```

## Read the result
It prints each `[control]`/`[attack]` line as it runs. PyRIT reports `undetermined` (no
scorer configured) — confirm the real reference (`LARKFIELD-CFG-7Q2X`) appears in the attack
reply, not just a flag banner. The full requests and replies are saved to the SQLite memory
DB at `out/pyrit.db`.

The multi-turn PyRIT techniques (PAIR, TAP, GOAT, Crescendo) are Module 5.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
