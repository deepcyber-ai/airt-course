# Getting started - AIRT Harness (Deep Cyber AI Red Teaming Framework)

One canonical, OpenAI-compatible API in front of any target - mock or live - with sessions, an
integrated guardrail, recorded evidence, and replay. Here's what to run. New to the framework? See **[Why AIRT Harness](why-airt-harness.html)** for the architecture and benefits.

> 🖥️ **On the course VM everything is pre-installed under `/opt/airt/src` - no git, no `sudo`.**
> Use `python` (the course venv is on your PATH), and just copy-paste the blocks below.

---

## First - check the VM

Before anything else, run the self-check (or the **"Check this VM"** menu item). It boots each
target briefly, prints PASS/FAIL, and shows an image-identity block naming the harness and
governance refs - **paste that block if you ever report a problem**.

```bash
airt-selfcheck
```

---

## Run a target

One command brings up the whole stack (tool server, target, API and GUI) for a target and prints
its URLs. Each target gets its own ports, so two can run side by side. The authoritative profile
list for *this* image is `~/labs/PROFILES.txt`.

```bash
airt-target larkfield      # Larkfield Assistant (DeepCyber CTF)
airt-target moneyagent     # Money Agent (Deep Vault Capital CTF)
airt-target governance     # Investigations (the agentic runtime governance demo)
airt-target status         # what is running, and on which ports
airt-target stop [name]    # stop one target (larkfield|moneyagent|governance), or all with no name
```

| Target | MCP | target | API | GUI |
|--------|-----|--------|-----|-----|
| Larkfield (twelve `OWASP{…}` flags, synthetic) | 8200 | 8089 | 8000 | 7860 |
| Money Agent (`DVC{…}`/`FCA{…}`, real DB effects) | 8210 | 8090 | 8001 | 7861 |
| Investigations (Cedar runtime governance) | — | 8091 | 8002 | 7862 |

**Three layers - point your tools at the right one.** The **GUI** (e.g. `:7860`) talks to the
**canonical API** (`harness.server`, e.g. `:8000`), which fronts the **target** mock (e.g. `:8089`).
Pointing the GUI at the target's port does not work. Red-team tools use the API
(`/v1/chat/completions`); you can also curl the target directly (see below).

Each target's mock port is whatever its **profile's `api.url`** declares - Larkfield `8089`, Money
Agent `8090`, Investigations `8091` - and `harness.server` dials exactly that. `airt-target` reads the
port from the profile, so the two can't drift; if you launch the mock by hand, its `--port` must match
the profile's `api.url` or the API answers with a 502.

**You need a live model to earn a flag.** With no credentials the stack still comes up, the GUI
works, and `airt-selfcheck` passes (it does not need a live model). But the course profiles read a
**model catalogue**, and there is **no echo fallback** for them: with no key present every chat
message comes back as `[ERROR] LLM backend unavailable`, not an answer - so no attack can fire a flag
until you select a model whose credential is present. `airt-target` prints a note when no key is
present. Add a key first: copy `.env.example` to `.env` (on the VM the active `.env` is
`/opt/airt/src/.env`, one level above both checkouts - do not add a second one deeper in the tree, it
would shadow it) and set one provider (`OPENAI_API_KEY`, or an AWS profile for Bedrock) as
**[Configuring & testing your models](configuring-models.html)** describes, then select that model with the GUI dropdown or `POST /model`. The
startup banner shows the selected model and how many of the catalogue's models have credentials; if
the target logs "No model in models.yaml has credentials present", that is why.

<details><summary>Appendix: the manual four-process recipe (what <code>airt-target</code> runs)</summary>

This starts only the **tool server** and the **target** - the API (`harness.server`) and GUI are the
other two layers, and `airt-target` starts all four. Each target uses its own ports (below), so two can
run at once. Each course profile picks its model from the catalogue and ignores `--backend`
(deprecated; it still steers the five legacy profiles), so with no key present every message returns
`[ERROR] LLM backend unavailable` and no flag fires - there is no echo fallback (see the credentials
note above).

```bash
# Larkfield  (target 8089)
cd /opt/airt/src/airt_harness
python profiles/deepcyber-ctf/vendor/larkfield-db-mcp/server.py --port 8200 --version 1.0.2 &
python -m harness.mock --profile profiles/deepcyber-ctf/profile.yaml --port 8089

# Deep Vault Capital  (target 8090 - NOT 8089; hardened: add --system-prompt profiles/deepvault-capital/mock/system_prompt_hardened.txt)
cd /opt/airt/src/airt_harness
python profiles/deepvault-capital/vendor/dvc-db-mcp/server.py --port 8210 &
python -m harness.mock --profile profiles/deepvault-capital/profile.yaml --port 8090

# Investigations (governance)  (target 8091) - its own checkout as cwd
cd /opt/airt/src/airt_governance
python -m harness.mock --profile profiles/investigations/profile.yaml --port 8091
```
</details>

---

## Talk to it & red-team it

Curl the **target** on its own port (Larkfield `:8089`, Money Agent `:8090`) - the examples use
Larkfield's `:8089`. OpenAI-style tools and the GUI use the **canonical API** `airt-target` also
starts (Larkfield `:8000`, Money Agent `:8001`), not the target port.

```bash
# Send a message (or use the OpenAI-compatible POST /v1/chat/completions)
curl -X POST http://localhost:8089/chat -H "Content-Type: application/json" \
  -d '{"input": "What is an ISA?"}'

# Toggle the HumanBound firewall (guardrail), then re-run the same attacks off vs on
curl -X POST http://localhost:8089/firewall -d '{"enabled": true}'

# Replay recorded sessions against the current target (optional LLM-judge score)
airt-replay profiles/default/intel/ --list-sessions
airt-replay profiles/default/intel/ --session abc123 -o results/replay.md
```

Sessions are kept with the `x-session-id` header. Every request/response is recorded as JSONL
(`mock-audit.jsonl`) - a tamper-evident audit trail every tool shares.

---

## Ports

Each target gets its own set, so two can run side by side.

| Target | MCP | target (mock) | API | GUI |
|--------|-----|--------|-----|-----|
| Larkfield | `8200` | `8089` | `8000` | `7860` |
| Money Agent | `8210` | `8090` | `8001` | `7861` |
| Investigations (governance) | — | `8091` | `8002` | `7862` |

The API fronts the target; the GUI talks to the API. Curl `/chat` and `/firewall` on the target port.

---

## Next

- **[Configuring & testing your models](configuring-models.html)** - add a key, switch models, and test.
- **`labs/CHOOSING-MODELS.md`** (ships with the **course materials**, not on this freshly-booted VM) -
  once you have the course labs, pick a stack with `AIRT_GROUP=openai` or `bedrock`. Nothing on the bare
  image reads that variable yet.
- Each profile's own **README** - its flags and how to trigger them.

_Synthetic targets and data throughout; authorised testing only._
