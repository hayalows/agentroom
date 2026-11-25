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
| base | FY2026E | 0.000 | 0.000000 | PASS | 27.75% | 13.00% | PASS | 346.6 | 13.1% |
| base | FY2027E | 0.000 | 0.000000 | PASS | 27.90% | 13.00% | PASS | 154.9 | 5.4% |
| base | FY2028E | 0.000 | 0.000000 | PASS | 25.96% | 13.00% | PASS | 46.5 | 1.6% |
| base | FY2029E | 0.000 | 0.000000 | PASS | 21.27% | 13.00% | PASS | -154.0 | -5.3% |
| base | FY2030E | 0.000 | 0.000000 | PASS | 15.15% | 13.00% | PASS | -308.2 | -11.4% |
| downside | FY2026E | 0.000 | 0.000000 | PASS | 28.01% | 13.00% | PASS | 343.9 | 13.0% |
| downside | FY2027E | 0.000 | 0.000000 | PASS | 24.36% | 13.00% | PASS | -62.7 | -2.3% |
| downside | FY2028E | 0.000 | 0.000000 | PASS | 15.70% | 13.00% | PASS | -391.5 | -15.4% |
| downside | FY2029E | 0.000 | 0.000000 | PASS | 6.04% | 13.00% | FAIL | -530.3 | -25.4% |
| downside | FY2030E | 0.000 | 0.000000 | PASS | -4.46% | 13.00% | FAIL | -683.6 | -46.3% |
| upside | FY2026E | 0.000 | 0.000000 | PASS | 27.70% | 13.00% | PASS | 354.7 | 13.4% |
| upside | FY2027E | 0.000 | 0.000000 | PASS | 29.29% | 13.00% | PASS | 252.2 | 8.6% |
| upside | FY2028E | 0.000 | 0.000000 | PASS | 29.38% | 13.00% | PASS | 208.4 | 6.6% |
| upside | FY2029E | 0.000 | 0.000000 | PASS | 27.95% | 13.00% | PASS | 127.9 | 3.8% |
| upside | FY2030E | 0.000 | 0.000000 | PASS | 25.77% | 13.00% | PASS | 80.3 | 2.3% |

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

Short-bill share of non-reserve cash (driver `short_bill_share_of_noncash_reserve_cash`; FY2025 observed 54.0% = 3561.795 / (9902.445 - 3306.666)). Model value 54.0%; 0% removes only the short-bill line (placements income, ROU and the capital proxy stay as in the model).
| Share | Scenario | FY2026E PAT | FY2027E PAT | FY2030E PAT | FY2030E CAR proxy |
| --- | --- | --- | --- | --- | --- |
| 0% | base | 308.4 | 3.0 | -804.2 | -4.10% |
| 0% | downside | 306.5 | -450.9 | -1273.9 | -38.31% |
| 0% | upside | 315.7 | 124.2 | -298.7 | 13.82% |
| 27% | base | 327.5 | 78.6 | -563.4 | 5.75% |
| 27% | downside | 325.2 | -258.6 | -994.9 | -21.31% |
| 27% | upside | 335.2 | 187.9 | -89.8 | 20.40% |
| 54% (model) | base | 346.6 | 154.9 | -308.2 | 15.15% |
| 54% (model) | downside | 343.9 | -62.7 | -683.6 | -4.46% |
| 54% (model) | upside | 354.7 | 252.2 | 80.3 | 25.77% |

Component yield table. FY2025 observed (note 8 / balance sheet) against the base FY2027E model rate. This is a calibration comparison, not a back-test of the engine, because FY2025 macro inputs are not in `macro.csv`.
| Component | FY2025 observed | Basis | Base FY2027E model |
| --- | --- | --- | --- |
| Loan interest / average loans | 24.51% | net loans (model basis) | 16.00% policy rate + spread |
| Loan interest / average loans | 13.84% | gross loans (not modelled) | n/a |
| Government securities interest / average (investment securities + short bills) | 19.59% | note 8 against balances | 11.75% blend, plus 5.50% 91-day bill on the short-bill share of cash |
| Placements interest / average other (non-bill, non-reserve) cash | 4.12% | cash less short bills less mandatory reserve | 4.12% held constant |
| Mandatory reserve / customer deposits | 25.01% | note 18 | 20% CRR proxy (macro.csv); the reserve is an eligibility proxy only |

