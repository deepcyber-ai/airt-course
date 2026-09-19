#!/usr/bin/env bash
# Lab 2 — garak against Larkfield · COMPLETE
#
#   bash modules/module4/garak/complete/run.sh            # both postures, full set
#   bash modules/module4/garak/complete/run.sh quick      # one small family, ~1 min
#
# No attacker or judge-model charge: garak's prompts are static and its
# detectors are rules or small classifiers. It costs only the target's own
# inference. Bring up the Larkfield level ladder first (labs-ctf/start-levels.sh).
#
# garak is installed in its OWN environment on the course VM, on PATH as `garak`
# (not `python3 -m garak` in the main course env). This script calls `garak`.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${HERE}/out"; mkdir -p "$OUT"

command -v garak >/dev/null 2>&1 || { echo "ERROR: 'garak' not on PATH — it lives in its own environment on the VM (see INSTALL-KALI.md)." >&2; exit 1; }

FULL="latentinjection.LatentInjectionReport,encoding.InjectBase64,promptinject.HijackHateHumans,dan.DanInTheWild,leakreplay.GuardianComplete"
QUICK="lmrc.Profanity"
PROBES="$FULL"; TAG="full"
if [ "${1:-}" = "quick" ]; then PROBES="$QUICK"; TAG="quick"; fi

run () {   # port label
  local port="$1" label="$2" log rc
  sed "s/8081/${port}/" "${HERE}/../starter/larkfield.json" > "${OUT}/target-${port}.json"
  log="${OUT}/${TAG}-${label}.log"
  echo "=== ${label} (:${port}) ==="
  # Keep the FULL log and propagate a scanner failure — do not let a piped grep
  # mask a non-zero exit and print "reports" over a crashed run.
  garak --model_type rest \
    --generator_option_file "${OUT}/target-${port}.json" \
    --probes "$PROBES" --generations 1 \
    --report_prefix "${OUT}/${TAG}-${label}" >"$log" 2>&1
  rc=$?
  grep -aE "ok on|garak run complete" "$log" || true
  if [ "$rc" -ne 0 ]; then
    echo "ERROR: garak exited ${rc} for ${label}. Full log: ${log}" >&2
    tail -5 "$log" >&2
    exit "$rc"
  fi
}

run 8081 neutral
run 8083 hardened

echo
echo "Reports in ${OUT}/ — .jsonl for the data, .html to read."
echo
echo "Now compare the two, PER PROBE. Read latentinjection specifically (see the"
echo "README on what that probe actually tests) before trusting the aggregate — a"
echo "marker is a discovery signal, not proof."
