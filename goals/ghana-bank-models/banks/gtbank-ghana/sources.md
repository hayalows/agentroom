# Sources: Guaranty Trust Bank (Ghana) Ltd (claude)

All retrieved 2026-11-25 (UTC). Primary publisher: the bank itself, index page https://www.gtbghana.com/about/financial-information (links read in full; each URL below was taken from that page).
Status: **listed** = found on the index, not read. **read in full** = I opened the PDF and extracted every number used in `financials.csv`.
Register name on the Bank of Ghana list: *Guaranty Trust Bank (Ghana) LTD* (see `sector/roster-verification/verification.md`).

| source_id | Title (from the file name) | Period | URL | Status |
| --- | --- | --- | --- | --- |
| GTB-FY25 | Dec 2025 Full Year Financials Publication (30-03-26) | FY2025 with FY2024 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Dec-2025-Full-Year-Financials-Publication-30-03-26-FN.pdf?dm=1774872338 | read in full |
| GTB-FY24 | Dec 2024 Full Year Financials Publication (27-03-25) | FY2024 with FY2023 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Dec-2024-Full-Year-Financials-Publication-27-03-25-FNN.pdf?dm=1744711123 | read in full |
| GTB-FY23 | 2023 Full Year Financials | FY2023 with FY2022 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/2023-Full-Year-Financials.pdf?dm=1712133556 | read in full |
| GTB-FY22 | Banking Financials Publication 2022 | FY2022 with FY2021 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Banking-Financials-Publication-2022.pdf?dm=1698251081 | listed (not read by original author) |
| GTB-FY21 | Full Year Financials Publication 2021 | FY2021 with FY2020 comparatives | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Full-Year-Financials-Publication-2021-DA-copy.pdf?dm=1698251470 | read in full |
| GTB-Q3-26 | Q3 2026 Financials Publication | 9M-2026 (latest interim) | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Q3-2026-Financials-Publication-Final.pdf?dm=1793292058 | read in full |
| GTB-Q2-26 | Q2 2026 Financials Publication (29-7-2026) | H1-2026 | https://gtbank-ghana.files.svdcdn.com/production/financial-information/Q2-2026-Financials-Publication-29-7-2026.pdf?dm=1785429505 | listed (not planned) |
| GTB-AR24 | 2024 Annual Report and Accounts (full) | FY2024, notes | https://gtbank-ghana.files.svdcdn.com/production/financial-information/2024-Annual-Report-and-Accounts-Full.pdf?dm=1744711425 | parsed audited note extracts in steward repair |
| GTB-AR22 | 2022 Annual Report and Accounts (full) | FY2022, notes | https://gtbank-ghana.files.svdcdn.com/production/financial-information/2022-Annual-Report-and-Accounts-Full-Doc-23.06.23.pdf?dm=1688362661 | listed (not read by original author) |

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
- FY21–24 gross loans and allowance now sourced; FY25 and interim remain unavailable.


## Steward repair (25 November 2026)
Claude original builder; authorized steward chatgpt-support. Codex independently retrieved FY22 summary and full notes; steward independently retrieved AR22/AR24 via secondary Firecrawl, text layer only. FY22 original assets/liabilities 7132.787/5797.165m vs FY23 comparison 7127.345/5791.723m: 5.442m deferred tax presentation difference, consistent with netting, no change to equity. Original FY22 PBT/PAT191.039/114.981m vs comparison191.038/114.980m rounding. FY21 original vs FY22 comparative interest 481.576/443.715, fees149.901/136.726, trading133.954/189.146, investments1013.537/1050.574, nonpledged764.426/727.389; same PAT315.446m/assets5035.451m. Keep original FY21 and later comparisons already chosen; no claim of identical presentation.
AR22 note17 p131 and AR24 note17 p158 gross and allowance added; note15 actual combined cash breakdown (gross memo and aggregate cash ECL). No artificial allocation of aggregate cash ECL; separate canonical due_from_banks unavailable. AR22/24 lease note 29 states ROU included in PPE; no double count. AR24 p10 parent98.32%; note3.6 regulatory capital/RWA and Tier1 added, note ratio FY24 37.01 vs later summary36.94, FY21 note38.53 vs original summary38.80. FY22 note without DDEP relief; FY23/24 with relief per note: 10% minimum excluding buffer, four-year recognition, new bonds 0% risk weights. Shared forecast threshold not legal advice. AR24 note3.5.1 +100bp PBT sensitivity FY24/23 11.984863/10.349744m; note3.5.2 5% cedi strengthening increases FY24/23 profit/equity1.606045/.747943m. Current actual FX exposure unknown. No visual verification claimed. Q3 source independently unverified; prior source register retained. Historical full note page identifiers use actual note sections where printed page unconfirmed.
