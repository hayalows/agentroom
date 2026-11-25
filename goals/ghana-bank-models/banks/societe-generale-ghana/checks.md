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
| 9M-2025 | 0.000 | 0.000 | 0.000 | -0.000 | -0.000 | NA |
| 9M-2026 | 0.000 | -0.000 | -0.000 | 0.000 | -0.000 | NA |

## Source and schema checks

- Historical rows: 354; duplicate bank/period/statement/key rows: 0; reported rows missing source/page: 0; unavailable rows with non-blank value: 0.
- Spot-checks against printed filing pages (visually verified): SG25AR printed p.66 total assets 9,676.100447 -> 9676.100447; SG24AR printed p.64 PAT 551.299247 -> 551.299247; SG26Q3 9M-2026 total assets 11,078.375 -> 11078.375. All match.

## Ratios: reported vs recomputed (%)

| Period | Reported CAR | Reported NPL | Derived LDR | Derived cost/income | Derived ROE | Derived ROA |
|---|---:|---:|---:|---:|---:|---:|
| FY2021 | 22.38 | 7.58 | 82.71 | 50.44 | 17.92 | 3.39 |
| FY2022 | 16.00 | 13.48 | 85.74 | 43.47 | 10.00 | 1.65 |
| FY2023 | 18.71 | 19.55 | 91.67 | 38.54 | 28.08 | 4.98 |
| FY2024 | 19.81 | 16.56 | 93.91 | 35.31 | 22.54 | 5.30 |
| FY2025 | 23.39 | 13.06 | 87.65 | 57.15 | 15.26 | 4.10 |
| 9M-2025 | 17.90 | 13.51 | NA | 52.02 | 13.51 | 3.33 |
| 9M-2026 | 18.52 | 13.98 | NA | 67.47 | 5.82 | 1.35 |

Reported CAR is the audited capital-adequacy note; the bank's narrative quotes a different basis (e.g. FY2025 17.5% excluding DDEP reliefs vs 23.39% audited) and this is recorded in `financials.csv` notes. ROE/ROA here use year-end equity/assets as a single-period ratio, so they differ slightly from the bank's average-balance ratios. Net-loan bridge for FY2026E and later is gross minus allowance; FY2021-FY2024 also net of a separately reported amortised-cost adjustment and interest in suspense.

<!-- FORECAST CHECKS GENERATED -->
## Forecast checks (generated from shared macro scenarios)

All forecast rows are estimated. Currency GHS millions; ratios in percent. Accounting arithmetic is checked before rounding. Cash-reserve and CAR checks are screening proxies, not regulatory returns. A negative cash residual or a positive gap is a flagged financing requirement, not an assumed funding source.

Rows: 915; scenario-years: 15; FY2025 residual RWA density: 0.668481; estimated 9M-2026 RWA: 9172.706; initial proxy regulatory capital: 1698.785 (anchored to the observed 18.52% CAR).

| Scenario | Year | Max bridge residual | CAR % | Min CAR % | Capital gap | Cash | CRR proxy | Reserve gap | Dividends |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 0.000 | 18.347 | 13.000 | 0.000 | 4074.032 | 1488.473 | 0.000 | 0.000 |
| base | FY2027E | 0.000 | 18.106 | 13.000 | 0.000 | 4393.059 | 1689.417 | 0.000 | 94.110 |
| base | FY2028E | 0.000 | 18.064 | 13.000 | 0.000 | 4784.675 | 1925.935 | 0.000 | 64.476 |
| base | FY2029E | 0.000 | 18.057 | 13.000 | 0.000 | 5211.935 | 2191.714 | 0.000 | 65.381 |
| base | FY2030E | 0.000 | 18.069 | 13.000 | 0.000 | 5685.441 | 2494.170 | 0.000 | 89.311 |
| downside | FY2026E | 0.000 | 17.538 | 13.000 | 0.000 | 3826.139 | 1416.912 | 0.000 | 0.000 |
| downside | FY2027E | 0.000 | 17.282 | 13.000 | 0.000 | 4016.429 | 1558.603 | 0.000 | 0.000 |
| downside | FY2028E | 0.000 | 16.520 | 13.000 | 0.000 | 4153.192 | 1714.463 | 0.000 | 0.000 |
| downside | FY2029E | 0.000 | 14.275 | 13.000 | 0.000 | 4097.377 | 1885.909 | 0.000 | 0.000 |
| downside | FY2030E | 0.000 | 10.650 | 13.000 | 285.416 | 3805.910 | 2065.071 | 0.000 | 0.000 |
| upside | FY2026E | 0.000 | 18.203 | 13.000 | 0.000 | 4221.436 | 1545.722 | 0.000 | 0.000 |
| upside | FY2027E | 0.000 | 18.691 | 13.000 | 0.000 | 4978.732 | 1839.409 | 0.000 | 0.000 |
| upside | FY2028E | 0.000 | 19.021 | 13.000 | 0.000 | 5897.197 | 2203.612 | 0.000 | 22.659 |
| upside | FY2029E | 0.000 | 19.092 | 13.000 | 0.000 | 6964.772 | 2644.334 | 0.000 | 119.375 |
| upside | FY2030E | 0.000 | 19.126 | 13.000 | 0.000 | 8269.330 | 3186.423 | 0.000 | 196.038 |

