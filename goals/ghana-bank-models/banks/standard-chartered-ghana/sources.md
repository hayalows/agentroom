# Sources: Standard Chartered Bank Ghana PLC (claude)

All retrieved 2026-11-25 (UTC). Primary publisher: the bank itself, index page https://www.sc.com/gh/about-us/financial-statements/ (read in full; every link below was taken from that page).
Status of each document: **listed** = found on the index and not read; **read in full** = I opened the PDF and extracted every number used in `financials.csv`.

| source_id | Title (as listed) | Period | URL | Status |
| --- | --- | --- | --- | --- |
| SCB-FY25 | Full year 2025 Financial Statement | FY2025 (with FY2024 comparatives) | https://av.sc.com/gh/content/docs/gh-full-year-financial-statement-annual-report.pdf | read in full |
| SCB-FY24 | Full Year 2024 Financial Statement | FY2024 (with FY2023 comparatives) | https://av.sc.com/gh/content/docs/gh-full-year-2024-financial-statement.pdf | read in full |
| SCB-FY23 | Full Year 2023 Financial Statement | FY2023 (with FY2022 comparatives) | https://av.sc.com/gh/content/docs/gh-full-year-2023-financial-statement.pdf | read in full |
| SCB-FY22 | SCB Ghana Full Year Financial Statement for year 2022 | FY2022 (with FY2021 comparatives) | https://av.sc.com/gh/content/docs/gh-full-year-financial-statement.pdf | listed |
| SCB-FY21 | SCB Ghana Full Year Financial Statement for year 2021 | FY2021 (with FY2020 comparatives) | https://av.sc.com/gh/content/docs/gh-scb-ghana-full-year-financial-statement-for-year-2021.pdf | read in full |
| SCB-Q3-26 | SCB Ghana Q3 Financial Statement for the year 2026 | 9M-2026 (latest interim) | https://av.sc.com/gh/content/docs/gh-scb-q3-finanacial-statement-for-the-year-2026.pdf | read in full |
| SCB-Q2-26 | SCB Ghana Q2 Financial Statement for the year 2026 | H1-2026 | https://av.sc.com/gh/content/docs/gh-scb-q2-financial-statement-2026.pdf | listed |
| SCB-Q1-26 | SCB Ghana Q1 Financial Statement for the year 2026 | Q1-2026 | https://av.sc.com/gh/content/docs/gh-scb-q1-financial-statement-2026.pdf | listed |

## Plan (my five milestones for this bank)
1. **Source inventory** (this file). Done.
2. **Read the reports and write `financials.csv`**. Done (see `build_financials.py`, 296 rows, 0 check failures).
3. **9M-2026 added** from SCB-Q3-26 (unaudited). Done.
4. **Forecast and checks**: assumptions on `sector/macro-assumptions/macro.csv`, `model.py`, `forecast.csv`, `checks.md`.
5. **README** (ownership, listing status, group vs bank-only, DDEP treatment, regulatory capital) and request independent review.

## Open questions I must answer from the documents (do not assume)
- Are the published statements **bank-only or group**? One news result mentioned "Group net interest income" for H1 2026. The spec requires bank-only rows; if only group figures exist, say so and label them.
- How did the bank treat the 2022 to 2023 domestic debt exchange (impairment, capital relief)?
- What minimum capital adequacy ratio does the bank itself cite for each period?

## Secondary items seen while searching (NOT used as numbers)
News and research notes mention FY2024 profit after tax down 12.6 percent and a 2025 return on equity of 28 percent. These are leads to check against the filing, not data.

## What reading the reports changed (v2 of this file)
- **Bank and group are both published; I used the BANK columns.** The FY2025 and 9M-2026 statements print separate Bank and Group columns. FY2021 prints bank only.
- **FY2023 was restated** in SCB-FY24 (booking of previously written-off loans corrected under IAS 8). I use the restated FY2023 and the restated 1 January 2023 balance sheet for FY2022. The originals are quoted in the notes of each row. I did not read the FY2022 report itself (SCB-FY22): its income statement is taken from the comparatives in SCB-FY23, and its balance sheet from the restated comparatives in SCB-FY24. **A reviewer should open SCB-FY22 and check FY2022 and the pre-restatement FY2022 balance sheet.**
- **Loans are shown net only.** Gross loans and the allowance are not in the summary statements, so those rows are `unavailable`.
- **Ratios** are as printed. ROE, ROA, cost-to-income and loan-to-deposit are my recomputations in `checks_history.md`, not bank-reported.

## Steward source and methodology addendum
GSE 2025 Factbook printed p142 https://gse.com.gh/wp-content/uploads/2026/10/GSE-2025-FACTBOOK-.pdf#page=148 (previous Codex visual source review), holding company87.03%, main market SCB and SCB PREF; https://gse.com.gh/listed-company/scb/ issuer profile. The dates differ, no definite listing date claimed; factbook consolidated figures not used. SCB-Q3-26 Bank columns: statutory reserve864.660m unchanged vs FY25; actual tax198.219m, PAT356.518m, paid dividend673.482m, OCI -15.833m. Balance sheet cash2999.277m vs cash-flow cash1045.538m; inferred difference1953.739m, not verified reserve eligibility. Act930 ss34–35 printed pp30–31 https://www.bog.gov.gh/wp-content/uploads/2019/09/BANKS-AND-SPECIALISED-DEPOSIT-ACT-2016.pdf independently visually reviewed: statutory fund tier12.5% for reserve above paid-up capital; transfer before dividends. Forecast applies annual allocation after tax and hypothetical capital/cash gates, not regulatory certification. Original history remains byte unchanged. FY2022 primary summary previously verified by Gemini, see preserved review.
