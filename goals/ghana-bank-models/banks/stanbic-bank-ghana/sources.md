# Stanbic Bank Ghana Ltd source register

Scope: **standalone Bank** (separate financial statements), 31 December fiscal year; values in `financials.csv` are **GHS millions** converted from the filings' GHS units (thousands in the annual reports and interims). Use FY2021-FY2025 and 9M-2026 (unaudited, cumulative). Never substitute Standard Bank Group figures. Page numbers cited in `financials.csv` are the **printed page numbers** in each PDF (the footer), not the PDF index.

| source_id | title | publisher | URL | period covered | retrieved |
| --- | --- | --- | --- | --- | --- |
| SB21AR | 2021 Annual Report and Financial Statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2021/2021%20Annual%20Report.pdf | FY2021 (with FY2020 comparatives) | 2026-11-25 |
| SB22AR | 2022 Annual Report and Financial Statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2022/2022%20Annual%20Report.pdf | FY2022 (with FY2021 comparatives) | 2026-11-25 |
| SB22SUM | 2022 Summary financial statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2022/2022%20Summary%20Financial%20Statements.pdf | FY2022/FY2021 summary | 2026-11-25 |
| SB23AR | 2023 Annual Report and Financial Statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2023/2023%20Annual%20Report.pdf | FY2023 (with FY2022 comparatives) | 2026-11-25 |
| SB23SUM | 2023 Summary financial statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2023/2023%20Summary%20Financial%20Statements.pdf | FY2023/FY2022 summary | 2026-11-25 |
| SB24AR | 2024 Annual Report and Financial Statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2024/2024%20Annual%20Report.pdf | FY2024 (with FY2023 comparatives) | 2026-11-25 |
| SB24SUM | 2024 Summary financial statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2024/2024%20Summary%20Financial%20Statements.pdf | FY2024/FY2023 summary | 2026-11-25 |
| SB25AR | 2025 Annual Report and Financial Statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2025/2025%20Annual%20Report.pdf | FY2025 (with FY2024 comparatives) | 2026-11-25 |
| SB25SUM | 2025 Summary financial statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2025/2025%20Summary%20Financial%20Statements.pdf | FY2025/FY2024 summary | 2026-11-25 |
| SB26Q3 | Q3 2026 Unaudited Financial Statements | Stanbic Bank Ghana Ltd | https://www.stanbicbank.com.gh/static_file/ghana/Downloadable%20Files/Financials/2026/Stanbic%20Bank%20Ghana%20Q3%202026%20Financial%20Statements.pdf | 9M-2026 (with 9M-2025 comparatives) | 2026-11-25 |
| BOGREG | Register of licensed banks | Bank of Ghana | https://www.bog.gov.gh/supervision-regulation/registered-institutions/banks/ | current register | 2026-11-25 |
| BOGMPR26 | Monetary Policy Report, September 2026 (solvency section) | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2026/10/Monetary-Policy-Report-September-2026.pdf | industry CAR and the 13.0% minimum; source shared by claude/codex | 2026-11-25 |
| ACT930 | Banks and Specialised Deposit-Taking Institutions Act, 2016 (Act 930), s.34 | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2019/09/BANKS-AND-SPECIALISED-DEPOSIT-ACT-2016.pdf | statutory reserve rule; source shared by chatgpt-support | 2026-11-25 |

## Page map (printed pages used in `financials.csv`)

- Income statement (`INCOME STATEMENT`): SB23AR p.48, SB24AR p.48, SB25AR p.47. Interim 9M-2026 income is page 1 of SB26Q3. The summary statements (SB22SUM, SB24SUM, SB25SUM) also carry the same income line items.
- Statement of financial position: SB23AR p.48, SB24AR p.49, SB25AR p.46. Interim 9M-2026 balance sheet is page 1 of SB26Q3.
- Loans and advances note 5.1 (gross, allowance, interest in suspense, net): SB22AR p.70 (FY2022 and FY2021 comparative, visually confirmed by chatgpt-support and codex), SB23AR p.85 (FY2023/FY2022), SB24AR p.85 (FY2024/FY2023), SB25AR p.80 (FY2025/FY2024).
- Cash and central-bank note 2/7 (coins, balances with central bank, due from other banks): SB23AR p.40 (FY2023/FY2022), SB24AR p.80 (FY2024/FY2023), SB25AR p.77 (FY2025/FY2024).
- Capital adequacy note (Tier 1, Tier 2, total regulatory capital, RWA): SB23AR p.68 (FY2023/FY2022), SB24AR p.137 (FY2024/FY2023), SB25AR p.132 (FY2025/FY2024). The summary statements carry the reported CAR/CET1/NPL ratios.
- Interim 9M-2026 ratios (CAR, CET1, NPL, leverage, liquidity) are page 1 of SB26Q3.

