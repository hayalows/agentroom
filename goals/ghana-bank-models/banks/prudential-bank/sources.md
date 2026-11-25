# Prudential Bank Ghana source register (provisional, Papa Kojo agent)

Scope: standalone Bank (not Group); fiscal year 31 December; GHS millions from source GHS thousands.

| Source ID | Issuer document | URL | Period / page basis |
|---|---|---|---|
| PBL22AR | Prudential Bank 2022 audited annual report | https://www.prudentialbank.com.gh/pdfs/1739187320_ANNUAL%20REPORT%202022.pdf | FY2021/22 printed pp57–58, loan note18 p105 |
| PBL24AR | Prudential Bank 2024 audited annual report | https://www.prudentialbank.com.gh/pdfs/1759249804_Annual%20Report%202024.pdf | FY2023 restated/FY2024 printed pp48–49, note16 p95, note42 p105 |
| PBL25SUM | Prudential Bank 2025 audited summary | https://www.prudentialbank.com.gh/pdfs/1789288644_ANNUAL%20REPORT%202025.pdf | FY2025 physical pp1–2, summary only |
| PBL26Q3 | Prudential Bank unaudited Sep 2026 (retrieval blocked) | https://www.prudentialbank.com.gh/pdfs/1793717792_FINANCIAL%20STATEMENT%20Q3%202026.pdf | URL located, indexed IAS10 disclosure; no usable statement bytes |
| PBL26CAP | Issuer announcement, 9 October 2026 | https://www.prudentialbank.com.gh/index.php/blogdetails/prudential-bank-ltd-completes-ghs-113-billion-strategic-capital-investment-from-bloom-africa-holdings-ghana-limited | GHSm1130 completed strategic capital investment after BoG approval; post-Sep event; split unknown |

Retrieved/checked 25 November 2026. FY21–24 normalized source figures credited to Codex's `assistance/remaining-banks/prudential-primary-source-pack-codex.md`; original indexed PDFs were opened by Codex, not visually verified. FY25 source recovered by Papa Kojo agent and both physical PDF pages inspected in earlier session. Alternate FY25 issuer URL: https://www.prudentialbank.com.gh/pdfs/1783333768_2025%20YEAR-END%20FINANCIAL%20STATEMENT.pdf . Full FY25 loan/ECL notes unavailable in summary. No use of Group columns.

## Mapping / caveats
- FY23 restated under FY24 note42: interest expense362.759m, other expense153.347m, NII311.887m; PAT unchanged. FY23/24 source loan note has distinct deductions for amounts written off108.725/102.774m after gross less ECL; nonadditive memo preserves bridge, not an invented allowance. FY22 note18.1/18.2 records investment impairment610.191m.
- FY25 audited summary: interest508.902/379.080m, fee146.449/47.070, trading110.825, other income186.455, operating income526.481, net impairment reversal61.915, staff202.244, depreciation28.762, other expense248.656 + lease finance0.826 =249.482, PBT107.908, tax75.955, PAT31.953. Cash2637.657, debt securities2190.767, net loans761.241, PPE400.421 + ROU10.454 + intangible1.003=411.878; other assets552.077 + DTA248.043 + current tax74.730 + employee benefit asset0.622 + equity securities2.196=877.668. Bank deposits16.870, customer6054.231, borrowings629.343, other liabilities115.328 + lease2.576=117.904. Statutory131.423 + credit risk192.399 + other9.401 + revaluation261.898=595.121. Equity60.863. CAR -20.19%, CET1 -22.19%, NPL57%, liquidity130%, leverage -10%. Gross loans, ECL and Tier1 not separately verified. FY25 PwC report 6 July 2026 describes going concern material uncertainty and capital shortfall1012m; no dividend. FY24 capital shortfall1135m. Do not equate book equity with regulatory capital.
- FY21–24 historical ratios not entered as actual until exact source pages checked. Net LDR derived from net loans / deposits; do not compare blindly with gross LDR. Other assets include tax assets and applicable equity/subsidiary investments; due_from_banks blank where a separate split cannot be verified.
- October 2026 capital injection is an actual announced event, but Sep 2026 balance sheet not available; never include the injection in Sep actual. No invented 2026 statement or CAR numerator. Model, if prepared on last audited year with a conditional post-event scenario, remains provisional until interim anchor is retrieved.

44/44 historical accounting identities reconcile exactly at GHS thousand precision (36 FY21–24, eight FY25; no FY25 gross/ECL bridge). Independent review still required.

- Statutory reserve forecast assumption: Act 930 s34, https://www.bog.gov.gh/wp-content/uploads/2019/09/BANKS-AND-SPECIALISED-DEPOSIT-ACT-2016.pdf ; FY25 opening reserve131.423m from PBL25SUM. Model transfers 50%, 25%, or 12.5% of positive annual PAT using the opening reserve and modeled stated capital. No dividends; not a legal-compliance finding.
