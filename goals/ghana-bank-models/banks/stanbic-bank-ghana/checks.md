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

- Historical rows: 303; duplicate bank/period/statement/key rows: 0; reported rows missing source/page: 0; unavailable rows with non-blank value: 0.
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

Rows: 915; scenario-years: 15; FY2025 residual RWA density: 0.278715; estimated 9M-2026 RWA: 19993.498; initial proxy regulatory capital: 4662.484 (anchored to the observed 23.32% CAR); FY2025 Tier 1 share of regulatory capital: 0.9137.

| Scenario | Year | Max bridge residual | CAR % | Min CAR % | Capital gap | Cash | CRR proxy | Reserve gap | Dividends |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 0.000 | 23.212 | 13.000 | 0.000 | 16435.913 | 6092.942 | 0.000 | 106.736 |
| base | FY2027E | 0.000 | 23.015 | 13.000 | 0.000 | 18527.555 | 6915.490 | 0.000 | 409.226 |
| base | FY2028E | 0.000 | 22.518 | 13.000 | 0.000 | 20899.117 | 7883.658 | 0.000 | 421.983 |
| base | FY2029E | 0.000 | 21.906 | 13.000 | 0.000 | 23493.634 | 8971.603 | 0.000 | 437.027 |
| base | FY2030E | 0.000 | 21.313 | 13.000 | 0.000 | 26426.486 | 10209.684 | 0.000 | 485.675 |
| downside | FY2026E | 0.000 | 19.601 | 13.000 | 0.000 | 14798.961 | 5800.012 | 0.000 | 0.000 |
| downside | FY2027E | 0.000 | 22.407 | 13.000 | 0.000 | 16448.087 | 6380.014 | 0.000 | 0.000 |
| downside | FY2028E | 0.000 | 24.190 | 13.000 | 0.000 | 18002.567 | 7018.015 | 0.000 | 0.000 |
| downside | FY2029E | 0.000 | 24.042 | 13.000 | 0.000 | 19143.219 | 7719.817 | 0.000 | 0.000 |
| downside | FY2030E | 0.000 | 22.678 | 13.000 | 0.000 | 19819.115 | 8453.199 | 0.000 | 0.000 |
| upside | FY2026E | 0.000 | 22.929 | 13.000 | 0.000 | 17159.156 | 6327.286 | 0.000 | 203.917 |
| upside | FY2027E | 0.000 | 21.662 | 13.000 | 0.000 | 20260.468 | 7466.198 | 0.000 | 547.414 |
| upside | FY2028E | 0.000 | 20.387 | 13.000 | 0.000 | 24030.331 | 8869.843 | 0.000 | 628.249 |
| upside | FY2029E | 0.000 | 20.078 | 13.000 | 0.000 | 28857.422 | 10555.113 | 0.000 | 495.960 |
| upside | FY2030E | 0.000 | 20.065 | 13.000 | 0.000 | 34890.990 | 12613.360 | 0.000 | 492.324 |

Accounting bridges: PASS (15/15). Capital below the shared minimum: 0/15 flagged. Cash-reserve proxy shortfalls: 0/15 flagged. Negative cash: 0/15 flagged.

FY2026 estimated earnings retain actual 9M income and estimate Q4 only. The Bank does not disclose a net FX position in the summary statements used, so no incremental FX translation P&L is modelled. Full prudential risk weights, OCI, capital deductions and liquidity eligibility are not available, so this is a simplified scenario analysis. Independent review required.

### Forward-yield calibration diagnostics

Interest income and expense use a **blended, anchor-implied yield carried forward for continuity**: yield_t = income_{t-1} / mean earning assets_{t-2,t-1}, drifted by the shared policy-rate ratio. This replaced a component-yield formula that priced idle cash at the policy rate and produced a 2026->2027 interest-income jump of about 53%. The table below shows the base FY2027 formula against a naive 9M-2026 x 4/3 annualisation; the method is continuous with the anchor, so the growth is now modest.

| Metric | 9M-2026 annualised (x4/3) | Base FY2027 formula | Formula vs run rate |
|---|---:|---:|---:|
| Interest income | 2633.040 | 2539.629 | -3.5% |
| Interest expense | 376.565 | 372.605 | -1.1% |

Out-of-sample check: the FY2024 implied earning-asset yield applied to FY2025 average earning assets predicts FY2025 interest income of about 3,563.0m versus the actual 3,415.7m (a 4.3% error), which supports the blended approach. The earning-asset base includes the cash/BoG residual, which contains non-earning reserve balances, so the blended yield is a portfolio average, not an eligible-reserve rate. Inter-bank balances (`due_from_banks`) are not given a separate income line. A reviewer should still treat the forward net-interest-income path as sensitive to this calibration.
