#!/usr/bin/env bash
# AMLUCS course pack — one-time PyRIT 'art' repair for the current VM image.
#
#   cd /opt/airt/airt-course
#   bash update-art.sh
#
# WHY. PyRIT's ascii_art_converter does `from art import text2art`, so the top-level
# `art/` module must be the ASCII-art library (which provides text2art). On the current
# attendee image, adversarial-robustness-toolbox (IBM ART) installed a top-level `art/`
# last and shadowed it, so EVERY PyRIT lab fails to import with
#   ImportError: cannot import name 'text2art' from 'art'
# This is a name collision, not a stale version — a version pin cannot fix it.
#
# WHAT THIS DOES. Force-reinstalls the ASCII-art `art` into the labs venv and verifies
# both PyRIT's import and the ASCII-art import work. It TRADES AWAY IBM ART (its
# `art.attacks` will stop importing) — the course uses no IBM ART, so that is free here.
# Idempotent: safe to run more than once. Run it once per box, as the VM admin.
#
# A rebuilt image fixes this durably by isolating IBM ART in its own venv
# (/opt/airt/art-venv); this script is only for the current image.
set -uo pipefail

VENV_PY="${AIRT_VENV_PYTHON:-/opt/airt/venv/bin/python}"

echo "PyRIT 'art' repair — labs venv python: $VENV_PY"

if [ ! -x "$VENV_PY" ]; then
  echo "ERROR: no python at $VENV_PY"
  echo "       Set AIRT_VENV_PYTHON to your labs venv python and re-run, e.g.:"
  echo "         AIRT_VENV_PYTHON=/path/to/venv/bin/python bash update-art.sh"
  exit 2
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "ERROR: 'uv' not found on PATH. The labs venv is uv-created (no pip inside it),"
  echo "       so this repair needs uv. Install uv or ask the VM admin, then re-run."
  exit 2
fi

echo "==> uv pip install --force-reinstall --no-deps 'art>=6.5.0'"
if ! uv pip install --python "$VENV_PY" --force-reinstall --no-deps 'art>=6.5.0'; then
  echo "FAIL: the reinstall did not complete — see the uv output above."
  exit 1
fi

echo "==> verifying imports"
fail=0
if "$VENV_PY" -c 'from art import text2art; print("  text2art OK")' 2>/dev/null; then :; else
  echo "  FAIL: 'from art import text2art' still does not work"; fail=1; fi
if "$VENV_PY" -c 'import pyrit.converter; print("  pyrit.converter OK")' 2>/dev/null; then :; else
  echo "  FAIL: 'import pyrit.converter' still does not work"; fail=1; fi

echo
if [ "$fail" = 0 ]; then
  echo "DONE — the PyRIT labs should import now. IBM ART (adversarial-robustness-toolbox)"
  echo "was intentionally traded away; the course does not use it. Re-run the smoke test:"
  echo "    cd /opt/airt/airt-course && AIRT_GROUP=openai bash smoke-test.sh"
  exit 0
else
  echo "NOT FIXED — the imports above still fail. Check that \$VENV_PY is the venv the labs"
  echo "actually run under (the smoke test uses 'python3' on PATH), and that no other"
  echo "top-level 'art/' is shadowing it."
  exit 1
fi
