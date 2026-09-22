# Lab 1 — promptfoo

> **OPTIONAL AFTER-COURSE REFERENCE.** Not part of the classroom task unless your trainer assigns it.

```bash
cd modules/module4/promptfoo/starter
npx promptfoo@0.123.0 eval --no-cache
npx promptfoo@0.123.0 view
```

> **On the course VM** promptfoo is installed globally at the pinned version, so you can
> drop the `npx promptfoo@0.123.0` prefix and just run `promptfoo eval …` and
> `promptfoo view`. (The `npx` form above is the portable version for your own machine.)

Everything is in `promptfooconfig.yaml`, comments included. Three TODOs at the
bottom of that file are the exercise. The target is Larkfield **L1 neutral**
(`:8089`) — bring it up with `airt-target larkfield`.

**Complete the read-only tasks only, unless the trainer explicitly assigns the deletion
task.** The deletion changes the database and needs an isolated target and a verified reset,
so it is not for a shared classroom target.

**No grader-model charge.** Assertions match on the target's own flag markers
(`OWASP{...}`), which are deterministic, so no grader model is involved.

**What you'll see.** promptfoo prints `Running N test cases…` and shows progress while the model
answers, then the results table and a `passed / failed` summary. Short pauses can
occur while requests are in progress. **Finding the details:** `promptfoo view` opens every prompt, reply and assertion result in a browser; the same data is the SQLite DB at `$PROMPTFOO_CONFIG_DIR/promptfoo.db`.

The configuration reads Larkfield's reply from the `output` field and starts a new
conversation for each test. Keep these settings. Larkfield awards each flag once per
conversation, so reusing a conversation could hide the same result in later tests.

A marker is a **discovery** signal, not proof of the objective — read the reply
and the evidence to see what actually happened. "No flag" means no configured flag
was observed, which on the neutral target may simply mean the probe was refused —
a valid result to record, not a broken setup.
