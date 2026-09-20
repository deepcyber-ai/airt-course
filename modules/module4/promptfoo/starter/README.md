# Lab 1 — promptfoo

```bash
cd modules/module4/promptfoo/starter
npx promptfoo@0.123.0 eval --no-cache
npx promptfoo@0.123.0 view
```

Everything is in `promptfooconfig.yaml`, comments included. Three TODOs at the
bottom of that file are the exercise. The target is Larkfield **L1 neutral**
(`:8089`) — bring it up with `airt-target larkfield`.

**No grader-model charge.** Assertions match on the target's own flag markers
(`OWASP{...}`), which are deterministic, so no grader model is involved.

Two details that break integrations elsewhere and are handled for you here: the
reply field is `output`, and there is no session header, so the harness mints a
fresh conversation per request. Reusing one session would let the first test
spend a flag and leave every later one looking secure.

A marker is a **discovery** signal, not proof of the objective — read the reply
and the evidence to see what actually happened. "No flag" means no configured flag
was observed, which on the neutral target may simply mean the probe was refused —
a valid result to record, not a broken setup.
