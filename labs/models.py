"""Resolve the attacker and scorer models chosen in the evaluation module.

One place decides which model attacks and which model judges, so a lab does not
hard-code either and switching between an attendee's own API key and sponsored
Bedrock is one environment variable rather than five config edits.

    export AIRT_ATTACKER=qwen        # what you picked as the attacker
    export AIRT_SCORER=gpt-4.1       # what you picked as the judge

Names come from ``models.yaml`` at the repo root — the same catalogue the
targets use. ``AIRT_SCORER`` falls back to ``AIRT_ATTACKER`` when unset.

Keeping them separate matters. If one setting drives both roles, a change in
results cannot be attributed to either, and you have a confounded experiment
rather than a comparison.

(c) 2026 Deep Cyber Ltd. Apache 2.0 licensed.
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml

try:
    # Keys for the non-OpenAI providers live in .env, the same file the mock
    # reads. Without this a key that is plainly present on disk reads as
    # absent, and the model is skipped as unreachable.
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

DEFAULT_ATTACKER = "qwen"

_CATALOGUE = Path(__file__).resolve().parent.parent / "models.yaml"


def catalogue() -> dict:
    data = yaml.safe_load(_CATALOGUE.read_text()) or {}
    return data.get("models", data)


def groups() -> dict:
    """The named single-provider stacks, so a student with only ONE provider can
    fill BOTH roles. See models.yaml `groups:` (openai / bedrock)."""
    data = yaml.safe_load(_CATALOGUE.read_text()) or {}
    return data.get("groups", {})


def _group() -> dict:
    """The selected AIRT_GROUP's config, validated, or {} when unset."""
    name = os.environ.get("AIRT_GROUP")
    if not name:
        return {}
    gs = groups()
    if name not in gs:
        raise SystemExit(
            f"AIRT_GROUP='{name}' is not a group. Available: {', '.join(sorted(gs))}")
    return gs[name]


def resolve(role: str = "attacker") -> tuple[str, dict]:
    """Return (name, spec) for ``attacker`` or ``scorer``.

    Precedence: an explicit AIRT_ATTACKER / AIRT_SCORER always wins; then the
    AIRT_GROUP's model for that role; then (for scorer) the resolved attacker;
    then the default. So `export AIRT_GROUP=openai` fills BOTH roles from one
    provider, and a single AIRT_SCORER override still swaps just the judge.
    """
    g = _group()
    if role == "scorer":
        name = (os.environ.get("AIRT_SCORER") or g.get("scorer")
                or os.environ.get("AIRT_ATTACKER") or g.get("attacker")
                or DEFAULT_ATTACKER)
    else:
        name = (os.environ.get("AIRT_ATTACKER") or g.get("attacker")
                or DEFAULT_ATTACKER)

    models = catalogue()
    if name not in models:
        raise SystemExit(
            f"'{name}' is not in models.yaml. Available: {', '.join(sorted(models))}"
        )
    return name, models[name]


def promptfoo_grader() -> str:
    """Promptfoo can't read this catalogue, so its lab config carries the grader
    id; this returns the right one for the selected group (default openai)."""
    return _group().get("promptfoo_grader", "openai:gpt-4o-mini")


def compare_pair() -> list[str]:
    """The two same-provider attacker names for the Module 6 comparison activity,
    from the selected group (falls back to the default attacker twice)."""
    c = _group().get("compare")
    return list(c) if c else [DEFAULT_ATTACKER, DEFAULT_ATTACKER]


def as_litellm(name: str, spec: dict) -> str:
    """Catalogue entry -> a LiteLLM model string.

    LiteLLM is how PyRIT reaches anything that is not OpenAI, and it is also
    what a proxy in front of Bedrock speaks.

    NOTE: this returns the model string only. For any provider that is
    OpenAI-*compatible* rather than OpenAI itself, the endpoint and key matter
    as much as the name — use ``attacker_target()`` instead of building a
    LiteLLMChatTarget from this alone.
    """
    if spec.get("type") == "aws-bedrock":
        return f"bedrock/{spec['model']}"
    if spec.get("type") == "ollama":
        return f"ollama/{spec['model']}"
    return f"openai/{spec['model']}"


