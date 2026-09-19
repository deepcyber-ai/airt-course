# Module 4 — Single-Turn Attacks (entry point)

One-shot attacks against **Larkfield** (the retail assistant). Start here, then open
each lab's own README.

**Labs in this folder**
- `promptfoo/` — a small set of aimed HTTP probes graded by two scorers, a
  deterministic flag-marker check and an LLM rubric (starter + complete)
- `spikee/` — a dataset aimed at this target, plus the GOAT adaptive attack in
  the complete half (starter + complete)
- `garak/` — known-jailbreak / encoding / injection probe families (starter +
  complete; each `run.sh` runs live, no recorded reports ship)

**Shared CTF exercises for this module** live in the sibling `labs-ctf/` folder
(shared across modules, launched with one level ladder):
- `labs-ctf/encoding/` — encoding-based evasion
- `labs-ctf/supply-chain/` — the poisoned tool-description diff
- `labs-ctf/levels/` — the L0–L4 posture ladder
- Bring the targets up with `bash labs-ctf/start-levels.sh` (needs the VM's pinned harness).

**Shared helpers** (model choice, budget, reset) are in the sibling `labs/` folder:
`labs/CHOOSING-MODELS.md`, `labs/models.py`, `labs/reset.sh`. Pick a model per
`MODELS-SETUP.md`; every lab finds `labs/` automatically (or set `AIRT_COURSE_ROOT`).
