# CalBank PLC source register

Scope: standalone Bank (`The Bank` / separate financial statements), 31 December fiscal year; GHS millions (converted from GHS thousands in official annual reports and quarterly statements). Covers FY2021–FY2025 and 9M-2026 (unaudited, cumulative). Do not substitute Group (`The Group` / consolidated) figures.

| source_id | title | publisher | URL | period covered | retrieved |
| --- | --- | --- | --- | --- | --- |
| CAL21 | Annual Report 2021 | CalBank PLC | https://calbank.net/wp-content/uploads/2026/01/CAL-Annual-Report-2021.pdf | FY2021, FY2020 comparative | 2026-11-25 |
| CAL22 | Annual Report 2022 | CalBank PLC | https://calbank.net/wp-content/uploads/2026/01/CAL-Annual-Report-2022.pdf | FY2022, FY2021 comparative | 2026-11-25 |
| CAL23 | Annual Report 2023 | CalBank PLC | https://calbank.net/wp-content/uploads/2026/01/CAL-Annual-Report-2023.pdf | FY2023, FY2022 comparative | 2026-11-25 |
| CAL24 | Annual Report 2024 | CalBank PLC | https://calbank.net/wp-content/uploads/2026/01/CAL-Annual-Report-2024.pdf | FY2024, FY2023 comparative | 2026-11-25 |
| CAL25 | CalBank PLC 2025 Annual Report | CalBank PLC | https://calbank.net/wp-content/uploads/2026/02/CalBank-PLC-2025-Annual-Report-FINAL_WEB.pdf | FY2025, FY2024 comparative | 2026-11-25 |
| CAL26Q3 | Unaudited Consolidated Financial Statements for the Nine Months Period Ended 30 September 2026 (PR-405 / Q3) | CalBank PLC / GSE | https://gse.com.gh/wp-content/uploads/2026/10/PR-405-CALBANK-PLC-UNAUDITED-CONSOLIDATED-FINANCIAL-STATEMENTS-FOR-THE-NINE-MONTHS-PERIOD-ENDED-30-SEPTEMBER-20262.pdf | 9M-2026, 9M-2025 comparative | 2026-11-25 |
| CAL22GSE | Summary Consolidated and Separate Financial Statements for the Year Ended December 31, 2022 (PR-129) | CalBank PLC via GSE | https://gse.com.gh/wp-content/uploads/2025/03/PR-129-CALBANK-SUMMARY-CONSOLIDATED-AND-SEPARATE-FINANCIAL-STATEMENTS-FOR-THE-YEAR-ENDED-DECEMBER-31-20222-1.pdf | FY2022, FY2021 comparative | 2026-11-25 |
| BOGREG | Register of licensed banks | Bank of Ghana | https://www.bog.gov.gh/supervision-regulation/registered-institutions/banks/ | current register (per `sector/roster-verification/verification.md`) | 2026-11-25 |
| S-BOG-SUM-NOV26 | Summary of Economic and Financial Data, November 2026 | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2026/11/Summary-of-Economic-and-Financial-Data-November-2026-1.pdf | Jan-Sep 2026 monthly 91-day bill mean used for funding-cost calibration | 2026-11-25 |

Access notes: `CAL26Q3` and `CAL22GSE` have selectable text. Annual reports `CAL21`–`CAL25` are the issuer's official reports. Historical line items use the Bank/separate columns; Group values are not mixed into the Bank series.


## Additional source checks and presentation bases

### Cost of funds
The model uses `cost_of_funds_pct = max(1.5, 0.7 + 0.18 × tbill_91d_pct)`, with rates entered in percentage points. The link is calibrated against two Bank-wide observed-period estimates:

| Period | Bill mean | Observed cost of funds | Model fit | Calculation and source |
| --- | ---: | ---: | ---: | --- |
| FY2025 | 15.38% | 3.470% | 3.468% | Interest expense 370.268m (CAL25 p64) / average FY2024-FY2025 deposits, bank funding and borrowings 10,670.087m (CAL25 p65); bill mean from `macro.csv`. |
| 9M-2026 annualized | 6.23% | 1.813% | 1.821% | Interest expense 151.631m annualized by 4/3 (CAL26Q3 physical PDF p1) / average FY2025-Sep2026 funding 11,152.078m (CAL25 p65; CAL26Q3 physical PDF p2). Bill mean is Jan-Sep 2026 from Bank of Ghana November 2026 Summary, p3. |

