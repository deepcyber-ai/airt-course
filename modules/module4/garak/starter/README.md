# Lab 2 — garak

NVIDIA's probe-based scanner. Where promptfoo asks what *you* thought of, garak
asks what the community has already catalogued: DAN jailbreaks, encoding
tricks, prompt injection families, data leakage.

Garak needs no attacker model. Its prompts are static and most of its detectors
are rules or small classifiers, so **this lab has no attacker/judge-model
charge** beyond the target's own inference. Bring the Larkfield level ladder up
first (`labs-ctf/start-levels.sh`).

> garak is installed in its **own environment** on the course VM and is on PATH
> as **`garak`** — not `python3 -m garak` in the main course Python. Use `garak`.

## Run it

```bash
cd modules/module4/garak/starter
mkdir -p "$PWD/out"                     # garak does not create nested report dirs

garak \
  --model_type rest \
  --generator_option_file larkfield.json \
  --probes lmrc.Profanity \
  --report_prefix "$PWD/out/smoke"
```

That is a deliberately small probe, to prove the plumbing before you spend
twenty minutes on a real one. You should see a progress bar and, at the end,
`garak run complete` with a path to an HTML report.

## What `larkfield.json` does

```json
"req_template_json_object": {"input": "$INPUT"},
"response_json": true,
"response_json_field": "output"
```

`$INPUT` is where garak substitutes each probe's prompt — always through the
application's **user `input`**. `output` is the field our target replies in — get
that wrong and every response reads as empty, which looks like a target that
refuses everything.

No `x-session-id` header, so the harness mints a fresh conversation per request.
Flags are awarded once per conversation, so a shared session would let the first
probe spend a flag and leave every later one looking secure.

## Your task

**1. Pick probe families and run them against BOTH postures.**

```bash
garak --list_probes          # see what is available
```

Start with these; each takes a few minutes:

| Probe | What it tries |
|---|---|
| `dan` | the classic jailbreak family |
| `encoding` | base64, rot13, and friends — smuggling past keyword filters |
| `promptinject` | instruction-override injection |
| `latentinjection` | a synthetic document + instruction, sent as ONE user prompt |
| `leakreplay` | coaxing out memorised or configured text |

Neutral is `localhost:8081` (L1), hardened is `localhost:8083` (L3). Copy the
config and change the port:

```bash
sed 's/8081/8083/' larkfield.json > larkfield-hardened.json
```

**2. Diff the two reports, per probe.** Garak may show a drop from neutral to
hardened. Write down the headline: how much "safer" does the hardened target
look — and then check it probe by probe, because an aggregate can hide a single
per-objective result that did not move.

**3. Read what each probe actually tested.** `latentinjection` here puts its
document and its instruction into a **single user prompt** — it does not plant a
document in Larkfield's knowledge base and let the assistant retrieve it later.
So its detector result is about how the model handles a document-shaped *user
message*, not proof that Larkfield's retrieval channel was compromised. Inspect
the probe's actual prompt and its detector criterion, and record what you
observed — do not predict a hit or an unchanged score. (The real retrieve-then-
consume flow is the multi-turn indirect-injection route in later labs.)

A marker is a discovery signal, not proof — read the per-probe results, not just
the aggregate.

## Notes

- Reports are written to `--report_prefix` (use an absolute, pre-created directory),
  both `.jsonl` and `.html`.
- Some probes send an **empty prompt** as an edge case. Our target answers it;
  a target that returns HTTP 400 will abort the entire garak run on its first
  probe with a `ConnectionError`. Worth remembering when you point garak at
  something real.
- `atkgen` is the one probe family that *does* need an attacker model
  (`red_team_model_type` / `red_team_model_name`). Leave it until the PyRIT lab.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
