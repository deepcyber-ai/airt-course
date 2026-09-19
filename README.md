# AMLUCS 2026 — Course Labs

The hands-on labs for the AI Red Team course.

## Start here

Go to the module you're on and open its README:

```
modules/module4/README.md      # e.g. Module 4
```

Each module README walks you through that module's labs and the exact commands.

## What's in this repo

| Folder / file | What it is |
|---|---|
| `modules/module1…10/` | **The labs for each module — this is where you work.** Open the README in your module. |
| `labs-ctf/` | The Capture-the-Flag exercises (encoding, blind, supply-chain, levels), run against a shared target ladder. Used in Modules 4 and 8. Bring the targets up with `bash labs-ctf/start-levels.sh`. |
| `labs/` | Shared helper **code** the labs import (model selection, flag detection, reset). You don't run these directly — the exercises call them. |
| `models.yaml` | The catalogue of **attacker / judge** models the tools use. Not the target — that's already running on the VM. |

**About the names:** `labs/` is a code library, `labs-ctf/` are exercises you *do*, and the per-module labs live under `modules/`. Three different things that unluckily share the word "labs".

## Before you run a lab

Your VM already has the model credentials set up. Pick a model group once per shell:

```bash
export AIRT_GROUP=openai        # or: bedrock
python3 labs/models.py          # prints what that resolves to
```

Then follow the commands in your module's README.
