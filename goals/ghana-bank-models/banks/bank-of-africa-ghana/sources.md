# Source-first historical checkpoint: bank-of-africa-ghana

Initial dataset, not submitted as complete bank model. Public issuer sources, retrieved 25 November 2026. GHS millions. No future estimates or unsupported source figures.

| ID | URL | Scope / verification |
|---|---|---|
| BOA22 | https://boaghana.com/wp-content/uploads/2023/04/BOA-2022-Summary-FS.pdf | FY22/21 audited summary; actual GHS; parsed |
| BOA23 | https://boaghana.com/wp-content/uploads/2024/03/BOA-2023-Full-Year-Financials.pdf | FY23/22 audited summary; actual GHS; visually inspected physical page 1 |
| BOA25 | https://boaghana.com/wp-content/uploads/2026/03/BOA-December-2025-Financials.pdf | FY25/24 audited summary; actual GHS; parsed; auditor 30 Mar 2026 |
| BOA26Q3 | https://boaghana.com/wp-content/uploads/2026/11/BoA_Financial-for-publication_20261029_fv.pdf | 9M26/25; GHS thousands; retrieved by secondary Firecrawl; physical page layout not independently rendered |
| BOA21 | https://boaghana.com/wp-content/uploads/2022/10/2021-FULL-YEAR-FINANCIAL.pdf | FY21 original linked, not yet read; compare reported FY21 asset/liability basis |
| BOA24 | https://boaghana.com/wp-content/uploads/2025/04/BOA-2024-Summary-financial-statement-FV.pdf | FY24 original linked, not yet read |

## Accounting and modelling notes
FY2021 uses FY22 audited comparative; original archive summary lists assets/liabilities 3158.632433/2449.125513 vs comparative 3158.215330/2448.708410; equal equity, difference 0.417103m; source basis unconfirmed, retain comparative and investigate. FY2025/24 annual original GHS not thousands (issuer index heading misleading), interim GHS thousands. FY26 Q3 parsed trading + other subtotal 69.639m conflicts with components 62.763+8.283=71.046; total operating income 331.627 reconciles with individual components; verify image before final acceptance, do not force subtotal. 9M26 dividends 180m, OCI +6.827m; equity 1032.783+50.242+6.827-180=909.852. Tax all-in; net income from other financial assets combined into other_operating_income; cash aggregates include interbank, no separate due_from_banks. Q3 gross loans/ECL not disclosed; avoid invented historical values. Annual report full-note evidence for loan ECL, cash reserve split, RWA and sensitivity still needed. Some source page images failed; FY23 only successful visual.

### Initial independent arithmetic
Eight checks per period (A=L+E, NII, PAT, asset/liability/equity components, operating income, PBT). Residuals GHS m; no plugs. Investigate any beyond .005m before submission.

| Period | A=L+E | NII | PAT | Assets sum | Liab sum | Equity sum | TOI | PBT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| FY2021 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2022 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2023 | 0 | 0 | 0 | 1.82 | 0 | 0 | 0 | -0.000002 |
| FY2024 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2025 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 9M-2025 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 9M-2026 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The source-page fields indicate physical PDF pages, not printed page numbers. Interim Firecrawl text lacks independently rendered page images; source scope and page pointers need visual verification. This is initial source work, not a full independent review. Loan gross/allowance, actual RWA/capital numerators, deposit composition and rate-sensitive maturities require full notes where available. No forecasts made.
