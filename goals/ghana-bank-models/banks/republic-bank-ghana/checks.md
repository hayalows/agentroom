# Republic Bank (Ghana) PLC checks

Recomputed from the committed `financials.csv` and `forecast.csv` by `model.py` (history) and the shared macro file (forecast). GHS millions; ratios in percent; tolerance 0.003. NA = input unavailable, not zero. `model.py` writes this whole file. Bank-only series.

## Historical balance and income bridges

| Period | Assets-L-E | Asset components | NII | Operating income | PAT | Net loans |
|---|---:|---:|---:|---:|---:|---:|
| FY2021 | -0.000 | 0.000 | -0.000 | 0.000 | -0.000 | 0.000 |
| FY2022 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | -0.000 |
| FY2023 | -0.000 | -0.000 | 0.000 | 0.000 | -0.000 | 0.000 |
| FY2024 | -0.000 | -0.000 | -0.000 | 0.000 | -0.000 | 0.000 |
| FY2025 | 0.000 | 0.000 | -0.000 | 0.000 | -0.000 | 0.000 |
| 9M-2025 | -0.000 | 0.000 | 0.000 | -0.000 | -0.000 | NA |
| 9M-2026 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | NA |

`due_from_banks` is unavailable (blank) for every period (the Bank reports no separate asset-side interbank line); it is treated as zero only inside the component bridge, so the bridge closes against the reported total. `loans_and_advances_net` for 9M-2025 / 9M-2026 is reported but its gross and allowance are unavailable, so the net-loan bridge is NA there.

## Source and schema checks

- Historical rows: 373; duplicate bank/period/statement/key rows: 0; reported rows missing source/page: 0; unavailable rows with non-blank value: 0.
- Spot-checks against printed filing pages (visually verified): RB25AR printed p.77 total assets 12,265,013 thousand -> 12265.013 m and total equity 1,234,220 thousand -> 1234.220 m; RB25AR printed p.76 bank profit before tax 392,850 thousand -> 392.850 m; RB24AR printed p.67 total assets 9,544,596 thousand -> 9544.596 m; RB26Q3 bank total assets 11,631,887 thousand -> 11631.887 m; RB21FS printed p.48 total assets 4,226,259 thousand -> 4226.259 m. All match.
- NOTE: the Bank-only PBT for FY2025 is 392.850m (RB25AR printed p.76). The figure 440.292m sometimes quoted is the GROUP column of the same statement and the GROUP 5-year highlight; it is never used in this bank series.

## Ratios: reported vs recomputed (%)

| Period | Reported CAR | Reported Tier 1 | Reported NPL | Derived LDR | Derived cost/income | Derived ROE | Derived ROA |
|---|---:|---:|---:|---:|---:|---:|---:|
| FY2021 | 27.63 | 25.63 | 15.32 | 59.79 | 61.79 | 11.84 | 1.93 |
| FY2022 | 21.25 | 18.25 | 19.85 | 52.43 | 57.14 | -10.10 | -1.32 |
| FY2023 | 19.24 | 16.24 | 15.95 | 44.98 | 56.03 | 16.47 | 1.88 |
| FY2024 | 18.20 | 15.65 | 15.64 | 53.38 | 57.47 | 19.16 | 1.97 |
| FY2025 | 20.15 | 18.15 | 14.15 | 44.10 | 55.33 | 20.63 | 2.08 |
| 9M-2025 | 16.75 | NA | 16.49 | NA | 56.47 | 15.28 | 1.81 |
| 9M-2026 | 17.83 | NA | 11.60 | NA | 66.93 | 9.06 | 1.02 |

Reported CAR is the audited capital-management note; from FY2022 to FY2024 it is stated on the Bank of Ghana DDEP-relief basis (minimum held at 10%), and FY2025 is stated after the reliefs were withdrawn in December 2025. Reported Tier 1 is the Tier 1/RWA ratio (the Bank discloses Tier 1, predominantly CET1, rather than a separate CET1 ratio). ROE/ROA here use year-end equity/assets as a single-period ratio. LDR and cost/income are NA where the interim summary omits gross loans.

### Loan loss and impairment cross-check

