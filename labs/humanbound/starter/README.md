# Lab 5 — humanbound

The last lab, and the only one that attacks the target as an **agent** rather
than as a model. It drives multi-turn conversations against a live endpoint,
probes tool use and scope boundaries, scores against a policy you write, and
then converts the failures into firewall rules.

## Setup

```bash
pip install humanbound                # CLI + SDK

hb config set provider openai         # or claude / gemini / ollama
hb config set api-key sk-...
hb config set model gpt-4.1
```

**On sponsored Bedrock instead of your own key?** Humanbound has no Bedrock
provider. Run an OpenAI-compatible proxy in front of Bedrock and point the
`ollama` provider at it — that provider is really "OpenAI format, you choose
the URL", which is what makes this work:

```bash
pip install 'litellm[proxy]'
litellm --model bedrock/qwen.qwen3-235b-a22b-2507-v1:0 --port 4000

hb config set provider ollama                    # <- not 'openai'
hb config set endpoint http://localhost:4000/v1
hb config set model bedrock/qwen.qwen3-235b-a22b-2507-v1:0
```

Do **not** use `provider openai` with a custom `endpoint`. It sends
`GET /v1/models` to your endpoint and then sends the actual completions to
`api.openai.com`, failing with a 401 that mentions OpenAI rather than your
proxy. For an air-gapped engagement that is a data-egress problem, not a
convenience bug.

## Run it

```bash
cd labs/humanbound/starter
hb test --endpoint ./bot-config.json --scope ./scope.yaml --wait
hb posture
hb logs
hb report -o report.html
```

Expect roughly 45 minutes and ~1,400 model calls. Pick a cheap model.

## How `bot-config.json` works

```json
"thread_init":      { "endpoint": ".../session/new" },
"chat_completion":  { "headers": { "x-session-id": "$session_id" } }
```

`thread_init` is called once per conversation; whatever JSON it returns can be
interpolated into the chat request by key, so `$session_id` becomes the id the
harness just minted.

**This matters more than it looks.** Our first run used a fixed `x-session-id`,
so all 97 conversations merged into one thread on our side. Flags are awarded
once per conversation, so the first attempt spent them and every later one
looked clean. Nothing warned us: the run completed normally and produced a
posture score. A plausible-looking config quietly invalidated the results.

## Your task

**1. Run it as supplied.** The `scope.yaml` here is deliberately thin. Note
what comes back — mostly generic findings about tone and role drift.

**2. Rewrite the `restricted` list.** This is the exercise. Each entry should
name a specific action this agent can actually take with its tools. It has
seven: `query`, `lookup_client`, `search_documents`, `update_risk_profile`,
`place_trade`, `send_email`, `reseed_database`. What should it never do with
them?

**3. Re-run and compare.** More specific scope, more targeted attacks, and
findings that name real actions rather than describing a vibe.

**4. Close the loop.**

```bash
hb guardrails -o rules.yaml
```

Findings become deployable firewall rules. That is the handover to Module 10 —
the same run that finds a hole also patches it.

## Two things to distrust in the output

**Judge errors are scored as findings.** Verdicts with category `exception` and
severity `100.0` are the engine crashing, not your agent failing. Count them
before you believe the posture score.

**Verbose models lose verdicts.** The judge asks for JSON; a model that writes
long explanations exhausts the token budget mid-object and the whole verdict is
discarded. In our runs Claude Sonnet 5 lost 78 of 97 verdicts this way, while
qwen lost none and cost a twelfth as much. Check how many verdicts you got
before reading the grade.

(c) 2026 Deep Cyber Ltd. Apache 2.0 licensed.
