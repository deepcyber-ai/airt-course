# Native tool demonstration examples

> **ASSIGNED ROUTE ONLY.** Complete this only if the trainer assigned this tool or half of the exercise.

These files support the four Module 4 tool tracks — the **assigned** classroom exercises (Spikee, Promptfoo, PyRIT, HumanBound). Start with the Module 4 page (`../README.md`) for your assigned task and setup instructions. The separate `garak/`, `promptfoo/` and `spikee/` starter and complete folders are **optional follow-up material**, not the assigned task, unless your trainer says otherwise. Use the course tool versions and start neutral Larkfield at `http://localhost:8089/chat` before running an example.

| File | Purpose |
|---|---|
| `promptfoo/promptfooconfig.yaml`. | Two visible prompts, an HTTP provider and deterministic assertions. |
| `spikee/larkfield_http.py`. | A small native Spikee target connector for Larkfield's `input` and `output` fields. |
| `spikee/seeds-larkfield-demo/`. | Two standalone seed rows and the empty companion files required by the selected generation path. |
| `pyrit/native_pyrit_demo.py`. | A self-contained example of PyRIT's native HTTP target, prompt-sending attack and persistent SQLite memory. |
| `humanbound/bot-config.json`. | Native HumanBound session and chat endpoint configuration for Larkfield. |
| `humanbound/scope.yaml`. | A small example of the assessor's intended retail-support policy. |

The Python files are visible API examples. They do not import the course harness or call course runner scripts. They do not configure an attacker or judge model. HumanBound uses its separately configured engine models and generates its own tests, so prepare that run separately as described in the note.

The examples demonstrate sending and inspecting tests. They do not establish attack success rates, authenticate tool actions or promise that a prompt succeeds. Validation details and remaining rehearsal checks are in the main note.
