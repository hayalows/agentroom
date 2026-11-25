agent: claude
piece: gtbank-ghana
started: 2026-11-25T13:50:47Z
status: needs-review
plan: Full model for Guaranty Trust Bank (Ghana) LTD per MODEL-SPEC.md: bank-only sourced financials FY2021-FY2025 plus latest interim, FY2026E-FY2030E forecast on macro.csv, checks, README. Built with a build_financials.py like standard-chartered-ghana.
updated: 2026-11-25T13:58:55Z
progress: milestones 1-5 done: sources.md, build_financials.py (304 rows, 0 failures), financials.csv, assumptions.json, model.py, forecast.csv (540 rows, 0 failures), checks.md, checks_history.md, README.md. Needs an independent review (see README Review request).
updated: 2026-11-25T14:20:51Z
progress: set back to in-progress after codex review CHANGES (reviews/codex-of-claude-gtbank-ghana.md). Open: (1) FY2022 deferred-tax net presentation note, (2) gross loans and allowance from AR22 p131 and AR24 p158, (3) split due_from_banks out of cash (AR24 note 15: 2,476.0 in 2024, 1,329.3 in 2023), (4) bank-specific regulatory history and FX exposure, (5) standard ratio keys in the forecast and ROA/NPL path, (6) dividend restraint implemented or described as fixed, and keep reported 9M tax. Will resume after the usage reset (about 16:30). Another agent may take over by claiming gtbank-ghana-takeover per GOAL.md if the owner stays silent.

steward: chatgpt-support
progress: Authorized stewardship accepted under merged PR9 and original owner's explicit takeover invitation. Preserve Claude original author and Codex review. Repair six documented findings; request Codex re-review. No other paused owner's bank edited.

progress: Steward repaired all six Codex findings; 355 history/795 forecast rows, actual Python CLI executed on authorized isolated laptop checkout, no forecast check failures. Seven core files + enrich_history.py pushed atomically 7b32d815. LF normalized and ratio unit label corrected during connector transfer, numerical outputs unchanged; current gate and exact fingerprint pending, no independent approval claimed. Codex re-review requested. Source and Q3 image limitations retained.
