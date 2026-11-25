# Consolidated Bank Ghana Limited (CBG)
 
**Status:** submitted for independent review. Historical data bank-only, December year-end, GHS millions. Government-owned universal bank; Ministry of Finance owns 100% at FY2025 per annual report p3. No listed equity identified. CBG commenced universal banking in August 2018 (H1-2026 note 1). Sources and limitations in sources.md.

## Historical findings

| Period | Assets | PAT | Equity | Reported CAR |
|---|---:|---:|---:|---:|
| FY2021 | 10,751.164 | 72.261 | 801.545 | 21.64% |
| FY2022 | 10,616.368 | -1,505.456 | -712.883 | -4.45% |
| FY2023 | 13,691.904 | -542.962 | 1,244.155 | 23.52% |
| FY2024 | 16,638.057 | 88.719 | 1,294.460 | 14.82% |
| FY2025 | 17,857.592 | 7.384 | 1,497.080 | 14.30% |
| H1-2026 | 19,196.087 | 59.552 | 1,559.894 | 14.91% |

The 2022 debt-exchange losses severely impaired capital. Stated capital increased 2,500m in 2023; this was an owner transaction, not profit. In H1-2026 198m already received as deposit for shares was transferred to stated capital, with no new equity from the transfer. H1-2026 deposits 16,134.384m, net loans 1,472.515m, investments 14,130.908m. Reported NPL 33.30%, CET1 13.74%; Tier 1 not separately disclosed. The annual report shows FY2025 regulatory capital 722.423m vs accounting equity 1,497.080m and DDEP relief fully absorbed. 2025 NPL 33.42% (12.50% FY24); reported ratio differs from amount/gross loans, so historical reported ratios are retained.

## Five-year forecast, illustrative not guidance

| Scenario | 2026E PAT | 2030E PAT | 2030E CAR proxy | 2030E capital gap to 13% |
|---|---:|---:|---:|---:|
| Base | 106.007 | -137.774 | 7.44% | 449.308 |
| Downside | -44.552 | -912.353 | -17.29% | 1,812.736 |
| Upside | 139.000 | 68.609 | 10.30% | 265.145 |

All three scenarios fall below the shared 13% CAR screen by FY2030E, even though upside remains profitable. In the base case the first capital gap occurs FY2028E; downside FY2027E; upside FY2028E. This is a model stress result, not a prediction of regulatory action or insolvency. No unannounced government support or regulatory relief is assumed. High securities exposure, declining yield paths and growth of operating costs and risk-weighted assets drive the result. Reported capital numerator and RWA at H1 are unavailable, so the model calibrates proxy RWA from FY2025 and the H1 CAR, not book equity. All 15 scenario-year accounting checks pass; capital shortfalls are separately flagged, not hidden.

Liquidity: 2025's 25% reserve requirement was waived (CBG25AR p118). H1 report states nil statutory liquidity defaults, but the present waiver and eligible reserves are not independently known. Applying the shared 20% requirement mechanically to customer deposits gives a 2026E base cash proxy gap of 1,708.369m; this is a standard-requirement stress screen, NOT an actual statutory breach. See checks.md for all cases. Tax at 35% on positive modeled profit with actual H1 tax preserved. No dividends due to accumulated losses, half positive incremental earnings transferred to reserves (consistent with FY2025 and H1). Forecast FX sensitivity is limited to 2025 net USD position and future shared exchange-rate movements, not all currency positions. No assumed sovereign loss repeat.

## Reproduce and limitations

Run `node model.mjs` (Node 18+, no dependencies) in this folder. Inputs financials.csv, assumptions.json and shared macro.csv. Outputs forecast.csv and checks.md. 421 history rows, 855 forecast rows; seven periods and 15 scenario-years. Engine executed in cloud JS; exact committed-output replay separately checked. Annual and interim historical residuals at most 0.001m, before rounding forecast bridges pass. Gross/allowance and cash split unavailable at June; explicitly estimated in model. H1 PDF was retrieved via Firecrawl secondary and parsed, not visually verified; direct web cache missed. Source comparative review and independent model review required. Five annual source periods and two H1 periods retained; Q3 2026 not located in issuer archive. Not audited forecasts or investment advice.
