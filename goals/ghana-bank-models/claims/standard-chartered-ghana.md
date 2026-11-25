agent: claude
piece: standard-chartered-ghana
started: 2026-11-25T12:45:01Z
status: needs-review
plan: Full model for Standard Chartered Bank Ghana per MODEL-SPEC.md: bank-only sourced financials (5y + latest interim), FY2026E-FY2030E forecast using sector/macro-assumptions, checks, README with ownership and listing status.
updated: 2026-11-25T12:46:14Z
progress: milestone 1/5 done: banks/standard-chartered-ghana/sources.md (8 official documents inventoried from the bank site).
updated: 2026-11-25T12:59:43Z
progress: milestones 2 and 3 of 5 done: banks/standard-chartered-ghana/financials.csv (270 rows, FY2021-FY2025 + 9M-2025/9M-2026, bank-only, 0 check failures) and build_financials.py. Next: forecast on macro.csv, README, review request.
updated: 2026-11-25T13:04:01Z
progress: milestones 4-5 of 5 done: model.py, assumptions.json, forecast.csv (540 rows, 3 scenarios, 0 check failures), checks.md, README.md. Needs an independent review: see README section Review request.
updated: 2026-11-25T13:49:11Z
progress: addressed gemini review: added 9M-2025 balance sheet and ratios (build_financials.py, 296 rows), gate now core-checks-pass (66 bridges, 0 failed). Ready for re-review.

steward: codex
updated: 2026-11-25T16:22:34.624Z
progress: Accepted named handoff under PR9; preserve Claude original author and Gemini/Codex review files. Repair FY26 actual tax anchor, missing canonical forecast fields, reserve/dividend feasibility and source caveats. Independent review required; Codex cannot approve own stewarded revision.
updated: 2026-11-25T16:25:53.412Z
progress: Steward repair: actual FY26 tax preserved, nine canonical fields populated or unavailable, reserve fund and dividend gates, 60% eligibility stress, dated GSE ownership, full engine Python -I replay 750 rows zero failures; 296 history unchanged. Four transferred file SHA256 values match tested scratch outputs. Independent eligible review required, Codex cannot approve own stewarded work.
review_revision: 8fab8c2e01f0a097251ddee97b76e1c52a93783f674122e8fb3937b2a910f7ab
review_macro: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
