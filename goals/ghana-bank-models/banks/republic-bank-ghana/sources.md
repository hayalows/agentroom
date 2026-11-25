# Republic Bank (Ghana) PLC source register

Scope: **standalone Bank** (separate financial statements), 31 December fiscal year; values in `financials.csv` are **GHS millions** converted from the filings' printed **GHS thousands**. Use FY2021--FY2025 and 9M-2026 (unaudited, cumulative) with 9M-2025 comparatives. **Never** substitute Group figures. Page numbers cited in `financials.csv` are the **printed page numbers** in each PDF (the footer), not the PDF index.

| source_id | title | publisher | URL | period covered | retrieved |
| --- | --- | --- | --- | --- | --- |
| RB21FS | 2021 Audited Financial Statements (RBGH 2021 v7 FINAL FS) | Republic Bank (Ghana) PLC | https://www.republicghana.com/wp-content/uploads/2022/04/RBGH-2021-v7-FINAL-FS-04-04-22.pdf | FY2021 (with FY2020 comparatives) | 2026-11-25 |
| RB23AR | 2022/2023 Annual Report (bank + group statements) | Republic Bank (Ghana) PLC | https://www.republicghana.com/ | FY2023 (with FY2022 comparatives) | 2026-11-25 |
| RB24AR | 2024 Annual Report and Financial Statements | Republic Bank (Ghana) PLC | https://www.republicghana.com/ | FY2024 (with FY2023 comparatives) | 2026-11-25 |
| RB24SUM | 2024 audited summary financial statements | Republic Bank (Ghana) PLC | https://www.republicghana.com/ | FY2024/FY2023 summary | 2026-11-25 |
| RB25AR | RFHL 2025 Annual Report containing Republic Bank (Ghana) PLC 2025 statements | Republic Financial Holdings Limited | https://www.republicghana.com/ | FY2025 (with FY2024 comparatives) | 2026-11-25 |
| RB26Q3 | Q3 2026 Unaudited Financial Statements | Republic Bank (Ghana) PLC | https://www.republicghana.com/ | 9M-2026 (with 9M-2025 comparatives) | 2026-11-25 |
| RB26Q2 | Q2 2026 Unaudited Financial Statements | Republic Bank (Ghana) PLC | https://www.republicghana.com/ | H1-2026 (cross-check) | 2026-11-25 |
| BOGREG | Register of licensed banks | Bank of Ghana | https://www.bog.gov.gh/supervision-regulation/registered-institutions/banks/ | current register | 2026-11-25 |
| GSELIST | Republic Bank (Ghana) PLC issuer profile | Ghana Stock Exchange | https://gse.com.gh/ | listing status | 2026-11-25 |

The shared macro file and its regulatory drivers live in `../../sector/macro-assumptions/macro.csv` (canonical fingerprint `b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df`); they are linked, not re-derived here.

## Page map (printed pages used in `financials.csv`)

- Statement of comprehensive income (bank column): RB21FS p.47, RB23AR p.59, RB24AR p.66, RB25AR p.76. Interim 9M-2026 income is p.1 of RB26Q3 (its comparative column gives 9M-2025).
- Statement of financial position (bank column): RB21FS p.48, RB23AR p.60, RB24AR p.67, RB25AR p.77. Interim 9M-2026 balance sheet is p.1 of RB26Q3 (comparative column gives 9M-2025).
- Five-year financial highlights (bank + group columns): RB24AR printed p.18; RB25AR printed p.35.
- Loans and advances note (gross carrying amount, ECL allowance): RB21FS p.90, RB23AR p.104, RB24AR p.112, RB25AR p.116.
- Loan loss provision ratio and gross NPL ratio (loans note 22h): RB21FS p.94, RB23AR p.110, RB24AR p.118, RB25AR p.121.
- Capital-management note (Tier 1, Tier 2, total capital, RWA, CAR): RB21FS p.151, RB23AR p.185, RB24AR p.194, RB25AR p.189.
- Interim quantitative disclosures (CAR, NPL, liquidity, leverage): RB26Q3 p.2.

## Access notes

