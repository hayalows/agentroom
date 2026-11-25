# GCB historical validation (provisional; forecast not yet built)

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

- 263 rows; duplicate bank/period/statement/key rows: 0; reported rows missing source/page: 0; unavailable rows with nonblank value: 0.
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

## Not yet tested

Five-year forecast, forecast CAR versus regulatory threshold, shared macro consistency, complete regulatory history, tax/FX note verification, and independent peer review. Claim remains in progress.
