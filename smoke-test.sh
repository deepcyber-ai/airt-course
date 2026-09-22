#!/usr/bin/env bash
# AMLUCS course pack — Module 4-7 lab smoke test.
#
#   cd /opt/airt/airt-course
#   AIRT_GROUP=openai bash smoke-test.sh      # (or AIRT_GROUP=bedrock)
#
# Confirms the labs run in THIS environment. It imports and runs the Python labs
# (M4 pyrit, M5 pyrit + single-attacker, M6 scorer, M7 attack/score), the Promptfoo
# labs (M4 starter, M5 single-attacker) and checks Garak is runnable, printing
# PASS / FAIL / SKIP per check. It changes nothing and pushes nothing. A live run
# costs a few US cents of model calls; the deterministic checks cost nothing.
#
# The Python labs read the provider key from /opt/airt/src/.env automatically; you only
# need AIRT_GROUP set. Promptfoo is a Node tool, so this script sources that .env into the
# shell for it. The pyrit checks need only the target (no model key).
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
export AIRT_GROUP="${AIRT_GROUP:-openai}"
TARGET="http://localhost:8089"

pass=0; fail=0; skip=0
step() { printf '\n=== %s ===\n' "$1"; }
ok()   { echo "  PASS: $1"; pass=$((pass+1)); }
no()   { echo "  FAIL: $1"; fail=$((fail+1)); }
sk()   { echo "  SKIP: $1"; skip=$((skip+1)); }

# Printed when a PyRIT lab fails to import `text2art` from `art`. This is a name
# collision (IBM ART shadowing the ASCII-art `art`), NOT a stale version — a pin
# cannot fix it. The venv is uv-created, so there is no pip inside it; use uv.
art_hint() {
  echo "     PyRIT's ascii_art_converter needs text2art from the 'art' package, but IBM ART"
  echo "     (adversarial-robustness-toolbox) has shadowed the top-level art/ module — a name"
  echo "     collision, not a stale version. Fix once, as the VM admin, restoring the ASCII-art"
  echo "     'art' in the labs venv (uv-created, so no pip inside — use uv):"
  echo "       uv pip install --python /opt/airt/venv/bin/python --force-reinstall --no-deps 'art>=6.5.0'"
  echo "     Verify: /opt/airt/venv/bin/python -c 'from art import text2art; print(\"ok\")'"
  echo "     The course uses no IBM ART; on a rebuilt image it lives in its own venv (/opt/airt/art-venv)."
  echo "     (This affects EVERY PyRIT lab, not just this one.)"
}

echo "Course pack: $HERE"
echo "AIRT_GROUP=$AIRT_GROUP   (attacker/scorer models come from models.yaml)"

# Writable working directory — the labs create course-runs/ and out/ here.
if ( : > .smoke-write-test ) 2>/dev/null; then rm -f .smoke-write-test
else echo "WARNING: this folder is not writable. The labs write course-runs/ and out/ here."
     echo "         Copy the pack somewhere writable (or run from your home dir) and retry."; fi

# Target
TARGET_UP=0
if curl -s -m3 "$TARGET/health" >/dev/null 2>&1; then TARGET_UP=1
else echo "NOTE: target $TARGET is down. Start it with:  airt-target larkfield"
     echo "      (target-dependent checks will be SKIPPED until it is up)"; fi

# Promptfoo launcher (installed globally on the VM; npx fallback for a laptop)
if command -v promptfoo >/dev/null 2>&1; then PF=(promptfoo)
elif command -v npx >/dev/null 2>&1; then PF=(npx -y promptfoo@0.123.0)
else PF=(); fi

# --- Module 6 (no attacker model; the offline check needs neither key nor target) ---

step "Module 6 — compare.py --offline (no key, no target)"
if python3 modules/module6/scorer-exercise/compare.py --offline 2>/dev/null | grep -q "FALLBACK"; then
  ok "M6 offline fallback"; else no "M6 offline"; fi

# --- Module 4 (the floor labs: one target, no attacker/scorer model) ---

step "Module 4 — promptfoo/starter (deterministic markers, no grader)"
if [ "$TARGET_UP" != 1 ]; then sk "M4 promptfoo — target :8089 down"
elif [ "${#PF[@]}" = 0 ]; then sk "M4 promptfoo — neither 'promptfoo' nor 'npx' found on PATH"
else
  pf_out="$( cd modules/module4/promptfoo/starter \
    && export PROMPTFOO_CONFIG_DIR="$PWD/runs/smoke" && mkdir -p "$PROMPTFOO_CONFIG_DIR" \
    && PROMPTFOO_DISABLE_SHARING=true "${PF[@]}" eval --no-cache --no-progress-bar 2>&1 )"
  if printf '%s' "$pf_out" | grep -qE "[0-9]+ passed|[0-9]+ failed"; then ok "M4 promptfoo (starter)"
  else no "M4 promptfoo"; printf '%s\n' "$pf_out" | tail -3; fi
fi

step "Module 4 — pyrit/complete (single-turn floor, target only)"
if [ "$TARGET_UP" = 1 ]; then
  pout="$(python3 modules/module4/pyrit/complete/complete.py 2>&1)"
  if echo "$pout" | grep -q "Memory database:"; then ok "M4 pyrit"
  elif echo "$pout" | grep -q "text2art"; then no "M4 pyrit — PyRIT 'art' shadowed"; art_hint
  else no "M4 pyrit"; echo "$pout" | tail -3; fi
