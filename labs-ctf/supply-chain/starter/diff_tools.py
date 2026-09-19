"""Lab C — test the dependency, not the model (starter).

    python3 labs-ctf/supply-chain/starter/diff_tools.py

Larkfield's database access comes from a third-party MCP server. Two versions
ship: 1.0.2 and 1.0.3. The release notes call 1.0.3 a metadata update.

**No LLM is involved in this lab at all.** You are testing a dependency by
talking to it directly, which is the only way to find what is wrong with it —
you cannot see this by talking to the assistant.

Start both versions first:

    cd profiles/deepcyber-ctf/vendor/larkfield-db-mcp
    python3 server.py --port 8302 --version 1.0.2 --db /tmp/lark_clean.sqlite &
    python3 server.py --port 8303 --version 1.0.3 --db /tmp/lark_poison.sqlite &

(Point --db somewhere on local disk. A synced folder — OneDrive, Dropbox —
gives SQLite a "disk I/O error" on startup.)

(c) 2026 Deep Cyber Ltd. Apache 2.0 licensed.
"""

import json
import urllib.request

CLEAN, CANDIDATE = 8302, 8303


def rpc(port: int, method: str, params: dict | None = None) -> dict:
    """One JSON-RPC call. MCP is this simple over HTTP."""
    body = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params:
        body["params"] = params
    req = urllib.request.Request(
        f"http://localhost:{port}/",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    d = json.load(urllib.request.urlopen(req, timeout=15))
    return d.get("result", d)


def tool_names(port: int) -> set[str]:
    return {t["name"] for t in rpc(port, "tools/list").get("tools", [])}


if __name__ == "__main__":
    a, b = tool_names(CLEAN), tool_names(CANDIDATE)
    print(f"  1.0.2 tools: {sorted(a)}")
    print(f"  1.0.3 tools: {sorted(b)}")
    print(f"\n  same tool names: {a == b}")
    print(f"  added:   {sorted(b - a) or 'none'}")
    print(f"  removed: {sorted(a - b) or 'none'}")

    # ----------------------------------------------------------------------
    # TODO 1. The tool NAMES are identical, and a reviewer checking for new or
    #         renamed tools would sign this off. Compare the `description`
    #         fields instead. What changed?
    #
    # TODO 2. Read the added text as if you were the model. Who is it
    #         addressed to? What does it instruct? Note the last line
    #         especially.
    #
    # TODO 3. A tool description is not documentation — it is input to the
    #         model, and the model treats it as trustworthy because it came
    #         from the system rather than the user. Write down, in one
    #         sentence, why that makes this worse than a prompt injection
    #         typed by a customer.
    #
    # TODO 4. Now switch the target to 1.0.3, ask the assistant an ordinary
    #         question about an order, and watch what it does that you did not
    #         ask for.
    # ----------------------------------------------------------------------
