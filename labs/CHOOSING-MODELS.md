# Choosing your attacker and your judge

## Pick your stack — one provider is enough

The attacker and the judge are two separate models, but **you do not need two
providers**. Pick the stack that matches the account you have, and both roles are
filled from it:

```bash
export AIRT_GROUP=openai     # attacker gpt-4.1 + judge gpt-4o-mini  — needs ONLY OPENAI_API_KEY
export AIRT_GROUP=bedrock    # attacker qwen   + judge haiku         — needs ONLY AWS Bedrock creds
```

That is the whole setup for someone with a single provider. `python3 labs/models.py`
prints exactly what each role (and the Promptfoo grader) resolves to under your
group. Groups live in `models.yaml` under `groups:`.

## Overriding a single role

Every lab reads the choice from the same place (`labs/models.py`), so swapping just
one model is one environment variable — and an explicit override always beats the
group:

```bash
export AIRT_ATTACKER=deepseek    # keep the group's judge, change only the attacker
export AIRT_SCORER=gpt-4.1        # keep the group's attacker, change only the judge
```

Names come from `models.yaml` — the same catalogue the targets use. Keeping the two
roles **separate** matters: if one setting drove both, a change in results could not
be attributed to either. With no group and no overrides, `AIRT_SCORER` falls back to
`AIRT_ATTACKER`, which defaults to `qwen`.

## Why the split is enforced, not just suggested

`labs/models.py` is the single resolver. It also carries the **endpoint-aware**
helpers (`attacker_target`, `litellm_kwargs`) that keep an OpenAI-compatible or
Bedrock model pointed at its real endpoint and key — a bare model name alone
misroutes those to `api.openai.com`, which reads as "this model can't attack/judge"
when the plumbing, not the model, was wrong. Use the resolver; don't hard-code a
model in a lab.

## Where each lab reads the judge

| Lab | Attacker from | Judge from | Notes |
|---|---|---|---|
| **PyRIT** (`modules/module5/pyrit`) | `AIRT_ATTACKER` | `AIRT_SCORER` (`--scorer llm`) | `--scorer marker` is the free deterministic default; `llm` calls a SelfAsk judge |
| **Spikee** (`modules/module4/spikee`) | attack/model opts | `airt_flags` (marker) or **`airt_llm`** (`AIRT_SCORER`) | pick per dataset entry with `judge_name` |
| **scorer exercise** (`modules/module6/scorer-exercise`) | — | `AIRT_SCORER` | `--offline` uses saved labelled verdicts, no key needed |
| **Promptfoo** (`modules/module4/promptfoo`) | HTTP target | **set in the config** (`defaultTest.options.provider`) | the ONE exception — see below |
| **HumanBound** (`labs/humanbound`) | scope engine | same engine (one provider, two roles) | rescore the saved trace for a second judge |

**Promptfoo is the exception.** It is JavaScript and cannot read `models.yaml`, so
its grader lives in `promptfooconfig.yaml` under `defaultTest.options.provider`
(marked `>>> CHANGE YOUR JUDGE HERE <<<`). Set a promptfoo provider id there
directly (`openai:gpt-4.1`, `bedrock:...`) and keep it in step with `AIRT_SCORER`
if you want one judge across all five tools.

## The defaults are a starting point, not a verdict

The shipped defaults (attacker `qwen`, a cheap capable judge such as
`gpt-4o-mini`) are a place to start, **not** a certified "best" scorer. Our own
review is explicit that a high agreement or lift figure does **not** select an
accuracy winner: a judge can score well by never firing SUCCESS, and the same
model changes verdicts when its criterion changes (`labs-ctf/HIGHLIGHTS.md` §
"Ranking LLM judges by raw agreement…" and § 33). So:

- **Run two judges side by side** — a deterministic marker check and a model
  judge — and read the columns together. Where they disagree is the finding.
- **Report the judge and its criterion as part of the result**, and keep the
  status counts (refusals, unparsed outputs, errors) rather than hiding them in
  an agreement percentage.
- **Change the judge and re-run.** It is one variable; treat it like one.

## Bringing your own key vs sponsored Bedrock

Both roles resolve through the same catalogue, so switching between your own API
key and sponsored Bedrock is a catalogue entry, not a code change. Keys for the
non-OpenAI providers live in `.env` (the same file the mock reads). A model with
no reachable key is skipped with a reason, never recorded as a silent failure.
