# Fidelity Bank — dynamic validation

Status: steward self-check only; independent review pending. Model replay from the exact committed source produced byte-identical forecast.csv. No external Node CLI execution claimed; JavaScript engine executed in the tool environment.

- History: 340 rows, 5 annual + 2 interim periods. Forecast: 1005 rows, 15 scenario-years. Schema errors 0, duplicate keys 0.
- Core arithmetic: 66/66 passes on rounded CSV; tolerance GHS 0.005m. Full history bridges: 61, full model forecast bridges: 135, plus 15 forecast equity roll-forwards. All passed before rounding.
- Actual Q3 equity: 2769.753 + 524.854 - 11.738 OCI - 317.438 dividends = 2965.431. Q4 only modeled, dividend paid already reflected in Q3 equity.
- Q3 estimated opening RWA 12358.64m, regulatory capital 2290.06m, CET1 1894.58m; calibrated to actual 18.53% and 15.33% ratios. Not reported Q3 absolute capital.
- Repricing: securities 73.63% within year; loans 45.99% within year; earning cash 16.10% of combined cash. Fitted securities yield 10.79%, funding cost 2.92%, funding beta 43.49%. +100bp static fit 25.71m matches reported 25.713m by construction, not validation. Frozen FY26 rates applied to FY24/25 balance averages give FY25 income 1806.26m vs actual 3162.81m: not a historical backtest; demonstrates rate regime sensitivity and limits of extrapolation. Slow reset 25% annually is a judgment.
- No CAR below standard 13% screen, no negative cash, no proxy reserve shortfall in these scenarios. This does NOT prove legal capital, liquidity or reserve compliance. Actual eligible reserve balance and full regulatory adjustments unavailable. 80% positive profit eligibility sensitivity included. NPL path independently assumed, not implied by allowance.
- Downside CAR exceeds base as no incremental dividend is paid and RWA grows more slowly. Not a claim that downside is safer. Profit downside < base < upside in all five years.

| Scenario | Year | PAT m | Assets m | CAR proxy | 80% eligible CAR | Full-year dividends m | Reserve proxy gap m |
|---|---|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 703.99 | 31273.10 | 18.83% | 18.55% | 380.14 | 0.00 |
| base | FY2027E | 884.51 | 35684.76 | 20.24% | 18.80% | 309.58 | 0.00 |
| base | FY2028E | 1013.39 | 40872.22 | 21.36% | 18.92% | 354.69 | 0.00 |
| base | FY2029E | 1176.00 | 46735.27 | 22.36% | 19.06% | 411.60 | 0.00 |
| base | FY2030E | 1351.12 | 53425.82 | 23.22% | 19.17% | 472.89 | 0.00 |
| downside | FY2026E | 560.78 | 29953.35 | 19.12% | 19.07% | 317.44 | 0.00 |
| downside | FY2027E | 597.67 | 33237.30 | 22.04% | 21.08% | 0.00 | 0.00 |
| downside | FY2028E | 591.48 | 36791.91 | 24.31% | 22.61% | 0.00 | 0.00 |
| downside | FY2029E | 533.28 | 40591.06 | 25.73% | 23.49% | 0.00 | 0.00 |
| downside | FY2030E | 461.08 | 44471.41 | 26.49% | 23.88% | 0.00 | 0.00 |
| upside | FY2026E | 752.03 | 32024.61 | 18.41% | 18.07% | 419.67 | 0.00 |
| upside | FY2027E | 959.68 | 36812.58 | 19.15% | 17.61% | 431.86 | 0.00 |
| upside | FY2028E | 1147.34 | 42629.68 | 19.70% | 17.13% | 516.30 | 0.00 |
| upside | FY2029E | 1394.30 | 49494.31 | 20.21% | 16.74% | 627.44 | 0.00 |
| upside | FY2030E | 1693.67 | 57741.13 | 20.63% | 16.38% | 762.15 | 0.00 |

Independent reviewer should inspect source pages, confirm historical claims/units and run node model.mjs, check assumption sensitivity and regulatory interpretation before acceptance.

## Round 2 liquidity sensitivity
FY25 central bank balance 5988.449m (71.4553% of aggregate cash); non-interest-bearing proxy 7031.319m exceeds central bank by 1042.870m. Both are estimates for forecast; neither proves reserve eligibility. FY25 98.0% of borrowings are overnight; top20 customer concentration 26.95%. At Q3 2026, 10%/20% borrowings runoff 442.233/884.466m; 10% of estimated top20 customer deposits 544.977m. No actual Q3 concentration reported. Deduct withdrawals from central bank proxy only as a static stress, reduce CRR by customer withdrawal, hold other assets/funding fixed. Dividend cap sensitivity is additional constraint on modeled payout (not a fresh model). No asserted probability or actual breach.

| Scenario | Year | CB-share gap m | 10% wholesale gap | 20% wholesale gap | 20% wholesale + top20 partial gap | CB-share dividend cap | Combined stress dividend cap |
|---|---|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 0.000 | 0.000 | 0.000 | 0.000 | 62.698 | 62.698 |
| base | FY2027E | 0.000 | 0.000 | 0.000 | 0.000 | 309.577 | 309.577 |
| base | FY2028E | 0.000 | 0.000 | 0.000 | 0.000 | 354.687 | 354.687 |
| base | FY2029E | 0.000 | 0.000 | 0.000 | 0.000 | 411.600 | 411.600 |
| base | FY2030E | 0.000 | 0.000 | 0.000 | 0.000 | 472.894 | 472.894 |
| downside | FY2026E | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| downside | FY2027E | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| downside | FY2028E | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| downside | FY2029E | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| downside | FY2030E | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| upside | FY2026E | 0.000 | 0.000 | 0.000 | 0.000 | 102.231 | 102.231 |
| upside | FY2027E | 0.000 | 0.000 | 0.000 | 0.000 | 431.858 | 431.858 |
| upside | FY2028E | 0.000 | 0.000 | 0.000 | 0.000 | 516.305 | 516.305 |
| upside | FY2029E | 0.000 | 0.000 | 0.000 | 0.000 | 627.436 | 627.436 |
| upside | FY2030E | 0.000 | 0.000 | 0.000 | 0.000 | 762.150 | 762.150 |

All central scenario PAT, assets and CAR unchanged. Source page corrections: FY21/22 pp44–45, approved FY25 deposit p150; audited cash split note17 p139, borrowings p151. Additional historical memo rows nonadditive. Rerun exact JS engine before independent review.
