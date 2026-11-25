# Fidelity Bank Ghana Limited (`fidelity-bank-ghana`) — Sources

**Entity modeled:** Fidelity Bank Ghana LTD ("The Bank", standalone separate financial statements per `MODEL-SPEC.md`).
**Currency & Units:** Ghana Cedis (`GHS`), reported in `GHS '000` in all primary filings and converted to `GHS millions` (`÷ 1,000`).
**Listing & Ownership Status:** Unlisted private/public-interest licensed commercial bank (not listed on the Ghana Stock Exchange). Wholly owns Fidelity Asia Bank (Labuan, Malaysia), Fidelity Securities and OrangeTech (approved FY2025 report pp2–3,142). At FY2025 top ordinary holders Africa Capital LLC 38.07%, AfricInvest 4.5 LLC 16.94%, LF III BankCo 16.94%, SSNIT 9.50%; approved report p161.

## Primary Official Sources (Bank Website)

1. **FY2025 & FY2024 Audited Annual Report (`FBL-AR25`)**
   - Title: *Fidelity Bank Ghana LTD Annual Report 2025* (172 pages; Independent Auditor's Report by PricewaterhouseCoopers, dated 30 March 2026)
   - URL: `https://fidelitybank.com.gh/wp-content/uploads/2026/06/2025-FBL-Annual-Report-Approved-Version-1.pdf`
   - Scope: Consolidated and Separate (Bank) Financial Statements for FY2025 and FY2024 comparative (approved edition printed pp76–77 statements, pp78–79 equity, p80 cash flow, pp81 onward notes).

2. **FY2024 & FY2023 Audited Annual Report (`FBL-AR24`)**
   - Title: *Fidelity Bank Ghana LTD Annual Report 2024* (168 pages; Independent Auditor's Report by Ernst & Young, dated 26 March 2025)
   - URL: `https://fidelitybank.com.gh/wp-content/uploads/2025/09/FBL-Annual-Report-2024.pdf`
   - Scope: Consolidated and Separate (Bank) Financial Statements for FY2024 and FY2023 comparative (`p.79` IS, `p.80` BS, `p.81–82` Changes in Equity, `p.83` Cash Flows, Notes `p.84–165`).

3. **FY2023 & FY2022 Audited Annual Report (`FBL-AR23`)**
   - Title: *Fidelity Bank Ghana LTD Annual Report 2023* (172 pages; Independent Auditor's Report by Ernst & Young, dated 27 March 2024)
   - URL: `https://fidelitybank.com.gh/wp-content/uploads/2025/09/FBL-Annual-Report-2023.pdf`
   - Scope: Consolidated and Separate (Bank) Financial Statements for FY2023 and FY2022 comparative (`p.76` IS, `p.77` BS, `p.78–79` Changes in Equity, `p.80` Cash Flows, Notes `p.81–169`).

4. **FY2022 & FY2021 (Restated) Audited Annual Report (`FBL-AR22`)**
   - Title: *Fidelity Bank Ghana Limited Annual Report 2022* (152 pages; Independent Auditor's Report by Ernst & Young, dated 27 April 2023)
   - URL: `https://fidelitybank.com.gh/wp-content/uploads/2025/09/FBL-Annual-Report-2022.pdf`
   - Scope: Consolidated and Separate (Bank) Financial Statements for FY2022 and restated FY2021 comparative (`p.48` IS, `p.49` BS, `p.50–51` Changes in Equity, `p.52` Cash Flows, Notes `p.56–144`).

5. **FY2021 Audited Annual Report (`FBL-AR21`)**
   - Title: *Fidelity Bank Ghana Limited Annual Report 2021* (132 pages; Independent Auditor's Report by Ernst & Young, dated 25 March 2022)
   - URL: `https://fidelitybank.com.gh/wp-content/uploads/2025/10/FBL-Annual-Report-2021.pdf`
   - Scope: Consolidated and Separate (Bank) Financial Statements for FY2021 (`p.44` IS, `p.45` BS, `p.46–47` Changes in Equity, `p.48` Cash Flows) — cross-checked against `FBL-AR22` Note 2.20 restatements.

6. **9M-2026 & 9M-2025 Unaudited Summary Financial Statements (`FBL-26Q3`)**
   - Title: *Unaudited Summary Consolidated and Separate Financial Statements for the Period Ended 30 September, 2026* (2 pages; signed by Board Chairman James Reynolds Baiden & Managing Director Julian Kingsley Opuni)
   - URL: `https://fidelitybank.com.gh/wp-content/uploads/2026/10/FBL-Financial-Statement-Q3-2026.pdf`
   - Scope: Bank and Group 9M-2026 (`30 Sep 2026`) and 9M-2025 comparative (`30 Sep 2025`) IS, BS, Changes in Equity, Cash Flows, plus Quantitative Disclosures (CAR `18.53%`, CET1 `15.33%`, Leverage `5.97%`, NPL `6.84%`, Liquid Ratio `169.71%`).
   - Note on `9M-2025` reclassification: `FBL-26Q3` reclassifies `109,033` (`GHS '000`) from Bank interest income (`2,187,483` in `FBL-25Q3` vs `2,078,450` in `FBL-26Q3`) and breaks out `Net trading income` (`358,649`) separately from `Other operating income` (`2,578`); total Bank `Operating income` (`2,058,388`) and `PAT` (`696,125`) are unchanged.

7. **9M-2025 Unaudited Summary Financial Statements (`FBL-25Q3`, cross-check)**
   - Title: *Unaudited Summary Consolidated and Separate Financial Statements for the Period Ended 30 September, 2025* (2 pages)
   - URL: `https://fidelitybank.com.gh/wp-content/uploads/2025/10/FBL-Financial-Statement-2025-Q3.pdf`
   - Scope: Cross-check for 9M-2025 pre-reclassification lines and 30 Sep 2025 BS.

## Steward source verification (2026-11-25)
Official archive https://fidelitybank.com.gh/investor-relations/financial-reports/ supplies approved FY25 PDF above. Parsed pp123 capital, 142 loan note, 133 tax, 131 trading, 161 shareholders. Visually checked printed pp105,108–109 (PDF index 108,111–112); capital/statement screenshots cache-missed. FY25 bank regulatory capital 2295.594m and RWA 10041.373m, CET1 2083.059m; FY24 1649.285m and 8435.183m. FY25 securities 8467.709m reprice within 12 months, 3032.879m after; cash 1349.370m interest-bearing, other cash non-interest-bearing. FY25 USD on-balance-sheet -216.636m before forwards; net hedge position cannot be inferred from this. Use FX stress only, not full unhedged exposure as actual earnings. Printed p109 bank +100bp sensitivity +25.713m (1.23% NII); the static table contains an inconsistency versus the p108 gap, preserve disclosed sensitivity and label fit. FY25 p122 regulatory DDEP relief lowered CAR minimum from 13% to 10%, CET1 6.5% to 5.5%, increased Tier2 limit; shared forward 13% standard screen. FY2022 loss -388.585m, aggregate impairment 1292.174m; FY25 p124 and p137 discuss DDEP/Eurobond investment ECL. Separate DDEP loss not independently extracted; do not assume recurring haircut. FY25 tax components 397.936m corporate plus 73.042m each levy. Original FY25 page pointers amended to approved printed page numbers where verified; other older report pointers and deposit notes still need independent source check.
FBL-26Q3 re-retrieved via user-authorized Firecrawl secondary (2 credits, 2 pages HTTP 200), bank-only assets 30351.339m, deposits 20221.785m, PAT 524.854m, CAR 18.53%, CET1 15.33%, NPL 6.84%, ordinary and preference dividends 282.800m and 34.638m, statutory reserve 905.192m (transfer 65.607m), other reserves 111.216m, credit risk reserve 93.299m, OCI -11.738m. Bank equity roll-forward: 2769.753+524.854-11.738-317.438=2965.431m. H1/Q3 cash split unavailable; combined cash kept with due_from_banks blank. Historical ratios canonical ROA/ROE aliases normalized; interim LDR net memo only. Q3 independent review pending.

Approved FY25 printed p106: bank USD 15% cedi weakening sensitivity -9.185m (parsed; page screenshot unavailable); not group +7.845m. Forecast uses constant effective hedged exposure -9.185/0.15 with annual USD exchange-rate change from FY2027; Q3 exposure unknown. FY25 bank loans repricing within 12 months 2181.160m; beyond 12 months 2561.855m (p108 visual).