## Access notes

- The FY2023-FY2025 full annual reports and the FY2022/FY2024/FY2025 summary statements downloaded with a valid `%PDF` header. The FY2021 and FY2022 **full** issuer PDFs returned an HTML stub when downloaded directly in this environment (the `static_file` route); the FY2021/FY2022 loan-note figures were recovered by codex from the web-indexed FY2022 report and visually confirmed by chatgpt-support, and the same comparatives appear in the FY2022 summary statement (`SB22SUM`), which matched exactly. Evidence is in `assistance/deepseek/stanbic-fy21-full/`.
- Only the text deliverables are committed to the repo; the source PDFs are not.
- The reported **CAR** in the capital-adequacy note equals the CAR in the summary statements for every overlapping year (FY2022 12.3%, FY2023 19.6%, FY2024 19.0%, FY2025 23.2%). The interim reports 23.32% at 9M-2026.
- The AR narrative quotes the **industry** NPL (e.g. 18.9% in December 2025), which is different from Stanbic's own reported NPL (24.63% at FY2025). `financials.csv` uses the bank's own summary-statement ratio and records the industry figure only in notes.

## Bank-specific items handled explicitly

- **Domestic Debt Exchange Programme (2022-2023).** SB23AR notes the Bank signed onto the DDEP on 14 February 2023 and that the maturity profiles of the affected instruments changed to 2027-2038 (note 4, printed p.81). The Bank's accounting consequences flow through the reported credit impairment charge and the investment-securities ECL stages (note 4.1); no separate DDEP loss line is modelled.
- **Capital and reserves.** Tier 1/Tier 2/RWA are taken from the audited capital-adequacy notes (see page map). The regulatory minimum CAR of 13.0% and cash reserve ratio of 20% come from the shared macro file (`sector/macro-assumptions/macro.csv`); not re-derived here.
- **Levies and special taxes.** The income statement separates an **Indirect tax** line from the direct **Income tax expense**. Both are stored: `income_tax` is the economic total of the two (so that `profit_after_tax = profit_before_tax - income_tax` holds) and the indirect tax is also kept separately as `x_indirect_tax`. `profit_before_tax` is the reported **Profit before indirect tax**.
- **Loan-loss allowance and interest in suspense.** FY2024 and FY2025 report interest in suspense as a separate deduction inside note 5.1 (`gross - allowance - interest in suspense = net`); those years store `x_interest_in_suspense`. FY2021-FY2023 report `net = gross - allowance` with no separate suspense. FY2021 additionally has a **regulatory-basis** gross (5,466.710m) and interest in suspense (78.277m) in risk note 30; the note-5.1 gross of 5,388.433m is **already net of** that suspense, so it is stored as `x_regulatory_gross_loans` / `x_iis_regulatory` and is **not** subtracted again (evidence in `assistance/deepseek/stanbic-fy21-full/chatgpt-support.md`).
- **Cedi depreciation.** Stanbic holds foreign-currency balances. A net monetary FX position is not disclosed in the summary statements used, so the model does **not** model any FX translation P&L and does not revalue the balance sheet by currency; this omission is stated in the README and `checks.md`, and no historical FX split is asserted. (An earlier draft of this register said FX revaluation was forecast by the model; that was incorrect and is corrected here.)

## Known gaps / follow-ups

- FY2021 has no standalone audited report locally; its income/balance-sheet lines come from the FY2022 report's comparative column (which matches the FY2022 summary), and its loan note from the visually confirmed FY2022 report note 5.1.
- FY2021 cash-and-cash-equivalents is presented as a single line (coins vs central-bank vs due-from-banks split not recovered); FY2022-FY2025 are split per note 2/7. 9M-2026 cash is also a single line.
- FY2023 borrowings (31,497) are taken from the FY2024 statement, which reclassified them out of provisions and other liabilities; the FY2023 statement itself showed no separate borrowings line.
- FY2022 interest in suspense is unresolved (the facing FY2022 spread mixes dates); left absent rather than guessed.
- Preferred CAR/CET1 basis is the audited capital-adequacy note, which the model uses directly.
