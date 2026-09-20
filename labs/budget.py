"""Persistent per-group Module 6 budget ledger.

The Module 6 ceiling (Charlie's table) is per GROUP across the WHOLE module,
and the module spans two activities that run as separate processes:

    attacker_eval.py   spends  attacker + target
    score_exercise.py  spends  scorer

A ledger that reset each process would let a group spend the ceiling twice (or
reset it by re-running). This ledger persists to a JSON file under the run
directory, so both scripts - and repeated invocations of either - count against
one shared ceiling. Offline runs never touch it (no service calls, no spend).

    AIRT_RUN_DIR/m6-budget.json     (default AIRT_RUN_DIR = course-runs/group-01)

(c) 2026 Deep Cyber Ltd. Apache 2.0 licensed.
"""
import json
import os
from pathlib import Path

# Module 6 ceiling, per group, across the module (Charlie's §5 table):
#   6 attacker  = 2 attackers x 3 candidate prompts each
#   7 target    = the 6 candidate attacks + 1 benign control
#   12 scorer   = the 6 responses scored under 2 criteria (in the scorer exercise)
BUDGET = {"attacker": 6, "target": 7, "scorer": 12}


def run_dir() -> Path:
    return Path(os.environ.get("AIRT_RUN_DIR", "course-runs/group-01"))


def ledger_path() -> Path:
    return run_dir() / "m6-budget.json"


class BudgetExceeded(SystemExit):
    """Raised (as a SystemExit) when a spend would break the ceiling."""


class Ledger:
    """Counts service calls across processes and refuses to exceed the ceiling.

    Every successful spend is persisted immediately (atomic tmp->replace), so a
    crash or a second process sees the true running total, not a stale one.
    """

    def __init__(self, path=None, budget=None):
        self.path = Path(path) if path else ledger_path()
        self.budget = dict(budget or BUDGET)
        self.used = {k: 0 for k in self.budget}
        self._load()

    def _load(self):
        if not self.path.exists():
            return
        try:
            saved = json.loads(self.path.read_text())
            used = saved.get("used", {})
            for k in self.used:
                self.used[k] = int(used.get(k, 0))
        except (ValueError, OSError, TypeError):
            # A corrupt ledger must not crash an attendee's lab. Start clean and
            # say so at the call site if it matters.
            self.used = {k: 0 for k in self.budget}

    def remaining(self, role) -> int:
        return self.budget[role] - self.used[role]

    def can(self, role, n=1) -> bool:
        return self.used[role] + n <= self.budget[role]

    def spend(self, role, n=1):
        """Charge n calls to `role`. Raises BudgetExceeded rather than overspend
        - the caller is expected to check can() first and fall back to SAVED."""
        if not self.can(role, n):
            raise BudgetExceeded(
                f"BUDGET EXCEEDED: {role} would reach {self.used[role] + n} of "
                f"{self.budget[role]} for this group across Module 6. Use the "
                f"saved fallback (run without --live), or start a fresh group "
                f"(set AIRT_RUN_DIR).")
        self.used[role] += n
        self._save()

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps({"budget": self.budget, "used": self.used}, indent=2))
        tmp.replace(self.path)  # atomic

    def reset(self, role=None):
        """Wipe persisted counts. With no role, start the whole group's Module 6
        budget over. With a role, reset ONLY that role's count (a scorer recovery
        must NOT zero the attacker/target calls already recorded for the group)."""
        if role is None:
            self.used = {k: 0 for k in self.budget}
        else:
            if role not in self.budget:
                raise KeyError(f"unknown budget role {role!r}")
            self.used[role] = 0
        self._save()

    def line(self) -> str:
        return "  ".join(f"{k} {self.used[k]}/{self.budget[k]}" for k in self.budget)
