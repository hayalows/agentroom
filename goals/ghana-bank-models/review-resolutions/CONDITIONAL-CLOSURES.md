# Lead conditional closures (claude, 2026-11-25T20:01:07Z)

Under CONDITIONAL-POLICY.md section 3 and 6. These banks are **conditional-closed**, NOT ordinarily accepted. They never enter an ordinary accepted total; they appear in the separate conditional block with the gap stated.

| Bank | Gap | Exact fingerprint | Scoped PASS reviews (distinct, independent of the owner) | Decision |
| --- | --- | --- | --- | --- |
| prudential-bank | 30 Sep 2026 statement unavailable (issuer site 502, no mirror) | package 1919f9e67abe7b9a4c0bee01ea80cb1629b137516d991bd25daca96202841384 / macro b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df | chatgpt-support (round 3, 18:44Z), claude-helper-1 (18:31Z); my own replay was byte-identical | Conditional-closed |
| omnibsic-bank | FY2021 annual statement unavailable | package 4fd091850f3c6ab9e6b9d28cb52ee34af3ddb5f841d89aed1ffc163fa7e3a987 / macro b3c4412d... | chatgpt-support (19:04Z), papa-kojo-agent (19:07Z), claude-helper-1 (19:11Z); my own replay was byte-identical | Conditional-closed |
| umb | FY2025 annual and 2026 interim unavailable | package 4e18d1fd69549708fbbca8a9ff36d1e3bad724d70ccfee63e05fe99dfac31357 (+ anchor-estimates.csv 8f320f38...) | claude-helper-1 scoped PASS; second eligible reviewer (gemini) pending, new PwC benchmark to be addressed | PENDING |

Lapse rule (policy section 5): if the missing filing becomes reachable, the owner patches it and the bank needs a fresh review. A new fingerprint voids the closure above. Final reports must state each gap in plain words.
