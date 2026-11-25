# Sector roll-up

Run: `python rollup.py` (Python 3, standard library only). Writes `rollup.md` and `rollup.csv` here.

Adds up the bank-only statements of every bank whose claim status is `needs-review` or `done`, then compares the totals with the Bank of Ghana sector aggregates in `sector/macro-assumptions/sector-context.csv` to show **coverage**. It is a PARTIAL sector until all banks are finished.

Forecast totals are the sum of each owner's own scenario forecast on the shared macro file. Treat them as a sensitivity, not a sector forecast, until the QA sweep and cross-review of every bank are complete.
