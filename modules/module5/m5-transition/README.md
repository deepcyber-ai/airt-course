# Module 5 closer — the components reveal

The five-minute transition at the end of Module 5. Module 5 ran the multi-turn
attacks with prepared settings and kept the spotlight on the *technique*. This
opens one **saved** trace and names the three things that were quietly at work:

```bash
python3 modules/module5/m5-transition/transition_view.py
```

- the **attacker** — the adversarial model that wrote each turn,
- the **technique** — how the search was organised (Crescendo here),
- the **scorer** — and the key point: it was a deterministic **rule** (a marker
  match), **not** a model. A model name in a config does not establish that an
  LLM judge was ever called.

That hands off to Module 6, where the scorer stops being invisible machinery and
becomes the subject. It is a saved trace, labelled as such — no live run, no spend.
