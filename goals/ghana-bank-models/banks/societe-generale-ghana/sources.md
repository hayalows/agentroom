# Societe Generale Ghana PLC source register

Scope: **standalone Bank** (separate financial statements), 31 December fiscal year; values in `financials.csv` are **GHS millions** converted from the filings' GHS units (thousands in the annual reports; the interim summary is printed in thousands). Use FY2021�?"FY2025 and 9M-2026 (unaudited, cumulative). Never substitute Group figures. Page numbers cited in `financials.csv` are the **printed page numbers** in each PDF (the footer), not the PDF index.

| source_id | title | publisher | URL | period covered | retrieved |
| --- | --- | --- | --- | --- | --- |
| SG21AR | 2021 Annual Report and Financial Statements | Societe Generale Ghana PLC | https://societegenerale.com.gh/fileadmin/user_upload/SG_Ghana/PDF/Annual_reports_in_low_definition/SG_Ghana_2021_Financials_with_signature.pdf | FY2021 (with FY2020 comparatives) | 2026-11-25 |
| SG22AR | 2022 Annual Report and Financial Statements | Societe Generale Ghana PLC | https://societegenerale.com.gh/fileadmin/user_upload/SG_Ghana/PDF/Annual_reports_in_low_definition/SG_Ghana_2022_Annual_Report.pdf | FY2022 (with FY2021 comparatives) | 2026-11-25 |
| SG22FIN | 2022 Audited summary financial statements | Societe Generale Ghana PLC | https://societegenerale.com.gh/fileadmin/user_upload/SG_Ghana/PDF/Annual_reports_in_low_definition/SG_Ghana_2022_Year_End_Financials.pdf | FY2022/FY2021 summary | 2026-11-25 |
| SG23AR | 2023 Annual Report and Financial Statements | Societe Generale Ghana PLC | https://societegenerale.com.gh/fileadmin/user_upload/SG_Ghana/PDF/Annual_reports_in_low_definition/2023_SG_Ghana_Annual_Financials_Report_.pdf | FY2023 (with FY2022 comparatives) | 2026-11-25 |
| SG24AR | 2024 Annual Report and Financial Statements | Societe Generale Ghana PLC | https://societegenerale.com.gh/fileadmin/user_upload/SG_Ghana/PDF/Annual_reports_in_low_definition/SG_Ghana_2024_Financials_FINAL.pdf | FY2024 (with FY2023 comparatives) | 2026-11-25 |
| SG25AR | 2025 Annual Report and Financial Statements | Societe Generale Ghana PLC | https://societegenerale.com.gh/fileadmin/user_upload/SG_Ghana/PDF/Annual_reports_in_low_definition/SGGH_Ghana_2025_Financials.Final_Annual_Report__uv_.pdf | FY2025 (with FY2024 comparatives) | 2026-11-25 |
| SG25FIN | 2025 Audited financial statements (summary publication) | Societe Generale Ghana PLC | https://societegenerale.com.gh/fileadmin/user_upload/SG_Ghana/PDF/Annual_reports_in_low_definition/SGGH_FS_for_NEWSPAPER_2025_.pdf | FY2025 audited summary | 2026-11-25 |
| SG26Q3 | Q3 2026 Unaudited Financial Statements (signed) | Societe Generale Ghana PLC | https://societegenerale.com.gh/fileadmin/user_upload/SG_Ghana/PDF/Annual_reports_in_low_definition/2026_SG_GH_Q3._Unaudited_Financials_signed_.pdf | 9M-2026 (with 9M-2025 comparatives) | 2026-11-25 |
| BOGREG | Register of licensed banks | Bank of Ghana | https://www.bog.gov.gh/supervision-regulation/registered-institutions/banks/ | current register | 2026-11-25 |
| GSELIST | Societe Generale Ghana issuer profile | Ghana Stock Exchange | https://gse.com.gh/listed-company/societe-generale-ghana/ | listing status | 2026-11-25 |
| BOGMPR26 | Monetary Policy Report, September 2026 (solvency section) | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2026/10/Monetary-Policy-Report-September-2026.pdf | industry CAR 19.1% in Aug 2026 vs 13.0% minimum; source shared by claude | 2026-11-25 |

