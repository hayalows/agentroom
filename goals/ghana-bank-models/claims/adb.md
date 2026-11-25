agent: gemini
piece: Agricultural Development Bank PLC
started: 2026-11-25T13:01:00Z
status: in-progress
steward: claude-helper-1
updated: 2026-11-25T14:10:14Z
progress: Round-2 fixes pushed for codex review (README refreshed with exact forecast & CAR shortfalls, non-tautological inv_sec>=0 + CRR proxy screen, assumptions.json 1:1 with model.py, ROE blank when avg_eq<=0, iterative Q4 inv_sec).
plan: Source bank-only FY2021-FY2025 and latest interim from public filings, build reproducible 3-scenario forecast using macro.csv, run dynamic checks, and submit README for review.
review_revision: 17056225a0db2b3922cd033f85c3e2735198e83cb104248fdbe2466819246147
review_macro: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

updated: 2026-11-25T18:14:09.000Z
progress: STEWARDSHIP ACCEPTED by claude-helper-1 (lead decision 18:30Z, availability handoff 'adb'). Original author gemini retained. Previous acceptance (17056225, codex round-2 PASS) preserved in git history and no longer applies to the new version. Scope: one new version with (1) ROU reclassification, 12 bank-periods, (2) earning on cash, T-bills and placements, (3) gross loans/ECL from note 21, (4) regulatory capital numerator. Will resubmit for fresh independent reviews.
