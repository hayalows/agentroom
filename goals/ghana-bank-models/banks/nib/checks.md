# NIB validation and sensitivity

408 historical rows; 960 forecast rows, 15 scenario-years. 59 historical detailed bridges, 135 forecast bridges, 15 equity roll-forwards. Maximum historical error 0.001m, forecast unrounded 0.000m. Q3 equity component sum differs from reported 0.001m; historical numbers unchanged, model opening equity uses component sum. No independent acceptance yet.

FY25 regulatory capital 1164.049m and RWA2146.629m, reported CAR54.23%. Estimated Q3 RWA 2916.093m, cap 895.240m, CET1 836.919m calibrated to reported CAR30.70% and CET1 28.70%. 100% net-loan proxy plus residual risk density 12.317%; not actual regulatory weights. Separate +50% residual density and 80% positive profit eligibility sensitivities. Estimated starting securities yield 10.936%, cost of funds 5.050%, earning cash fraction 46.527%, central bank balance fraction 41.067%. Repricing weights and reset speeds assumed, not issuer contractual maturities. Frozen FY26 rates on FY25 average stocks predict interest income 784.716m vs 1225.243m actual: different rate regime, not a passed backtest.

| Scenario | Year | PAT m | CAR % | 80% eligible CAR % | Higher RWA density CAR % | 13% gap m | CB-share reserve proxy gap m | 10% deposit runoff gap m | Retained earnings m |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 152.850 | 31.151 | 30.844 | 24.221 | 0.000 | 1563.252 | 2631.828 | -2275.404 |
| base | FY2027E | 134.146 | 30.972 | 29.933 | 24.242 | 0.000 | 1718.844 | 2924.999 | -2158.027 |
| base | FY2028E | 173.282 | 30.886 | 29.137 | 24.380 | 0.000 | 1913.364 | 3281.144 | -2006.405 |
| base | FY2029E | 203.365 | 30.880 | 28.511 | 24.575 | 0.000 | 2135.940 | 3684.048 | -1828.460 |
| base | FY2030E | 188.503 | 30.233 | 27.485 | 24.213 | 0.000 | 2396.331 | 4148.541 | -1663.521 |
| downside | FY2026E | 38.032 | 31.095 | 31.095 | 23.780 | 0.000 | 1421.348 | 2416.590 | -2375.870 |
| downside | FY2027E | -16.659 | 29.772 | 29.772 | 22.511 | 0.000 | 1508.894 | 2577.087 | -2392.529 |
| downside | FY2028E | -54.662 | 26.932 | 26.932 | 20.180 | 0.000 | 1628.159 | 2775.052 | -2447.191 |
| downside | FY2029E | -133.834 | 21.018 | 21.018 | 15.730 | 0.000 | 1820.427 | 3052.190 | -2581.025 |
| downside | FY2030E | -276.451 | 11.171 | 11.171 | 8.355 | 56.498 | 2070.559 | 3387.066 | -2857.476 |
| upside | FY2026E | 168.134 | 30.018 | 29.632 | 23.513 | 0.000 | 1605.733 | 2705.737 | -2262.030 |
| upside | FY2027E | 174.163 | 29.573 | 28.340 | 23.451 | 0.000 | 1740.595 | 3009.560 | -2109.637 |
| upside | FY2028E | 203.127 | 28.836 | 26.939 | 23.145 | 0.000 | 1921.630 | 3396.243 | -1931.902 |
| upside | FY2029E | 263.904 | 28.450 | 25.948 | 23.103 | 0.000 | 2144.495 | 3861.129 | -1700.986 |
| upside | FY2030E | 294.648 | 27.815 | 24.884 | 22.808 | 0.000 | 2420.992 | 4428.425 | -1443.169 |

All 15 periods positive combined cash; non-interest-bearing and central-bank-share reserve screens flag gaps in all periods. This is not evidence of actual regulatory reserve deficiency: current eligible reserve amounts and exemptions unavailable. No funding injection assumed. Downside breaches 13% CAR screen in 2030 (conditional capital gap56.498m), higher-density stress worse. No dividends; retained earnings remain negative in all scenarios. Deposit for shares3425.621m is not added to stated capital or injected again. FY26 Q4 statutory reserve transfer 12.5% of cumulative positive PAT; observed YTD transfer zero. FY25 annual source transfer 42.989m supports rate. Associate profit model kept separate in memo, not double counted. FX not modeled separately; net exposure not extracted.

## Gross loan opening sensitivity
Alternative 40% allowance share rather than FY25 51.60% retains reported net loans but changes gross/allowance opening and subsequent loan/impairment forecasts. No change in opening net-loan RWA. FY2030:

| Scenario | PAT m | CAR % | 13% gap m |
|---|---:|---:|---:|
| base | 157.160 | 27.020 | 0.000 |
| downside | -275.234 | 4.476 | 246.534 |
| upside | 245.090 | 25.477 | 0.000 |

Source note page numbers and visual verification remain pending. Run node model.mjs from this folder for forecast.csv; exact fetched pure engine replay required before submission.

## Round 2 additional diagnostics
427 history / 975 forecast rows; exact engine replay of original 960 rows matches byte-for-byte, unchanged in revised output. 15 additional eligibility ratio memos. FY25 recapitalization bridge 650+1471.972+385-450.907=2056.065m; net bond1021.065, noncash1406.065. Net securities FY25 and FY24 sum7414.832/3491.058m. Restricted cash note exceeds central bank face amount; no regulatory compliance claim. Hypothetical fixed deduction342.5621m from modeled regulatory capital only (10% of shares deposit); no book asset/impairment changes. FY2030 stress rows:
"nib","FY2030E","ratios","x_car_shares_deposit_haircut_pct","23.9210","percent","assumptions.json; ../../sector/macro-assumptions/macro.csv","","estimated","Estimated ratio or stress proxy","base"
"nib","FY2030E","ratios","x_car_shares_deposit_haircut_pct","0.0827","percent","assumptions.json; ../../sector/macro-assumptions/macro.csv","","estimated","Estimated ratio or stress proxy","downside"
"nib","FY2030E","ratios","x_car_shares_deposit_haircut_pct","22.7809","percent","assumptions.json; ../../sector/macro-assumptions/macro.csv","","estimated","Estimated ratio or stress proxy","upside"

Fast share sensitivity, FY2030 PAT GHS m (other drivers fixed):
| Fast share | Base | Downside | Upside |
|---|---:|---:|---:|
| 25% | 219.385 | -256.928 | 341.645 |
| 50% | 188.503 | -276.451 | 294.648 |
| 75% | 157.620 | -296.236 | 247.650 |
No contractual repricing inferred. Current model function executed in isolated JS, no independent Node CLI claimed.
