# Sources: Guaranty Trust Bank (Ghana) Ltd (claude)

All retrieved 2026-11-25 (UTC). Primary publisher: the bank itself, index page https://www.gtbghana.com/about/financial-information (links read in full; each URL below was taken from that page).
Status: **listed** = found on the index, not read. **read in full** = I opened the PDF and extracted every number used in `financials.csv`.
Register name on the Bank of Ghana list: *Guaranty Trust Bank (Ghana) LTD* (see `sector/roster-verification/verification.md`).

| source_id | Title (from the file name) | Period | URL | Status |
| --- | --- | --- | --- | --- |
| GTB-FY25 | Dec 2025 Full Year Financials Publication (30-03-26) | FY2025 with FY2024 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Dec-2025-Full-Year-Financials-Publication-30-03-26-FN.pdf?dm=1774872338 | read in full |
| GTB-FY24 | Dec 2024 Full Year Financials Publication (27-03-25) | FY2024 with FY2023 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Dec-2024-Full-Year-Financials-Publication-27-03-25-FNN.pdf?dm=1744711123 | read in full |
| GTB-FY23 | 2023 Full Year Financials | FY2023 with FY2022 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/2023-Full-Year-Financials.pdf?dm=1712133556 | read in full |
| GTB-FY22 | Banking Financials Publication 2022 | FY2022 with FY2021 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Banking-Financials-Publication-2022.pdf?dm=1698251081 | listed (not read) |
| GTB-FY21 | Full Year Financials Publication 2021 | FY2021 with FY2020 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Full-Year-Financials-Publication-2021-DA-copy.pdf?dm=1698251470 | read in full |
| GTB-Q3-26 | Q3 2026 Financials Publication | 9M-2026 (latest interim) | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Q3-2026-Financials-Publication-Final.pdf?dm=1793292058 | read in full |
| GTB-Q2-26 | Q2 2026 Financials Publication (29-7-2026) | H1-2026 | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Q2-2026-Financials-Publication-29-7-2026.pdf?dm=1785429505 | listed (not planned) |
| GTB-AR24 | 2024 Annual Report and Accounts (full) | FY2024, notes | https://gtbank-ghana.files.svdcdn.com/production/financial-information/2024-Annual-Report-and-Accounts-Full.pdf?dm=1744711425 | listed (for gross loans and allowance if needed) |
| GTB-AR22 | 2022 Annual Report and Accounts (full) | FY2022, notes | https://gtbank-ghana.files.svdcdn.com/production/financial-information/2022-Annual-Report-and-Accounts-Full-Doc-23.06.23.pdf?dm=1688362661 | listed (not read) |

## Plan (five milestones)
1. Source inventory (this file). Done.
2. Read GTB-FY25, GTB-FY24, GTB-FY23 and GTB-FY21 (GTB-FY22 not read) and write `financials.csv` with `build_financials.py`; check identities.
3. Add 9M-2026 and the 9M-2025 comparative (both statements) from GTB-Q3-26. Done.
4. Forecast on `macro.csv` v1.1, **calibrated to 9M-2026 actuals** (interest income and expense and the capital ratio within a few percent, as the reviews of CalBank showed is needed), with `checks.md`.
5. README (ownership, restatements, DDEP, regulatory capital), run `sector/qa-sweep/validate.py`, request review.

## Questions to answer from the documents (not assumed)
- Bank-only or group? (The Bank of Ghana register lists the bank itself; GTBank Ghana may have no subsidiaries.)
- Was any prior year restated (SCB was; check FY2023 and FY2022 comparatives against the later reports)?
- DDEP treatment, and the capital ratio the bank itself reports against the 13% minimum.
- Are loans shown net only (then gross loans and the allowance are `unavailable` unless I read the annual-report notes)?

## Answers to the questions above
- Single entity, no group.
- No profit restatement; FY2023 was re-presented in GTB-FY24 (see README).
- DDEP: FY2022 net impairment 557.0m; FY2023 and FY2024 modification losses on investment securities 410.4m and 343.0m.
- Loans are net only: gross loans and allowance are `unavailable`.
