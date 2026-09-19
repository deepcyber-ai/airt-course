# Lab 4 — PyRIT

```bash
python3 modules/module5/pyrit/starter/attack.py
```

Runs as supplied: single-turn probes through `PromptSendingAttack`, reporting
which flags they trigger. Three TODOs at the bottom of `attack.py` take you to
multi-turn.

PyRIT 1.0 changed substantially from 0.x and most examples online are still
0.x. The three that will catch you:

- `PromptRequestResponse` is now `Message`
- memory must be initialised (`initialize_pyrit_async`) before any target
- `AttackResult.last_response` is a `MessagePiece`; the text is on
  `.converted_value`, and there is no `.get_value()` at that level

Set `AIRT_ATTACKER` to whichever model you chose in the evaluation module —
`labs/models.py` resolves it against `models.yaml`, so switching between your
own key and sponsored Bedrock is one environment variable.
