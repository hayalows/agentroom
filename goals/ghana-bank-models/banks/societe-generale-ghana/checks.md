# Societe Generale Ghana PLC checks

Recomputed from the committed `financials.csv` and `forecast.csv` by `model.py` (history) and the shared macro file (forecast). GHS millions; ratios in percent; tolerance 0.003. NA = input unavailable, not zero. `model.py` writes this whole file.

## Historical balance and income bridges

| Period | Assets-L-E | Asset components | NII | Operating income | PAT | Net loans |
|---|---:|---:|---:|---:|---:|---:|
| FY2021 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | 0.000 |
| FY2022 | -0.000 | 0.000 | 0.000 | 0.000 | -0.000 | -0.000 |
| FY2023 | 0.000 | 0.000 | -0.000 | 0.000 | -0.000 | 0.000 |
| FY2024 | 0.000 | 0.000 | -0.000 | 0.000 | 0.000 | 0.000 |
| FY2025 | 0.000 | 0.000 | 0.000 | -0.000 | -0.000 | 0.000 |
| 9M-2026 | 0.000 | 0.000 | -0.000 | 0.000 | -0.000 | NA |

## Source and schema checks

- Historical rows: 294; duplicate bank/period/statement/key rows: 0; reported rows missing source/page: 0; unavailable rows with non-blank value: 0.
- Spot-checks against printed filing pages (visually verified): SG25AR printed p.66 total assets 9,676.100447 -> 9676.100447; SG24AR printed p.64 PAT 551.299247 -> 551.299247; SG26Q3 9M-2026 total assets 11,078.375 -> 11078.375. All match.

## Ratios: reported vs recomputed (%)

| Period | Reported CAR | Reported NPL | Derived LDR | Derived cost/income | Derived ROE | Derived ROA |
|---|---:|---:|---:|---:|---:|---:|
| FY2021 | 22.38 | 7.58 | 82.71 | 50.44 | 17.92 | 3.39 |
| FY2022 | 16.00 | 13.48 | 85.74 | 43.47 | 10.00 | 1.65 |
| FY2023 | 18.71 | 19.55 | 91.67 | 38.54 | 28.08 | 4.98 |
| FY2024 | 19.81 | 16.56 | 93.91 | 35.31 | 22.54 | 5.30 |
| FY2025 | 23.39 | 13.06 | 87.65 | 57.15 | 15.26 | 4.10 |
| 9M-2026 | 18.52 | 13.98 | NA | 67.47 | 5.82 | 1.35 |

Reported CAR is the audited capital-adequacy note; the bank's narrative quotes a different basis (e.g. FY2025 17.5% excluding DDEP reliefs vs 23.39% audited) and this is recorded in `financials.csv` notes. ROE/ROA here use year-end equity/assets as a single-period ratio, so they differ slightly from the bank's average-balance ratios. Net-loan bridge for FY2026E and later is gross minus allowance; FY2021-FY2024 also net of a separately reported amortised-cost adjustment and interest in suspense.

<!-- FORECAST CHECKS GENERATED -->
## Forecast checks (generated from shared macro scenarios)

All forecast rows are estimated. Currency GHS millions; ratios in percent. Accounting arithmetic is checked before rounding. Cash-reserve and CAR checks are screening proxies, not regulatory returns. A negative cash residual or a positive gap is a flagged financing requirement, not an assumed funding source.

Rows: 855; scenario-years: 15; FY2025 residual RWA density: 0.668481; estimated 9M-2026 RWA: 9172.706; initial proxy regulatory capital: 1698.785 (anchored to the observed 18.52% CAR).

| Scenario | Year | Max bridge residual | CAR % | Min CAR % | Capital gap | Cash | CRR proxy | Reserve gap | Dividends |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 0.000 | 18.188 | 13.000 | 0.000 | 4055.919 | 1488.473 | 0.000 | 17.181 |
| base | FY2027E | 0.000 | 18.088 | 13.000 | 0.000 | 4388.618 | 1689.417 | 0.000 | 78.685 |
| base | FY2028E | 0.000 | 18.062 | 13.000 | 0.000 | 4780.335 | 1925.935 | 0.000 | 62.548 |
| base | FY2029E | 0.000 | 18.057 | 13.000 | 0.000 | 5205.823 | 2191.714 | 0.000 | 65.082 |
| base | FY2030E | 0.000 | 18.068 | 13.000 | 0.000 | 5676.911 | 2494.170 | 0.000 | 89.181 |
| downside | FY2026E | 0.000 | 17.538 | 13.000 | 0.000 | 3829.089 | 1416.912 | 0.000 | 0.000 |
| downside | FY2027E | 0.000 | 17.282 | 13.000 | 0.000 | 4025.566 | 1558.603 | 0.000 | 0.000 |
| downside | FY2028E | 0.000 | 16.523 | 13.000 | 0.000 | 4170.034 | 1714.463 | 0.000 | 0.000 |
| downside | FY2029E | 0.000 | 14.283 | 13.000 | 0.000 | 4123.824 | 1885.909 | 0.000 | 0.000 |
| downside | FY2030E | 0.000 | 10.666 | 13.000 | 283.544 | 3844.336 | 2065.071 | 0.000 | 0.000 |
| upside | FY2026E | 0.000 | 18.203 | 13.000 | 0.000 | 4217.631 | 1545.722 | 0.000 | 0.000 |
| upside | FY2027E | 0.000 | 18.690 | 13.000 | 0.000 | 4967.186 | 1839.409 | 0.000 | 0.000 |
| upside | FY2028E | 0.000 | 19.021 | 13.000 | 0.000 | 5876.025 | 2203.612 | 0.000 | 22.464 |
| upside | FY2029E | 0.000 | 19.092 | 13.000 | 0.000 | 6931.536 | 2644.334 | 0.000 | 119.085 |
| upside | FY2030E | 0.000 | 19.126 | 13.000 | 0.000 | 8220.700 | 3186.423 | 0.000 | 195.584 |

Accounting bridges: PASS (15/15). Capital below the shared minimum: 1/15 flagged. Cash-reserve proxy shortfalls: 0/15 flagged. Negative cash: 0/15 flagged.

FY2026 estimated earnings retain actual 9M income and estimate Q4 only. The Bank does not disclose a net FX position in the summary statements used, so no incremental FX translation P&L is modelled. Full prudential risk weights, OCI, capital deductions and liquidity eligibility are not available, so this is a simplified scenario analysis. Independent review required.
