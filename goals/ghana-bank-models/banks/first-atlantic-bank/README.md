# First Atlantic Bank PLC — standalone Ghana bank model

Status: submitted for independent review. Listed on Ghana Stock Exchange 19 December 2025; FY25 largest shareholders Kedari Nominees 46.6%, AFIG Fund II 21.0% (issuer audited appendix). Excludes Liberia subsidiary consolidation; includes bank investment in subsidiary. Five annual periods plus two cumulative interims; sources in sources.md.

| Period | Assets m | PAT m | Equity m | CAR % |
|---|---:|---:|---:|---:|
| FY2021 | 4675.001 | 116.358 | 715.145 | 22 |
| FY2022 | 7428.291 | -0.157 | 969.253 | 18 |
| FY2023 | 10466.259 | 290.901 | 1260.154 | 17 |
| FY2024 | 13323.324 | 336.679 | 1596.833 | 16.98 |
| FY2025 | 19191.093 | 483.607 | 2207.634 | 20.61 |
| 9M2026 | 21752.334 | 260.884 | 2368.517 | 14.54 |

2022 impairment 229.824m; 2023 DDEP modification loss 289.120m separately memoed, included in normalized impairment. FY2025 capital increase includes 202.194m external issue and 117.163m bonus share transfer. The latter is not external capital. 2024 DDEP regulatory capital relief 279.818m, zero 2025. FY25 bank other assets include e-money 4916.141m, backed by cash per source. September 2026 deposits 19018.718m, net loans 2527.127m, NPL11.20%, CAR14.54%. Actual 9M dividends 100m and net impairment reversal3.702m.

## Forecast FY2026E–FY2030E
| Scenario | 2026 PAT m | 2030 PAT m | 2030 assets m | 2030 CAR % | 2030 reserve gap m | 2030 additive runoff gap m |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | 358.422 | 936.515 | 39082.943 | 24.541 | 625.377 | 1588.375 |
| downside | 302.232 | 300.067 | 28400.172 | 20.215 | 255.906 | 843.726 |
| upside | 378.516 | 1174.766 | 44509.530 | 24.396 | 677.896 | 1757.800 |

All scenarios remain above the shared 13% capital screen; cash reserve and additive settlement screens identify material gaps as deposit and lending growth outpace free cash. Base 2030 estimated CAR 24.54% with no incremental dividends after observed 9M2026 dividend; 80% profit-eligibility stress 21.24%, separate FX stress 23.68%. Capital and eligible reserves are proxies, not regulatory returns. No funding plug; reported cash is combined bank balances, not unrestricted eligible liquidity. Source-repricing profile, FX sign caveat, e-money and reserve assumptions are explicit. Shared macro.csv drives rates, GDP, CPI, FX and prudential screens. Run node model.mjs from this folder to reproduce forecast.csv; exact fetched engine replay matched, 66 core identities passed. 414 history and 900 forecast rows. Round 1 independent calculation replay and Q3 text source checks passed; older and interim PDF images remain unavailable. Not investment advice.

## Round 2 risk repairs

FY25 actual mandatory BoG cash 18.395% of combined cash vs FY24 56.922%; no claim of current eligibility. Added separate FY25-share reserve stress and same non-interest-pool deposit/e-money runoff sensitivity. Deposit beta .2/.4/.6 tested; no central forecasts changed. See checks.md for exact results, source cash-flow restatement and interest-sensitivity limitations in sources.md. Await independent re-review.
