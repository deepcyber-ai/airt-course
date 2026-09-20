"""Module 5 · PyRIT — single (starter).

The floor: one prompt, one reply. No prepared attack model, no stopping check.
YOUR TASK: pick one threat from Module 3, write a single prompt for it in OBJECTIVE,
and name the flag you expect in EXPECTED_FLAG so the run separates it from collateral.

    export AIRT_ATTACKER=qwen            # or AIRT_GROUP=openai (multi-turn only)
    python3 modules/module5/pyrit/single/starter.py
"""
import asyncio
import sys
from pathlib import Path

# _common.py is in the pyrit/ dir one level up — works whether this ships under
# labs/pyrit/ (source) or modules/module5/pyrit/ (export). _common resolves the
# course root itself for the shared labs/ helpers.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _common import make_target, show, save_trace   # noqa: E402

OBJECTIVE = ("...")
EXPECTED_FLAG = "llm0X_your_expected_flag"


async def main() -> None:
    if OBJECTIVE.strip() in ("", "...") or EXPECTED_FLAG.startswith("llm0X"):
        raise SystemExit("FAIL-CLOSED: set OBJECTIVE (your Module 3 threat) and "
                         "EXPECTED_FLAG (the flag you expect) before running — the "
                         "placeholders would spend calls for nothing.")
    from pyrit.setup import initialize_pyrit_async, IN_MEMORY
    await initialize_pyrit_async(memory_db_type=IN_MEMORY)
    from pyrit.executor.attack import PromptSendingAttack

    target = make_target()
    attack = PromptSendingAttack(objective_target=target)
    result = await attack.execute_async(objective=OBJECTIVE)
    show(result, target, EXPECTED_FLAG)
    save_trace(target, "single-starter")


if __name__ == "__main__":
    asyncio.run(main())
