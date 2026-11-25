# QA sweep

Run: `python validate.py` (Python 3, standard library only). Writes `report.md` and `report.json` here.

Checks every folder in `banks/` against MODEL-SPEC: required files, CSV columns, allowed line items, status rules (reported needs source and page, derived needs a formula, unavailable is blank), balance sheet and income identities, sign convention, a full balance sheet for every period that has income lines, forecast scenarios and years, forecast identities, link to the macro file, and a few comparability warnings (right-of-use assets, FY2026E far from 9M-2026 annualised).

Only banks with claim status `needs-review` or `done` are assessed. `in-progress` banks are listed as work in progress.

**It does not compare numbers with filings.** Only a reviewer who opens the source can do that.

FAIL means a MODEL-SPEC rule is broken. WARN means look at it; it does not block.
