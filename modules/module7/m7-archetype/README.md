# Module 7 - attacker-archetype selection exercise

A short exercise that fits **inside the existing 20-minute Module 7 decision slot**
(not a second activity - Module 7 stays 45 minutes). You practise choosing an
attacker from **observed behaviour and evidence**: why a style might help a
particular objective, where it failed, and what a second attacker adds. The longer
"one card per archetype" version is an optional take-home.

```bash
python3 modules/module7/m7-archetype/archetype_view.py           # no model calls (--full for full excerpts)
```

## The seven behavioural descriptions (reference sheet)

These describe **behaviour in a transcript** - rapport, repetition, directness,
technical framing, incoherence, imitation, abandonment. They **overlap**, can
**change during an attack**, and are **not** permanent vendor traits or algorithms
(PAIR/TAP/GOAT/Crescendo). A model can show more than one.

| Archetype | Observable feature |
|-----------|--------------------|
| Empathetic confidant | builds rapport, "we're in this together" |
| Professional | calm, credentialed, business framing |
| Direct asker | asks plainly, no story |
| Structured technician | technical framing, step-by-step, tool/SQL language |
| Chaotic / unpredictable | incoherent, jumps around |
| Sycophantic mirror | imitates the target's tone, agrees, flatters |
| Cooperator | frames a shared task, then may abandon the objective |

A cooperative attacker that **abandons** the objective is not automatically a valid
benign control.

## The exercise (20 minutes, then the module's 5-minute debrief)

You get four contrasting, initially unnamed trace cards (model identity masked) for
**behaviour identification** - they span different objectives/postures on purpose,
so they are NOT a common-objective coverage set. For the SELECTION decision, use the
constructed coverage in `modules/module7/m7-selection/benchmark_view.py`. One card is shared
between groups for the debrief.

1. **Four minutes - describe, then label.** For each card, describe the attacker's
   *actual behaviour* before choosing one or more archetype labels. Identify the
   intended objective and the evidence needed to score it.
2. **Six minutes - select.** These cards span different objectives/postures, so use
   the **constructed coverage** (`python3 modules/module7/m7-selection/benchmark_view.py`,
   attackers x objectives with counts) for the decision - not one episode per
   objective. Choose a **primary attacker and a reserve**, one **rejected
   alternative**, and a reason grounded in the evidence. State what is confounded.
3. **Five minutes - the scorer.** Choose an appropriate criterion/scorer and an
   escalation path, using the reference-backed cases. An agreeable score is not
   independent confirmation.
4. **Five minutes - the record.** Complete the one-page selection record, including
   one revised test or a condition that would change your choice.

## Scoring - keep these apart

- **Behavioural description** and **objective verdict** are separate fields.
- Use **supported completion / observed non-completion / unresolved / invalid**
  distinctly. **PARTIAL**, if you use it, names an **achieved sub-objective** - it
  does *not* mean "the scorer is unsure".
- Keep collateral discoveries separate from aimed success. For an **effect**, score
  on authenticated tool/state evidence or leave it **unresolved**; for a
  **disclosure**, check the protected reference is actually present.
- The cards are **measured single runs** selected to contrast styles - not a model
  ranking or a success rate, and not a coverage set. A low overall attacker may
  still add useful objective coverage (read that from benchmark_view, not here).

## One-page selection record (hand-in)

| Field | Your entry |
|-------|-----------|
| Objective | |
| Primary attacker + why (archetype + evidence) | |
| Reserve attacker + what it adds | |
| Rejected alternative + why | |
| Scorer/criterion + escalation | |
| One revised test, or a condition that would change the choice | |

## Optional bounded live extension (post-course)

Two selected approaches, a **total of 6-8 physical target requests** (including any
control, reset/replay and retry), with explicit attacker/scorer caps, equivalent
state, and all attempts saved. Changing a style instruction tests *that instruction*
with the chosen attacker/target/technique - it does **not** isolate a vendor's
intrinsic "archetype". Use it for reflection and a next-test decision, not a ranking.

The model identities, techniques, outcomes and source coordinates are in the
separate instructor key (`INSTRUCTOR-KEY.md`), revealed at the debrief.