## Page map (printed pages used in `financials.csv`)

- Income statement: SG21AR p.51, SG22AR p.54, SG23AR p.61, SG24AR p.64, SG25AR p.65. Interim 9M-2026 income is p.1 of SG26Q3.
- Statement of financial position: SG21AR p.52, SG22AR p.55, SG23AR p.62, SG24AR p.65, SG25AR p.66. Interim 9M-2026 balance sheet is p.1 of SG26Q3.
- Loans and advances note (gross, amortised-cost adjustment, interest in suspense, allowance): SG21AR p.76, SG22AR p.78, SG23AR p.90, SG24AR p.96, SG25AR p.95.
- Other statistics / gross NPL ratio and loan-loss provision ratio: SG21AR p.77, SG22AR p.79, SG23AR p.90, SG24AR p.96, SG25AR p.95.
- Capital adequacy note (CAR): SG21AR p.111, SG22AR p.113, SG23AR p.127, SG24AR p.133, SG25AR p.133. Interim CAR is p.1 of SG26Q3.

## Access notes

- All issuer PDFs above returned HTTP 200 with a valid `%PDF` header on retrieval; the derived text is committed nowhere (only the text deliverables are in the repo). Extraction used `pypdf`.
- **Page numbers in the annual reports skip physical pages** in places and the printed footer differs from the PDF index by roughly 5 pages in earlier reports and ~6 in later reports. Every cited page in `financials.csv` was verified against the printed footer (see page map above).
- The **CAR basis differs by source**: the audited capital-adequacy note gives a consistent series 22.38% (FY2021) → 16.00% (FY2022) → 18.71% (FY2023) → 19.81% (FY2024) → 23.39% (FY2025). The narrative sections separately quote figures on a different basis: FY2023 13.9% with DDEP reliefs / 8.3% without, FY2024 14.0% with reliefs / 11.3% without, FY2025 17.5% (reliefs excluded in 2025). `financials.csv` uses the audited-note series as `car_pct` and records the narrative alternative in `notes`. A reviewer should confirm which basis is preferred for peer comparison.
- The **interim 9M-2026 statement has no loan note**: gross loans, allowance, amortised-cost adjustment and interest in suspense for 9M-2026 are marked `unavailable` (never guessed). Net loans and the balance sheet are reported.
- Group vs bank: Societe Generale Ghana PLC reports a Bank set and (where applicable) consolidated sets; only the **Bank** columns are used. The 2022 audited summary's statement of changes in equity is used only as a cross-check (SG22FIN).

## Bank-specific items handled explicitly

- **Domestic Debt Exchange Programme (2022�?"2023).** SG22AR p.18 (Managing Director's review) and SG23AR p.23 note the DDEP and describe limited impact on the Bank's profitability; SG24AR p.106 (note) gives the 5 December 2022 DDEP launch detail. The Bank's own accounting consequences are captured through the reported impairment charge and capital notes; no separate DDEP loss line is modelled.
- **Capital and reserves.** CAR per the audited capital-adequacy notes (see page map). Regulatory minimum CAR of 13.0% and cash reserve ratio of 20% are taken from the shared macro file (`sector/macro-assumptions/macro.csv`), which cites the Bank of Ghana notices; they are not re-derived here.
- **Levies and special taxes.** The income tax charge is reported as a single line (`income_tax`); the National Fiscal Stabilisation Levy / COVID-19 levy and the growth-and-sustainability levy are not separately disclosed in the summary statements and are therefore not split out. Flagged for the forecast.
- **Cedi depreciation.** SG holds foreign-currency assets and liabilities; the net monetary FX position is not disclosed in the summary statements used, so FX revaluation is left to the forecast using the shared `ghs_per_usd_end` driver, and no historical FX split is asserted.

## Known gaps / follow-ups

- 9M-2026 gross loans and allowance unavailable.
- Historical gross loans by stage and the split of interest in suspense from impairment are in note 20 (p.76 etc.) and are captured; the FY2025 report shows net = gross �?" allowance exactly (no separate IIS line), noted in `financials.csv`.
- Historic Bank of Ghana reserve-notice timeline is owned by the shared macro work; not re-derived here.
- Preferred CAR basis for peer comparison to be confirmed by a reviewer.
