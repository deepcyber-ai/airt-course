#!/usr/bin/env bash
# Reset a target between runs. Three things need clearing and all three matter.
#
# The third is the one people forget: flags are awarded once per conversation,
# so restoring the data without clearing the scorer gives you a target whose
# data is back but whose scorer believes everything has been earned. That reads
# exactly like a target that has stopped being vulnerable.
#
#   bash labs/reset.sh            # Act 1 (8090 / mcp 8210)
#   bash labs/reset.sh 8091 8211  # Act 2
#
# NOT SAFE FOR CONCURRENT TEAMS SHARING ONE TARGET. Step 1 reseeds the shared
# database and step 3 clears EVERY session ({"all": true}) on that port - it is a
# GLOBAL reset of the named instance, so one team running it wipes another team's
# data, evidence and earned flags. For a multi-team module (M8) give each team its
# OWN target instance (its own ports and database) and reset only that instance.
# SAVE EVIDENCE BEFORE RESETTING: a reseed/session clear is irreversible, and a
# new conversation does not restore a business database. After reset, confirm the
# baseline (the reseed reported ok and a known row is back) before the next run.
set -uo pipefail

TARGET_PORT="${1:-8090}"
MCP_PORT="${2:-8210}"
COLLECTOR_PORT="${3:-8401}"

echo "resetting target :$TARGET_PORT  mcp :$MCP_PORT  collector :$COLLECTOR_PORT"

# 1. the data — restore every row, including ones an attack deleted
curl -s -m 30 "localhost:$MCP_PORT/" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"reseed_database","arguments":{}}}' \
  >/dev/null && echo "  [ok] database reseeded" || echo "  [!!] database reseed FAILED"

# 2. what the collector received — otherwise a previous exfiltration still counts
curl -s -m 15 -X POST "localhost:$COLLECTOR_PORT/__reset" \
  >/dev/null && echo "  [ok] collector cleared" || echo "  [--] collector not running (fine if unused)"

# 3. the scorer's memory of which flags are spent
curl -s -m 15 -X POST "localhost:$TARGET_PORT/session/reset" \
  -H 'Content-Type: application/json' -d '{"all": true}' \
  >/dev/null && echo "  [ok] scorer sessions cleared" || echo "  [!!] scorer reset FAILED"

echo "done."
