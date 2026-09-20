#!/usr/bin/env python3
"""Module 8 - isolated per-team targets and a scoped, per-team reset.

Five teams run the full DVC engagement at once. Each team needs its OWN target
instance and its OWN database, so one team's attack (or reset) never touches
another team's state. Isolation here means: each team's MCP server owns a distinct
port AND a distinct SQLite file, and each team's mock is BOUND to its own MCP with
--mcp-url (without that flag every mock inherits the profile default and they all
share one database - the bug this version fixes).

    python3 scripts/m8_teams.py plan --teams 5
        Print each team's ports, database and the exact launch + reset commands.

    python3 scripts/m8_teams.py reset --team 3
        Reset ONLY team 3: reseed its own MCP database and clear its own mock
        sessions. Verifies each step's real result and FAILS (non-zero) if the
        reseed did not confirm - it does not trust the first HTTP status.

    python3 scripts/m8_teams.py verify-plan --teams 5   # offline: prove no collisions
    python3 scripts/m8_teams.py budget --team 3         # sum this team's tool-side sends

DVC's send_email tool delivers to a loopback COLLECTOR (default 8401), so each team
gets its own collector port and its MCP is bound to it with --collector - otherwise
all teams' mail routes to one shared 8401. The 36-request/team allowance is NOT
enforced by the mock (harness.mock does not count requests); track it from the
team's own attack-tool ledgers (see `budget`). The mock's audit log is written per
profile, so teams sharing the DVC profile share that audit file; the isolated
evidence is each team's DATABASE (its own --db) and its own run directory - save
those before a reset. Audit-file isolation would need a harness flag and is out of
scope here; it is stated, not silently claimed.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
"""
import argparse
import json
import sys
from pathlib import Path

PROFILE = "deepvault-capital"
VENDOR = f"profiles/{PROFILE}/vendor/dvc-db-mcp/server.py"   # actual path (not root vendor/)
COLLECTOR = f"profiles/{PROFILE}/vendor/dvc-collector/collector.py"
M8_TARGET_BUDGET = 36
DB_DIR = "/tmp/airt-m8-teams"


def plan_stacks(k, base_mcp_port=8300, base_mock_port=8500, base_collector_port=8700, db_dir=DB_DIR):
    """One config per team, with a DISTINCT mock port, MCP port, collector port and
    database file. Fails closed on any collision (per field and across all ports)."""
    stacks = []
    for i in range(k):
        stacks.append({
            "team": i + 1,
            "mcp_port": base_mcp_port + i,
            "mock_port": base_mock_port + i,
            "collector_port": base_collector_port + i,
            "db_path": str(Path(db_dir) / f"{PROFILE}-team-{i + 1}.sqlite"),
            "run_dir": f"course-runs/team-{i + 1}",
        })
    for field in ("mcp_port", "mock_port", "collector_port", "db_path"):
        vals = [s[field] for s in stacks]
        if len(set(vals)) != len(vals):
            raise ValueError(f"stack plan has duplicate {field}: {vals}")
    all_ports = [s[p] for s in stacks for p in ("mcp_port", "mock_port", "collector_port")]
    if len(set(all_ports)) != len(all_ports):
        raise ValueError(f"port shared across roles: {sorted(all_ports)}")
    return stacks


def _self():
    """This script's own path, so printed self-references are correct wherever it
    runs (committed at scripts/, shipped to the attendee tree at tools/)."""
    return Path(sys.argv[0]).name and f"python3 {sys.argv[0]}" or "python3 m8_teams.py"


def cmd_plan(a):
    stacks = plan_stacks(a.teams)
    print(f"Module 8 - {a.teams} isolated teams for {PROFILE}  "
          f"(budget {M8_TARGET_BUDGET} target requests/team, tracked - see `budget`)\n")
    print("# Run the launch commands FROM THE PINNED HARNESS ROOT (the tree with")
    print("# profiles/), e.g.  cd /opt/airt/src/airt_harness  - the paths below are")
    print("# relative to it, and the DVC profiles come from the harness, not the course export.\n")
    print(f"# once, create the database directory:\nmkdir -p {DB_DIR}\n")
    for s in stacks:
        t = s["team"]
        print(f"Team {t}:")
        print(f"  ports  mock {s['mock_port']}  mcp {s['mcp_port']}  collector {s['collector_port']}   db {s['db_path']}")
        print(f"  run-dir (evidence/ledgers)  {s['run_dir']}")
        print("  launch:")
        print(f"    python {COLLECTOR} --port {s['collector_port']} &")
        print(f"    python {VENDOR} --port {s['mcp_port']} --db {s['db_path']} "
              f"--collector http://localhost:{s['collector_port']} &")
        print(f"    python -m harness.mock --profile profiles/{PROFILE}/profile.yaml "
              f"--port {s['mock_port']} --mcp-url http://localhost:{s['mcp_port']}")
        print(f"  reset THIS team only:")
        print(f"    {_self()} reset --team {t}\n")
    print("Save each team's evidence (DB query results, tool ledgers, transcripts) BEFORE")
    print("a reset. A new conversation does not restore a business database, and the DVC")
    print("MCP reseeds its database - keep the pre-reset state if you need it.")


