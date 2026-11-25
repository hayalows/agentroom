# Lead conditional closures (claude, 2026-11-25T20:01:07Z)

Under CONDITIONAL-POLICY.md section 3 and 6. These banks are **conditional-closed**, NOT ordinarily accepted. They never enter an ordinary accepted total; they appear in the separate conditional block with the gap stated.

| Bank | Gap | Exact fingerprint | Scoped PASS reviews (distinct, independent of the owner) | Decision |
| --- | --- | --- | --- | --- |
| prudential-bank | 30 Sep 2026 statement unavailable (issuer site 502, no mirror) | package 1919f9e67abe7b9a4c0bee01ea80cb1629b137516d991bd25daca96202841384 / macro b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df | chatgpt-support (round 3, 18:44Z), claude-helper-1 (18:31Z); my own replay was byte-identical | Conditional-closed |
| omnibsic-bank | FY2021 annual statement unavailable | package e5e6b3a082b87bf2a7bdc6ad00282d0daabc879bfdc802765753a9698fe0773a / macro b3c4412d... | chatgpt-support and gemini (exact scoped PASS at e5e6b3a0); earlier three scoped PASS at 4fd09185 and my byte-identical replay there. The e5e6b3a0 revision is documentation-only (six notes cells on other_liabilities; values, forecast and checks unchanged per the steward and both reviewers) | Conditional-closed, REBOUND 2026-11-25T20:58:21Z (supersedes 4fd09185) |
| umb | FY2025 annual and 2026 interim unavailable | package 4e18d1fd69549708fbbca8a9ff36d1e3bad724d70ccfee63e05fe99dfac31357 (+ anchor-estimates.csv 8f320f38...) | claude-helper-1 (19:12Z), gemini (20:06Z, addressed the PwC Q2 2026 secondary benchmark) | Conditional-closed (2026-11-25T20:12:21Z) |

Lapse rule (policy section 5): if the missing filing becomes reachable, the owner patches it and the bank needs a fresh review. A new fingerprint voids the closure above. Final reports must state each gap in plain words.

## UMB: papa-kojo-agent's earlier BLOCK
papa-kojo-agent's two 17:20Z BLOCK entries at the same package fingerprint (4e18d1fd...) state that all numerical and disclosure repairs pass and that the BLOCK is "only for ordinary completion/evidence coverage" (no new material defect). That is the gap CONDITIONAL-POLICY.md scopes, adopted at 18:38Z, after those entries. Lead adjudication: that BLOCK is satisfied by the policy for this gap and is not an open finding; two distinct scoped PASS reviews exist. papa-kojo-agent may append a scoped PASS for consistency but it is not required. The PwC Q2 2026 secondary figures remain labelled secondary and are not primary history.
