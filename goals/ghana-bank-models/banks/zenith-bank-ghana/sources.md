# Sources: Zenith Bank (Ghana) Ltd (claude-helper-1)

All read 2026-11-25 (UTC). Publisher: the bank itself. Index page: https://www.zenithbank.com.gh/about-us/financial-report/ (every link below was taken from that page).
Entity: Zenith Bank (Ghana) Ltd, a private limited company, 99.42% owned by Zenith Bank PLC (Nigeria); **not listed on the Ghana Stock Exchange**. The audited statements say the bank had no subsidiaries, so the statements are **bank-only** and no group/bank mix is possible (ZEN-FY25 p.3, as transcribed).

## How I read the documents (honest limits)
- The workspace shell cannot download from zenithbank.com.gh (proxy 403 for non-allowlisted hosts). I read each PDF with a fetch tool that returns a **model-assisted transcription** of the page text, not the raw file. Every figure in `financials.csv` therefore passed through that tool.
- **Two column-order errors were found and corrected** (both interim reports): the tool labelled the current-period column as the comparative. The proof is arithmetic, not trust: 9M-2025 equity 2,909,096 = FY2024 equity 2,052,272 + 9M-2025 profit 856,824, and 9M-2026 equity 4,107,719 = FY2025 equity 3,049,986 + 9M-2026 profit 1,057,733 (both exact, GH¢'000). The Q3-2024 report snippet (PBT 881,953; total assets 19,174,160) independently identifies that column as September 2024. See `checks_history.md`, section "Interim column orientation".
- Annual statements were checked three ways: arithmetic identities, the same figure in two consecutive annual reports (current report and next year's comparative), and equity roll-forward. Results are in `checks_history.md`.
- No page of any PDF was viewed as an image. A reviewer who can open the PDFs should confirm the spot-checks listed in `checks.md`.

| source_id | Title (as listed) | Period | URL | Status |
| --- | --- | --- | --- | --- |
| ZEN-FY25 | 2025 Signed Financial Statements (audited, PwC report 25 Mar 2026) | FY2025, comparative FY2024 | https://www.zenithbank.com.gh/media/hd1h4lbg/2025-full-audited-financial-statements_final-signed.pdf | read: statements, notes 11-15, 17-21, 26-28, capital, dividends |
| ZEN-FY24 | 2024 Signed Financial Statements | FY2024, comparative FY2023 | https://www.zenithbank.com.gh/media/r0uc23zr/2024-audited-full-year-financial-statements-zenith-bank-ghana-ltd.pdf | read: statements, risk notes 3.2.3, capital |
| ZEN-FY23 | 2023 Signed Financial Statements (audit report 15 Mar 2024) | FY2023, comparative FY2022 | https://www.zenithbank.com.gh/media/034pjfzj/zenith-bank-ghana-ltd-2023-signed-financial-statements.pdf | read: statements, notes 17-21, capital |
| ZEN-FY22 | 2022 Signed Financial Statements (audit report 19 Apr 2023) | FY2022, comparative FY2021 | https://www.zenithbank.com.gh/media/ae2dktyf/2022-full-year-financial-statements.pdf | read: income statement, notes 11, 15, 17, 19, 21, capital. Balance-sheet page was missing from the transcription, so FY2022 balance sheet comes from ZEN-FY23 comparatives |
| ZEN-FY21 | 2021 Signed Financial Statements (audit report 11 Feb 2022) | FY2021, comparative FY2020 | https://www.zenithbank.com.gh/media/qc4poxaw/2021-annual-report-final-signed-plus-cover.pdf | read: statements, notes, capital |
| ZEN-Q3-26 | Unaudited Financial Statements, period ended 30 Sep 2026 | 9M-2026, comparative 9M-2025 and 30 Sep 2025 balance sheet | https://www.zenithbank.com.gh/media/tprbyuce/unaudited-financial-statements-quarter-3-2026_final.pdf | read: all statements and regulatory table (columns re-oriented, see above) |
| ZEN-Q3-25 | Unaudited Financial Statements, period ended 30 Sep 2025 | 9M-2025 and 30 Sep 2025 balance sheet | https://www.zenithbank.com.gh/media/a54p02ee/unaudited-financial-statements-quarter-3-2025-final-2.pdf | read: used only to cross-check orientation of ZEN-Q3-26 (its comparative column is Sep 2024) |
| ZEN-Q3-24 | Unaudited Financial Statements, period ended 30 Sep 2024 | 9M-2024 | https://www.zenithbank.com.gh/media/ro1lf5f2/zenith-bank-unaudited-financial-statements-for-publication_q3-2024.pdf | seen as a search snippet only (PBT 881,953; total equity and liabilities 19,174,160); used for orientation proof |
| ZEN-SUM25 | Summary Financial Statements for the Year Ended 31 December 2025 | FY2025 | https://www.zenithbank.com.gh/media/slfplz33/summary-financial-statements-december-2025-final-signed.pdf | seen as a search snippet only; its income-statement figures match ZEN-FY25 |

## Not used
- Annual Reports (the glossy "Report" PDFs): not needed, the signed financial statements carry the audited numbers.
- Group figures of Zenith Bank PLC (Nigeria): different entity, naira, not comparable.

## Dated events cited in the forecast narrative (review finding F6)
- Domestic debt exchange (DDEP) dates and terms: ZEN-FY25 note 19, p.99 (as read by the independent reviewer); the FY2022 impairment of 1,157.5m is in ZEN-FY23 comparatives / Note 11.
- End of the regulatory relief on the debt-exchange impairment: ZEN-FY25 note 4, p.87 (as read by the independent reviewer). The author did not open these pages.
- Statutory reserve tiers: Banks and Specialised Deposit-Taking Institutions Act 2016 (Act 930) s.34, official Bank of Ghana PDF printed p.30 (as read by the independent reviewer).
- FY2025 repricing schedule p.81 and regulatory capital pp.86-87 of ZEN-FY25: transcribed from the reviewer's visual check, not read by the author.
