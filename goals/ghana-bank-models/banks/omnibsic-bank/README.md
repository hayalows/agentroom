# OmniBSIC Bank Ghana — provisional model

Bank-only, GHS millions; unlisted universal bank formed by merger of OmniBank and Sahel Sahara Bank; current ownership percentages not independently verified. Four complete annual historical periods FY2022–FY2025 plus 9M2025/26. FY2021 full statements unavailable; FY21 equity and allowance partially sourced in sources.md, not imputed. FY2025 full audited report now recovered; FY2024 net loan difference reconciled by later ECL allowance (gross unchanged). Q3 2026 assets 20,749.490m; deposits 17,063.937m; net loans 2,286.902m; PAT 234.301m; reported CAR 19.55%; NPL 11.08%; retained deficit 251.111m. Forecast draft uses actual 9M plus Q4; shared macro, net-loan credit risk, observed 50% statutory transfer, no dividend and no new capital assumption. Liquidity proxy uses FY25 audited restricted cash share; no proof of compliance. All outputs estimates. Source register details DDEP, levies and source limitations.

Latest audited FY2025 note 4 establishes regulatory capital 869.566m and RWA 4,873.315m (17.84% reported CAR). FY25 RWA/assets 22.5803% is now used as a central forecast proxy rather than original FY24 38%; the actual September 2026 RWA and numerator remain unknown. The 38% and 48% denominator stresses retain the estimated central numerator, and the book-cap alternative is retained (not binding at the central opening). FY25 audited cash mix implies 58.59% unrestricted balances/placements and 33.99% restricted BoG, used as illustrative proxies only. All forecasts remain estimated. FY2021 full annual still missing.

| FY2030E | PAT m | CAR proxy % | 38% RWA stress % | 48% RWA stress % | 48% combined gap m |
|---|---:|---:|---:|---:|---:|
| base | 97.735 | 21.308 | 12.662 | 10.024 | 508.086 |
| downside | -505.863 | 5.337 | 3.171 | 2.511 | 1350.397 |
| upside | 326.294 | 24.897 | 14.794 | 11.712 | 251.555 |

Reproduce node model.mjs. 945 forecasts, 120 engine checks. 310 historical observations. Exact revised package needs independent review; FY2021 missing so excluded from accepted totals. Not investment advice.

**conditional: FY2021 annual statement unavailable.** Under the lead's 18:38 scope decision, FY2022–FY2025 and 9M2025/26 remain the only actual coverage. ROU assets are already included once in property_equipment_intangibles alongside PPE and intangibles; x_right_of_use_assets is a non-additive memo. Other_assets excludes ROU. Classification follows the existing source register; numeric rows unchanged. Not ordinary accepted; exact revised review required.