- **Bank vs Group.** Every Republic Bank (Ghana) statement prints a **Bank** and a **Group** column side by side, and both the five-year highlights and the narrative "NET PROFIT (GHS MILLIONS)" tables carry the same split. This package uses the **Bank** column **only**. In particular, FY2021--FY2025 **bank** PBT is 125.649, -26.105, 231.550, 295.894, 392.850; the frequently quoted 137.397, -15.195, 252.425, 329.039, 440.292 are the **Group** figures and are never used in the bank series. (The Group 2025 PBT of 440.292m is the source of the "440.29" narrative headline.)
- **Restatement of FY2023.** The FY2023 annual report (RB23AR p.60) shows bank total assets of 6,952,222 thousand and total liabilities of 6,160,294 thousand, without deferred-tax netting. The FY2024 report (RB24AR p.67) restates FY2023 to total assets 6,924,025 thousand and total liabilities 6,132,097 thousand, and the FY2024/FY2025 five-year highlights use the **restated** 6,924,025. `financials.csv` uses the **restated** FY2023 balance sheet (RB24AR p.67) so the series is consistent with the published five-year history; the income statement (unchanged) is taken from RB24AR p.66.
- **Interim gross loans.** The 9M-2026 and 9M-2025 interim summaries show **net** loans only; gross loans and the ECL allowance are marked `unavailable` (never guessed). The forecast estimates 9M gross from 9M net using the FY2025 reported allowance/gross ratio and labels it `estimated`.
- **Income tax fork.** Republic Bank reports the two bank levies (Growth & Sustainability Levy, Financial Sector Recovery Levy) as separate lines below profit before tax, then income tax expense. The canonical `income_tax` row is the **total** below-PBT charge (levies + tax) so `profit_after_tax = profit_before_tax - income_tax` holds; the levies and the pure tax line are kept as `x_` memos.
- All issuer PDFs were downloaded and parsed with stdlib tools (the FY2021 PDF with PyMuPDF); every cited page was read from the printed footer. Derived text is committed nowhere — only the deliverables are in the repo.

## Bank-specific items handled explicitly

- **Domestic Debt Exchange Programme (2022--2023).** The Bank participated. The FY2022 impairment charge jumped to GHS237.662m (RB23AR p.59), causing a bank loss before tax of -26.105m and a loss after tax of -66.837m; the FY2023 charge fell back to 66.773m. From FY2022 the Bank applied Bank of Ghana DDEP **forbearance** in its capital computation (minimum CAR held at 10%, losses spread over four years, Tier 2 cap raised to 3% of RWA); the reliefs were **withdrawn in December 2025** (RB25AR p.189), so FY2025 CAR is stated without them. No separate DDEP haircut is modelled; the accounting effect flows through the reported impairment and the capital note.
- **Capital and reserves.** CAR is taken from the audited capital-management note (see page map). The regulatory minimum CAR of 13.0% and the cash reserve ratio of 20% are taken from the shared macro file, which cites the Bank of Ghana notices; they are not re-derived here.
- **Levies and special taxes.** The growth & sustainability levy and the financial sector recovery levy are reported separately (see the income tax fork above) and are kept as `x_` memos.
- **Cedi depreciation.** The Bank reports exchange differences inside its cash-flow statement (13.306m in 9M-2026, 41.574m in 9M-2025) but does not disclose a separate net monetary FX position in the summary statements used, so **no FX revaluation is modelled** (see `assumptions.json` driver `fx`). Flagged rather than guessed.

## Known gaps / follow-ups

- 9M-2026 and 9M-2025 gross loans and ECL allowance are unavailable.
- The FY2022 (RB22AR) and FY2023 (RB23AR) source URLs are the publisher's landing area; the FY2023 income/SoFP and FY2022 comparatives were read from RB23AR. A reviewer should confirm the canonical RB22AR/RB23AR URLs.
- The historic Bank of Ghana reserve-notice timeline is owned by the shared macro work; not re-derived here.
- No separate CET1 ratio is disclosed (only Tier 1), so canonical `car_pct`/`tier1_pct` are the reported figures.
