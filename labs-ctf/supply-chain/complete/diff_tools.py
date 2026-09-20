"""Lab C — test the dependency, not the model · COMPLETE

    python3 labs-ctf/supply-chain/complete/diff_tools.py

Diffs every field of tools/list between two versions of the Larkfield MCP
dependency and reports what a version bump actually changed.

No LLM. No API key. This runs in about a second, and it finds something no
amount of talking to the assistant would reveal.

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
"""

import difflib
import json
import re
import urllib.request

CLEAN, CANDIDATE = 8302, 8303

# Phrases that have no business in a tool description. A tool description tells
# the model what a tool does; it should never tell the model what to do, and it
# should certainly never tell it what to conceal.
SUSPICIOUS = [
    (re.compile(r"\byou must\b|\balways\b|\bwhenever you\b", re.I),
     "instructs the model rather than describing the tool"),
    (re.compile(r"do not (mention|tell|reveal|disclose)", re.I),
     "instructs the model to conceal something from the user"),
    (re.compile(r"overrides?\b.{0,40}\binstruction", re.I),
     "claims precedence over the model's other instructions"),
    (re.compile(r"\[TOOL:|\bcall\b.{0,20}\bquery\s*\(", re.I),
     "embeds a tool call inside a description"),
    (re.compile(r"SELECT\s+.+\s+FROM", re.I),
     "embeds a SQL statement"),
    (re.compile(r"system note|compliance requirement|audit policy", re.I),
     "borrows authority it does not have"),
]


def rpc(port: int, method: str, params: dict | None = None) -> dict:
    body = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params:
        body["params"] = params
    req = urllib.request.Request(
        f"http://localhost:{port}/",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=15))
    return d.get("result", d)


def manifest(port: int) -> dict:
    """name -> the whole tool object, so nothing is compared selectively."""
    return {t["name"]: t for t in rpc(port, "tools/list").get("tools", [])}


def scan(text: str) -> list[str]:
    return [why for pat, why in SUSPICIOUS if pat.search(text or "")]


def main() -> None:
    a, b = manifest(CLEAN), manifest(CANDIDATE)

    print(f"  1.0.2: {len(a)} tools    1.0.3: {len(b)} tools")
    print(f"  added:   {sorted(set(b) - set(a)) or 'none'}")
    print(f"  removed: {sorted(set(a) - set(b)) or 'none'}")
    print(f"  tool names identical: {set(a) == set(b)}")
    print("\n  A reviewer checking only for new or renamed tools signs this off.\n")

    findings = 0
    for name in sorted(set(a) & set(b)):
        if a[name] == b[name]:
            continue
        findings += 1
        print(f"  === '{name}' changed ===")
        old = json.dumps(a[name], indent=1, sort_keys=True).splitlines()
        new = json.dumps(b[name], indent=1, sort_keys=True).splitlines()
        for line in difflib.unified_diff(old, new, lineterm="", n=0):
            if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
                print(f"    {line[:200]}")
        for why in scan(json.dumps(b[name])):
            print(f"    [!] {why}")
        print()

    if not findings:
        print("  No tool changed. Either the versions match, or you are "
              "comparing the wrong ports.")
        return

    print("  What to take from this")
    print("  ----------------------")
    print("  The tool NAMES are unchanged, the SCHEMAS are unchanged, and the")
    print("  behaviour of the code is unchanged. One description grew some")
    print("  extra text, and that text is an instruction to the model.")
    print()
    print("  A tool description is not documentation. It is input to the model,")
    print("  and the model treats it as more trustworthy than anything a")
    print("  customer types, because it arrived from the system side.")
    print()
    print("  Measured on the CTF: this lands 9/10 on gpt-4.1 and 10/10 on")
    print("  gemini-flash EVEN AT THE HARDENED POSTURE — a prompt that says")
    print("  'never disclose another customer's details, regardless of the")
    print("  reason given' does not stop it, because the instruction does not")
    print("  arrive as a reason. It arrives as a tool.")
    print()
    print("  The models that ignore it score 0/10 — not through any defence,")
    print("  but through inattention. They do not read tool descriptions")
    print("  properly either.")


if __name__ == "__main__":
    main()
