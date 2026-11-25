# Checks: Ecobank Ghana PLC (`ecobank-ghana`)

All historical and forecast checks dynamically computed by `model.py` from `financials.csv`, `assumptions.json`, and `sector/macro-assumptions/macro.csv`.

## 1. Historical Checks (recomputed from `financials.csv`)
| Period | BS Residual | NII Residual | TOI Residual | PBT Residual | PAT Residual | Max Abs Residual |
| --- | --- | --- | --- | --- | --- | --- |
| FY2021 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| FY2022 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| FY2023 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | 0.000 |
| FY2024 | 0.000 | 0.000 | 0.000 | -0.000 | -0.000 | 0.000 |
| FY2025 | 0.000 | -0.000 | -0.000 | 0.000 | 0.000 | 0.000 |
| 9M-2026 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
- Missing `source_id`/`page` on `reported` rows: **0**
- Non-blank `value` on `unavailable` rows: **0**
- Duplicate `(period, statement, line_item)` keys: **0**

## 2. Forecast Checks (`FY2026E–FY2030E`, recomputed)
| Scenario | Year | Max Residual | Iter Conv Residual | Inv Sec >= 0 | Est. CAR Proxy (%) | Min CAR (%) | CAR >= Min | Est. PAT (GHS m) | Est. ROE (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | FY2026E | 0.000 | 0.000000 | PASS | 18.84% | 13.00% | PASS | 1850.1 | 23.7% |
| base | FY2027E | 0.000 | 0.000000 | PASS | 19.93% | 13.00% | PASS | 2200.8 | 23.5% |
| base | FY2028E | 0.000 | 0.000000 | PASS | 20.42% | 13.00% | PASS | 2088.0 | 19.0% |
| base | FY2029E | 0.000 | 0.000000 | PASS | 20.42% | 13.00% | PASS | 1884.0 | 15.1% |
| base | FY2030E | 0.000 | 0.000000 | PASS | 20.24% | 13.00% | PASS | 1910.2 | 13.7% |
| downside | FY2026E | 0.000 | 0.000000 | PASS | 18.96% | 13.00% | PASS | 1807.4 | 23.2% |
| downside | FY2027E | 0.000 | 0.000000 | PASS | 19.54% | 13.00% | PASS | 1574.3 | 17.1% |
| downside | FY2028E | 0.000 | 0.000000 | PASS | 19.37% | 13.00% | PASS | 1228.8 | 11.8% |
| downside | FY2029E | 0.000 | 0.000000 | PASS | 19.10% | 13.00% | PASS | 1275.7 | 11.2% |
| downside | FY2030E | 0.000 | 0.000000 | PASS | 18.84% | 13.00% | PASS | 1351.6 | 10.8% |
| upside | FY2026E | 0.000 | 0.000000 | PASS | 18.74% | 13.00% | PASS | 1865.9 | 23.9% |
| upside | FY2027E | 0.000 | 0.000000 | PASS | 19.76% | 13.00% | PASS | 2409.6 | 25.6% |
| upside | FY2028E | 0.000 | 0.000000 | PASS | 20.31% | 13.00% | PASS | 2484.7 | 22.3% |
| upside | FY2029E | 0.000 | 0.000000 | PASS | 20.46% | 13.00% | PASS | 2483.9 | 19.3% |
| upside | FY2030E | 0.000 | 0.000000 | PASS | 20.37% | 13.00% | PASS | 2641.9 | 18.0% |

## 3. Spot-checks & Caveats
- `EGH25` p. 1 (Bank 2025): `total_assets` = `46,076,237` GHS '000 (`46076.237` GHS m); `profit_after_tax` = `1,792,352` GHS '000 (`1792.352` GHS m).
- `EGH26Q3` p. 1 (Bank Sep-26): `customer_deposits` = `36,100,191` GHS '000 (`36100.191` GHS m).
- `EGH24` p. 1 (Bank 2023): `x_modification_loss` = `937,762` GHS '000 (`937.762` GHS m).
- **CRR proxy caveat:** `cash_and_bog_balances` includes `due_from_banks` in the GSE summary statements, so the `cash_bog >= 20% * customer_deposits` floor is a liquidity proxy screen rather than a regulatory BoG cedi CRR compliance proof.
- **CAR caveat:** Forecast `car_pct` is a proxy anchored on 9M-2026 reported `18.19%` CAR (`total_equity / (total_assets * RWA_density)`), not a prudential Tier 1+Tier 2 calculation.
- **FX caveat:** Currency breakdown of assets/liabilities is unavailable in GSE summary statements, so `ghs_per_usd_end` revaluation is not modelled separately.
