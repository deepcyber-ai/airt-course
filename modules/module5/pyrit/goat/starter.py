"""Module 5 · PyRIT — goat (starter).

YOUR TASK: put a Module 3 threat in OBJECTIVE and name its flag in EXPECTED_FLAG, so
the stopping check pairs the objective with its own signal.

    export AIRT_ATTACKER=qwen            # or AIRT_GROUP=openai (multi-turn only)
    python3 modules/module5/pyrit/goat/starter.py
"""
import asyncio
import sys
from pathlib import Path

# _common.py is in the pyrit/ dir one level up — works whether this ships under
# labs/pyrit/ (source) or modules/module5/pyrit/ (export). _common resolves the
# course root itself for the shared labs/ helpers.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _common import make_target, make_attack_model, stopping_check, show, save_trace, GOAT_PROMPT   # noqa: E402

OBJECTIVE = ("...")
EXPECTED_FLAG = "llm0X_your_expected_flag"


async def main() -> None:
    if OBJECTIVE.strip() in ("", "...") or EXPECTED_FLAG.startswith("llm0X"):
        raise SystemExit("FAIL-CLOSED: set OBJECTIVE (your Module 3 threat) and "
                         "EXPECTED_FLAG (the flag you expect) before running — the "
                         "placeholders would spend calls for nothing.")
    from pyrit.setup import initialize_pyrit_async, IN_MEMORY
    await initialize_pyrit_async(memory_db_type=IN_MEMORY)
    from pyrit.executor.attack import (RedTeamingAttack, AttackAdversarialConfig,
                                       AttackScoringConfig)
    target = make_target()
    attack = RedTeamingAttack(
        objective_target=target,
        attack_adversarial_config=AttackAdversarialConfig(
            target=make_attack_model(), system_prompt=GOAT_PROMPT),
        attack_scoring_config=AttackScoringConfig(objective_scorer=stopping_check(EXPECTED_FLAG)),
        max_turns=6)
    result = await attack.execute_async(objective=OBJECTIVE)
    show(result, target, EXPECTED_FLAG)
    save_trace(target, "goat-starter")


if __name__ == "__main__":
    asyncio.run(main())
