# Source-first historical checkpoint: bank-of-africa-ghana

Historical and forecast source register; revised candidate for independent review. Public issuer sources, retrieved 25 November 2026. GHS millions. Historical figures and memo sensitivity clearly separated; future estimates in forecast.csv.

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
| FY2023 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -0.000002 |
| FY2024 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2025 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 9M-2025 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 9M-2026 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The source-page fields indicate physical PDF pages, not printed page numbers. Interim Firecrawl text lacks independently rendered page images; source scope and page pointers need visual verification. This is initial source work, not a full independent review. Loan gross/allowance, actual RWA/capital numerators, deposit composition and rate-sensitive maturities require full notes where available. Initial forecast and review repairs now published.

FY23 current tax asset confirmed GHS3,355,786 (not GHS1,535,786); other_assets recomputed 191.922877m from all three source lines, resolving 1.820m transcription difference. 56/56 checks now pass at GHS0.005m tolerance. No plug.

## Review repair evidence (Codex independent review 15:15 GMT)
- BOA22 physical p1 qualified auditor opinion (27 Apr 2023): GHS80.883183m omitted investment securities impairment, contrary to IFRS9. Reported PBT/PAT unchanged. Illustrative pre-tax full recognition PBT 14.061693 - 80.883183 = -66.821490m, not corrected audited profit and no recurring future impairment assumed. FY23 summary unmodified opinion repeats FY22 PAT; no inferred restatement. FY25 unmodified.
- BOA-GH24 Ghana-specific report https://bank-of-africa.net/wp-content/uploads/2025/09/BOA-RA-2024-Ghana.pdf (capital adequacy table, 2024 report, retrieved 25 Nov 2026 by Codex; text only): Tier1/RWA FY23 666.2/2231.7m; FY24 758.0/2454.5m; Tier2 dash. Rounded Ghana local-bank figures. FY24 capital/book equity ~85.3%, RWA/assets ~53.25%. Absolute September 2026 capital remains unknown.
- BOA21 vs BOA22 comparative: original other assets 113.593195m versus 113.176092m; original other liabilities 69.254182m versus other plus derivative liabilities 68.837079m. Both differ .417103m, equity unchanged. Retain FY22 comparative without asserting cause.

Historical ROA/ROE use adjacent annual average balances where available; gross LDR only for available regulatory gross amounts; net LDR separate. All supplemental source facts credited to Codex's primary-source review; no independent second visual retrieval claimed. 
