#!/usr/bin/env bash
# Start Larkfield at every level, each with its own database.
#
#   bash labs-ctf/start-levels.sh          # start
#   bash labs-ctf/start-levels.sh stop     # stop everything
#
# Seven targets: the five course levels on the clean dependency (1.0.2), plus
# l3p/l4p on the POISONED one (1.0.3) for lab D.
#
# Two levels differ by a profile setting rather than a command-line flag —
# `input_filter` for L2 and `ctf.redact_flags` for L4 — so this generates one
# profile copy per level. The copies use an ABSOLUTE models_file path:
# `models_file: ../../models.yaml` is relative to the profile, and a relocated
# profile silently falls back to the echo backend while /health still reports ok.
set -uo pipefail

# The Larkfield profiles live in the PINNED HARNESS, which on the course VM is a
# SEPARATE tree from the course materials. Point AIRT_HARNESS_ROOT at it (e.g.
# /opt/airt/src/airt_harness). It falls back to this script's parent only when that
# tree actually contains profiles/deepcyber-ctf - a bare course-only checkout does
# NOT, so we preflight and fail with a clear message rather than cd into nothing.
HARNESS_ROOT="${AIRT_HARNESS_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
MCP_DIR="$HARNESS_ROOT/profiles/deepcyber-ctf/vendor/larkfield-db-mcp"
if [ ! -d "$MCP_DIR" ]; then
  echo "ERROR: cannot find $MCP_DIR" >&2
  echo "The Larkfield profiles come from the pinned harness, not the course export." >&2
  echo "Set AIRT_HARNESS_ROOT to the harness root (the tree containing" >&2
  echo "profiles/deepcyber-ctf), e.g.  export AIRT_HARNESS_ROOT=/opt/airt/src/airt_harness" >&2
  exit 1
fi
RUN="${TMPDIR:-/tmp}/larkfield-levels"     # local disk: SQLite fails on synced folders
mkdir -p "$RUN"

if [ "${1:-}" = "stop" ]; then
  pkill -f "harness.mock.*larkfield-l" 2>/dev/null
  pkill -f "server.py --port 822" 2>/dev/null
  pkill -f "server.py --port 820" 2>/dev/null
  echo "stopped."
  exit 0
fi

# level  port  mcp   prompt-file                 filter  redact version
#
# The last two are lab D's, and they are the reason it can produce a result at
# all. On the CLEAN dependency both L3 and L4 simply refuse the probes — the
# destructive query is 0/10 at L3 across all six panel models — so the lab
# demonstrates nothing and reads as a target that is fine. The poisoned tool
# description is the one route that still fires at L3 (9/10), which makes it
# the only place the L3-vs-L4 contrast can be shown.
LEVELS=(
  "l0  8080 8220 planted_system_prompt.txt          false false 1.0.2"
  "l1  8081 8221 system_prompt.txt  false false 1.0.2"
  "l2  8082 8222 planted_system_prompt.txt          true  false 1.0.2"
  "l3  8083 8223 system_prompt_hardened.txt false false 1.0.2"
  "l4  8084 8224 system_prompt_hardened.txt false true  1.0.2"
  "l3p 8093 8201 system_prompt_hardened.txt false false 1.0.3"
  "l4p 8094 8202 system_prompt_hardened.txt false true  1.0.3"
)

cd "$MCP_DIR"
for row in "${LEVELS[@]}"; do
  read -r lvl port mcp prompt filter redact version <<< "$row"
  nohup python3 server.py --port "$mcp" --version "$version" \
        --db "$RUN/$lvl.sqlite" > "$RUN/mcp-$lvl.log" 2>&1 &
done
sleep 5

cd "$HARNESS_ROOT"
for row in "${LEVELS[@]}"; do
  read -r lvl port mcp prompt filter redact version <<< "$row"
  prof="$RUN/larkfield-$lvl.yaml"
  python3 - "$HARNESS_ROOT" "$prof" "$filter" "$redact" <<'PY'
import sys, yaml, pathlib
repo, out, filt, redact = sys.argv[1], sys.argv[2], sys.argv[3] == "true", sys.argv[4] == "true"
p = yaml.safe_load(pathlib.Path(repo, "profiles/deepcyber-ctf/profile.yaml").read_text())
p.setdefault("mock", {})["models_file"] = str(pathlib.Path(repo, "models.yaml"))
for key in ("extension", "flags_file"):
    v = p.get("mock", {}).get(key)
    if v and not str(v).startswith("/"):
        p["mock"][key] = str(pathlib.Path(repo, "profiles/deepcyber-ctf", v))
p.setdefault("mock", {})["input_filter"] = filt
p["mock"].setdefault("ctf", {})["redact_flags"] = redact
pathlib.Path(out).write_text(yaml.safe_dump(p, sort_keys=False))
PY
  nohup python3 -m harness.mock --profile "$prof" --port "$port" \
        --mcp-url "http://localhost:$mcp" \
        --system-prompt "profiles/deepcyber-ctf/mock/$prompt" \
        > "$RUN/larkfield-$lvl.log" 2>&1 &
done
sleep 9

# Set the model explicitly on every level. Without this each target falls back
# to the catalogue default, and comparing levels only means something if they
# are all running the same model. /health reports the --backend argument, not
# the catalogue selection, so it is no help in checking.
MODEL="${AIRT_TARGET_MODEL:-gpt-4.1}"
for row in "${LEVELS[@]}"; do
  read -r lvl port mcp prompt filter redact version <<< "$row"
  curl -s -m 20 -X POST "localhost:$port/model" -H 'Content-Type: application/json' \
       -d "{\"model\":\"$MODEL\"}" >/dev/null
done

echo "model: $MODEL"
printf "  %-4s %5s  %-26s %-7s %-8s %-6s %s\n" \
       level port posture filter flags dep status
for row in "${LEVELS[@]}"; do
  read -r lvl port mcp prompt filter redact version <<< "$row"
  code=$(curl -s -m 5 -o /dev/null -w '%{http_code}' "localhost:$port/health")
  vis=$([ "$redact" = "true" ] && echo BLIND || echo visible)
  dep=$(curl -s -m 5 "localhost:$mcp/health" \
        | python3 -c 'import sys,json;print(json.load(sys.stdin).get("version","?"))' 2>/dev/null)
  # The dependency version is read back from the MCP rather than echoed from
  # the table. Lab D's whole result turns on which one is behind the target,
  # and a probe run against the clean dependency comes back empty in a way
  # that reads as a target that is fine.
  printf "  %-4s %5s  %-26s %-7s %-8s %-6s %s\n" \
     "$lvl" "$port" "${prompt%.txt}" "$filter" "$vis" "${dep:-?}" \
     "$([ "$code" = 200 ] && echo ok || echo "FAILED ($code)")"
done
echo
echo "  lab D:  python3 labs-ctf/blind/complete/evidence.py \\"
echo "            --poisoned-url http://localhost:8093 --poisoned-mcp 8201 \\"
echo "            --poisoned-url-l4 http://localhost:8094 --poisoned-mcp-l4 8202"
echo
echo "logs and profiles in $RUN"