| Period | Gross loans | ECL allowance | Allowance/gross % | Loan LL provision ratio (reported) | NPL ratio (reported) |
|---|---:|---:|---:|---:|---:|
| FY2021 | 1892.39 | 144.39 | 7.63 | 7.63 | 15.32 |
| FY2022 | 2144.58 | 186.56 | 8.70 | NA | 19.85 |
| FY2023 | 2639.49 | 209.74 | 7.95 | NA | 15.95 |
| FY2024 | 3264.38 | 210.33 | 6.44 | 6.44 | 15.64 |
| FY2025 | 3690.49 | 232.83 | 6.31 | 6.31 | 14.15 |
| 9M-2025 | NA | NA | NA | NA | 16.49 |
| 9M-2026 | NA | NA | NA | NA | 11.60 |

The implied allowance/gross ratio equals the Bank's reported loan loss provision ratio where both are available (FY2025 6.31%, FY2024 6.44%), confirming the net-loan bridge.

<!-- FORECAST CHECKS GENERATED -->
## Forecast checks (generated from shared macro scenarios)

All forecast rows are estimated. Currency GHS millions; ratios in percent. Accounting arithmetic is checked before rounding. Cash-reserve and CAR checks are screening proxies, not regulatory returns. A negative cash residual or a positive gap is a flagged financing requirement, not an assumed funding source.

Rows: 915; scenario-years: 15; FY2025 residual RWA density: 0.136864; estimated 9M-2026 RWA: 5302.739; initial proxy regulatory capital: 945.478 (anchored to the observed 17.83% CAR).

| Scenario | Year | Max bridge residual | CAR % | Min CAR % | Capital gap | Cash | CRR proxy | Reserve gap | Dividends |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 0.000 | 17.179 | 13.000 | 0.000 | 3561.977 | 1502.183 | 0.000 | 0.000 |
| base | FY2027E | 0.000 | 17.009 | 13.000 | 0.000 | 4043.743 | 1719.999 | 0.000 | 25.987 |
| base | FY2028E | 0.000 | 17.006 | 13.000 | 0.000 | 4624.535 | 1977.999 | 0.000 | 20.000 |
| base | FY2029E | 0.000 | 17.008 | 13.000 | 0.000 | 5275.466 | 2270.743 | 0.000 | 31.549 |
| base | FY2030E | 0.000 | 17.013 | 13.000 | 0.000 | 6020.952 | 2606.813 | 0.000 | 55.985 |
| downside | FY2026E | 0.000 | 15.520 | 13.000 | 0.000 | 3156.662 | 1415.518 | 0.000 | 0.000 |
| downside | FY2027E | 0.000 | 14.831 | 13.000 | 0.000 | 3262.917 | 1542.915 | 0.000 | 0.000 |
| downside | FY2028E | 0.000 | 13.030 | 13.000 | 0.000 | 3299.146 | 1681.777 | 0.000 | 0.000 |
| downside | FY2029E | 0.000 | 9.246 | 13.000 | 233.154 | 3200.765 | 1833.137 | 0.000 | 0.000 |
| downside | FY2030E | 0.000 | 3.831 | 13.000 | 597.127 | 2934.878 | 1988.954 | 0.000 | 0.000 |
| upside | FY2026E | 0.000 | 17.395 | 13.000 | 0.000 | 4196.947 | 1617.735 | 0.000 | 0.000 |
| upside | FY2027E | 0.000 | 18.018 | 13.000 | 0.000 | 5372.843 | 1941.282 | 0.000 | 51.786 |
| upside | FY2028E | 0.000 | 18.036 | 13.000 | 0.000 | 6798.045 | 2345.069 | 0.000 | 126.212 |
| upside | FY2029E | 0.000 | 18.047 | 13.000 | 0.000 | 8549.073 | 2837.534 | 0.000 | 198.858 |
| upside | FY2030E | 0.000 | 18.088 | 13.000 | 0.000 | 10744.114 | 3447.604 | 0.000 | 280.148 |

Accounting bridges: PASS (15/15). Capital below the shared minimum: 2/15 flagged. Cash-reserve proxy shortfalls: 0/15 flagged. Negative cash: 0/15 flagged.

### Effective cost of risk vs the scenario input