Earning-base sensitivities (base scenario; each row changes one driver, the others stay at model values).
| Driver | Setting | FY2026E PAT | FY2027E PAT | FY2030E PAT | FY2030E CAR proxy |
| --- | --- | --- | --- | --- | --- |
| placements inclusion | 0% | 323.5 | 57.7 | -538.8 | 5.69% |
| placements inclusion | 50% | 335.1 | 106.2 | -424.3 | 10.63% |
| placements inclusion | 100% (model) | 346.6 | 154.9 | -308.2 | 15.15% |
| loan yield spread | -2 pp | 339.7 | 124.0 | -391.4 | 12.14% |
| loan yield spread | +2 pp | 353.6 | 185.8 | -225.1 | 18.12% |

Capital stress (static, FY2030E; absolute gap = capital needed to reach the minimum CAR less capital held, GHS m). Illustrative: no interim regulatory numerator or RWA is published, so these show how far the proxy depends on the numerator and the RWA density.
| Scenario | Basis | Numerator | RWA density | CAR | Gap to min CAR |
| --- | --- | --- | --- | --- | --- |
| base | model proxy (regulatory numerator) | 1106.5 | 23.79% | 15.15% | 0.0 |
| base | book equity numerator, version 1 density | 2545.9 | 49.69% | 16.69% | 0.0 |
| base | regulatory numerator, 38% density | 1106.5 | 38.00% | 9.49% | 410.0 |
| base | regulatory numerator, 48% density | 1106.5 | 48.00% | 7.51% | 809.1 |
| downside | model proxy (regulatory numerator) | -303.5 | 23.79% | -4.46% | 1188.1 |
| downside | book equity numerator, version 1 density | 1135.9 | 49.69% | 7.99% | 711.5 |
| downside | regulatory numerator, 38% density | -303.5 | 38.00% | -2.79% | 1716.3 |
| downside | regulatory numerator, 48% density | -303.5 | 48.00% | -2.21% | 2088.1 |
| upside | model proxy (regulatory numerator) | 2044.2 | 23.79% | 25.77% | 0.0 |
| upside | book equity numerator, version 1 density | 3483.6 | 49.69% | 21.02% | 0.0 |
| upside | regulatory numerator, 38% density | 2044.2 | 38.00% | 16.13% | 0.0 |
| upside | regulatory numerator, 48% density | 2044.2 | 48.00% | 12.77% | 36.6 |

A negative CAR that becomes less negative at a higher density is not an improvement in capital: compare the absolute gaps.

Statutory reserve memo (forecast rows `x_statutory_reserve`, `x_statutory_transfer`): the 9M-2026 fund (534.049m) and year-to-date transfer (150.857m, 50.0% of PAT) are reported; the tiers are in `assumptions.json` and are not verified against the Act. Transfers move amounts between reserves and retained earnings, so total equity and CAR are unaffected. Year-by-year amounts are in `forecast.csv`; the table shows the transfer tier amounts for positive-profit years.
| Scenario | Year | PAT | 12.5% | 25% | 50% |
| --- | --- | --- | --- | --- | --- |
| base | FY2026E | 346.6 | 43.3 | 86.7 | 173.3 |
| base | FY2027E | 154.9 | 19.4 | 38.7 | 77.5 |
| base | FY2028E | 46.5 | 5.8 | 11.6 | 23.2 |
| downside | FY2026E | 343.9 | 43.0 | 86.0 | 172.0 |
| upside | FY2026E | 354.7 | 44.3 | 88.7 | 177.4 |
| upside | FY2027E | 252.2 | 31.5 | 63.0 | 126.1 |
| upside | FY2028E | 208.4 | 26.1 | 52.1 | 104.2 |
| upside | FY2029E | 127.9 | 16.0 | 32.0 | 63.9 |
| upside | FY2030E | 80.3 | 10.0 | 20.1 | 40.1 |

## 4. Spot-checks & Caveats
- `ADB25` p. 1: `total_assets` = `17,887,521` GHS '000 (`17887.521` GHS m); `profit_after_tax` = `367,291` GHS '000 (`367.291` GHS m).
- `ADB26Q3` p. 1–2: `customer_deposits` = `15,362,718` GHS '000 (`15362.718` GHS m); `profit_after_tax` = `301,714` GHS '000 (`301.714` GHS m).
- **CRR proxy caveat:** `cash_and_bog_balances` includes `due_from_banks` in FY2023–9M-2026 summary statements; `cash_bog >= 20% * customer_deposits` is a liquidity proxy screen, not regulatory BoG cedi CRR compliance.
- **CAR & solvency caveat:** Forecast `car_pct` is a proxy: FY2025 reported regulatory capital (note 5.7.2) rolled forward by the change in book equity, over total assets x RWA density backed out of the reported `9M-2026` `27.41%` CAR, with no automatic capital injection assumed. Where `car_pct < 13%` (flagged `FAIL`), that reflects the proxy under stressed/normalizing yields rather than a demonstrated regulatory breach.
