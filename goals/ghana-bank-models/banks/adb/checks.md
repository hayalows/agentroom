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
| Scenario | Year | Max Residual | Iter Conv Residual | Inv Sec >= 0 | Est. CAR Proxy (%) | Min CAR (%) | CAR >= Min | Est. PAT (GHS m) | Est. ROE (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | FY2026E | 0.000 | 0.000000 | PASS | 26.68% | 13.00% | PASS | 276.1 | 10.6% |
| base | FY2027E | 0.000 | 0.000000 | PASS | 23.10% | 13.00% | PASS | -146.3 | -5.5% |
| base | FY2028E | 0.000 | 0.000000 | PASS | 17.81% | 13.00% | PASS | -415.7 | -17.5% |
| base | FY2029E | 0.000 | 0.000000 | PASS | 10.76% | 13.00% | FAIL | -755.9 | -42.1% |
| base | FY2030E | 0.000 | 0.000000 | PASS | 2.88% | 13.00% | FAIL | -1009.0 | -110.4% |
| downside | FY2026E | 0.000 | 0.000000 | PASS | 26.96% | 13.00% | PASS | 273.3 | 10.5% |
| downside | FY2027E | 0.000 | 0.000000 | PASS | 19.65% | 13.00% | PASS | -599.7 | -24.6% |
| downside | FY2028E | 0.000 | 0.000000 | PASS | 9.06% | 13.00% | FAIL | -1095.7 | -69.1% |
| downside | FY2029E | 0.000 | 0.000000 | PASS | -1.84% | 13.00% | FAIL | -1261.8 | -309.9% |
| downside | FY2030E | 0.000 | 0.000000 | PASS | -13.15% | 13.00% | FAIL | -1461.0 | N/A (avg_eq<=0) |
| upside | FY2026E | 0.000 | 0.000000 | PASS | 26.57% | 13.00% | PASS | 287.1 | 11.0% |
| upside | FY2027E | 0.000 | 0.000000 | PASS | 24.20% | 13.00% | PASS | 25.8 | 0.9% |
| upside | FY2028E | 0.000 | 0.000000 | PASS | 20.96% | 13.00% | PASS | -100.6 | -3.7% |
| upside | FY2029E | 0.000 | 0.000000 | PASS | 16.50% | 13.00% | PASS | -338.4 | -13.5% |
| upside | FY2030E | 0.000 | 0.000000 | PASS | 11.53% | 13.00% | FAIL | -518.6 | -25.0% |

## 3. Spot-checks & Caveats
- `ADB25` p. 1: `total_assets` = `17,887,521` GHS '000 (`17887.521` GHS m); `profit_after_tax` = `367,291` GHS '000 (`367.291` GHS m).
- `ADB26Q3` p. 1–2: `customer_deposits` = `15,362,718` GHS '000 (`15362.718` GHS m); `profit_after_tax` = `301,714` GHS '000 (`301.714` GHS m).
- **CRR proxy caveat:** `cash_and_bog_balances` includes `due_from_banks` in FY2023–9M-2026 summary statements; `cash_bog >= 20% * customer_deposits` is a liquidity proxy screen, not regulatory BoG cedi CRR compliance.
- **CAR & solvency caveat:** Forecast `car_pct` is a proxy anchored on `9M-2026` reported `27.41%` CAR with no automatic capital injection assumed. Where `car_pct < 13%` (flagged `FAIL`), that reflects the proxy under stressed/normalizing yields rather than a demonstrated regulatory breach.