`cost_of_risk` in `assumptions.json` is the input; the allowance-build floor (max of the risk-based charge and the increase in the allowance stock) can lift the effective rate in fast-growth scenarios. Both are shown.

| Scenario | Year | Input cost of risk % | Effective charge / avg gross loans % | Impairment charge |
|---|---:|---:|---:|---:|
| base | FY2026E | 1.50 | 1.61 | 71.096 |
| base | FY2027E | 1.50 | 1.50 | 73.843 |
| base | FY2028E | 1.50 | 1.50 | 86.225 |
| base | FY2029E | 1.50 | 1.50 | 100.791 |
| base | FY2030E | 1.50 | 1.50 | 117.723 |
| downside | FY2026E | 3.00 | 3.24 | 139.175 |
| downside | FY2027E | 3.00 | 3.00 | 132.025 |
| downside | FY2028E | 3.00 | 3.00 | 138.626 |
| downside | FY2029E | 3.00 | 3.00 | 145.558 |
| downside | FY2030E | 3.00 | 3.00 | 152.463 |
| upside | FY2026E | 0.80 | 0.79 | 35.571 |
| upside | FY2027E | 0.80 | 1.14 | 59.390 |
| upside | FY2028E | 0.80 | 1.18 | 74.600 |
| upside | FY2029E | 0.80 | 1.19 | 91.697 |
| upside | FY2030E | 0.80 | 1.21 | 114.412 |

### Downside decomposition (cost pass-through vs credit)

The downside presents a combined stress. To separate the two drivers, the table below shows, for FY2030E, the base and downside operating costs and impairment. Opex growth is CPI plus 8 points in the downside (higher than base), so part of the downside outcome is cost pass-through driven mechanically by the shared macro downside inflation path, not by credit losses.

| Scenario | Year | Total operating income | Operating costs | Impairment | Profit before tax | Tax | PAT |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | FY2030E | 1411.821 | 837.943 | 117.723 | 456.155 | 159.654 | 296.501 |
| downside | FY2030E | 794.900 | 967.281 | 152.463 | -324.845 | 0.000 | -324.845 |
| upside | FY2030E | 1950.381 | 758.477 | 114.412 | 1077.492 | 377.122 | 700.370 |

**Counterfactual: downside with base cost growth — a one-year marginal diagnostic.** Below, downside FY2030E operating costs are recomputed by applying the **base** opex growth spread to the downside FY2029 opening cost lines, holding the downside operating income and impairment charge fixed. This is a single-year diagnostic: the FY2029 opening costs already embed four years of cumulative downside opex, so it isolates only the FY2030 growth-rate substitution.

| FY2030E variant | Operating costs | Profit before tax | Tax | PAT |
|---|---:|---:|---:|---:|
| Downside as modelled (CPI+5) | 967.281 | -324.845 | 0.000 | -324.845 |
| Downside with base cost growth (CPI+4) | 946.162 | -303.725 | 0.000 | -303.725 |

With base cost growth the downside FY2030E profit before tax changes to -303.725 from -324.845, about 7% of the modelled downside FY2030E profit-before-tax magnitude. Because the FY2029 opening costs already embed cumulative downside opex, this is one year of cost pass-through, not the whole five-year effect.

### Tax treatment and dividends in the anchor year

FY2026E retains the actual 9M-2026 tax charge and adds tax on any positive estimated Q4 profit before tax. No deferred-tax credit is recognised for a Q4 loss, so if the downside Q4 is a loss the annual effective rate exceeds the 35% input; this is the model's stated treatment, not an error. The observed 9M-2026 equity already reflects the GHS42.598m dividend paid in 2026 (RB26Q3), so no additional Q4-2026 dividend is assumed and `x_model_dividends` is zero in FY2026E for every scenario. The statutory reserve transfer is modelled at 25% of positive PAT (source-confirmed FY2024 46.926m / FY2025 63.648m); it is an internal equity transfer, so total equity and regulatory capital are unaffected, but it caps distributable retained earnings for dividends.

FY2026 estimated earnings retain actual 9M income and estimate Q4 only. The Bank does not disclose a net FX position in the summary statements used, so no incremental FX translation P&L is modelled. Full prudential risk weights, OCI, capital deductions and liquidity eligibility are not available, so the capital and reserve checks are simplified screening proxies. Independent review required.
