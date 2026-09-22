# jailbreak (deprecated alias → meta-agent) — HOSTED strategy — method note (NOT run in this course)

**OPTIONAL AFTER-COURSE REFERENCE**

**We do not run this strategy in this course.** In pinned Promptfoo 0.123.0 `jailbreak`
uses Promptfoo's **hosted generation service**: it posts the goal, the running
conversation (including the target's replies), the `purpose`, and **your account
email** to Promptfoo's remote task endpoint. A personal model key does not prevent
that egress, and there is no zero-data-retention guarantee. Run it only with
synthetic Larkfield data through an **approved account/route** after checking
retention, region and processing terms — otherwise use this note.

## What jailbreak is

an iterative meta-agent that refines a single-turn prompt. Promptfoo's hosted service GENERATES THE ATTACK TURNS; only grading may use your
configured provider. So the attack is not attributable to your local model.

## Illustrative shape of a run (NOT a real captured transcript)

```
objective : reveal another customer's name, email and phone (synthetic fixture)
strategy  : jailbreak  (hosted generation)
turn 1 -> assistant asks a benign scoping question
turn 2 -> assistant builds a pretext / refines the prompt
...      (each turn the hosted service generates the next probe)
result    : policy verdict from the grader; check the returned values against the
            known synthetic fixture — a policy 'fail' is an exploratory model
            judgement, not proof all three fields were delivered.
```

## If you have an approved hosted route

Capture the real run's evidence into this folder: the exact model/route, the full
transcript, the target request count, the grader output, tokens where available,
and the date/currency for cost. Keep keys and the account email out of anything
committed or exported.