else sk "M4 pyrit — target :8089 down"; fi

step "Module 4 — garak (runnable)"
if command -v garak >/dev/null 2>&1; then
  if garak --list_probes 2>&1 | grep -qiE "lmrc|dan|encoding"; then ok "M4 garak (runnable)"
  else no "M4 garak — installed but --list_probes returned no probes"; fi
else sk "M4 garak — 'garak' not on PATH (installed in its own venv on the VM)"; fi

# --- Module 5 (pyrit floor, then the single-turn attacker+scorer, then promptfoo) ---

step "Module 5 — pyrit/single (single-turn floor, target only)"
if [ "$TARGET_UP" = 1 ]; then
  fout="$(python3 modules/module5/pyrit/single/complete.py 2>&1)"
  if echo "$fout" | grep -q "target requests this run"; then ok "M5 pyrit single"
  elif echo "$fout" | grep -q "text2art"; then no "M5 pyrit single — PyRIT 'art' shadowed"; art_hint
  else no "M5 pyrit single"; echo "$fout" | tail -3; fi
else sk "M5 pyrit single — target :8089 down"; fi

step "Module 5 — pyrit/single-attacker/complete.py (attacker + scorer)"
if [ "$TARGET_UP" = 1 ]; then
  sout="$(python3 modules/module5/pyrit/single-attacker/complete.py 2>&1)"
  if echo "$sout" | grep -q "scorer verdict"; then ok "M5 single-attacker"
  elif echo "$sout" | grep -qiE "no reachable endpoint|api_key|AIRT_ENV_FILE"; then sk "M5 single-attacker — model key not found"
  elif echo "$sout" | grep -q "text2art"; then no "M5 single-attacker — PyRIT 'art' shadowed"; art_hint
  else no "M5 single-attacker"; echo "$sout" | tail -3; fi
else sk "M5 single-attacker — target :8089 down"; fi

step "Module 5 — promptfoo/single-attacker (Node — needs the key in the shell)"
if [ "$TARGET_UP" != 1 ]; then sk "promptfoo — target :8089 down"
elif [ "${#PF[@]}" = 0 ]; then sk "promptfoo — neither 'promptfoo' nor 'npx' found on PATH"
else
  [ -f /opt/airt/src/.env ] && { set -a; . /opt/airt/src/.env; set +a; }
  if [ -z "${OPENAI_API_KEY:-}" ]; then sk "promptfoo — OPENAI_API_KEY not in shell (source /opt/airt/src/.env)"
  else
    # Capture the output first: promptfoo exits non-zero when tests "fail" (an attacker win),
    # and pipefail would otherwise read that exit instead of whether it ran. The smoke question
    # is only "did it run and grade?", so check the output for a results line.
    pf_out="$( cd modules/module5/promptfoo/single-attacker \
      && export PROMPTFOO_CONFIG_DIR="$PWD/runs/smoke" && mkdir -p "$PROMPTFOO_CONFIG_DIR" \
      && PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION=true PROMPTFOO_DISABLE_SHARING=true \
         "${PF[@]}" redteam run -c complete.yaml -o "$PROMPTFOO_CONFIG_DIR/redteam.yaml" --no-progress-bar 2>&1 )"
    if printf '%s' "$pf_out" | grep -qE "[0-9]+ passed|[0-9]+ failed"; then ok "promptfoo (single-attacker)"
    else no "promptfoo"; printf '%s\n' "$pf_out" | tail -3; fi
  fi
fi

# --- Module 6 live, Module 7 (need an attacker/scorer model key) ---

step "Module 6 — compare.py (live scorer)"
out="$(python3 modules/module6/scorer-exercise/compare.py 2>&1)"
if echo "$out" | grep -qE "disagreement|SUCCESS|FAILURE"; then ok "M6 live scorer"
elif echo "$out" | grep -qiE "no reachable endpoint|api_key|AIRT_ENV_FILE"; then sk "M6 live — model key not found (check /opt/airt/src/.env or export the key)"
else no "M6 live"; echo "$out" | tail -3; fi

step "Module 7 — attack.py + score.py"
if [ "$TARGET_UP" = 1 ]; then
  aout="$(python3 modules/module7/attacker-scorer/attack.py --attacker gpt-4.1 2>&1)"
  trace="$(printf '%s\n' "$aout" | grep -oE 'course-runs/module7/[^ ]*-trace\.json' | head -1)"
  if [ -n "$trace" ]; then
    if python3 modules/module7/attacker-scorer/score.py --run "$trace" --scorer gpt-4o-mini 2>&1 | grep -q "MODEL VERDICT"; then
      ok "M7 attack + score"; else no "M7 score"; fi
  elif echo "$aout" | grep -qiE "no reachable endpoint|api_key"; then sk "M7 — model key not found"
  else no "M7 attack"; echo "$aout" | tail -3; fi
else sk "M7 — target :8089 down"; fi

step "SUMMARY"
echo "  PASS=$pass  FAIL=$fail  SKIP=$skip"
if [ "$fail" = 0 ]; then echo "  Smoke OK — the labs run in this environment."; exit 0
else echo "  Some checks FAILED — see the lines above."; exit 1; fi
