#!/usr/bin/env bash
# Module 5 · Spikee — crescendo (multi-turn) (complete)
#
# Runs spikee's 'crescendo' attack against Larkfield. objective = cross-customer PII (same as every method).
# The attacker + judge (why/how to choose) are Module 6; the judge here is the FREE
# marker judge airt_flags (no model call).
#
# ONE-TIME setup (same workspace as the Module 4 spikee lab): a spikee workspace at
# ~/spikee-ws with targets/larkfield_mt.py and judges/airt_flags.py copied in, and
# 'spikee init' already run (that provides the goat attack). Run this FROM there.
#
# Run:
#   cd ~/spikee-ws
#   export SPIKEE_ATTACKER=bedrock/qwen.qwen3-235b-a22b-2507-v1:0   # your attacker as provider/model
#   bash <course>/modules/module5/spikee/crescendo/complete.sh
#
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SEEDS="${HERE}/../seeds-pii"
: "${SPIKEE_ATTACKER:?set SPIKEE_ATTACKER to your attacker model, e.g. bedrock/qwen.qwen3-235b-a22b-2507-v1:0}"
[ -f targets/larkfield_mt.py ] || { echo "Run from your spikee workspace (targets/larkfield_mt.py missing — see README)."; exit 1; }

spikee generate --seed-folder "$SEEDS" --format user-input --include-standalone-inputs --tag m5crescendoc
DS=$(ls -t datasets/*m5crescendoc*.jsonl | head -1)
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-eu-west-2}" \
spikee test --dataset "$DS" --target larkfield_mt --target-options port=8089 \
  --attack crescendo --attack-only --attack-options model="$SPIKEE_ATTACKER" --threads 1
