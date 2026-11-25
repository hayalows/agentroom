# Stanbic Bank Ghana Ltd checks

Recomputed from the committed `financials.csv` and `forecast.csv` by `model.py` (history) and the shared macro file (forecast). GHS millions; ratios in percent; tolerance 0.003. NA = input unavailable, not zero. `model.py` writes this whole file.

## Historical balance and income bridges

| Period | Assets-L-E | Asset components | NII | Operating income | PAT | Net loans |
|---|---:|---:|---:|---:|---:|---:|
| FY2021 | -0.000 | 0.000 | -0.000 | 0.000 | -0.000 | 0.000 |
| FY2022 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | -0.000 |
| FY2023 | -0.000 | 0.000 | -0.000 | -0.000 | -0.000 | 0.000 |
| FY2024 | -0.000 | -0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| FY2025 | -0.000 | -0.000 | 0.000 | 0.000 | -0.000 | 0.000 |
| 9M-2026 | -0.000 | -0.000 | 0.000 | -0.000 | 0.000 | NA |

## Source and schema checks

- Historical rows: 296; duplicate bank/period/statement/key rows: 0; reported rows missing source/page: 0; unavailable rows with non-blank value: 0.
- Spot-checks against printed filing pages (visually verified): SB25AR printed p.46 total assets 36,708,145k -> 36708.145; SB25AR printed p.47 PAT 1,608,667k -> 1608.667; SB24AR printed p.49 total assets 32,590,921k -> 32590.921; SB26Q3 9M-2026 total assets 43,243,634k -> 43243.634. All match.

## Ratios: reported vs recomputed (%)

| Period | Reported CAR | Reported CET1 | Reported NPL | Derived LDR | Derived cost/income | Derived ROE | Derived ROA |
|---|---:|---:|---:|---:|---:|---:|---:|
| FY2021 | 19.20 | 17.20 | 6.70 | 54.23 | 47.68 | 20.75 | 2.89 |
| FY2022 | 12.30 | 12.30 | 8.96 | 48.08 | 46.77 | -3.67 | -0.34 |
| FY2023 | 19.60 | 16.60 | 16.24 | 36.34 | 38.02 | 43.01 | 5.20 |
| FY2024 | 19.00 | 16.00 | 17.08 | 40.52 | 41.42 | 28.15 | 3.57 |
| FY2025 | 23.20 | 21.20 | 24.63 | 40.90 | 40.41 | 28.03 | 4.38 |
| 9M-2026 | 23.32 | 21.32 | 9.54 | NA | 46.53 | 16.38 | 2.09 |

Reported CAR/CET1 are the Bank's own summary quantitative disclosures; the audited capital-adequacy note agrees (FY2022 12.3%, FY2023 19.6%, FY2024 19.0%, FY2025 23.2%). ROE/ROA and cost/income here use year-end/single-period figures. `income_tax` is the sum of the reported indirect and direct tax. FY2022 was a loss year: direct tax was a credit.

## Forecast checks

All forecast rows are estimated. Currency GHS millions; ratios in percent. Accounting arithmetic is checked before rounding. Cash-reserve and CAR checks are screening proxies, not regulatory returns. A negative cash residual or a positive gap is a flagged financing requirement, not an assumed funding source.

Rows: 870; scenario-years: 15; FY2025 residual RWA density: 0.278715; estimated 9M-2026 RWA: 19993.498; initial proxy regulatory capital: 4662.484 (anchored to the observed 23.32% CAR); FY2025 Tier 1 share of regulatory capital: 0.9137.

| Scenario | Year | Max bridge residual | CAR % | Min CAR % | Capital gap | Cash | CRR proxy | Reserve gap | Dividends |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 0.000 | 23.212 | 13.000 | 0.000 | 16374.334 | 6092.942 | 0.000 | 106.736 |
| base | FY2027E | 0.000 | 25.006 | 13.000 | 0.000 | 18878.990 | 6915.490 | 0.000 | 746.217 |
| base | FY2028E | 0.000 | 26.340 | 13.000 | 0.000 | 21741.521 | 7883.658 | 0.000 | 826.231 |
| base | FY2029E | 0.000 | 27.420 | 13.000 | 0.000 | 24925.213 | 8971.603 | 0.000 | 917.658 |
| base | FY2030E | 0.000 | 28.362 | 13.000 | 0.000 | 28540.677 | 10209.684 | 0.000 | 1048.288 |
| downside | FY2026E | 0.000 | 19.601 | 13.000 | 0.000 | 14993.963 | 5800.012 | 0.000 | 0.000 |
| downside | FY2027E | 0.000 | 24.079 | 13.000 | 0.000 | 17444.990 | 6380.014 | 0.000 | 0.000 |
| downside | FY2028E | 0.000 | 27.758 | 13.000 | 0.000 | 20034.718 | 7018.015 | 0.000 | 0.000 |
| downside | FY2029E | 0.000 | 29.623 | 13.000 | 0.000 | 22438.717 | 7719.817 | 0.000 | 0.000 |
| downside | FY2030E | 0.000 | 30.315 | 13.000 | 0.000 | 24621.458 | 8453.199 | 0.000 | 0.000 |
| upside | FY2026E | 0.000 | 22.929 | 13.000 | 0.000 | 16907.706 | 6327.286 | 0.000 | 203.917 |
| upside | FY2027E | 0.000 | 23.469 | 13.000 | 0.000 | 20028.867 | 7466.198 | 0.000 | 1030.751 |
| upside | FY2028E | 0.000 | 23.767 | 13.000 | 0.000 | 23810.935 | 8869.843 | 0.000 | 1217.514 |
| upside | FY2029E | 0.000 | 24.101 | 13.000 | 0.000 | 28374.896 | 10555.113 | 0.000 | 1498.115 |
| upside | FY2030E | 0.000 | 24.393 | 13.000 | 0.000 | 33946.767 | 12613.360 | 0.000 | 1838.262 |

Accounting bridges: PASS (15/15). Capital below the shared minimum: 0/15 flagged. Cash-reserve proxy shortfalls: 0/15 flagged. Negative cash: 0/15 flagged.

FY2026 estimated earnings retain actual 9M income and estimate Q4 only. The Bank does not disclose a net FX position in the summary statements used, so no incremental FX translation P&L is modelled. Full prudential risk weights, OCI, capital deductions and liquidity eligibility are not available, so this is a simplified scenario analysis. Independent review required.
