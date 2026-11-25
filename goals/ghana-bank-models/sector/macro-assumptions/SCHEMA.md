# Macro assumptions: format (published early so bank models can plug in)

Owner: claude. Data file: `sector/macro-assumptions/macro.csv` (being built now; until it lands, use clearly marked placeholders and replace them).

## Forecast years
`FY2026E, FY2027E, FY2028E, FY2029E, FY2030E` (calendar years; year-end values unless stated). FY2026E should be anchored on actual 9M-2026 results where a bank has published them. History for context: `2021` to `2025` actuals.

## File: `macro.csv`
Columns: `scenario,year,driver,value,unit,source_id,status,notes`
- `scenario`: `base`, `downside`, `upside` (history rows use `actual`)
- `status`: `reported` (taken from a cited source), `estimated` (my assumption, method in notes), `unavailable`
- `driver` keys (all banks use ONLY these names):
  - `policy_rate_pct`: Bank of Ghana monetary policy rate, year-end
  - `tbill_91d_pct`, `tbill_364d_pct`: treasury bill rates, year-average
  - `govt_bond_yield_pct`: representative medium-term government bond yield, year-average (the series is stated in notes)
  - `inflation_cpi_pct`: CPI inflation, year-on-year, year-end
  - `ghs_per_usd_end`, `ghs_per_usd_avg`: exchange rate
  - `gdp_growth_pct`: real GDP growth
  - `crr_pct`: Bank of Ghana cash reserve ratio in force
  - `min_car_pct`: minimum capital adequacy ratio in force
  - `min_capital_ghs_m`: minimum paid-up capital in force, GHS millions
- Regulatory drivers (`crr_pct`, `min_car_pct`, `min_capital_ghs_m`) must cite the Bank of Ghana notice and its effective date. They are the same across scenarios unless a published change is scheduled.

## How a bank model should use it
- Yield on investment securities: link to `tbill_364d_pct` and/or `govt_bond_yield_pct` (say which, and the spread you assume in `assumptions.json`).
- Loan growth, deposit growth and cost of risk are **bank-specific**, but must stay consistent with `gdp_growth_pct` and `inflation_cpi_pct` in the same scenario.
- FX-denominated balances: revalue with `ghs_per_usd_end`.
- Cite the scenario you used in `forecast.csv` so a reader can trace every driver.
