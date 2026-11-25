# Checks: CalBank PLC (`calbank`)

All checks recomputed by `model.py` from `financials.csv`, `assumptions.json`, and `sector/macro-assumptions/macro.csv`.

## 1. Historical Balance Sheet, Loan Bridge & Income Bridge (FY2021–FY2025, 9M-2026)
- **Balance sheet balances (`total_assets = total_liabilities + total_equity`)**: PASS — residual = `0.000` GHS millions across all 6 periods (including negative equity `-184.903` in FY2023).
- **Asset / Liability / Equity component sums**: PASS — residual = `0.000` GHS millions across all 6 periods.
- **Loan bridge (`loans_and_advances_net = loans_and_advances_gross - loan_loss_allowance`)**: PASS — residual = `0.000` GHS millions for FY2021–FY2025 (`9M-2026` gross/allowance marked `unavailable`).
- **Income bridge (`NII`, `TOI`, `PBT`, `PAT`)**: PASS — residual = `0.000` GHS millions across all 6 periods (accounting for `x_lease_finance_cost`, negative `impairment_charge` for net impairment gains in FY2024–9M-2026, and negative `income_tax` for tax benefits in FY2022–FY2023).

## 2. Forecast Balance Sheet & Regulatory CAR Checks (`FY2026E–FY2030E`)
| Scenario | Year | BS Residual | Est. CAR (%) | BoG Min CAR (%) | CAR >= Min | Est. PAT (GHS m) | Est. ROE (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| base | FY2026E | 0.000 | 23.17% | 13.00% | PASS | 440.3 | 25.2% |
| base | FY2027E | 0.000 | 25.90% | 13.00% | PASS | 421.2 | 19.3% |
| base | FY2028E | 0.000 | 27.29% | 13.00% | PASS | 365.6 | 14.2% |
| base | FY2029E | 0.000 | 27.30% | 13.00% | PASS | 279.1 | 9.6% |
| base | FY2030E | 0.000 | 26.84% | 13.00% | PASS | 249.0 | 7.9% |
| downside | FY2026E | 0.000 | 22.70% | 13.00% | PASS | 359.9 | 21.1% |
| downside | FY2027E | 0.000 | 23.62% | 13.00% | PASS | 183.5 | 9.3% |
| downside | FY2028E | 0.000 | 22.38% | 13.00% | PASS | 39.9 | 1.9% |
| downside | FY2029E | 0.000 | 20.64% | 13.00% | PASS | -3.1 | -0.1% |
| downside | FY2030E | 0.000 | 18.35% | 13.00% | PASS | -66.5 | -3.2% |
| upside | FY2026E | 0.000 | 23.79% | 13.00% | PASS | 509.3 | 28.6% |
| upside | FY2027E | 0.000 | 27.27% | 13.00% | PASS | 539.3 | 23.4% |
| upside | FY2028E | 0.000 | 29.81% | 13.00% | PASS | 556.9 | 19.5% |
| upside | FY2029E | 0.000 | 31.38% | 13.00% | PASS | 537.0 | 15.8% |
| upside | FY2030E | 0.000 | 32.39% | 13.00% | PASS | 556.7 | 14.1% |

## 3. Spot-checks of `reported` rows against source PDFs
1. `CAL25` p. 65 (Bank 2025): `total_assets` = `11,899,483` GHS '000 = `11899.483` GHS m (matches `financials.csv`).
2. `CAL25` p. 142 (Bank 2025, Note 26): `loans_and_advances_gross` = `1,290,234` GHS '000 = `1290.234` GHS m; `loan_loss_allowance` = `219,354` GHS '000 = `219.354` GHS m (matches `financials.csv`).
3. `CAL24` p. 66 (Bank 2023): `total_equity` = `(184,903)` GHS '000 = `-184.903` GHS m (matches `financials.csv`).
4. `CAL26Q3` p. 1–2 (Bank Sep-26): `profit_after_tax` = `321,670` GHS '000 = `321.67` GHS m; `customer_deposits` = `10,633,698` GHS '000 = `10633.698` GHS m (matches `financials.csv`).

## 4. Citation & Spec Integrity
- Every `reported` row has a non-empty `source_id` and `page`.
- Every `unavailable` row has a blank `value`.
