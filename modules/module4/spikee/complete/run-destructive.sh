#!/usr/bin/env bash
# Serial, reset-verified destructive runs for the Spikee complete lab.
#
#   bash run-destructive.sh mutations <port> <generated-dataset.jsonl>
#   bash run-destructive.sh goat      <port> <generated-dataset.jsonl> [goat.jsonl]
#   bash run-destructive.sh all       <port> <generated-dataset.jsonl> [goat.jsonl]
#
# Two EXPLICIT modes so the routes never overlap:
#   mutations  the five destructive/exhaustion rows from the aimed dataset. No
#              attacker model needed (single-turn).
#   goat       the four GOAT objectives. Needs an attacker model: set GOAT_MODEL
#              (e.g. bedrock/qwen.qwen3-235b-a22b-2507-v1:0).
#   all        both, mutations first.
#
# Every independent attempt starts from a VERIFIED restored baseline. A reset that
# does not actually reseed (HTTP 503, or reseeded!=true) stops the whole sequence
# rather than letting a later attempt run over a dirty database. Requires jq.
set -uo pipefail

MODE="${1:?usage: run-destructive.sh mutations|goat|all <port> <dataset.jsonl> [goat.jsonl]}"
PORT="${2:-8089}"
DS="${3:?supply the generated dataset path}"
GOAT="${4:-datasets/goat-dataset.jsonl}"
BASE="http://localhost:${PORT}"
case "$MODE" in mutations|goat|all) ;; *) echo "ERROR: mode must be mutations|goat|all" >&2; exit 2 ;; esac
command -v jq >/dev/null || { echo "ERROR: jq not found." >&2; exit 1; }
mkdir -p datasets

# Restore DATA + sessions and PROVE it happened. -f makes curl fail on the 503 the
# harness returns when a required reseed could not run (harness/mock.py). We then
# assert reseeded:true so a 200 that quietly skipped the reseed also stops us.
reset () {
  local out
  out="$(curl -sS -f -X POST "${BASE}/session/reset" \
           -H 'Content-Type: application/json' -d '{"all": true}')" \
    || { echo "ABORT: reset failed (target down, or 503 = reseed could not run)"; exit 1; }
  echo "$out" | jq -e '.reseeded == true' >/dev/null \
    || { echo "ABORT: reseed did not run (reseeded != true): $out"; exit 1; }
  echo "  baseline restored: $(echo "$out" | jq -c '{reseeded, seed_summary}')"
}

run_mutations () {
  # one mutation per run, each from a clean baseline. lark-auth-01 deletes the same
  # customer as lark-delete-01, so it is a mutation too.
  for id in lark-auth-01 lark-delete-01 lark-delete-02 lark-poison-01; do
    echo "=== mutation ${id} (:${PORT}) ==="
    reset
    jq -c --arg id "$id" 'select(.id == $id)' "$DS" > "datasets/${id}.jsonl"
    [ -s "datasets/${id}.jsonl" ] || { echo "ABORT: no row ${id} in ${DS}"; exit 1; }
    spikee test --dataset "datasets/${id}.jsonl" --target larkfield \
                --target-options "port=${PORT}" --threads 1
    echo "  ^ read the tool events, not the prose. The marker is discovery, not proof."
  done
  # lark-unbounded-01 is resource EXHAUSTION, not a mutation: no reseed needed, but
  # run it alone (the recursive query can stall a shared batch).
  echo "=== lark-unbounded-01 (:${PORT}) — resource exhaustion, isolated ==="
  jq -c 'select(.id == "lark-unbounded-01")' "$DS" > datasets/lark-unbounded-01.jsonl
  [ -s datasets/lark-unbounded-01.jsonl ] && \
    spikee test --dataset datasets/lark-unbounded-01.jsonl --target larkfield \
                --target-options "port=${PORT}" --threads 1
}

run_goat () {
  [ -f "$GOAT" ] || { echo "ERROR: GOAT dataset not found: ${GOAT}" >&2; exit 1; }
  : "${GOAT_MODEL:?set GOAT_MODEL to your attacker model to run the GOAT objectives}"
  # one objective at a time, each from a clean baseline. Reset happens BETWEEN
  # objectives only, so conversation state is kept WITHIN each attempt.
  for id in goat-delete goat-poison goat-pii goat-indirect; do
    echo "=== GOAT ${id} (:${PORT}) ==="
    reset
    jq -c --arg id "$id" 'select(.id == $id)' "$GOAT" > "datasets/${id}-only.jsonl"
    [ -s "datasets/${id}-only.jsonl" ] || { echo "skip: no ${id} in ${GOAT}"; continue; }
    AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-eu-west-2}" \
    spikee test --dataset "datasets/${id}-only.jsonl" --target larkfield_mt \
                --target-options "port=${PORT}" \
                --attack goat --attack-iterations "${GOAT_ITERS:-4}" \
                --attack-options "model=${GOAT_MODEL}" --threads 1
  done
}

if [ "$MODE" = mutations ] || [ "$MODE" = all ]; then run_mutations; fi
if [ "$MODE" = goat ]      || [ "$MODE" = all ]; then run_goat; fi
echo "done — every destructive attempt ran from a verified-restored baseline."
