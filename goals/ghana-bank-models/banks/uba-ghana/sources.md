# United Bank for Africa (Ghana) Ltd: source register (owner: claude-helper-1)

Bank-only (separate) statements; UBA Ghana has no subsidiaries disclosed in the statements I read (unknown: not confirmed from a subsidiaries note). Values in `financials.csv` are GHS millions: annual statements print whole cedis, interim statements print thousands. Costs are positive; an impairment reversal is negative.

## Entity facts
- **Owner:** United Bank for Africa Plc (Nigeria) holds **90.77%** (6,717,433,850 of 7,400,500,000 shares); Gold Coast Investment Project Ltd 6.71%, Teachers Fund 2.03%, Unique Insurance Co Ltd 0.31%, Labour Enterprises Trust Co Ltd 0.18% (UBA25AR p.156; the same table is in UBA24AR p.148 for 2024). Observed.
- **Listing:** I did not find UBA Ghana on any exchange list; it publishes on its own site. Unknown: not confirmed against the Ghana Stock Exchange list.
- **Stated capital:** GHS 400m throughout FY2021 to 9M-2026 (the shared macro file's minimum paid-up capital is 400m). Observed.

## Sources (all fetched 2026-11-25 through the fetch tool; text layer only, no page images)
| source_id | document | URL | covers |
| --- | --- | --- | --- |
| UBA22FS | UBA Ghana 2022 Financial Statement (audited statements and notes extract) | https://www.ubaghana.com/wp-content/uploads/sites/14/2023/04/UBA-Ghana-2022-Financial-Statement.pdf | FY2022 and FY2021 |
| UBA22AR | UBA Ghana 2022 Full Annual Report | https://www.ubaghana.com/wp-content/uploads/sites/14/2023/05/UBA-final-Full-Annual-Report-2022-.pdf | FY2022, FY2021 loan note (p.96) |
| UBA23FS | UBA FN 31 Dec 2023 (audited) | https://www.ubaghana.com/wp-content/uploads/sites/14/2024/03/UBA_FN-31Dec2023-v5.pdf | FY2023 and FY2022 |
| UBA24FS | UBA FN 31 Dec 2024 (audited) | https://www.ubaghana.com/wp-content/uploads/sites/14/2025/04/UBA_FN-31Dec2024-v5.pdf | FY2024 and FY2023 |
| UBA24AR | UBA Ghana 2024 Full Annual Report | https://www.ubaghana.com/wp-content/uploads/sites/14/2025/07/UBA-AR2024-Full-Book.pdf | FY2024, FY2023 notes (loans p.134-136, tax pp.129-130, capital pp.122-123, shareholding p.148) |
| UBA25FS | UBA Ghana 2025 Financial Statement (audited) | https://www.ubaghana.com/wp-content/uploads/sites/14/2026/03/UBA-Ghana-2025-Financial-Statement.pdf | FY2025 and FY2024 |
| UBA25AR | UBA Ghana Full Annual Report 2025 | https://www.ubaghana.com/wp-content/uploads/sites/14/2026/05/UBA-AR2025-May112026.pdf | FY2025 notes (loans p.136, tax p.128, capital p.122, shareholding p.156) |
| UBA26Q3 | UBA Ghana Q3 2026 unaudited financial statements | https://www.ubaghana.com/wp-content/uploads/sites/14/2026/11/Final-UBA-Q3-30-SEPT-2026-Fs-7-1.pdf | 9M-2026 and the 9M-2025 comparative |
| UBA26Q2 | UBA Ghana 30 June 2026 unaudited statements | https://www.ubaghana.com/wp-content/uploads/sites/14/2026/07/30-JUNE-2026-FN-v3-update.pdf | H1-2026 cross-check only (not used in financials.csv) |

Investor page (list of all documents): https://www.ubaghana.com/investor-relations/

## Page references: what a reader can and cannot check
- The statement PDFs (UBA22FS to UBA25FS, UBA26Q3) returned text with **no printed page numbers**. Rows from them use the statement name (`SoCI` income statement, `SoFP` financial position, `SoCE` changes in equity, `Note 4` regulatory disclosures) as the page. A reviewer must find the statement in the PDF; it is the first sheets of each document.
- Annual-report note rows carry the printed page returned by the fetch tool for that note (see table above). I did not see a page image of any of them.
- **Not verified visually:** every number was read from a text extraction. The statement identities, comparative columns and equity roll-forwards in `checks_history.md` are the checks I could run.

## Observations that shape the model (observed)
1. **Interim column orientation proven.** Opening equity 1,895.745 + comprehensive income 200.129 - dividends 304.860 = 1,791.014, the printed 30 Sep 2026 equity (checks_history.md section 3). FY2024 and FY2025 roll exactly.
2. **Statutory reserve transfer** is 25.0% of profit after tax in FY2022 to FY2024 (opening reserve below the 400m stated capital) and 12.5% in FY2025 (opening reserve 436.9m above it), matching the Act 930 s34 tiers (50 / 25 / 12.5%). The Act text itself was not re-read for this bank; it was read by chatgpt-support in the Zenith review (BoG PDF printed p.30).
3. **Levies.** The 2024 and 2025 tax charge includes a Growth and Sustainability levy and a Financial Sector Recovery levy of 5% of profit before tax each, on top of 25% income tax (effective 35%). 9M-2026 tax is 41.3% of profit before tax and H1-2026 44.1% (UBA26Q2); the cause is not disclosed.
4. **Credit quality swing.** Stage 3 gross loans fell from 165.0m (FY2024) to 28.3m (FY2025) after 134.7m of write-offs; the allowance fell from 202.6m to 62.8m and the reported gross NPL ratio from 12.5% to 2.11%. A 118.99m reversal of expected credit losses on all financial assets sits in FY2025 operating results (mostly securities). Dated debt-exchange context: UBA22AR auditor's report (pp.59-60, Note 20) attributes GHS 266m of the 282m FY2022 securities impairment to the Government Domestic Debt Exchange Programme.
5. **Property and equipment** rose from 122.3m (30 Jun 2026) to 320.3m (30 Sep 2026). The cause is not stated in the statement. Unknown.
6. **Dividend.** 2025 final dividend recommended 146.452m, subject to Bank of Ghana approval (UBA25FS Note 6). 304.860m was paid in 9M-2026; that exceeds the 2025 recommendation (the difference may include the 157.290m 2024 dividend that was also recommended; inferred, not stated).
