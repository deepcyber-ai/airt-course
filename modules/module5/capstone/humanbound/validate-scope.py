#!/usr/bin/env python3
"""Fail-closed preflight for a HumanBound scope. Run BEFORE hb test.

    python3 validate-scope.py scope.complete.yaml

Checks business_scope is a non-empty string and every permitted/restricted item is
a non-empty string (a stray colon turns an item into a key:value mapping, which
HumanBound rejects), and that no TODO placeholder remains.
"""
import sys
import yaml


def main(path: str) -> None:
    d = yaml.safe_load(open(path))
    errs = []
    if not isinstance(d.get("business_scope"), str) or not d["business_scope"].strip():
        errs.append("business_scope must be a non-empty string")
    for k in ("permitted", "restricted"):
        v = d.get(k)
        if not isinstance(v, list) or not v:
            errs.append(f"{k} must be a non-empty list")
            continue
        for i, item in enumerate(v):
            if not isinstance(item, str) or not item.strip():
                errs.append(f"{k}[{i}] must be a non-empty string "
                            f"(got {type(item).__name__}: {item!r}) — check for a stray ':'")
            elif "TODO" in item:
                errs.append(f"{k}[{i}] still contains TODO")
    if errs:
        print("SCOPE INVALID — fix before running hb test:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print("scope OK")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "scope.complete.yaml")
