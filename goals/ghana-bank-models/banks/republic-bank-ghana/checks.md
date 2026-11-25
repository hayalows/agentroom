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

- Historical rows: 480; duplicate bank/period/statement/key rows: 0; reported rows missing source/page: 0; unavailable rows with non-blank value: 0.
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

Rows: 1020; scenario-years: 15; FY2025 residual RWA density: 0.136864; estimated 9M-2026 RWA: 5302.739; initial proxy regulatory capital: 945.478 (anchored to the observed 17.83% CAR).

| Scenario | Year | Max bridge residual | CAR % | Min CAR % | Capital gap | Cash | CRR proxy | Reserve gap | Dividends |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 0.000 | 17.179 | 13.000 | 0.000 | 3561.977 | 1502.183 | 0.000 | 0.000 |
| base | FY2027E | 0.000 | 16.938 | 13.000 | 0.000 | 4039.058 | 1719.999 | 0.000 | 0.000 |
| base | FY2028E | 0.000 | 16.697 | 13.000 | 0.000 | 4600.804 | 1977.999 | 0.000 | 0.000 |
| base | FY2029E | 0.000 | 16.464 | 13.000 | 0.000 | 5226.914 | 2270.743 | 0.000 | 0.000 |
| base | FY2030E | 0.000 | 16.330 | 13.000 | 0.000 | 5950.137 | 2606.813 | 0.000 | 0.000 |
| downside | FY2026E | 0.000 | 15.520 | 13.000 | 0.000 | 3156.662 | 1415.518 | 0.000 | 0.000 |
| downside | FY2027E | 0.000 | 16.255 | 13.000 | 0.000 | 3343.927 | 1542.915 | 0.000 | 0.000 |
| downside | FY2028E | 0.000 | 16.809 | 13.000 | 0.000 | 3526.776 | 1681.777 | 0.000 | 0.000 |
| downside | FY2029E | 0.000 | 16.387 | 13.000 | 0.000 | 3654.483 | 1833.137 | 0.000 | 0.000 |
| downside | FY2030E | 0.000 | 15.195 | 13.000 | 0.000 | 3690.636 | 1988.954 | 0.000 | 0.000 |
| upside | FY2026E | 0.000 | 17.395 | 13.000 | 0.000 | 4196.947 | 1617.735 | 0.000 | 0.000 |
| upside | FY2027E | 0.000 | 16.725 | 13.000 | 0.000 | 5279.619 | 1941.282 | 0.000 | 0.000 |
| upside | FY2028E | 0.000 | 16.211 | 13.000 | 0.000 | 6638.452 | 2345.069 | 0.000 | 0.000 |
| upside | FY2029E | 0.000 | 16.006 | 13.000 | 0.000 | 8332.100 | 2837.534 | 0.000 | 0.000 |
| upside | FY2030E | 0.000 | 15.991 | 13.000 | 0.000 | 10471.964 | 3447.604 | 0.000 | 0.000 |

Accounting bridges: PASS (15/15). Capital below the shared minimum: 0/15 flagged. Cash-reserve proxy shortfalls: 0/15 flagged. Negative cash: 0/15 flagged.

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

The downside presents a combined stress. To separate the two drivers, the table below shows, for FY2030E, the base and downside operating costs and impairment. Downside opex growth is the shared downside CPI plus a 5-point spread, versus the base's shared base CPI plus a 4-point spread, so part of the downside outcome is cost pass-through driven mechanically by the shared macro downside inflation path, not by credit losses.

| Scenario | Year | Total operating income | Operating costs | Impairment | Profit before tax | Tax | PAT |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | FY2030E | 1291.441 | 837.943 | 117.723 | 335.775 | 117.521 | 218.254 |
| downside | FY2030E | 1096.939 | 967.281 | 152.463 | -22.805 | 0.000 | -22.805 |
| upside | FY2030E | 1434.496 | 758.477 | 114.412 | 561.607 | 196.562 | 365.044 |

**Counterfactual: downside with base cost growth — a one-year marginal diagnostic.** Below, downside FY2030E operating costs are recomputed by applying the **BASE** opex growth (shared base CPI plus the 4-point base spread) to the downside FY2029 opening cost lines, holding the downside operating income and impairment charge fixed. Note this changes BOTH the inflation path (downside CPI -> base CPI) and the spread (downside -> base); it is not the same downside CPI with an alternative spread. This is a single-year diagnostic: the FY2029 opening costs already embed four years of cumulative downside opex, so it isolates only the FY2030 growth-rate substitution.

| FY2030E variant | Operating costs | Profit before tax | Tax | PAT |
|---|---:|---:|---:|---:|
| Downside as modelled (CPI+5) | 967.281 | -22.805 | 0.000 | -22.805 |
| Downside with base cost growth (CPI+4) | 946.162 | -1.685 | 0.000 | -1.685 |