def cmd_verify_plan(a):
    stacks = plan_stacks(a.teams)
    ports = [s[p] for s in stacks for p in ("mock_port", "mcp_port", "collector_port")]
    dbs = [s["db_path"] for s in stacks]
    ok = len(set(ports)) == len(ports) and len(set(dbs)) == len(dbs)
    print(f"teams={a.teams}  unique ports={len(set(ports))}/{len(ports)}  "
          f"unique dbs={len(set(dbs))}/{len(dbs)}  -> "
          f"{'ISOLATED (distinct mock+mcp+db per team)' if ok else 'COLLISION'}")
    return 0 if ok else 1


def cmd_reset(a):
    import requests
    stacks = plan_stacks(max(a.team, 5))
    s = next((x for x in stacks if x["team"] == a.team), None)
    if s is None:
        raise SystemExit(f"no such team {a.team}")
    print(f"resetting ONLY team {a.team}:  mcp {s['mcp_port']}  mock {s['mock_port']}  collector {s['collector_port']}")
    ok = True
    # 1. reseed THIS team's MCP database, and CHECK the JSON-RPC result (not just HTTP 200)
    try:
        r = requests.post(f"http://localhost:{s['mcp_port']}/", timeout=30, json={
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": "reseed_database", "arguments": {}}})
        body = {}
        try:
            body = r.json()
        except ValueError:
            body = {}
        if r.status_code != 200 or "error" in body or "result" not in body:
            print(f"  [!!] reseed FAILED (status {r.status_code}, body keys {list(body)[:4]})")
            ok = False
        else:
            print(f"  [ok] database reseeded (team {a.team} MCP {s['mcp_port']})")
    except Exception as e:  # noqa: BLE001
        print(f"  [!!] reseed FAILED: {e}")
        ok = False
    # 2. clear THIS team's mock sessions - CHECK the status, fail on 5xx
    try:
        r = requests.post(f"http://localhost:{s['mock_port']}/session/reset", timeout=15,
                          json={"all": True})
        if r.status_code != 200:
            print(f"  [!!] mock session reset FAILED (status {r.status_code})")
            ok = False
        else:
            print(f"  [ok] mock sessions cleared (team {a.team} mock {s['mock_port']})")
    except Exception as e:  # noqa: BLE001
        print(f"  [!!] mock session reset FAILED: {e}")
        ok = False
    # 3. clear THIS team's mail collector
    try:
        r = requests.post(f"http://localhost:{s['collector_port']}/__reset", timeout=15)
        if r.status_code != 200:
            print(f"  [!!] collector reset FAILED (status {r.status_code})")
            ok = False
        else:
            print(f"  [ok] collector cleared (team {a.team} collector {s['collector_port']})")
    except Exception as e:  # noqa: BLE001
        print(f"  [--] collector not running (fine if mail is not in scope): {e}")
    if not ok:
        print("  RESET DID NOT COMPLETE - do NOT continue until the baseline is restored.")
        return 1
    print("  done. Confirm a known row is back (query the team's db) before the next run.")
    return 0


def cmd_budget(a):
    """Sum this team's tool-side physical sends from the transport ledgers its attack
    tools write into the team run directory. This TRACKS the 36-request allowance;
    the mock does not enforce it."""
    rd = Path(f"course-runs/team-{a.team}")
    total = 0
    files = list(rd.rglob("transport.jsonl")) + list(rd.rglob("m5-transport.jsonl"))
    for f in files:
        try:
            total += sum(1 for line in f.read_text().splitlines() if line.strip())
        except OSError:
            pass
    print(f"team {a.team}: {total} TRACKED physical sends across {len(files)} tool ledger(s) "
          f"in {rd}  (allowance {M8_TARGET_BUDGET})")
    print("  NB: this counts only tool ledgers in the run dir. Manual curl/browser/scanner")
    print("  requests are NOT counted - a zero or low tracked count is not zero exposure.")
    if total > M8_TARGET_BUDGET:
        print("  OVER the tracked allowance.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("--teams", type=int, default=5)
    v = sub.add_parser("verify-plan"); v.add_argument("--teams", type=int, default=5)
    r = sub.add_parser("reset"); r.add_argument("--team", type=int, required=True)
    b = sub.add_parser("budget"); b.add_argument("--team", type=int, required=True)
    a = ap.parse_args()
    return {"plan": cmd_plan, "verify-plan": cmd_verify_plan,
            "reset": cmd_reset, "budget": cmd_budget}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main() or 0)
