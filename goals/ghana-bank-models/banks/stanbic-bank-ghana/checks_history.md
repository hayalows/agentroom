# Stanbic Bank Ghana Ltd historical checks

Recomputed from the committed `financials.csv`. GHS millions; ratios in percent; tolerance 0.003. NA = input unavailable, not zero.

## Balance and income bridges

| Period | Assets-L-E | Asset components | Liab components | Equity components | NII | Operating income | PAT | Net loans |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| FY2021 | -0.000 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | -0.000 | 0.000 |
| FY2022 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | 0.000 | 0.000 | -0.000 |
| FY2023 | -0.000 | 0.000 | 0.000 | 0.000 | -0.000 | -0.000 | -0.000 | 0.000 |
| FY2024 | -0.000 | -0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| FY2025 | -0.000 | -0.000 | -0.000 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 |
| 9M-2025 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | NA |
| 9M-2026 | -0.000 | -0.000 | 0.000 | 0.000 | 0.000 | -0.000 | 0.000 | NA |

## Source and schema checks

- Historical rows: 367; duplicate keys: 0; reported rows missing source/page: 0; unavailable rows with a value: 0.
- Spot-checks against the audited pages: FY2025 total assets 36,708,145k = 36708.145; FY2025 PAT 1,608,667k = 1608.667; FY2024 total assets 32,590,921k = 32590.921; 9M-2026 total assets 43,243,634k = 43243.634.

## Reported vs derived ratios (%)

| Period | Reported CAR | Reported CET1 | Reported NPL | Derived LDR | Derived cost/income | Derived ROE | Derived ROA |
|---|---:|---:|---:|---:|---:|---:|---:|
| FY2021 | 19.20 | 17.20 | 6.70 | 54.23 | 47.68 | 20.75 | 2.89 |
| FY2022 | 12.30 | 12.30 | 8.96 | 48.08 | 46.77 | -3.67 | -0.34 |
| FY2023 | 19.60 | 16.60 | 16.24 | 36.34 | 38.02 | 43.01 | 5.20 |
| FY2024 | 19.00 | 16.00 | 17.08 | 40.52 | 41.42 | 28.15 | 3.57 |
| FY2025 | 23.20 | 21.20 | 24.63 | 40.90 | 40.41 | 28.03 | 4.38 |
| 9M-2025 | 24.84 | 21.84 | 26.78 | NA | 39.41 | 23.45 | 3.18 |
| 9M-2026 | 23.32 | 21.32 | 9.54 | NA | 46.53 | 16.38 | 2.09 |

Reported CAR/CET1 come from each year's unaudited/audited summary quantitative disclosures; the capital-adequacy note agrees (FY2022 12.3%, FY2023 19.6%, FY2024 19.0%, FY2025 23.2%). ROE/ROA and cost/income here use year-end or single-period figures, so they differ slightly from any average-balance ratios. LDR uses gross loans over customer deposits. `income_tax` is the sum of the reported indirect and direct tax.

## Result

- **PASS** - all bridge residuals within tolerance.
