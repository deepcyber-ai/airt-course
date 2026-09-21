#!/usr/bin/env bash
# Lab 2 — garak against Larkfield · COMPLETE
#
#   bash modules/module4/garak/complete/run.sh                  # full set, neutral posture
#   bash modules/module4/garak/complete/run.sh quick            # one small family, ~1 min
#   POSTURE=hardened bash modules/module4/garak/complete/run.sh # after restarting hardened
#
# Each run writes to out/<tag>-<POSTURE>* (POSTURE defaults to 'neutral'), so a
# neutral run and a later hardened run are kept side by side, not overwritten.
#
# No attacker or judge-model charge: garak's prompts are static and its
# detectors are rules or small classifiers. It costs only the target's own
# inference. Bring up ONE Larkfield target first (airt-target larkfield -> :8089).
# The posture is only the system prompt: to compare hardened, restart the SAME
# target with the hardened prompt and re-run this script (see the README).
#
# garak is installed in its OWN environment on the course VM, on PATH as `garak`
# (not `python3 -m garak` in the main course env). This script calls `garak`.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${HERE}/out"; mkdir -p "$OUT"
POSTURE="${POSTURE:-neutral}"

command -v garak >/dev/null 2>&1 || { echo "ERROR: 'garak' not on PATH — it lives in its own environment on the VM (see INSTALL-KALI.md)." >&2; exit 1; }

FULL="latentinjection.LatentInjectionReport,encoding.InjectBase64,promptinject.HijackHateHumans,dan.DanInTheWild,leakreplay.GuardianComplete"
QUICK="lmrc.Profanity"
PROBES="$FULL"; TAG="full"
if [ "${1:-}" = "quick" ]; then PROBES="$QUICK"; TAG="quick"; fi

run () {   # port
  local port="$1" log rc
  sed "s/8089/${port}/" "${HERE}/../starter/larkfield.json" > "${OUT}/target-${port}.json"
  log="${OUT}/${TAG}-${POSTURE}.log"
  echo "=== ${POSTURE} (:${port}) ==="
  echo "  garak output streams below (and is also saved to ${log})."
  echo "  (the full set is a few minutes; run 'bash \"${HERE}/run.sh\" quick' for a ~1 min check.)"
  # Keep the FULL log and propagate a scanner failure — do not let a piped grep
  # mask a non-zero exit and print "reports" over a crashed run.
  garak --model_type rest \
    --generator_option_file "${OUT}/target-${port}.json" \
    --probes "$PROBES" --generations 1 \
    --report_prefix "${OUT}/${TAG}-${POSTURE}" 2>&1 | tee "$log"
  rc=${PIPESTATUS[0]}          # garak's exit, not tee's (pipefail is set above)
  grep -aE "ok on|garak run complete" "$log" || true
  if [ "$rc" -ne 0 ]; then
    echo "ERROR: garak exited ${rc} for ${POSTURE}. Full log: ${log}" >&2
    tail -5 "$log" >&2
    exit "$rc"
  fi
}

run 8089

echo
echo "Reports in ${OUT}/ — .jsonl for the data, .html to read."
echo
echo "This run wrote out/${TAG}-${POSTURE}*. To compare postures: restart the target"
echo "with the hardened prompt (same :8089, same model), then re-run with"
echo "  POSTURE=hardened bash \"${HERE}/run.sh\" ${1:-}"
echo "and diff out/${TAG}-neutral* against out/${TAG}-hardened*, PER PROBE. Read"
echo "latentinjection specifically (see the"
echo "README on what that probe actually tests) before trusting the aggregate — a"
echo "marker is a discovery signal, not proof."
