# Checks: Ecobank Ghana PLC (`ecobank-ghana`)

All checks recomputed by `model.py` from `financials.csv`, `assumptions.json`, and `sector/macro-assumptions/macro.csv`.

## 1. Historical Balance Sheet & Income Bridge (FY2021–FY2025, 9M-2026)
- **Balance sheet balances (`total_assets = total_liabilities + total_equity`)**: PASS — residual = `0.000` GHS millions across all 6 periods.
- **Asset / Liability / Equity component sums**: PASS — residual = `0.000` GHS millions across all 6 periods.
- **Income bridge (`NII`, `TOI`, `PBT`, `PAT`)**: PASS — residual = `0.000` GHS millions across all 6 periods (accounting for `x_lease_finance_cost` in all periods and `x_modification_loss = 937.762` in FY2023).
- **Unavailable items**: `due_from_banks`, `loans_and_advances_gross`, `loan_loss_allowance`, `tier1_pct` (and `roe_pct`/`roa_pct` for interim 9M-2026) are left blank with `status=unavailable` because GSE summary statements report net loans and combined cash & cash equivalents only.

## 2. Forecast Balance Sheet & Regulatory CAR Checks (`FY2026E–FY2030E`)
| Scenario | Year | BS Residual | Est. CAR (%) | BoG Min CAR (%) | CAR >= Min | Est. PAT (GHS m) | Est. ROE (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| base | FY2026E | 0.000 | 22.41% | 13.00% | PASS | 2161.5 | 27.2% |
| base | FY2027E | 0.000 | 23.93% | 13.00% | PASS | 2434.8 | 25.0% |
| base | FY2028E | 0.000 | 24.80% | 13.00% | PASS | 2346.6 | 20.3% |
| base | FY2029E | 0.000 | 25.13% | 13.00% | PASS | 2165.3 | 16.4% |
| base | FY2030E | 0.000 | 25.21% | 13.00% | PASS | 2200.0 | 14.8% |
| downside | FY2026E | 0.000 | 22.18% | 13.00% | PASS | 1927.3 | 24.6% |
| downside | FY2027E | 0.000 | 23.67% | 13.00% | PASS | 1707.6 | 18.3% |
| downside | FY2028E | 0.000 | 24.11% | 13.00% | PASS | 1350.6 | 12.7% |
| downside | FY2029E | 0.000 | 24.32% | 13.00% | PASS | 1340.3 | 11.4% |
| downside | FY2030E | 0.000 | 24.38% | 13.00% | PASS | 1359.2 | 10.5% |
| upside | FY2026E | 0.000 | 22.41% | 13.00% | PASS | 2288.4 | 28.5% |
| upside | FY2027E | 0.000 | 23.75% | 13.00% | PASS | 2742.2 | 27.6% |
| upside | FY2028E | 0.000 | 24.63% | 13.00% | PASS | 2871.7 | 24.1% |
| upside | FY2029E | 0.000 | 25.21% | 13.00% | PASS | 2913.7 | 20.9% |
| upside | FY2030E | 0.000 | 25.55% | 13.00% | PASS | 3100.1 | 19.3% |

## 3. Spot-checks of `reported` rows against source PDFs
1. `EGH25` p. 1 (Bank 2025): `total_assets` = `46,076,237` GHS '000 = `46076.237` GHS m (matches `financials.csv`).
2. `EGH25` p. 1 (Bank 2025): `profit_after_tax` = `1,792,352` GHS '000 = `1792.352` GHS m (matches `financials.csv`).
3. `EGH26Q3` p. 1 (Bank Sep-26): `customer_deposits` = `36,100,191` GHS '000 = `36100.191` GHS m (matches `financials.csv`).
4. `EGH24` p. 1 (Bank 2023): `x_modification_loss` = `937,762` GHS '000 = `937.762` GHS m (matches `financials.csv`).

## 4. Citation & Spec Integrity
- Every `reported` row has a non-empty `source_id` and `page`.
- Every `unavailable` row has a blank `value`.
