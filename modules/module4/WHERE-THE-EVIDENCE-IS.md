# Module 4 — where each tool keeps the evidence

The report on screen is a **summary**. The raw prompts and replies — the actual
evidence for your write-up — live in the files below. Run each command from the
tool's own directory.

| Tool | Summary view | Raw evidence (prompts + replies) | Read it |
|---|---|---|---|
| **garak** | `out/<tag>-<posture>.report.html` | `out/<tag>-<posture>.hitlog.jsonl` — **only the failures** (what got through, with the reply). `.report.jsonl` = every attempt. | `jq -c '{probe, prompt, output}' out/full-neutral.hitlog.jsonl` |
| **Promptfoo** | `promptfoo view` (browser) | SQLite DB: `$PROMPTFOO_CONFIG_DIR/promptfoo.db` | `promptfoo view` &nbsp;·&nbsp; or `sqlite3 "$PROMPTFOO_CONFIG_DIR/promptfoo.db"` |
| **Spikee** | the printed `success` summary | `results/results_…jsonl` (path printed at the end) — full transcript + judge output | `jq -c . results/results_*.jsonl` |
| **PyRIT** | the `[control]`/`[attack]` lines it prints | SQLite memory DB: `out/pyrit.db` | `sqlite3 out/pyrit.db ".tables"` then read the message table |
| **HumanBound** | `read-results.py` output | the prepared-run files under `native-demo/humanbound/prepared-run/` | `python3 …/humanbound/prepared-run/read-results.py` |

## Reading the numbers

garak's `%` is **resilience** — higher means the target *resisted* more — and
**DC-5 is its best grade**. So a **low** score is the interesting probe. A `100%`
probe (like `leakreplay`) has an **empty hitlog**, because nothing got through.

Promptfoo's **fail** on an attack case means the assertion caught the target
misbehaving — i.e. the attack **worked**. Spikee's `success: true` means the same
thing. Same event, opposite words.

## If a field comes back empty

The exact JSONL keys and the PyRIT table name vary a little by version. If a
`jq`/`sqlite3` field is blank, look at the shape first, then adjust:

```bash
head -1 results/results_*.jsonl | python3 -m json.tool   # spikee: see the keys
sqlite3 out/pyrit.db ".tables"                            # pyrit: see the table name
```