With base cost growth the downside FY2030E profit before tax changes to -1.685 from -22.805, about 93% of the modelled downside FY2030E profit-before-tax magnitude. Because the FY2029 opening costs already embed cumulative downside opex, this is one year of cost pass-through, not the whole five-year effect.

### Statutory reserve fund (Act 930 s34), tracked separately

Act 930 section 34 printed p30 sets three bands based on opening reserve / paid-up capital: below 50%: 50%; 50% to below 100%: 25%; at least 100%: 12.5%. FY2025 closing statutory fund 368.101m / stated capital 401.191m implies 25%. The issuer Q3 Bank statement of changes in equity (p1) confirms the fund remained 368.101m and YTD statutory transfer was zero. FY2026 therefore uses positive full-year PAT less zero YTD transfer; later periods use opening fund and positive annual PAT. Central policy applies at least the statutory band and a 25% floor, and the statutory-only minimum is a sensitivity. Actual FY2026 final transfer is not yet published. Internal equity transfer, no effect on total equity or capital before dividends.

| Year | Statutory fund | Stated capital | Fund/capital % | s34 band % | Band transfer (sensitivity) | Central policy transfer |
|---|---:|---:|---:|---:|---:|---:|
| base FY2026E | 400.877 | 401.191 | 99.9 | 25.0 | 32.776 | 32.776 |
| base FY2027E | 434.755 | 401.191 | 108.4 | 25.0 | 33.878 | 33.878 |
| base FY2028E | 474.763 | 401.191 | 118.3 | 12.5 | 20.004 | 40.009 |
| base FY2029E | 520.196 | 401.191 | 129.7 | 12.5 | 22.716 | 45.432 |
| base FY2030E | 574.759 | 401.191 | 143.3 | 12.5 | 27.282 | 54.563 |
| downside FY2026E | 368.101 | 401.191 | 91.8 | 25.0 | 0.000 | 0.000 |
| downside FY2027E | 390.847 | 401.191 | 97.4 | 25.0 | 22.746 | 22.746 |
| downside FY2028E | 412.957 | 401.191 | 102.9 | 25.0 | 22.110 | 22.110 |
| downside FY2029E | 421.345 | 401.191 | 105.0 | 12.5 | 4.194 | 8.388 |
| downside FY2030E | 421.345 | 401.191 | 105.0 | 12.5 | 0.000 | 0.000 |
| upside FY2026E | 415.376 | 401.191 | 103.5 | 25.0 | 47.275 | 47.275 |
| upside FY2027E | 455.465 | 401.191 | 113.5 | 12.5 | 20.044 | 40.089 |
| upside FY2028E | 507.074 | 401.191 | 126.4 | 12.5 | 25.805 | 51.610 |
| upside FY2029E | 576.268 | 401.191 | 143.6 | 12.5 | 34.597 | 69.194 |
| upside FY2030E | 667.529 | 401.191 | 166.4 | 12.5 | 45.631 | 91.261 |

### FY2025 interest back-test (note-8 split vs the earning-base formula)

The FY2025 note-8 IMPLIED yields and note-9 implied costs are the calibration anchor: each is the reported bank line divided by the FY2025 AVERAGE earning balance, so applying it back to the same balances reproduces the reported split exactly by construction (residual 0.000). That is an accounting identity, disclosed as such, not an out-of-sample test. The forecast applies the SAME earning/funding base and starts each yield at its FY2025 implied level, then reprises only PARTIALLY (a proportional beta below 1) toward the falling shared macro rates, because the loan book is fixed/slow-repricing and the amortised-cost securities book is largely held to maturity.

| Component | FY2025 implied yield/cost (%) | Reported (note 8/9) | Model at implied level | Residual |
|---|---:|---:|---:|---:|
| Interest income on loans (gross) | 14.579 | 506.986 | 506.986 | 0.000 |
| Interest income on amortised-cost investment securities | 17.136 | 335.338 | 335.338 | 0.000 |
| Interest income on cash and cash equivalents | 9.706 | 404.318 | 404.318 | -0.000 |
| Total interest income | | 1246.642 | 1246.642 | 0.000 |

FY2025 implied yields: loans 14.58%, amortised-cost securities 17.14%, cash 9.71%; implied costs: customer deposits 3.14%, wholesale funding 15.56%. Pass-through betas (fraction of the macro move carried into the year): loans 0.60, securities 0.50, cash 0.50, deposits 0.50, wholesale 0.60. These betas are policy judgements, not reported figures.

The reported securities+cash subtotal ties to the FY2025 note-8 split; the amortised-cost investment income INCLUDES pledged assets (which are amortised-cost financial assets), and FVTPL securities are EXCLUDED (their return sits in the net FVTPL line). The earning cash base excludes the CRR-proxy reserve (non-earning).

