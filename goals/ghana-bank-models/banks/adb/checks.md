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
| base | FY2026E | 0.000 | 0.000000 | PASS | 27.31% | 13.00% | PASS | 323.5 | 12.3% |
| base | FY2027E | 0.000 | 0.000000 | PASS | 25.83% | 13.00% | PASS | 57.7 | 2.1% |
| base | FY2028E | 0.000 | 0.000000 | PASS | 21.74% | 13.00% | PASS | -102.0 | -3.7% |
| base | FY2029E | 0.000 | 0.000000 | PASS | 14.45% | 13.00% | PASS | -355.2 | -13.9% |
| base | FY2030E | 0.000 | 0.000000 | PASS | 5.69% | 13.00% | FAIL | -538.8 | -25.5% |
| downside | FY2026E | 0.000 | 0.000000 | PASS | 27.57% | 13.00% | PASS | 321.3 | 12.2% |
| downside | FY2027E | 0.000 | 0.000000 | PASS | 21.23% | 13.00% | PASS | -216.6 | -8.1% |
| downside | FY2028E | 0.000 | 0.000000 | PASS | 9.66% | 13.00% | FAIL | -573.6 | -25.2% |
| downside | FY2029E | 0.000 | 0.000000 | PASS | -3.00% | 13.00% | FAIL | -736.8 | -45.4% |
| downside | FY2030E | 0.000 | 0.000000 | PASS | -16.64% | 13.00% | FAIL | -915.6 | -114.9% |
| upside | FY2026E | 0.000 | 0.000000 | PASS | 27.25% | 13.00% | PASS | 331.1 | 12.6% |
| upside | FY2027E | 0.000 | 0.000000 | PASS | 27.21% | 13.00% | PASS | 152.4 | 5.3% |
| upside | FY2028E | 0.000 | 0.000000 | PASS | 25.80% | 13.00% | PASS | 93.7 | 3.1% |
| upside | FY2029E | 0.000 | 0.000000 | PASS | 22.94% | 13.00% | PASS | -6.6 | -0.2% |
| upside | FY2030E | 0.000 | 0.000000 | PASS | 18.98% | 13.00% | PASS | -111.1 | -3.7% |

## 3. Source bridges and short-bill sensitivity (v2)
| Period | Bridge | Residual (GHS m) |
| --- | --- | --- |
| FY2024 | gross loans - allowance - net loans | 0.000 |
| FY2024 | note 8 components - interest_income | 0.000 |
| FY2024 | regulatory capital - CET1 - tier 2 | -0.000 |
| FY2024 | cash - short bills - mandatory reserve (must be >= 0) | 3424.854 |
| FY2025 | gross loans - allowance - net loans | 0.000 |
| FY2025 | note 8 components - interest_income | 0.000 |
| FY2025 | regulatory capital - CET1 - tier 2 | 0.000 |
| FY2025 | cash - short bills - mandatory reserve (must be >= 0) | 3033.984 |
- Capital proxy anchors: FY2025 reported regulatory capital 1038.461; rolled to 9M-2026 by the change in book equity = 1322.469; implied RWA = 4824.768; RWA / total assets = 23.79%. Reported FY2025 RWA / total assets = 21.36%.
- Right-of-use assets are inside `property_equipment_intangibles` once (never in `other_assets`): FY2021 150.555 of 292.322; FY2022 110.923 of 347.347; FY2023 95.627 of 325.806; FY2024 72.591 of 279.842; FY2025 47.738 of 229.544; 9M-2026 26.408 of 219.905. `ROU <= PPE` holds in every period: PASS.

Short-bill share of non-reserve cash (driver `short_bill_share_of_noncash_reserve_cash`; FY2025 observed 54.0% = 3561.795 / (9902.445 - 3306.666)). Model value 54.0%; 0% reproduces the version before this repair on this line only.
| Share | Scenario | FY2026E PAT | FY2027E PAT | FY2030E PAT | FY2030E CAR proxy |
| --- | --- | --- | --- | --- | --- |
| 0% | base | 276.1 | -146.3 | -1009.0 | -15.16% |
| 0% | downside | 273.3 | -599.7 | -1461.0 | -50.93% |
| 0% | upside | 287.1 | 25.8 | -518.6 | 4.99% |
| 27% | base | 304.4 | -28.0 | -781.0 | -4.35% |
| 27% | downside | 302.6 | -409.5 | -1203.1 | -33.60% |
| 27% | upside | 311.7 | 88.9 | -318.8 | 12.28% |
| 54% (model) | base | 323.5 | 57.7 | -538.8 | 5.69% |
| 54% (model) | downside | 321.3 | -216.6 | -915.6 | -16.64% |
| 54% (model) | upside | 331.1 | 152.4 | -111.1 | 18.98% |

## 4. Spot-checks & Caveats
- `ADB25` p. 1: `total_assets` = `17,887,521` GHS '000 (`17887.521` GHS m); `profit_after_tax` = `367,291` GHS '000 (`367.291` GHS m).
- `ADB26Q3` p. 1–2: `customer_deposits` = `15,362,718` GHS '000 (`15362.718` GHS m); `profit_after_tax` = `301,714` GHS '000 (`301.714` GHS m).
- **CRR proxy caveat:** `cash_and_bog_balances` includes `due_from_banks` in FY2023–9M-2026 summary statements; `cash_bog >= 20% * customer_deposits` is a liquidity proxy screen, not regulatory BoG cedi CRR compliance.
- **CAR & solvency caveat:** Forecast `car_pct` is a proxy: FY2025 reported regulatory capital (note 5.7.2) rolled forward by the change in book equity, over total assets x RWA density backed out of the reported `9M-2026` `27.41%` CAR, with no automatic capital injection assumed. Where `car_pct < 13%` (flagged `FAIL`), that reflects the proxy under stressed/normalizing yields rather than a demonstrated regulatory breach.
