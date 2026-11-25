# QA sweep

Run: `python validate.py` (Python 3, standard library only). Writes `report.md` and `report.json` here.

Checks every folder in `banks/` against MODEL-SPEC: required files, CSV columns, allowed line items, status rules (reported needs source and page, derived needs a formula, unavailable is blank), balance sheet and income identities, sign convention, a full balance sheet for every period that has income lines, forecast scenarios and years, forecast identities, link to the macro file, and a few comparability warnings (right-of-use assets, FY2026E far from 9M-2026 annualised).

Only banks with claim status `needs-review` or `done` are assessed. `in-progress` banks are listed as work in progress.

**It does not compare numbers with filings.** Only a reviewer who opens the source can do that.

FAIL means a MODEL-SPEC rule is broken. WARN means look at it; it does not block.


## v1.2 bounded correction (2026-11-25T17:43:47.975Z)
Pinned e73b4e6ee367d2f5e63a3465a0e3a57815917321; full QA run covers 23 folders, 2 FAIL/6 WARN overall, all 18 accepted banks have zero FAIL. Both FAIL concern Prudential FY23/24 gross-loan bridges; known write-off memo may not match validator naming rule, investigate before classifying as actual errors. Gemini fault injection fixed: duplicate/invalid line item continue, downstream later PAT corruption detected, only actually removed downside FY30 missing; takeover claim correctly assessed; finite numeric guards, malformed/missing headers, unavailable numeric rows, invalid status and wrong bank detected. Eight simultaneous faults + both missing-header cases and takeover/finite tests pass. No bank file edits. Pinned report not live; QA diagnostic not ordinary acceptance.
Run in a clean LF checkout: `python validate.py --input-root PATH_TO_REPO --output-dir PATH_OUTSIDE_REPO`. To replay pinned snapshot, use this revision's validator with a separate clean checkout of report's source commit. Run `python -I test_faults.py PATH_TO_REPO PATH_TO_VALIDATE_PY` for regression tests; the test mutates only temporary copied files. The report records the complete source SHA, not the generation commit. Claim status is diagnostic inclusion; exact supervisor acceptance remains separate. Invalid numerical cells are not silently zeroed. Request independent review from Gemini.
