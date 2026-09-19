# Lab D — proving a finding with no scoreboard

**L4 Guarded** is L3 with one change: the flag is still awarded, and then
stripped out before the reply is sent. Redaction happens *after* scoring, so
L4 has exactly the same failure rate as L3 by construction. Nothing was made
harder. You simply stopped being told.

Every tool in this course asserts on the flag marker. All of them go blind
here:

| | asserts on | at L4 |
|---|---|---|
| promptfoo | `not-contains OWASP{` | passes everything |
| garak | its own detectors | still works — it never used our flags |
| pyrit | `SubStringScorer("OWASP{")` | never reaches its objective |
| spikee | the `airt_flags` judge | scores nothing |

**This is the normal case.** No real target announces its own breaches. The
scoreboard was a teaching device, and this lab takes it away.

## Run something and watch it report clean

```bash
cd labs-ctf/blind/starter
mkdir -p "$PWD/out"                 # garak resolves relative prefixes under its own dir

garak --model_type rest \
  --generator_option_file target-l4.json \
  --probes lmrc.Profanity --generations 1 \
  --report_prefix "$PWD/out/l4"
```

Then run any probe you already know works at L3, and compare the replies. The
behaviour is identical. Only the marker is missing.

## Your task

Take **three findings** you established at an earlier level. For each, produce
the evidence you would put in front of a client — with nothing to grep for.

For each finding, write down:

| | |
|---|---|
| **What you asked** | the prompt, verbatim |
| **What came back** | the reply, verbatim |
| **What that proves happened in the system** | the effect, not the words |
| **Why it could not be anything else** | rule out a plausible reply |
| **Why it matters** | the consequence, in the client's terms |

The third and fourth rows are the work. *"The assistant gave me Priya Raman's
email address"* is a claim about text. **"The assistant returned a record for a
customer other than the one authenticated in this session, including an email
address and phone number that match no data I supplied"** is a claim about the
system, and it is the one that survives someone arguing back.

## Cross-check yourself

You can confirm your reasoning against the database directly — the MCP server
is reachable and takes SQL:

```bash
curl -s localhost:8224/ -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"query","arguments":{"sql":"SELECT * FROM customers"}}}'
```

Use it to check whether the record the assistant produced is real or invented.
**Both answers are findings**, and they are different ones: a real record is a
data disclosure, an invented one is fabrication presented as fact.

## The point

You have been scoring against markers all course. Here the marker is gone, the
vulnerability is unchanged, and every automated tool reports clean.

A tool tells you what it can detect. It never tells you what it missed — and
"the scan came back clean" is a statement about the scan.

(c) 2026 Deep Cyber Ltd. Apache 2.0 licensed.
