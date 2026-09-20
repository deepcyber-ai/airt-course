"""Spikee target for the AIRT Harness — single AND multi-turn.

The starter target handles one payload at a time and decides success itself.
GOAT and the other adaptive attacks need more: they hold a conversation, so the
target has to keep each conversation separate and hand back the reply *text*
rather than a verdict.

Two changes from the starter version:

  * ``turn_types=[Turn.SINGLE, Turn.MULTI]``
  * ``process_input`` accepts ``spikee_session_id`` — spikee mints one per
    conversation and passes it on every turn. Map it to the harness's
    ``x-session-id`` and the whole conversation lands in one thread.

Scoring moves to a separate judge (``airt_flags`` for the flag marker, or
``airt_llm`` for the model-based grade). It has to: a multi-turn attack needs the
reply text back to build its next turn, so the target cannot return a bool.

Install:

    cp larkfield_mt.py targets/
    cp ../judges/airt_flags.py judges/     # and airt_llm.py for the LLM comparison

(c) 2026 Deep Cyber Ltd. Deep Cyber course material, under the course licence (see LICENCE.md). Not open source.
"""

import uuid
from typing import Optional

import requests

from spikee.templates.target import Target
from spikee.utilities.enums import ModuleTag, Turn
from spikee.utilities.hinting import ModuleDescriptionHint, ModuleOptionsHint


class LarkfieldMultiTurnTarget(Target):
    def __init__(self):
        super().__init__(turn_types=[Turn.SINGLE, Turn.MULTI])
        # spikee session id -> harness session id
        self._sessions: dict[str, str] = {}

    def get_description(self) -> ModuleDescriptionHint:
        return (
            [ModuleTag.SINGLE, ModuleTag.MULTI],
            "AIRT Harness target with conversation support, for GOAT and other "
            "multi-turn attacks. Pair with the 'canary' judge.",
        )

    def get_available_option_values(self) -> ModuleOptionsHint:
        return ["port=8081", "port=8083"], False

    def _harness_session(self, spikee_session_id: Optional[str], port: str) -> str:
        """One harness conversation per spikee conversation.

        Reusing a single id across conversations would merge them, and because
        each flag is awarded once per conversation the first attempt would
        spend it and leave every later one looking clean.
        """
        key = spikee_session_id or str(uuid.uuid4())
        if key not in self._sessions:
            try:
                r = requests.post(f"http://localhost:{port}/session/new", timeout=30)
                self._sessions[key] = r.json()["session_id"]
            except Exception:
                self._sessions[key] = f"spikee-{uuid.uuid4().hex[:12]}"
        return self._sessions[key]

    def process_input(
        self,
        input_text,
        system_message: Optional[str] = None,
        target_options: Optional[str] = None,
        spikee_session_id: Optional[str] = None,
    ):
        port = "8081"
        if target_options and "port=" in target_options:
            port = target_options.split("port=", 1)[1].split(",")[0].strip()

        text = getattr(input_text, "text", None) or str(input_text)
        sid = self._harness_session(spikee_session_id, port)

        resp = requests.post(
            f"http://localhost:{port}/chat",
            json={"input": text},
            headers={"Content-Type": "application/json", "x-session-id": sid},
            timeout=180,
        )
        resp.raise_for_status()
        # Return the text, not a verdict: a multi-turn attack needs the reply
        # to write its next turn. The canary judge does the scoring.
        return resp.json().get("output", "")
