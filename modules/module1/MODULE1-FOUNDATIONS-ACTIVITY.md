# Module 1 - Foundations: learner excerpts and reflection

AMLUCS 2026 - Foundations (75 min). A lecture and demonstration module: there is
no coding lab. This sheet holds the learner-visible excerpts to look at and a
short reflection to write. The full source key stays with the instructor.

## What you are shown

**1. The red-teaming process, from the field.** Figure 4, "Phases of a GenAI Red
Teaming Process Blueprint", reproduced here as
[`owasp-red-teaming-figure4.png`](owasp-red-teaming-figure4.png) from the OWASP Top
10 for LLMs GenAI Red Teaming Guide v1.0 (printed page 25). Credit OWASP; licensed
CC BY-SA 4.0 (the licence text is included as `owasp-figure-licence.txt`; the figure
is unchanged). Source:
https://genai.owasp.org/resource/genai-red-teaming-guide/ . The reference does not
imply OWASP endorsement of this course.

**2. The O'Brien lookup demo (Live, ~5 min).** The instructor sends the same
customer-lookup request against two builds of the same assistant. The MODEL output
is byte-identical; a single line of application code decides whether the second
customer's record is returned. Watch where the decision actually sits.

  - This is a **benign lookup comparison**, chosen to isolate one variable. It is
    NOT an injection attack, and it is NOT a measured attack-success rate. Do not
    read it as "the model is X% vulnerable".

## Reflect (write two or three sentences each)

1. In the O'Brien demo the model output did not change. Where did the security
   outcome actually get decided, and what does that imply about where to look for
   failures in an LLM application?
2. A control that refuses everyone blocks every attack. Why is "did the attack get
   through?" not, on its own, enough to say a control works?
3. Pick one phase of the OWASP blueprint. What evidence would tell you that phase
   was actually done, rather than just claimed?

## How this connects forward

You will keep meeting the same distinction all week: a flag, a model's own claim,
and an authenticated action (a real database or audit effect) are DIFFERENT
observations. Module 2 stands the targets up; by Module 8 you run a full
engagement and have to defend which of the three you actually have.
