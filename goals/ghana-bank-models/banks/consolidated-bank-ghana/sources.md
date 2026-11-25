# Consolidated Bank Ghana: source register (bank-only, provisional)

Retrieved 2026-11-25 UTC. Original GHS thousands converted to GHS millions. Issuer annual financial statements, printed page numbers.

| ID | Source | Publisher | Period | URL | Access |
|---|---|---|---|---|---|
| CBG25AR | Annual report and financial statements | CBG | FY2025 / FY2024 comparative | https://www.cbg.com.gh/documents/downloads/94547bf971dcd7a391360a221b4ebc26b801dd0938fe893a95365aea0e9f6fa2 | Parsed text; screenshot cache miss |
| CBG23AR | Annual report and financial statements | CBG | FY2023 / FY2022 comparative | https://www.cbg.com.gh/documents/downloads/6ed61e999dd8f8d5ca62c0394963840e04e97915adc3be3a40e6d48e515d2d29 | Parsed text; screenshot cache miss |
| CBG22AR | Annual report and financial statements | CBG | FY2022 / FY2021 comparative | https://www.cbg.com.gh/documents/downloads/d44351ea04364a2a4ffd4e59d66e8d224dc2f5a75aac2c2a608e68a9adcee485 | Parsed text; screenshot cache miss |
| CBG24AR | Annual report and financial statements | CBG | FY2024 | https://www.cbg.com.gh/documents/downloads/2024-audited-financial-statements | Located; comparative cross-check pending |
| CBG21SUM | Financial summary | CBG | FY2021 | https://www.cbg.com.gh/documents/downloads/2021-financial-summary | Located; comparative cross-check pending |
| CBG26H1 | Interim financial statements | CBG | H1-2026 | https://www.cbg.com.gh/documents/downloads/75d314b4b9316c468a45f521cffd98894c0a2461935070b5c5507c427e2972be | Retrieved 2-page issuer PDF via authorized secondary Firecrawl, HTTP 200 (2 reported credits); parsed text, not visual |

Archive: https://www.cbg.com.gh/documents/annual-financial-reports . Latest archive-listed interim H1-2026 retrieved; no Q3 2026 filing located. No interim estimates presented as reported.

## Material source observations
- FY2022 negative equity GHS712.883m; FY2023 stated capital rose by GHS2,500m while retained losses increased. Do not book recapitalisation as earnings. FY2025 shares deposit GHS198m separate from stated capital.
- 2023 report p85 reports GHS1,517.292m bond modification loss and investment ECL movements; reconcile with P&L rather than double counting.
- FY2025 report p98 says DDEP transitional capital adjustments fully absorbed, yet capital table shows 10% minimum while p96 discusses 13%; both documented, do not infer regulatory compliance solely from table. p91 cash-reserve dispensation. FY2023 report p85 records 15% vs 14% FY2022 reserve requirement.
- FY2025 report p82 reports NPL ratio 33.42% (FY2024 12.50%) and NPL amount 739.263066m (302.638713m); amounts divided by reported gross loans give different ratios. Preserve reported ratio and disclose inconsistency; do not substitute without explanation.
- FY2025 income statement p40 PBT 20.402m; tax reconciliation p105 PBT 20.403m. Keep face statement. FY2024 reported PAT differs from face PBT minus all tax/levy components by 0.001m. No balancing plugs.
- Note 15 separates cash on hand plus Bank of Ghana from Nostro plus placements for all five years. Canonical cash and due-from-banks are disjoint; aggregate face cash remains as an extension. Canonical income_tax includes corporate tax and both levies, which are separately retained as extensions. 
- No independent visual verification yet. 

- FY2025 p97/98 regulatory capital GHS722.423m and RWA GHS5,050.277m, versus FY2024 GHS841.389m and GHS5,679.037m. DDEP CET1 relief falls from GHS1,538.499m to zero. Book equity must not be used as regulatory capital. FY2025 p86–87 net FX short position GHS110.904m; USD short GHS60.283m, USD 10% weakening sensitivity loss GHS6.028m. Use FX sensitivity and cap regulatory capital separately from accounting equity.

- CBG26H1 p1 reports H1-2026 PBT 75.034m, PAT 59.552m, assets 19,196.087m, deposits 16,134.384m, net loans 1,472.515m. p2 reports CAR 14.91%, CET1 13.74%, NPL 33.30%; nil statutory liquidity defaults. 198m deposit for shares transferred into stated capital during H1, no new equity injection. H1 comparative equity statement has inconsistent parsed subtotal; balance-sheet and total comprehensive income agree, no adjustment made. Interim cash aggregate includes due-from-banks; split, gross loans and allowance unavailable. Q1 official PDF parsed but not added since H1 supersedes it; Q1 screenshot cache missed. H1 source has no separate Tier 1 ratio. No visual check claimed.
