# First Atlantic dynamic model checks

- 404 historical and 870 forecast rows. 5 annual, 2 interim, 15 scenario-years. No schema errors/duplicates. 66/66 rounded core identities, max 0.001m. 61 full historical bridges, 135 forecast bridges and 15 equity roll-forwards pass. FY21 and FY24 source rounding; Q3 2026 reported tax components vs PAT residual 0.001m retained through FY26. Tolerance GHS0.005m. Exact fetched JS engine replay reproduced committed forecast.csv byte-for-byte; not external Node CLI.
- Reported FY25 capital 1745.571m and RWA 8469.738m; Q3 estimated RWA 9813.618m and capital 1426.900m, fitted to reported CAR14.54%. Estimated regulatory capital, not accounting equity. 80% eligibility stress and separate adverse FX sensitivity; no actual capital numerator or Tier1 at Q3.
- FY25 securities repricing within year 29.236%, earning cash share 36.881%; assumed slow reset20% annually. Q3 fitted securities yield 14.229%, deposit funding cost 1.840%. Frozen FY26 yields on FY24/25 stocks produce 792.377m vs reported FY25 interest income 1430.665m, NOT a backtest; different rate regime illustrates limit. Funding beta 40% assumption, not fitted to disclosed full contractual gap. Source p87 repricing loan total differs 0.022m vs balance sheet; no reconciliation invented.
- 9M actual equity bridge: 2207.634 +260.884 -100=2368.518m vs reported2368.517m (0.001m rounding). No new capital assumed, actual dividends paid already included. FY26 model reserves use full-year positive PAT because no 9M statutory reserve transfer. Statutory reserve band from opening balance only. Incremental dividend cap includes reserve proxy and capital buffer; no incremental dividend in any modeled year.
- Other assets contain material cash-backed e-money; estimated separate e-money grows with deposits. Non-interest-bearing cash proxy compared to shared CRR; separate additive 10% deposit runoff +10% e-money settlement stress conservatively allows overlap. Not a regulatory liquidity test or a forecast of actual deposit withdrawal. No hidden borrowing or artificial cash injection.
- FX adverse screen uses absolute disclosed 5.307m per 1% currency move from FY25, linked to shared USD path (other currencies not modeled); sign of source narrative inconsistent with positive net asset FX position, no central incremental FX gain/loss. Cumulative stress is separate, gross pre-tax and illustrative. DDEP loss not repeated; actual 9M impairment reversal preserved, positive future modeled provisions floor at stock increase.

| Scenario | Year | PAT m | CAR proxy % | 80% eligible CAR % | Adverse FX CAR % | Reserve gap m | Additive runoff gap m |
|---|---|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 358.422 | 15.045 | 14.852 | 15.045 | 0.000 | 134.537 |
| base | FY2027E | 495.995 | 17.384 | 16.363 | 17.000 | 46.532 | 474.368 |
| base | FY2028E | 629.116 | 19.769 | 17.944 | 19.129 | 251.115 | 856.184 |
| base | FY2029E | 781.090 | 22.215 | 19.620 | 21.438 | 429.448 | 1203.731 |
| base | FY2030E | 936.515 | 24.541 | 21.236 | 23.685 | 625.377 | 1588.375 |
| downside | FY2026E | 302.232 | 15.346 | 15.259 | 15.346 | 0.000 | 0.000 |
| downside | FY2027E | 219.949 | 16.537 | 16.025 | 15.685 | 0.000 | 0.000 |
| downside | FY2028E | 234.457 | 17.644 | 16.734 | 16.228 | 0.000 | 209.854 |
| downside | FY2029E | 283.754 | 18.940 | 17.602 | 17.161 | 72.174 | 524.423 |
| downside | FY2030E | 300.067 | 20.215 | 18.474 | 18.202 | 255.906 | 843.726 |
| upside | FY2026E | 378.516 | 14.846 | 14.620 | 14.846 | 0.000 | 236.572 |
| upside | FY2027E | 585.222 | 17.414 | 16.264 | 17.193 | 77.108 | 543.476 |
| upside | FY2028E | 755.406 | 19.910 | 17.897 | 19.576 | 256.658 | 900.432 |
| upside | FY2029E | 947.698 | 22.272 | 19.476 | 21.871 | 455.375 | 1301.244 |
| upside | FY2030E | 1174.766 | 24.396 | 20.907 | 23.963 | 677.896 | 1757.800 |

CAR below 13%: 0/15. Reserve proxy gaps: 10/15. Additive runoff gaps: 13/15. Negative cash: 0/15. All modeled amounts conditional, no regulatory certification. Independent review pending; source screenshots older notes missed, Q3 Firecrawl parsed only.
