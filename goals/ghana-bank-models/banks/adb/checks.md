# Checks: Agricultural Development Bank PLC (`adb`)

All historical and forecast checks dynamically computed by `model.py` from `financials.csv`, `assumptions.json`, and `sector/macro-assumptions/macro.csv`.

## 1. Historical Checks (recomputed from `financials.csv`)
| Period | BS Residual | NII Residual | TOI Residual | PBT Residual | PAT Residual | Max Abs Residual |
| --- | --- | --- | --- | --- | --- | --- |
| FY2021 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | 0.000 |
| FY2022 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | 0.002 |
| FY2023 | 0.000 | -0.000 | -0.000 | 0.000 | -0.000 | 0.000 |
| FY2024 | 0.000 | 0.000 | -0.000 | -0.000 | 0.000 | 0.000 |
| FY2025 | 0.000 | 0.000 | 0.000 | 0.000 | -0.000 | 0.001 |
| 9M-2026 | -0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.001 |
- Note: `9M-2026` PAT residual of `0.001` GHS m reflects 1-thousand rounding in `ADB26Q3` (`478,525 - 176,812 = 301,713` vs. reported `301,714`).
- Missing `source_id`/`page` on `reported` rows: **0**
- Non-blank `value` on `unavailable` rows: **0**
- Duplicate `(period, statement, line_item)` keys: **0**

## 2. Forecast Checks (`FY2026E–FY2030E`, recomputed)
| Scenario | Year | Max Residual | Est. CAR Proxy (%) | Min CAR (%) | CAR >= Min | CRR >= 20% | Est. PAT (GHS m) | Est. ROE (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | FY2026E | 0.000 | 26.60% | 13.00% | PASS | PASS | 266.3 | 10.2% |
| base | FY2027E | 0.000 | 23.02% | 13.00% | PASS | PASS | -146.8 | -5.5% |
| base | FY2028E | 0.000 | 17.73% | 13.00% | PASS | PASS | -416.2 | -17.6% |
| base | FY2029E | 0.000 | 10.68% | 13.00% | FAIL | PASS | -756.4 | -42.4% |
| base | FY2030E | 0.000 | 2.80% | 13.00% | FAIL | PASS | -1009.5 | -111.9% |
| downside | FY2026E | 0.000 | 26.88% | 13.00% | PASS | PASS | 264.8 | 10.2% |
| downside | FY2027E | 0.000 | 19.57% | 13.00% | PASS | PASS | -600.2 | -24.8% |
| downside | FY2028E | 0.000 | 8.98% | 13.00% | FAIL | PASS | -1096.3 | -69.5% |
| downside | FY2029E | 0.000 | -1.93% | 13.00% | FAIL | PASS | -1262.4 | -317.7% |
| downside | FY2030E | 0.000 | -13.24% | 13.00% | FAIL | PASS | -1461.5 | 151.5% |
| upside | FY2026E | 0.000 | 26.48% | 13.00% | PASS | PASS | 276.5 | 10.6% |
| upside | FY2027E | 0.000 | 24.11% | 13.00% | PASS | PASS | 25.5 | 0.9% |
| upside | FY2028E | 0.000 | 20.88% | 13.00% | PASS | PASS | -101.1 | -3.7% |
| upside | FY2029E | 0.000 | 16.43% | 13.00% | PASS | PASS | -338.8 | -13.6% |
| upside | FY2030E | 0.000 | 11.46% | 13.00% | FAIL | PASS | -519.0 | -25.2% |

## 3. Spot-checks & Caveats
- `ADB25` p. 1: `total_assets` = `17,887,521` GHS '000 (`17887.521` GHS m); `profit_after_tax` = `367,291` GHS '000 (`367.291` GHS m).
- `ADB26Q3` p. 1–2: `customer_deposits` = `15,362,718` GHS '000 (`15362.718` GHS m); `profit_after_tax` = `301,714` GHS '000 (`301.714` GHS m).
- **CAR caveat:** Forecast `car_pct` is a proxy anchored on 9M-2026 reported `27.41%` CAR, not a prudential Tier 1+Tier 2 calculation.
