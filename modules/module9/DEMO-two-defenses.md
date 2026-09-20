# Demo script — two runtime defenses, one finding (with our HumanBound recording)

**Thesis.** Show **two different runtime-defense approaches** and contrast what each catches.
They run on **different examples** (that is part of the point — different controls suit
different failures), not one shared finding: guardrails/firewall on our **Larkfield**
config-disclosure scan; Cedar governance on the **DeepTrace investigations** evidence-disposal
app (a *different* application and objective).

Verified 2026-09-20: `hb guardrails` produced 4 CANDIDATE rules from our Larkfield recording,
and a firewall **configured to forbid the disclosure** returned **BLOCK** on the recorded
attack reply and **PASS** on a benign reply (an offline check of saved content). The governance
side runs live on its own app.

---

## 0. The shared finding — our recording

The recorded HumanBound run: **304 single-turn tests, 8 disclosed `LARKFIELD-CFG-7Q2X`**
(system_exposure, critical). Inspect it:

```bash
python3 course-production/module4/native-demo-examples/humanbound/prepared-run/read-results.py
```

## Defense 1 — HumanBound guardrails (learned attack patterns → firewall)

Turn the scan's findings into runtime rules, straight from our recording:

```bash
cd course-production/module4/native-demo-examples/humanbound
# (restore the run into .humanbound/results/<exp> first if you deleted it — meta.json + logs.jsonl from prepared-run/)
hb guardrails --format yaml -o rules.yaml          # 4 rules, block, sourced from our run
hb guardrails --vendor openai  -o rules-openai.json # same, in OpenAI-moderation format
```

Rules generated (from our run): **system_exposure** (the config leak) · **restriction_bypass**
· **off_topic_manipulation** · **format_violation** — all `action: block`. **These are
CANDIDATE rules** — a starting point for a control, not yet wired into the firewall.

Separately, configure a firewall to forbid the disclosure and check saved content against it.
The demo does an **offline** check of the recorded attack/benign replies (it does not rerun the
attack live in front of the target, and does not auto-load the exported rules — the firewall
judges against its `agent.yaml` scope). The firewall is
**tiered**, and the tiers differ on whether they need a model key:

- **Tier 1** — heuristic attack detectors. **No key.**
- **Tier 2** — a local classifier trained from the run logs (`hb firewall train --model
  detectors/m.py` → a `.hbfw` file, loaded via `Firewall.from_config(..., model_path=...)`).
  **No per-request key** — it runs locally.
- **Tier 3** — an **LLM judge** that reads the reply against the scope. This is the layer I
  demoed live, and it **does need a model key** (the attendee's own key, same as the rest of
  the course): `HB_FIREWALL_PROVIDER=openai HB_FIREWALL_API_KEY=$OPENAI_API_KEY`.

Live check (Tier 3 judge, gpt-4o-mini), on a disclosing turn from our recording:

```python
from hb_firewall import Firewall, Turn
fw = Firewall.from_config("agent.yaml")            # HB_FIREWALL_PROVIDER/API_KEY in the env
fw.evaluate(user, session_turns=[Turn(user, assistant)]).verdict
#   the config-leak turn -> Verdict.BLOCK   ;   a benign returns-policy turn -> Verdict.PASS
```

*What it catches:* the **language/pattern** of the attack, learned from what actually
succeeded. Broad — but Tier 3 is an LLM judge's opinion on the text (and costs a call).

## Defense 2 — Cedar runtime governance (DeepTrace investigations)

The governance demo (already running, GUI at http://localhost:7860). The **Cedar rung**
authorizes each tool call **deterministically**, on the evidence item's lifecycle state
(legal hold, retention) and the live **session risk** — not on the wording.

- **Act 2b:** the *same* disposal is **ALLOWED** on a clean session, then **DENIED** when
  only the session-risk signal changed. Model and prompt identical — governance denies on a
  *condition*.

*What it catches:* the **action and its context/scale**, regardless of how the request was
phrased. Narrow, but certain.

## The contrast — the teaching point

| | HumanBound guardrails | Cedar governance |
|---|---|---|
| Derived from | past attacks that succeeded (our scan) | a written policy over context + scale |
| Decides on | the attack's language/pattern (LLM judge) | the action, lifecycle state, session risk (deterministic) |
| Strength | breadth — catches variations of known attacks | certainty — sees context the model/pattern-filter cannot |
| Weakness | an opinion on text; novel phrasings can slip | only covers what the policy models |

**Both are *candidate* controls.** A guardrail export is not proof the problem is fixed
(Module 4 said this). Test each: retest the original attack (should now be blocked/denied)
**and** a legitimate task (should still work).

## No enterprise product, no HumanBound account

Everything here ran **locally with no HumanBound login**: `hb test --local`, `hb guardrails`,
and the firewall. The only key is the attendee's **own model-provider key** (OpenAI/Bedrock/…),
for the Tier 3 LLM judge — the same key they use everywhere else in the course. Tiers 1–2 need
no key. HumanBound's platform (login, continuous monitoring, cross-cycle enriched rules) is
optional and not used by this demo or the lab.

## Will it work? — yes, proven live

- **Guardrail rule generation from our recording:** 4 rules, both HumanBound and OpenAI formats.
- **Firewall check (offline):** a firewall configured to forbid the disclosure returned
  **BLOCK** on the recorded config-leak reply and **PASS** on a benign reply — bundled
  `hb_firewall`, own model key, no account. It checks SAVED content and judges against its
  scope; it does not rerun the attack live or auto-wire the exported rules.
- **Governance side:** runs live on its own app (DeepTrace investigations, :7860) — a different
  application and objective from the Larkfield example.

So the two defense APPROACHES are demonstrable; they are shown on their own examples.
