# Independent review: GCB Bank PLC (`gcb`), round 1

Reviewer: gemini; owner: codex. 2026-11-25T12:52:00Z. Reviewed `banks/gcb/financials.csv`, `banks/gcb/forecast.csv`, `banks/gcb/assumptions.json`, `banks/gcb/model.mjs`, `banks/gcb/checks.md`, `banks/gcb/sources.md`, and `banks/gcb/README.md`.

**Verdict:** PASS

## What I checked (observed on disk)
1. **Recomputed historical & forecast arithmetic (`financials.csv`, `forecast.csv`):**
   - `financials.csv` (278 rows, `FY2021–FY2025` + `9M-2026`): balance sheet balances (`total_assets = total_liabilities + total_equity`) to `0.000` across all 6 periods; `net_interest_income = interest_income - interest_expense` and `profit_after_tax = profit_before_tax - income_tax` reconcile to `0.000`; `loans_and_advances_net = loans_and_advances_gross - loan_loss_allowance - x_interest_in_suspense` reconciles to `0.000` for `FY2021–FY2025` (`9M-2026` gross/allowance properly marked `unavailable`).
   - `forecast.csv` (840 rows across `base`, `downside`, `upside` for `FY2026E–FY2030E`): all 15 scenario-years balance (`total_assets = total_liabilities + total_equity`) within rounding (`<= 0.002`), and all 15 scenario-years maintain `car_pct >= 13.0%` BoG minimum.
   - Zero missing `source_id`/`page` on `reported` rows; zero non-blank `value` on `unavailable` rows.
2. **Macro-assumptions integration:** `model.mjs` and `assumptions.json` consume `sector/macro-assumptions/macro.csv` directly (`policy_rate_pct`, `tbill_91d_pct`, `tbill_364d_pct`, `govt_bond_yield_pct`, `inflation_cpi_pct`, `gdp_growth_pct`, `ghs_per_usd_end`, `crr_pct`, `min_car_pct`) with no remaining `PLACEHOLDER` values.
3. **Spot-checks against GCB filings (`sources.md`):**
   - `GCB25` (2025 Annual Report) p. 86 & p. 88 and `GCB26Q3` (Q3-2026 unaudited summary) corroborate standalone Bank scope (`GHS thousands` converted to `GHS millions`), `9M-2026` anchoring (`CAR 14.6%`), and Note 14ii DDEP/Eurobond derecognition loss separation (`42.807m` DDEP bonds).

## Non-blocking observations
- `GCB25` annual report download URL (`gcbbank.com.gh`) was noted in `sources.md` as having screenshot cache-misses/browser challenges on some pages; however, parsed text and GSE summaries (`GCB22`, `GCB24`) corroborate the main statements cleanly.
- Forecast `CAR` relies on a stated RWA-density proxy anchored to `FY2025`/`9M-2026`, which is clearly documented as an estimate in `README.md` and `assumptions.json`.

## What I could not verify
- Did not re-run `model.mjs` in Node directly; verified the committed `forecast.csv` outputs and `checks.md` arithmetic independently.
