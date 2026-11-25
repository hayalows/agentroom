# Checks: CalBank PLC (`calbank`)

All historical and forecast checks dynamically computed by `model.py` from `financials.csv`, `assumptions.json`, and `sector/macro-assumptions/macro.csv`.

## 1. Historical Checks (recomputed from `financials.csv`)
| Period | BS Residual | NII Residual | TOI Residual | PBT Residual | PAT Residual | Max Abs Residual |
| --- | --- | --- | --- | --- | --- | --- |
| FY2021 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | 0.000 |
| FY2022 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| FY2023 | 0.000 | -0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| FY2024 | 0.000 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 |
| FY2025 | 0.000 | -0.000 | -0.000 | -0.000 | 0.000 | 0.000 |
| 9M-2026 | 0.000 | -0.000 | 0.000 | -0.000 | 0.000 | 0.000 |
- Missing `source_id`/`page` on `reported` rows: **0**
- Non-blank `value` on `unavailable` rows: **0**
- Duplicate `(period, statement, line_item)` keys: **0**

## 2. Forecast Checks (`FY2026E–FY2030E`, recomputed)
| Scenario | Year | Max Residual | Iter Conv Residual | Inv Sec >= 0 | Est. CAR Proxy (%) | Min CAR (%) | CAR >= Min | Est. PAT (GHS m) | Est. ROE (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | FY2026E | 0.000 | 0.000000 | PASS | 18.75% | 13.00% | PASS | 410.8 | 23.7% |
| base | FY2027E | 0.000 | 0.000000 | PASS | 19.67% | 13.00% | PASS | 352.4 | 16.7% |
| base | FY2028E | 0.000 | 0.000000 | PASS | 19.25% | 13.00% | PASS | 275.0 | 11.5% |
| base | FY2029E | 0.000 | 0.000000 | PASS | 18.20% | 13.00% | PASS | 168.2 | 6.5% |
| base | FY2030E | 0.000 | 0.000000 | PASS | 16.93% | 13.00% | PASS | 118.2 | 4.4% |
| downside | FY2026E | 0.000 | 0.000000 | PASS | 18.91% | 13.00% | PASS | 397.7 | 23.0% |
| downside | FY2027E | 0.000 | 0.000000 | PASS | 18.49% | 13.00% | PASS | 165.7 | 8.2% |
| downside | FY2028E | 0.000 | 0.000000 | PASS | 16.97% | 13.00% | PASS | 24.1 | 1.1% |
| downside | FY2029E | 0.000 | 0.000000 | PASS | 15.25% | 13.00% | PASS | -19.3 | -0.9% |
| downside | FY2030E | 0.000 | 0.000000 | PASS | 13.41% | 13.00% | PASS | -73.9 | -3.6% |
| upside | FY2026E | 0.000 | 0.000000 | PASS | 18.65% | 13.00% | PASS | 415.1 | 23.9% |
| upside | FY2027E | 0.000 | 0.000000 | PASS | 19.26% | 13.00% | PASS | 327.2 | 15.5% |
| upside | FY2028E | 0.000 | 0.000000 | PASS | 18.94% | 13.00% | PASS | 343.6 | 14.3% |
| upside | FY2029E | 0.000 | 0.000000 | PASS | 18.28% | 13.00% | PASS | 316.1 | 11.9% |
| upside | FY2030E | 0.000 | 0.000000 | PASS | 17.37% | 13.00% | PASS | 297.7 | 10.3% |

## 3. Spot-checks & Caveats
- `CAL25` p. 65 (Bank 2025): `total_assets` = `11,899,483` GHS '000 (`11899.483` GHS m).
- `CAL25` p. 142 (Bank 2025, Note 26): `loans_and_advances_gross` = `1,290,234` GHS '000; `loan_loss_allowance` = `219,354` GHS '000.
- `CAL26Q3` p. 1–2 (Bank Sep-26): `profit_after_tax` = `321,670` GHS '000 (`321.67` GHS m); `customer_deposits` = `10,633,698` GHS '000 (`10633.698` GHS m).
- **CRR proxy caveat:** `cash_and_bog_balances` includes `due_from_banks` in summary statements; `cash_bog >= 20% * customer_deposits` is a liquidity proxy screen, not regulatory BoG cedi CRR compliance.
- **CAR caveat:** Forecast `car_pct` is a proxy calibrated to `9M-2026` reported `18.4%` CAR (`total_equity / (total_assets * RWA_density)`), not a prudential Tier 1+Tier 2 calculation.
