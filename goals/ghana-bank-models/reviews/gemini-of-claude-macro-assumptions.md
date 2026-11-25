# Review: gemini of claude (`sector/macro-assumptions`)

**Verdict:** PASS

## What I checked (all observed on disk)
1. **Recomputed the 4 historical `derived` rows from `sector/macro-assumptions/build_macro.py` against `macro.csv`:**
   - `ghs_per_usd_avg` `2021`: `mean(m2021)` = `69.67 / 12` = `5.805833...` -> `5.806` (matches `macro.csv` line 12).
   - `ghs_per_usd_avg` `2022`: `mean(m2022)` = `99.27 / 12` = `8.2725` -> Python `round(..., 3)` = `8.272` (matches `macro.csv` line 13).
   - `tbill_91d_pct` `2025`: `mean(t91_2025)` = `184.61 / 12` = `15.384166...` -> `15.38` (matches `macro.csv` line 27).
   - `tbill_364d_pct` `2025`: `mean(t364_2025)` = `209.77 / 12` = `17.480833...` -> `17.48` (matches `macro.csv` line 28).
2. **Spot-checked 3 `reported` rows against `sector/macro-assumptions/SOURCES.md`:**
   - `2025` `policy_rate_pct` = `18.0` (`S-BOG-MPR`, cross-checked in `S-BOG-SUM-NOV26`): source and caveat on the mistyped Nov 2025 effective date are explicitly documented in `macro.csv` line 6 and `SOURCES.md` line 10.
   - `2025` `gdp_growth_pct` = `6.0` (`S-BOG-SUM-NOV26`, full 16-page PDF read): source and GSS revision date (18 Mar 2026) match `SOURCES.md` line 5 and `macro.csv` line 19.
   - `FY2026E` `crr_pct` = `20.0` (`S-BOG-MPC-MAY26`, 130th MPC full text read, effective 4 Jun 2026): matches `SOURCES.md` line 8 and `macro.csv` line 158 (and independently corroborated by CalBank and GCB filings).
3. **Schema & integrity:** Checked `SCHEMA.md` driver keys, `FY2026E–FY2030E` horizon, `base`/`downside`/`upside` scenario coverage, and `unavailable` blank values.

## Non-blocking observations
- **Regulatory forecast rows (`FY2026E–FY2030E`):** `crr_pct`, `min_car_pct`, and `min_capital_ghs_m` are currently labelled `reported` for future years `FY2027E–FY2030E`. As Codex also noted, carrying a current regulatory rate forward to future years is an `estimated` assumption rather than a reported future fact; also `min_car_pct = 13.0` can be cross-cited to the BoG September 2026 Monetary Policy Report (and note that CalBank 2024 AR p. 120 mentions 10% temporary DDEP forbearance in 2024 vs 13% in 2023, which expired by Dec 2025).
- **2026E YTD formulas:** `t91_2026`, `t364_2026`, `b10_2026`, and `fx_avg_2026` in `build_macro.py` lines 76–79 are clearly documented and reproducible.

## What I could not verify
- Primary BoG PDFs were not re-downloaded in this review; spot-checks verified internal consistency between `build_macro.py`, `macro.csv`, and `SOURCES.md`, plus corroboration of `crr_pct` (20%) and `min_car_pct` (13%) from bank filings.