### Source inconsistencies and reference data

- **Note 9 printed NII subtotal.** RB25AR printed p107 shows a note-9 `Net Interest Income` subtotal of 693.096m (bank), which disagrees with the face NII of 708.510m (p76). The note-9 COMPONENTS tie to the face: interest income 1,246.642m and interest expense 538.132m give 708.510m. The model keeps the FACE 708.510m and discloses the printed note subtotal inconsistency here rather than matching it mechanically.
- **Foreign-currency exposure (RB25AR printed p180) and sensitivity (p182).** FY2025 bank net on-balance-sheet exposure: EUR -1.262m, USD -14.593m, GBP -1.555m (FY2024 comparatives +0.166m/+16.388m/+1.392m). A 10% move gives a P&L impact of -0.126m/-1.437m/-0.156m (total -1.719m if jointly applied) and an equity impact of -0.082m/-0.934m/-0.101m (total -1.117m); FY2024 comparatives +15/+1,640/+140 (P&L) and +10/+1,066/+91 (equity) in GHS thousands. The model retains the central NO-FX-REVALUATION assumption (the balance sheet is not revalued by currency) and adds this as a bounded reference sensitivity only: on the FY2025 net position a 10% cedi move is about -1.719m P&L and -1.117m equity, immaterial against model PAT.
- **2026 ICAAP CAR comparison (RB25AR printed p190).** The Bank's own 2026 ICAAP forecasts CAR 18.11% (regulatory capital 1,049.935m, RWA 5,798.105m). The model's FY2026E base CAR proxy is 17.179% (93 bps lower). This is NOT an error and is not matched mechanically: the ICAAP is a forward regulatory-capital forecast at a different date using the Bank's own PD/LGD risk weights and Pillar-2 add-ons, whereas the model proxy uses a single FY2025 residual RWA-density calibration and anchors interim capital on the reported 17.83% Q3 CAR. The two differ by methodology and reporting date, not by an arithmetic mistake.

### Tax treatment and dividends in the anchor year

FY2026E retains the actual 9M-2026 tax charge and adds tax on any positive estimated Q4 profit before tax. No deferred-tax credit is recognised for a Q4 loss, so if the downside Q4 is a loss the annual effective rate exceeds the 35% input; this is the model's stated treatment, not an error. The observed 9M-2026 equity already reflects the GHS42.598m dividend paid in 2026 (RB26Q3), so no additional Q4-2026 dividend is assumed and `x_model_dividends` is zero in FY2026E for every scenario. The statutory reserve transfer is modelled at a conservative minimum of 25% of positive annual PAT or the applicable Act 930 band, less actual YTD transfer, with the statutory-only band as a sensitivity; it is an internal equity transfer, so total equity and regulatory capital are unaffected, but it caps distributable retained earnings for dividends. See the statutory-reserve section above.

FY2026 estimated earnings retain actual 9M income and estimate Q4 only. The Bank reports a net on-balance-sheet FX position (RB25AR p180) but the model keeps a central NO-FX-REVALUATION assumption; the reported FY2025 exposure and a bounded 10% sensitivity are shown above. Full prudential risk weights, OCI, capital deductions and liquidity eligibility are not available, so the capital and reserve checks are simplified screening proxies. Independent review required.

### Additional collateral and wholesale repricing diagnostic

Illustrative static stress, not a full model rerun: 20% of pledged securities is an incremental collateral haircut (not a loss or free cash); +100bp on average borrowings, bank funding and bonds is gross annual pre-tax expense before behavioral or capital feedback. The original pledged assets are already restricted. FY2026 applies one quarter of the annual funding shock, preserving reported nine months.

| Scenario | Year | 20% pledged haircut (GHS m) | Incremental wholesale interest (GHS m) |
|---|---|---:|---:|
| base | FY2026E | 574.303 | 7.255 |
| base | FY2027E | 640.348 | 31.734 |
| base | FY2028E | 717.190 | 36.420 |
| base | FY2029E | 803.253 | 41.844 |
| base | FY2030E | 899.643 | 48.037 |
| downside | FY2026E | 577.105 | 7.042 |
| downside | FY2027E | 669.442 | 29.136 |
| downside | FY2028E | 773.205 | 31.759 |
| downside | FY2029E | 889.186 | 34.617 |
| downside | FY2030E | 1018.118 | 37.642 |
| upside | FY2026E | 570.802 | 7.539 |
| upside | FY2027E | 616.466 | 35.051 |
| upside | FY2028E | 671.948 | 42.214 |
| upside | FY2029E | 735.783 | 51.041 |
| upside | FY2030E | 809.361 | 61.900 |
