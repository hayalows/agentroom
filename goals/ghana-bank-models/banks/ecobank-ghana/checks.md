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
| Scenario | Year | Max Residual | Est. CAR Proxy (%) | Min CAR (%) | CAR >= Min | CRR >= 20% | Est. PAT (GHS m) | Est. ROE (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | FY2026E | 0.000 | 18.82% | 13.00% | PASS | PASS | 1836.9 | 23.5% |
| base | FY2027E | 0.000 | 19.91% | 13.00% | PASS | PASS | 2200.3 | 23.5% |
| base | FY2028E | 0.000 | 20.40% | 13.00% | PASS | PASS | 2087.5 | 19.0% |
| base | FY2029E | 0.000 | 20.40% | 13.00% | PASS | PASS | 1883.4 | 15.1% |
| base | FY2030E | 0.000 | 20.23% | 13.00% | PASS | PASS | 1909.7 | 13.8% |
| downside | FY2026E | 0.000 | 18.94% | 13.00% | PASS | PASS | 1796.1 | 23.1% |
| downside | FY2027E | 0.000 | 19.52% | 13.00% | PASS | PASS | 1573.7 | 17.2% |
| downside | FY2028E | 0.000 | 19.35% | 13.00% | PASS | PASS | 1228.2 | 11.9% |
| downside | FY2029E | 0.000 | 19.08% | 13.00% | PASS | PASS | 1275.1 | 11.2% |
| downside | FY2030E | 0.000 | 18.82% | 13.00% | PASS | PASS | 1351.1 | 10.8% |
| upside | FY2026E | 0.000 | 18.71% | 13.00% | PASS | PASS | 1851.2 | 23.7% |
| upside | FY2027E | 0.000 | 19.74% | 13.00% | PASS | PASS | 2409.0 | 25.6% |
| upside | FY2028E | 0.000 | 20.29% | 13.00% | PASS | PASS | 2484.2 | 22.4% |
| upside | FY2029E | 0.000 | 20.44% | 13.00% | PASS | PASS | 2483.4 | 19.3% |
| upside | FY2030E | 0.000 | 20.35% | 13.00% | PASS | PASS | 2641.4 | 18.0% |

## 3. Spot-checks & Caveats
- `EGH25` p. 1 (Bank 2025): `total_assets` = `46,076,237` GHS '000 (`46076.237` GHS m); `profit_after_tax` = `1,792,352` GHS '000 (`1792.352` GHS m).
- `EGH26Q3` p. 1 (Bank Sep-26): `customer_deposits` = `36,100,191` GHS '000 (`36100.191` GHS m).
- `EGH24` p. 1 (Bank 2023): `x_modification_loss` = `937,762` GHS '000 (`937.762` GHS m).
- **CRR screening caveat:** `cash_and_bog_balances` includes due-from-banks in the summary statements; exact BoG cedi CRR eligibility cannot be isolated without note disclosures.
- **CAR caveat:** Forecast `car_pct` is a proxy anchored on 9M-2026 reported 18.19% CAR (`total_equity / (total_assets * RWA_density)`), not a prudential Tier 1+Tier 2 calculation.
