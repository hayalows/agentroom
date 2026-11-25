# GCB historical validation

Date: 2026-11-25. Recomputed from the committed financials.csv, not from a separate hand-entered table. All amounts below are in GHS millions; rounding tolerance 0.003. Residual = reported total minus recomputed total. NA = input unavailable, not zero.

| Period | Assets-L-E | Asset components | Liability components | Equity components | NII | Operating income | PBT | PAT | Net loans |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FY2021 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2022 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2023 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2024 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2025 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 9M-2026 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | NA |

Historical balance and income bridges: PASS, all available residuals zero. Loan reconciliation: PASS for five audited years; unavailable for 9M-2026. FY2021 and FY2022 subtract separately reported interest in suspense; FY2024 PBT subtracts GHS 297.212m investment derecognition loss separately. No invented interim gross loans or allowances.

## Source and schema checks

- 278 rows; duplicate bank/period/statement/key rows: 0; reported rows missing source/page: 0; unavailable rows with nonblank value: 0.
- Spot-check against GCB24 separate-bank FY2024 page 1 (visually inspected): total assets GHS 42,584.343m; net interest income GHS 3,375.422m; PAT GHS 1,209.164m. All three match historical CSV. Additional visual verification of other filings pending where screenshot access failed.

## Ratios (%)

| Period | Reported CAR | Reported NPL | Derived gross LDR | Derived cost/income | Derived ROE | Derived ROA |
|---|---:|---:|---:|---:|---:|---:|
| FY2021 | 20.90 | 15.98 | 39.52 | 52.56 | NA | NA |
| FY2022 | 17.86 | 20.59 | 38.31 | 53.48 | -25.30 | -2.81 |
| FY2023 | 19.20 | 20.20 | 36.80 | 47.64 | 42.78 | 4.12 |
| FY2024 | 17.47 | 15.06 | 35.03 | 46.37 | 35.29 | 3.48 |
| FY2025 | 18.02 | 10.31 | 43.43 | 46.87 | 40.63 | 4.30 |
| 9M-2026 | 14.60 | 4.80 | NA | 45.10 | 36.43 | 4.14 |

Derived ROA/ROE use mean opening and closing assets/equity; 9M-2026 income annualised, not a full-year result. Cost/income excludes impairments and investment derecognition. Comparison to separately disclosed ROA/ROE/cost-income/loan-deposit ratios remains open; do not treat arithmetic proxies as bank-reported figures. CET1 is not silently substituted for Tier 1. FY2025 regulatory CAR from annual-report capital/RWA = 18.02%, vs summary 18.02%. FY2024 = 17.47%, vs summary 17.47%. Differences within 0.01 percentage points.

## Remaining historical limitations

Complete regulatory history, source-image verification of some filings and comparison to separately reported profitability ratios remain open. Annual-report tax/FX/DDEP notes are now included in financials.csv; note-level evidence is in sources.md. Peer review required.

<!-- FORECAST CHECKS GENERATED -->
## Forecast checks (generated from shared macro scenarios)

All forecast rows estimated. Currency GHS millions; ratios percentages. Accounting arithmetic checked before rounding. Cash reserve and CAR checks are screening proxies, not regulatory returns. A negative cash residual or positive gap is a flagged financing requirement; not an assumed funding source.

Rows: 840; scenario-years: 15; FY2025 residual RWA density: 0.268437; estimated September 2026 RWA: 38666.896; initial proxy regulatory capital: 5645.367 (anchored to observed 14.6% CAR).

| Scenario | Year | Max bridge residual | CAR % | Min CAR % | Capital gap | Cash | CRR proxy | Reserve gap | Paid capital vs min | Allowance other movement |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| base | FY2026E | 0.000 | 15.519 | 13.000 | 0.000 | 16540.326 | 10585.027 | 0.000 | 500.000 / 400.000 | 875.285 |
| base | FY2027E | 0.000 | 19.308 | 13.000 | 0.000 | 20275.823 | 12194.536 | 0.000 | 500.000 / 400.000 | 55.762 |
| base | FY2028E | 0.000 | 22.348 | 13.000 | 0.000 | 24520.230 | 14098.398 | 0.000 | 500.000 / 400.000 | 57.713 |
| base | FY2029E | 0.000 | 24.864 | 13.000 | 0.000 | 29238.269 | 16252.173 | 0.000 | 500.000 / 400.000 | 77.945 |
| base | FY2030E | 0.000 | 27.032 | 13.000 | 0.000 | 34619.818 | 18724.708 | 0.000 | 500.000 / 400.000 | 94.256 |
| downside | FY2026E | 0.000 | 14.377 | 13.000 | 0.000 | 14798.911 | 9879.358 | 0.000 | 500.000 / 400.000 | 0.000 |
| downside | FY2027E | 0.000 | 17.054 | 13.000 | 0.000 | 17364.816 | 11115.449 | 0.000 | 500.000 / 400.000 | 650.005 |
| downside | FY2028E | 0.000 | 18.997 | 13.000 | 0.000 | 19950.154 | 12472.574 | 0.000 | 500.000 / 400.000 | 741.302 |
| downside | FY2029E | 0.000 | 19.588 | 13.000 | 0.000 | 22110.232 | 13964.047 | 0.000 | 500.000 / 400.000 | 839.695 |
| downside | FY2030E | 0.000 | 19.297 | 13.000 | 0.000 | 23775.602 | 15534.825 | 0.000 | 500.000 / 400.000 | 966.343 |
| upside | FY2026E | 0.000 | 15.671 | 13.000 | 0.000 | 17148.986 | 10988.266 | 0.000 | 500.000 / 400.000 | 1385.038 |
| upside | FY2027E | 0.000 | 19.697 | 13.000 | 0.000 | 21855.549 | 13010.962 | 0.000 | 500.000 / 400.000 | 0.000 |
| upside | FY2028E | 0.000 | 22.926 | 13.000 | 0.000 | 27443.407 | 15494.363 | 0.000 | 500.000 / 400.000 | 0.000 |
| upside | FY2029E | 0.000 | 25.742 | 13.000 | 0.000 | 34162.726 | 18475.633 | 0.000 | 500.000 / 400.000 | 0.000 |
| upside | FY2030E | 0.000 | 28.133 | 13.000 | 0.000 | 42297.351 | 22115.722 | 0.000 | 500.000 / 400.000 | 0.000 |

Accounting bridges: PASS (15/15). Capital below shared minimum: 0/15 flagged. Cash reserve proxy shortfalls: 0/15 flagged. Negative cash: 0/15 flagged. Paid capital below shared minimum: 0/15. Negative allowance-other movement: 0/15; this is an unexplained allowance bridge component, not a reported recovery.
FY2026 estimated earnings retain actual 9M income and estimate Q4 only. FY2026 tax does not override reported 9M. FX translation separately estimated from FY2027; EUR/GBP and actual interim USD balances unavailable. Full prudential risk weights, OCI, capital deductions and liquidity eligibility are not available, so model is a simplified scenario analysis. Current paid-up capital threshold verification and non-GCB reported ratio comparisons remain open. Independent review required.

