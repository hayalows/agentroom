# Source-first historical checkpoint: first-national-bank-ghana

Historical and forecast source register; revised candidate for independent review. Public issuer sources, retrieved 25 November 2026. GHS millions. Historical figures and memo sensitivity clearly separated; future estimates in forecast.csv.

| ID | URL | Scope / verification |
|---|---|---|
| FNB22 | https://www.firstnationalbank.com.gh/downloads/Ghana/financial-reports/2022/Financialpublication_December2022.pdf | FY22/21 audited summary, p1 statements, p2 ratios; parsed |
| FNB23 | https://www.firstnationalbank.com.gh/downloads/Ghana/financial-reports/2023/SummaryFinancialStatements_Dec2023.pdf | FY23/22 audited summary, p1 statements, p2 ratios; parsed |
| FNB25 | https://www.firstnationalbank.com.gh/downloads/Ghana/financial-reports/2025/SummaryFinancialStatements_December2025.pdf | FY25/24 audited summary, p1 statements visually verified, p2 ratios parsed |
| FNB26Q3 | https://www.firstnationalbank.com.gh/downloads/Ghana/financial-reports/2026/FNB_unaudited_financial_for_the_period_ended_30_September_2026.pdf | 9M26/25 parsed by secondary Firecrawl, p1 statements p2 ratios/equity; no web page images |
| FNB21 | https://www.firstnationalbank.com.gh/downloads/Ghana/financial-reports/2021/SummaryFinancialStatementsDecember2021.pdf | FY21 original linked, not yet read |
| FNB24 | https://www.firstnationalbank.com.gh/downloads/Ghana/financial-reports/2024/SummaryFinancialStatements_December2024.pdf | FY24 original linked, not yet read |

## Accounting and modelling notes
Entity First National Bank Ghana Ltd, subsidiary of FirstRand, NOT FBNBank Ghana/FirstBank. All source figures GHS thousands. Current source summaries report net loans on face and regulatory gross loans in notes; gross-net differences are memo adjustments, not verified IFRS ECL. Keep allowance unavailable until full note confirms comparability. FNB FY22 contribution towards capital 40.067m included in reserves_other alongside statutory 1.713m; separate statutory balance memo. 2025 paid-up capital grew by 358.572m (ordinary share proceeds) from 938.985 to 1297.557m; no assumed future injection. 9M26 PAT 48.823m added to 1003.049m equity gives 1051.872m, unchanged capital. Accumulated losses remain -309.925m; dividend restrictions must be explicit. 2022 loss -340.464m, impairment 263.159m; no separate DDEP attribution without notes. FY25 corporate tax credit 7.487m offset by two 5.518m levies; all-in tax 3.549m. Q3 comparative from 2026 filing; FY25 original/2025Q3 may differ. Combine trading/derivatives/tax/subsidiary and other assets, include operating leases in other expenses. Combined cash not pure BoG balances; full note unavailable for current period. FY22 summary cash flow note restricted BoG 516.832m/212.907m FY22/21; use memo if relevant, no future compliance claim. FY2021 and FY2022/23 face PPE includes unspecified ROU basis; confirm note. Annual gross loan notes and capital ratios page 2. Only FY25 p1 visual verified; older and current interim parsed. Full report risk notes still required where available.

### Initial independent arithmetic
Eight checks per period (A=L+E, NII, PAT, asset/liability/equity components, operating income, PBT). Residuals GHS m; no plugs. Investigate any beyond .005m before submission.

| Period | A=L+E | NII | PAT | Assets sum | Liab sum | Equity sum | TOI | PBT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| FY2021 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2022 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2023 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2024 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| FY2025 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 9M-2025 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 9M-2026 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The source-page fields indicate physical PDF pages, not printed page numbers. Interim Firecrawl text lacks independently rendered page images; source scope and page pointers need visual verification. This is initial source work, not a full independent review. Loan gross/allowance, actual RWA/capital numerators, deposit composition and rate-sensitive maturities require full notes where available. Initial forecast and review repairs now published.

## Review repair evidence (Codex independent review 15:15 GMT)
- FNB25 physical p1 FY25 nonpledged trading 205.753m, pledged 320.918m, derivative asset 50.831m, deferred tax asset 40.165m. FNB26Q3 p1 208.015/84.511/0.610/40.165m, 9M25 comparable 115.177/229.173/12.814/0.797m. Non-additive memos within other_assets. Central zero assumed marginal trading interest; alternative 50% trading earning stock with refitted yield; pledged assets not available cash. FY25/FY24 other financial instrument interest 23.340/13.328m, source note per Codex. Actual Sep RWA unavailable; CAR decline from 34.08% to 24.07% despite book equity increase demonstrates changing regulatory eligibility/density. FY25 and FY24 statutory transfers 53.407/9.120m despite deficit, 50% PAT. No dividends assumed.

Historical ROA/ROE use adjacent annual average balances where available; gross LDR only for available regulatory gross amounts; net LDR separate. All supplemental source facts credited to Codex's primary-source review; no independent second visual retrieval claimed. 
