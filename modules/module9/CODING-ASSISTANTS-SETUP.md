# Configuring a coding assistant on the course VM

**OPTIONAL AFTER-COURSE REFERENCE**

*A one-page reference for the four AI coding assistants installed on the course VM: Claude Code, Codex, Gemini CLI and Aider.*

Choose one assistant for the exercise. Configuring all four adds setup time and cost for no teaching benefit, so the practical choice is the account you already hold. The four differ in how they sign in and in which provider receives the repository they read.

A coding assistant authenticates through its own account or key. This is separate from the course target. The target model reads its provider key from `/opt/airt/src/.env`; the assistant does not need that credential. An assistant with file or command access may still be able to read `.env` or `/opt/airt/src/.env`, so launch it from the extracted course folder and deny any request from it to read, print or modify those files. Do not paste `.env` into an assistant prompt, and do not add an assistant key to `.env`.

The exact sign-in prompt and command flags change between releases. Confirm them with each tool's own `--version` and `--help` on the VM before the session, rather than relying on the values recorded here.

## The four assistants

Each is launched from the repository root, so it reads the working directory and the project instructions. The provider named in the last column receives the repository content the assistant reads.

| Assistant | Sign-in options | Launch | Provider that receives the repository |
|---|---|---|---|
| Claude Code | A Claude subscription or Anthropic Console sign-in, or `ANTHROPIC_API_KEY` | `claude` in the repository root | Anthropic |
| Codex | A ChatGPT account sign-in, or `OPENAI_API_KEY` | `codex` in the repository root | OpenAI |
| Gemini CLI | A Google account sign-in, or `GEMINI_API_KEY` | `gemini` in the repository root | Google |
| Aider | The key for the provider of the model you select | `aider --no-auto-commits --no-dirty-commits --model <name> <file>` | The provider of the selected model |

## Aider

Aider is model-agnostic, so name the provider and model rather than relying on a default. Select the model with `--model` and set the matching key in the environment (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY` or `GEMINI_API_KEY`). Disable automatic commits with `--no-auto-commits` and `--no-dirty-commits`, so the diff is reviewed before anything is recorded in git. Start from a clean working tree and scope it to the one file you expect to change, for example `aider --no-auto-commits --no-dirty-commits --model <name> modules/module5/pyrit/reference/attack.py`.

## What the assistant sees

The assistant reads the repository you point it at, and that content reaches the provider named above. Use only the synthetic course material in the course repository, and only a provider approved for the course. Do not give an assistant a credential it does not need, and do not send client data or real records through it.

© 2026 Deep Cyber Ltd. Course materials licensed for internal use. See `LICENCE.md` in your course folder.