def attacker_target(name: str, spec: dict):
    """Build a PyRIT chat target for a catalogue model, endpoint and all.

    ``as_litellm`` returns ``openai/<model>`` for every non-Bedrock entry and
    drops ``base_url`` and ``api_key_env`` on the floor. That is correct only
    when the provider really is OpenAI. For gemini-flash (Google's
    OpenAI-compatible endpoint) and glm (Fireworks) it sent the request to
    api.openai.com, which fails with an unauthorised model rather than
    anything that names the real cause — so both read as "this model cannot
    be an attacker" when the catalogue entry was fine and the plumbing was not.

    Returns None when the model cannot be reached, so a caller can skip it and
    say why rather than recording an empty result that looks like a refusal.
    """
    from pyrit.prompt_target import LiteLLMChatTarget

    kind = spec.get("type")
    if kind == "aws-bedrock":
        return LiteLLMChatTarget(model_name=f"bedrock/{spec['model']}")
    if kind == "ollama":
        return LiteLLMChatTarget(model_name=f"ollama/{spec['model']}",
                                 endpoint=spec.get("base_url",
                                                   "http://localhost:11434"))

    # openai-compatible and fireworks both speak the OpenAI wire format; they
    # differ only in endpoint and key.
    base = spec.get("base_url") or (
        "https://api.fireworks.ai/inference/v1" if kind == "fireworks"
        else "https://api.openai.com/v1")
    key_env = spec.get("api_key_env") or (
        "FIREWORKS_API_KEY" if kind == "fireworks" else "OPENAI_API_KEY")
    key = os.environ.get(key_env)
    if not key:
        return None
    return LiteLLMChatTarget(model_name=f"openai/{spec['model']}",
                             endpoint=base, api_key=key)


def litellm_kwargs(name: str, spec: dict):
    """LiteLLM completion kwargs for a catalogue model, endpoint AND key — the
    same routing attacker_target() applies, for callers that talk to litellm
    directly (e.g. a one-shot single-turn generation) rather than through a
    PyRIT LiteLLMChatTarget. Using as_litellm() alone here is the bug this
    avoids: it drops base_url/api_key and misroutes OpenAI-compatible/fireworks
    models to api.openai.com. Returns None when a required key is absent, so the
    caller can skip and say why rather than recording a false failure."""
    kind = spec.get("type")
    if kind == "aws-bedrock":
        return {"model": f"bedrock/{spec['model']}"}
    if kind == "ollama":
        return {"model": f"ollama/{spec['model']}",
                "api_base": spec.get("base_url", "http://localhost:11434")}
    base = spec.get("base_url") or (
        "https://api.fireworks.ai/inference/v1" if kind == "fireworks"
        else "https://api.openai.com/v1")
    key_env = spec.get("api_key_env") or (
        "FIREWORKS_API_KEY" if kind == "fireworks" else "OPENAI_API_KEY")
    key = os.environ.get(key_env)
    if not key:
        return None
    return {"model": f"openai/{spec['model']}", "api_base": base, "api_key": key}


def describe(role: str = "attacker") -> str:
    name, spec = resolve(role)
    kind = "Bedrock" if spec.get("type") == "aws-bedrock" else "own key"
    return f"{role}: {name} ({spec.get('model')}, {kind})"


if __name__ == "__main__":
    grp = os.environ.get("AIRT_GROUP")
    print(f"  AIRT_GROUP = {grp or '(none)'}  "
          f"[available: {', '.join(sorted(groups())) or 'none'}]")
    for r in ("attacker", "scorer"):
        try:
            print(" ", describe(r))
        except SystemExit as e:
            print(" ", e)
    print(f"  promptfoo grader = {promptfoo_grader()}")
