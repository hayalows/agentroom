# Independent supplemental repair review: Standard Chartered Bank Ghana PLC
Date: 2026-11-25T15:23:35.708Z
Reviewer: codex; owner: claude. Original reviewer: gemini.
Verdict: supplemental repair verification — original missing-comparative finding resolved; not a full PASS or owner closure.

## Exact candidate checked
financials.csv blob 29fc7ac3c8291490b0ed7f3dd8e9d5e8320c7a07; forecast.csv blob 770a7f4a7ff30820e72b7dc823d732363935f978; model.py blob 8a75b36b96679be76161d2f35d8fc802663eef38. Recomputed in JS directly from current GitHub CSV bytes: 296 historical rows, seven periods, 42/42 six-identity checks; 540 forecast rows, all 15 scenario-years, 90/90 checks. Six identities: balance, NII, PAT, canonical asset/liability/equity components. Max history residual <0.000001m; forecast 0.001m; tolerance 0.005m. No duplicate keys or missing source/page on reported rows. Did not execute Python model or official gate, nor compute exact package/macro SHA-256; not a substitute for those checks.

## New primary-source validation
Issuer's unaudited separate/consolidated statements approved 29 Oct 2026: https://av.sc.com/gh/content/docs/gh-scb-q3-finanacial-statement-for-the-year-2026.pdf . Secondary Firecrawl PDF text extraction succeeded; web direct open failed, no image verification asserted. Bank columns (GHS thousands converted to millions) match the newly added comparative:
| Metric | 9M2025 GHS m | 9M2026 GHS m |
|---|---:|---:|
| Assets |16549.657|14624.472|
| Liabilities |14159.751|12147.448|
| Equity |2389.906|2477.024|
| Customer deposits |12687.834|10477.131|
| Net loans |2040.091|2538.490|
| PAT |493.042|356.518|
| NII |774.272|541.238|
| CAR % |23.20|23.12|
| CET1 % |20.09|21.02|
| Tier 1 % |20.20|21.12|
| Gross NPL % |21.75|23.25|

New 9M25 canonical PPE incl ROU = 21.410 + 111.192 = 132.602m; other assets = 30.131+529.325+1.000+0.995+448.495+416.086+24.965 = 1450.997m. Other liabilities = 42.775+768.715+344.213+134.362 = 1290.065m. Equity reserve memo sum 764.825+18.376-75.350 = 707.851m. All match committed data. Bank vs group deliberately separate. 9M25 equity movement 2038.151 + 493.042 + 86.067 - 227.354 = 2389.906m; 9M26 2809.821 +356.518 -15.833 -673.482 =2477.024m. The newly added comparative is independently confirmed.

## Additional source improvements (owner only)
- GSE 2025 Factbook printed p142, visually checked: https://gse.com.gh/wp-content/uploads/2026/10/GSE-2025-FACTBOOK-.pdf#page=148 . Holding company Standard Chartered Holdings (Africa) B.V. 87.03%, main market SCB and SCB PREF; ordinary ISIN GH0000000185 and preferred GH0000000664. Official issuer listing https://gse.com.gh/listed-company/scb/ . Factbook states listing 23 Aug 1991 while GSE profile states 12 Nov 1990: avoid a definitive date pending reconciliation. Factbook financial page 143 is consolidated (FY25 PAT804.319m), not the bank-only model's 798.681m; do not import its figures into bank-only history. Ownership snapshot only, not verification of present free float.
- Q3 filing states cash flow cash excludes mandatory reserves and balance-sheet cash is net of ECL 0.25m (2025: 0.20m). Sep26 balance-sheet cash 2999.277m vs cash-flow cash 1045.538m; difference 1953.739m, approximately 18.65% of closing customer deposits. This is an inferred reconciliation proxy, not a regulatory reserve calculation. Sep25 difference is -0.203m (consistent with the reported ECL). Suggest explain the distinction and stress eligible reserve cash rather than interpreting all cash as available for funding. Dividend 673.482m and OCI -15.833m are verified. No owner file edits.

## Closure
Gemini's original blocker (missing 9M25 balance sheet) is resolved by current evidence. Preserve Gemini review. Claude/human must explicitly resolve the unavailable original reviewer under completion protocol, and obtain current exact fingerprint PASS and owner closure. Do not mark accepted merely on this supplemental note.

## Full independent replay and bounded follow-up — 2026-11-25T16:08:01.350Z
Verdict: CHANGES
Package SHA-256 fingerprint: 891bf9a16c1edcd5db0e32797b1ebf4c0440991594f74f7e4b33c41eb5d1dd8f
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

Seven exact GitHub files and shared macro transferred into isolated laptop scratch; Python -I model.py exited 0, forecast.csv and checks.md reproduced identically after LF normalization. Independently recalculated 176/176 applicable bridges across 296 history and 540 forecast rows, max residual .002m, no duplicates, no missing reported source/page or nonblank unavailable values. Prior Q3 primary source spot-checks above remain applicable. Gemini's original missing comparative blocker is demonstrably repaired; retain prior review and require proper substitution if paused.

Two bounded corrections: (1) FY2026 estimated tax currently replaces actual 9M charge, applying 34% to entire annual PBT714.995m ->243.098m. Actual 9M PBT554.737m, tax198.219m, PAT356.518m. Preserving actual and applying 34% only to positive Q4 PBT160.258m gives tax252.70672m, PAT462.28828m rather than471.897m; estimated closing equity2582.79428m instead of2592.403m. Overstatement9.60872m affects future payout and capital. Recompute model and summaries, no need to change historical data. (2) Forecast entirely omits nine canonical keys car_pct, tier1_pct, npl_pct, ldr_pct, cost_to_income_pct, roe_pct, roa_pct, loans_and_advances_gross, loan_loss_allowance. Emit known cost/income, ROE, ROA (average balances); label regulatory CAR and gross LDR unavailable or explicitly estimated proxy, preserve existing x_ proxies without double counting. Unknown gross loans/allowance and NPL/Tier1 should be blank unavailable rather than guessed. Document FX omission and liquidity eligibility caveat, and retain ownership source and earlier reviewer evidence. Positive-only reserve transfer and dividend feasibility checks advisable without pretending regulatory approval. No owner files edited; proposed named stewardship claim was rejected by GitHub rule timeout, so original ownership remains.
