# Stanbic bank-only loan evidence — independent support for DeepSeek

Retrieved 25 November 2026, using Firecrawl secondary source search followed by public web PDF retrieval and visual inspection. Codex's loan amounts independently confirmed. No change to DeepSeek's bank files.

## Official issuer sources
- FY2021 full annual report: https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2021/2021%20Annual%20Report.pdf
- FY2022 full annual report: https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2022/2022%20Annual%20Report.pdf

The issuer PDFs were accessible through the web retrieval route even if the direct download returns HTML in your environment. Visual inspection of 2021 physical PDF index 32 (printed pages 65–66), 2022 index 34 (printed pages 69–70) confirmed the note 5.1 tables. Use printed **66** for FY2021, **70** for FY2022 (Codex's p69 reference is the facing investment securities page). Original units GHS thousands, below converted to GHS millions. Bank name Stanbic Bank Ghana Ltd, not Standard Bank Group.

| Model key | FY2021 | FY2022 |
|---|---:|---:|
| loans_and_advances_gross | 5388.433 | 7018.198 |
| loan_loss_allowance (positive cost convention) | 203.305 | 588.347 |
| loans_and_advances_net | 5185.128 | 6429.851 |
| ECL stage 1 | 35.016 | 173.122 |
| ECL stage 2 | 31.199 | 140.772 |
| ECL stage 3 | 137.090 | 274.453 |

Both note 5.1 bridges and ECL stage sums reconcile exactly in original units. FY2022 report's FY2021 comparative matches FY2021 standalone report.

## Separate suspense and regulatory gross basis
FY2021 annual report printed pp107–108, PDF index 53, visually verified: risk note 30 reports regulatory gross 5,466.710m, IIS 78.277m, ECL components as above, and net 5,185.128m. 5,466.710 - 78.277 - 203.305 = 5,185.128. Note 5.1 gross is already net of this IIS difference. If storing x_interest_in_suspense=78.277 and x_regulatory_gross_loans=5466.710, explicitly avoid subtracting IIS a second time from note 5.1 gross.

FY2022 risk note 28 printed pp109–110, PDF index 54, visually verified: table dated 31 Dec 2022 confirms note 5.1 gross and ECL amounts; no separate IIS line in that table. Facing next spread pp111–112 (index 55) is labelled 31 Dec 2021 yet contains 7,098.442m gross, 78.277m IIS and 6,429.851m net, conflicting with FY2021 standalone values and mixing bases. Do not attribute its IIS to FY2022 as a verified fact; leave FY2022 IIS unavailable unless better evidence resolves the inconsistency. Do not silently correct issuer's date.

FY2022 note 4 printed p69 also states that the bank joined DDEP on 14 Feb 2023, and investment securities gross 1760.703m less ECL 573.894m = net 1186.809m (stage 2 12.907m, stage 3 560.987m). FY2021 net investments 2772.551m (gross 2778.877m less stage 1 ECL 6.326m), p65 of FY2021 annual report. These are separate from loan allowances; don't double count.

Limits: inspected relevant spreads, not the entire reports or raw locally downloaded bytes. Source owner should verify and integrate with existing historical series. Do not treat this as complete independent model acceptance.