Both funding-cost figures are derived ratios, not bank-reported pricing. FY2026E is nine-month actuals plus a Q4 estimate, so Q4 uses an implied 91-day bill mean of 4.55% from the full-year 5.81% estimate and Jan-Sep actual mean of 6.23%, with Nov-Dec at 4.52% as stated in `macro.csv`. Q4 loan yield uses the day-weighted policy rate of 12.57% (14% through 17 Nov and 11% from 18 Nov). Q4 investment-yield proxies use the 9.447% latest 364-day auction and 15.01% 10-year yield held for Nov-Dec in `macro.csv`; these are applied for the Q4 calculation, not asserted as observed quarter-average yields. This keeps full-year average rates separate from Q4-only flows.

### Right-of-use asset mapping
The original historical aggregate already included ROU. The additional reclassification counted the same ROU twice and deducted it twice from other assets. Corrected Bank-only amounts, GHS millions; source text verified, page images not independently verified.

| Period | PPE | Intangibles | ROU | Correct PPE aggregate | Correct other assets | Source |
|---|---:|---:|---:|---:|---:|---|
| FY2021 | 412.938 | 74.062 | 89.070 | 576.070 | 942.114 | CAL21 p51 |
| FY2022 | 622.319 | 81.731 | 85.047 | 789.097 | 555.395 | CAL22 p60 |
| FY2023 | 637.653 | 80.340 | 75.161 | 793.154 | 1017.855 | CAL24 p66 FY23 comparative |
| FY2024 | 570.143 | 81.062 | 60.700 | 711.905 | 1159.930 | CAL25 p65 FY24 comparative |
| FY2025 | 710.955 | 72.830 | 53.960 | 837.745 | 1205.646 | CAL25 p65 |
| 9M-2026 | 692.377 | 66.933 | 49.379 | 808.689 | 1601.782 | CAL26Q3 physical PDF p2 |

Python replay confirmed only 30 classification rows changed and all other forecast rows unchanged. No new data or assumptions invented.

### Retained earnings and regulatory capital
For FY2024, `financials.csv` keeps the SoFP Bank retained earnings of GHS (1,209.108)m from CAL25 p65. The Directors' table on p22 reports GHS (946.562)m excluding transfers to regulatory reserves. The SoCE on p67 reconciles the difference: opening (1,202.955) + PAT 256.393 - statutory-reserve transfer 64.098 - credit-risk-reserve transfer 198.448 = closing (1,209.108).

Historical CAR rows use the Bank values from CAL25 p122: 18.87% for FY2025 and (7.22%) for FY2024. The Group CAR values are 19.80% and (6.38%); the Chairman's p14 narrative refers to Group CAR.

CAL26Q3's Statement of Changes in Equity is physical PDF p3 (the interim file has no printed page numbers). It shows opening retained earnings (858.272)m, 9M PAT 321.670m, transfers of 1.000m to statutory reserves and 24.127m to credit-risk reserves, and closing retained earnings (561.729)m. The 9M equity rollforward does not report a dividend movement or amount. FY2026E assumes no Q4 payout; the output row `x_dividends_paid` exposes modeled payments in later years.

### Statutory reserve and dividend restrictions
CAL26Q3 Bank balance sheet p2: statutory reserve 611.291m, stated capital 1421.535m; statement of changes in equity p3: YTD statutory allocation 1.000m. Two nonadditive source-linked memo rows. Opening fund inferred 610.291m. Act 930 ss34–35, printed pp30–31, visually checked in the official BoG PDF https://www.bog.gov.gh/wp-content/uploads/2019/09/BANKS-AND-SPECIALISED-DEPOSIT-ACT-2016.pdf . Model uses opening annual reserve-to-capital tier (50/25/12.5% of positive after-tax annual profit), subtracts actual YTD allocation before Q4 transfer, then tests remaining retained earnings and capital buffer before payout. No assertion of dividend authorization, bank-specific waiver or further credit-risk reserve allocation. CAL26Q3 page references follow existing physical-page convention; earlier independent reviewers corroborated text, not newly verified visual bank pages here.
