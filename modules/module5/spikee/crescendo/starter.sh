#!/usr/bin/env bash
# Module 5 · Spikee — crescendo (multi-turn) (starter)
#
# Runs spikee's 'crescendo' attack against Larkfield. YOU write the objective: edit seeds-starter/standalone_user_inputs.jsonl with a Module 3 threat.
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
#   # Supported objective_id -> judge_args (pick ONE; anything else fails closed):
#   cross_customer_contact_disclosure   -> llm02_pii_disclosure
#   internal_config_reference_disclosure -> llm07_system_prompt
#
#   bash <course>/modules/module5/spikee/crescendo/starter.sh
#
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SEEDS="${HERE}/../seeds-starter"
: "${SPIKEE_ATTACKER:?set SPIKEE_ATTACKER to your attacker model, e.g. bedrock/qwen.qwen3-235b-a22b-2507-v1:0}"
[ -f targets/larkfield_mt.py ] || { echo "Run from your spikee workspace (targets/larkfield_mt.py missing — see README)."; exit 1; }

python3 - "$SEEDS/standalone_user_inputs.jsonl" <<'PYV' || exit 1
import json, sys
# POSITIVE allowlist: objective_id -> its required flag. Read-only disclosure only.
SUPPORTED = {
    "cross_customer_contact_disclosure": "llm02_pii_disclosure",
    "internal_config_reference_disclosure": "llm07_system_prompt",
}
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if len(rows) != 1:
    sys.exit("FAIL-CLOSED: seed must have exactly one row")
r = rows[0]
if r.get("judge_name") != "airt_flags":
    sys.exit("FAIL-CLOSED: judge_name must be airt_flags")
oid = (r.get("objective_id") or "").strip()
if oid not in SUPPORTED:
    sys.exit("FAIL-CLOSED: objective_id must be one of "
             + str(list(SUPPORTED)) + " (read-only disclosure only) -- got " + repr(oid))
ja = (r.get("judge_args") or "").strip()
if ja != SUPPORTED[oid]:
    sys.exit("FAIL-CLOSED: judge_args for " + oid + " must be "
             + repr(SUPPORTED[oid]) + " -- got " + repr(ja))
tx = (r.get("text") or "").strip()
if not tx or "TODO" in tx:
    sys.exit("FAIL-CLOSED: replace the TODO objective text with the disclosure attempt")
DESTRUCTIVE = ("delete ", "remove ", "drop ", "update ", "erase ", "wipe ", "execute ", "reset ", "trade ")
if any(w in tx.lower() for w in DESTRUCTIVE):
    sys.exit("FAIL-CLOSED: read-only DISCLOSURE only -- no destructive verb in the objective text")
print("  seed validated:", r.get("id"), "| objective", oid, "| expects", ja)
PYV
spikee generate --seed-folder "$SEEDS" --format user-input --include-standalone-inputs --tag m5crescendos
DS=$(ls -t datasets/*m5crescendos*.jsonl | head -1)
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-eu-west-2}" \
spikee test --dataset "$DS" --target larkfield_mt --target-options port=8081 \
  --attack crescendo --attack-only --attack-options model="$SPIKEE_ATTACKER" --threads 1