Accounting bridges: PASS (15/15). Capital below the shared minimum: 1/15 flagged. Cash-reserve proxy shortfalls: 0/15 flagged. Negative cash: 0/15 flagged.

### Effective cost of risk vs the scenario input

`cost_of_risk` in `assumptions.json` is the input; the allowance-build floor (max of the risk-based charge and the increase in the allowance stock) can lift the effective rate in fast-growth scenarios. Both are shown.

| Scenario | Year | Input cost of risk % | Effective charge / avg gross loans % | Impairment charge |
|---|---:|---:|---:|---:|
| base | FY2026E | 1.50 | 0.88 | 47.518 |
| base | FY2027E | 1.50 | 1.73 | 102.763 |
| base | FY2028E | 1.50 | 1.78 | 122.520 |
| base | FY2029E | 1.50 | 1.76 | 140.347 |
| base | FY2030E | 1.50 | 1.76 | 162.522 |
| downside | FY2026E | 3.50 | 2.79 | 148.971 |
| downside | FY2027E | 3.50 | 3.50 | 195.983 |
| downside | FY2028E | 3.50 | 3.50 | 213.622 |
| downside | FY2029E | 3.50 | 3.50 | 232.848 |
| downside | FY2030E | 3.50 | 3.50 | 253.197 |
| upside | FY2026E | 0.80 | 0.70 | 38.136 |
| upside | FY2027E | 0.80 | 1.91 | 118.466 |
| upside | FY2028E | 0.80 | 1.98 | 147.846 |
| upside | FY2029E | 0.80 | 2.00 | 180.315 |
| upside | FY2030E | 0.80 | 2.04 | 223.376 |

### Downside decomposition (cost pass-through vs credit)

The downside presents a combined stress. To separate the two drivers, the table below shows, for FY2030E, the base and downside operating costs and impairment. Opex growth is CPI plus 8 points in the downside (higher than base), so part of the downside loss is cost pass-through driven mechanically by the shared macro downside inflation path, not by credit losses. A reader should treat the downside CAR path as a combined cost-and-credit stress, not a credit-only stress.

| Scenario | Year | Total operating income | Operating costs | Impairment | Profit before tax | Tax | PAT |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | FY2030E | 1947.594 | 1123.271 | 162.522 | 661.802 | 231.631 | 430.171 |
| downside | FY2030E | 1346.608 | 1437.026 | 253.197 | -343.615 | 0.000 | -343.615 |
| upside | FY2030E | 2515.664 | 1016.746 | 223.376 | 1275.541 | 446.439 | 829.102 |

**Counterfactual: downside with base cost growth — a one-year marginal diagnostic.** The table above keeps the downside's CPI-plus-8pt opex rule. Below, downside FY2030E operating costs are recomputed by applying the **base** opex growth spread to the downside FY2029 opening cost lines, holding the downside operating income and impairment charge fixed. This is a single-year marginal diagnostic, not a full five-year base-cost path: the FY2029 opening costs already embed four years of cumulative downside opex, so it isolates only the FY2030 growth-rate substitution and cannot by itself attribute the whole remaining loss to credit and rates.

| FY2030E variant | Operating costs | Profit before tax | Tax | PAT |
|---|---:|---:|---:|---:|
| Downside as modelled (CPI+8) | 1437.026 | -343.615 | 0.000 | -343.615 |
| Downside with base cost growth (CPI+4) | 1369.761 | -276.350 | 0.000 | -276.350 |

The FY2030E gap between the two rows is the FY2030 growth-rate substitution only: with base cost growth the downside FY2030E loss changes to -276.350 from -343.615, about 20% of the modelled downside FY2030E loss magnitude. Because the FY2029 opening costs already embed cumulative downside opex, this is one year of cost pass-through, not the whole five-year effect; the residual is credit, rates and earlier-years' cumulative cost.

### Tax treatment in the anchor year

FY2026E retains the actual 9M-2026 tax charge and adds tax on any positive estimated Q4 profit before tax. No deferred-tax credit is recognised for a Q4 loss, so if the downside Q4 is a loss the annual effective rate exceeds the 35% input; this is the model's stated treatment, not an error. Dividends: the observed 9M-2026 equity already reflects the FY2025 final dividend of GHS173.669m paid in 2026 (SG26Q3), so no additional Q4-2026 dividend is assumed.

FY2026 estimated earnings retain actual 9M income and estimate Q4 only. The Bank does not disclose a net FX position in the summary statements used, so no incremental FX translation P&L is modelled. Full prudential risk weights, OCI, capital deductions and liquidity eligibility are not available, so this is a simplified scenario analysis. Independent review required.
