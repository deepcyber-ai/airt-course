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

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import yaml

def _parse_env_line(line: str):
    """Parse one .env line into (KEY, VALUE), or None for a blank/comment line.

    Supports ``export KEY=...``, single/double quotes, and a trailing `` # comment`` on an
    unquoted value. Raises ValueError on a malformed assignment (invalid name, unterminated
    quote) so a corrupt credential file is never loaded silently."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if "=" not in stripped:
        raise ValueError(f"not a KEY=VALUE line: {line!r}")
    key, _, rest = stripped.partition("=")
    key = key.strip()
    if key.startswith("export "):
        key = key[len("export "):].strip()
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
        raise ValueError(f"invalid variable name: {key!r}")
    rest = rest.strip()
    if rest[:1] in ("'", '"'):
        quote = rest[0]
        end = rest.find(quote, 1)
        if end == -1:
            raise ValueError(f"unterminated quote for {key}")
        val = rest[1:end]
        trailing = rest[end + 1:]
        if not re.match(r"^(\s*|\s+#.*)$", trailing):
            raise ValueError(f"unexpected text after quoted value for {key}: {trailing!r}")
    else:
        m = re.search(r"\s#", rest)          # whitespace-then-# starts an inline comment
        val = (rest[:m.start()] if m else rest).strip()
    return key, val


def _credential_keys() -> set[str]:
    """Provider-credential variable names we may import from a .env. Model-SELECTION
    variables (AIRT_GROUP / AIRT_ATTACKER / AIRT_SCORER), TARGET_* and run paths are never
    imported — model selection stays an explicit shell choice."""
    keys = {"OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "FIREWORKS_API_KEY",
            "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN",
            "AWS_PROFILE", "AWS_REGION", "AWS_DEFAULT_REGION"}
    try:
        for spec in catalogue().values():
            env = spec.get("api_key_env")
            if isinstance(env, str) and env:
                keys.add(env)
    except Exception:
        pass
    return keys


def _load_env_file(path: Path, allowed: set[str]) -> None:
    """Load only the allowed credential keys from a .env into os.environ, never overriding a
    variable already set. Atomic: the WHOLE file is parsed and validated first, and nothing is
    written to the environment unless every line is valid. Raises ValueError on a malformed line
    or OSError on an unreadable file, leaving os.environ unchanged."""
    pending: dict[str, str] = {}
    for line in path.read_text().splitlines():
        parsed = _parse_env_line(line)
        if parsed is None:
            continue
        key, val = parsed
        pending[key] = val
    for key, val in pending.items():
        if key in allowed and key not in os.environ:
            os.environ[key] = val


def load_env():
    """Load model-provider credentials from the .env for whatever environment we run under.

    Deterministic order (no walk through every working-directory ancestor):
      1. ``$AIRT_ENV_FILE`` if set — the SOLE authoritative source. If it is missing,
         unreadable or malformed we stop with an error rather than fall back to another
         account.
      2. otherwise, in order: the course root's .env (the tree with models.yaml), the
         installed harness root's .env and its parent (on the VM, /opt/airt/src/.env), then
         /opt/airt/src/.env. Every existing one is read; the first value wins per key.

    Only provider-credential variables are imported (see ``_credential_keys``). An
    already-exported variable is never overwritten.
    """
    allowed = _credential_keys()

    if "AIRT_ENV_FILE" in os.environ:      # present (even if empty) => the sole authoritative source
        explicit = os.environ["AIRT_ENV_FILE"]
        path = Path(explicit) if explicit else None
        if not explicit or not path.is_file():
            raise SystemExit(f"AIRT_ENV_FILE={explicit!r} is empty, missing or unreadable - "
                             f"refusing to fall back to another .env.")
        try:
            _load_env_file(path, allowed)
        except (ValueError, OSError) as exc:
            raise SystemExit(f"AIRT_ENV_FILE={explicit!r} could not be loaded: {exc}")
        return path

    candidates: list[Path] = []
    root = os.environ.get("AIRT_COURSE_ROOT")
    if root:
        candidates.append(Path(root) / ".env")
    for base in Path(__file__).resolve().parents:
        if (base / "models.yaml").is_file():
            candidates.append(base / ".env")
            break
    try:
        import harness
        hroot = Path(harness.__file__).resolve().parent.parent
        candidates.append(hroot / ".env")
        candidates.append(hroot.parent / ".env")
    except Exception:
        pass
    candidates.append(Path("/opt/airt/src/.env"))

    loaded, seen = None, set()
    for cand in candidates:
        try:
            cand = cand.resolve()
        except Exception:
            continue
        if cand in seen or not cand.is_file():
            continue
        seen.add(cand)
        try:
            _load_env_file(cand, allowed)      # a malformed non-explicit .env is skipped
            loaded = loaded or cand
        except (ValueError, OSError):
            continue
    return loaded

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


load_env()   # load provider credentials once on import (see load_env)
