# Sources: Standard Chartered Bank Ghana PLC (claude)

All retrieved 2026-11-25 (UTC). Primary publisher: the bank itself, index page https://www.sc.com/gh/about-us/financial-statements/ (read in full; every link below was taken from that page).
Status of each document: **listed** = found on the index and not yet read. I will change this column to **read** when I have opened the PDF and extracted numbers from it.

| source_id | Title (as listed) | Period | URL | Status |
| --- | --- | --- | --- | --- |
| SCB-FY25 | Full year 2025 Financial Statement | FY2025 (with FY2024 comparatives) | https://av.sc.com/gh/content/docs/gh-full-year-financial-statement-annual-report.pdf | listed |
| SCB-FY24 | Full Year 2024 Financial Statement | FY2024 (with FY2023 comparatives) | https://av.sc.com/gh/content/docs/gh-full-year-2024-financial-statement.pdf | listed |
| SCB-FY23 | Full Year 2023 Financial Statement | FY2023 (with FY2022 comparatives) | https://av.sc.com/gh/content/docs/gh-full-year-2023-financial-statement.pdf | listed |
| SCB-FY22 | SCB Ghana Full Year Financial Statement for year 2022 | FY2022 (with FY2021 comparatives) | https://av.sc.com/gh/content/docs/gh-full-year-financial-statement.pdf | listed |
| SCB-FY21 | SCB Ghana Full Year Financial Statement for year 2021 | FY2021 (with FY2020 comparatives) | https://av.sc.com/gh/content/docs/gh-scb-ghana-full-year-financial-statement-for-year-2021.pdf | listed |
| SCB-Q3-26 | SCB Ghana Q3 Financial Statement for the year 2026 | 9M-2026 (latest interim) | https://av.sc.com/gh/content/docs/gh-scb-q3-finanacial-statement-for-the-year-2026.pdf | listed |
| SCB-Q2-26 | SCB Ghana Q2 Financial Statement for the year 2026 | H1-2026 | https://av.sc.com/gh/content/docs/gh-scb-q2-financial-statement-2026.pdf | listed |
| SCB-Q1-26 | SCB Ghana Q1 Financial Statement for the year 2026 | Q1-2026 | https://av.sc.com/gh/content/docs/gh-scb-q1-financial-statement-2026.pdf | listed |

## Plan (my five milestones for this bank)
1. **Source inventory** (this file). Done.
2. **Read FY2025, FY2023 and FY2021 reports**: each holds two years, so together they cover FY2021 to FY2025. Use FY2024 and FY2022 to cross-check restated comparatives. Extract income statement, balance sheet and ratios into `financials.csv` in the spec format.
3. **Add 9M-2026** from SCB-Q3-26 and anchor FY2026E on it.
4. **Forecast and checks**: assumptions on `sector/macro-assumptions/macro.csv`, `model.py`, `forecast.csv`, `checks.md`.
5. **README** (ownership, listing status, group vs bank-only, DDEP treatment, regulatory capital) and request independent review.

## Open questions I must answer from the documents (do not assume)
- Are the published statements **bank-only or group**? One news result mentioned "Group net interest income" for H1 2026. The spec requires bank-only rows; if only group figures exist, say so and label them.
- How did the bank treat the 2022 to 2023 domestic debt exchange (impairment, capital relief)?
- What minimum capital adequacy ratio does the bank itself cite for each period?

## Secondary items seen while searching (NOT used as numbers)
News and research notes mention FY2024 profit after tax down 12.6 percent and a 2025 return on equity of 28 percent. These are leads to check against the filing, not data.
