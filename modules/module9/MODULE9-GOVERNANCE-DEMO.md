# Module 9/10 supporting demo: runtime governance (route + fallback)

A short instructor demonstration: with a Cedar policy on, an agentic target's tool
actions are authorized at runtime, and the same attack that succeeded without the
policy is stopped by it. **Cedar returns allow or deny**; any *escalation* (e.g.
routing to a human) is the application's own response to that decision, not a Cedar
verdict. This is a demonstration, not an attendee lab, and it runs from a DEDICATED
governance checkout — not from the sample document tree in this repo.

**What to show:** a **denied** action with the resource **unchanged** afterwards, and
an **allowed** action on disposable data — the trusted decision and its effect on
state, not just the model's refusal text. Supply the exact launch/reset steps for the
implementation you actually run (its real backend and policy file); keep secrets and
production resources out of the demonstration.

## What this is and is not

- The executable governance target lives in the separate **airt_governance**
  checkout (reviewed revision, tag `v1.0.0-governance`), provisioned on the VM at
  `/opt/airt/src/airt_governance`. The `profiles/investigations/` tree in the main
  repo holds SAMPLE documents; it is not the executable governance target.
- The Cedar policy is the control being shown. Name the backend you are actually
  running against. A local shim or echo backend demonstrates the policy engine, it
  does NOT demonstrate a Microsoft (or any named vendor) backend - do not claim a
  backend you did not run.
- If the live governance integration is not part of the tested VM image for your
  session, use the saved fallback below and say so.

## Live route (from the governance checkout)

Use a port that does NOT clash with the CTF targets. **8091 is already the hardened
DVC port**, so do not reuse it here; pick a free port for governance (e.g. 8093) and
confirm nothing else is listening first.

The policy-enablement mechanism belongs to the `airt_governance` checkout, not the
CTF harness, and its exact flag/config differs by revision. **Do not assume a
`--policy` flag** - the reviewed governance mock parser does not take one. Take the
actual enablement (a config file, an env var, or a profile setting) from that
checkout's own help/README for the revision you run, the same way you would check a
tool's `--help` before trusting a flag:

```bash
cd /opt/airt/src/airt_governance
# 1. check how THIS revision enables the Cedar policy (do not guess a flag):
python -m harness.mock --help        # and the governance README for the policy switch

# 2. policy OFF, then ON, on a free non-CTF port (8093 here), running the SAME
#    tool action each time and reading the policy DECISION, not just the prose.
```

Show the policy decision in the response, not just the refusal text: a governance
DENY and a model refusal read alike as prose, and crediting the policy with the
model's reticence overstates the control. Record which backend produced the
response - a shim/echo backend does not demonstrate any named vendor backend.

## Saved fallback (offline)

A labelled saved fallback ships with this demo:
[`fixtures/governance-fallback.json`](fixtures/governance-fallback.json). It is a
**constructed** illustrative pair - the SAME tool action with the policy OFF
(executed) and ON (DENY by the policy engine) - with the backend and policy-version
fields left as placeholders to fill from a real capture. Walk it when the live
integration is unavailable. It demonstrates the mechanism; it is **not** a recording
of a live run. Replace it with an authenticated capture from the governance checkout
when one exists, and name the real backend and policy version then.

## Honesty checklist

- [ ] Named the backend actually used (not implied from a shim).
- [ ] Separate port/state from the CTF targets; policy enablement was explicit.
- [ ] Policy decision shown, distinct from a model refusal.
- [ ] If saved, labelled as a recorded trace with backend + policy version.
- [ ] Governance target came from the dedicated checkout, not the sample tree.
