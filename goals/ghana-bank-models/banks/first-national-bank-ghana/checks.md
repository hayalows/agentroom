# Model checks

History 317 rows; forecast 1050 rows; 176 accounting identities, max residual 1.137e-12 GHS m (before rounding). All pass at 0.005m.
Missing gross/allowance, actual regulatory capital numerator/RWA, and actual eligible CRR are not tested or assumed known.

## Calibration

- yieldS: 12.3561%
- yieldL: 17.3561%
- yieldC: 1.8534%
- funding: 4.5237%
- netCor: 0.9227%
- cashRatio: 42.8670%

## Scenario results (GHS m; CAR proxy %)

| Scenario | Year | PAT | Assets | CAR proxy | 80% eligibility | Half-cash CRR gap | Securities | Dividends | Retained earnings |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 72.998 | 7519.930 | 23.980 | 23.872 | 0.000 | 2208.350 | 0.000 | -322.249 |
| base | FY2027E | 104.202 | 8401.435 | 23.542 | 23.030 | 0.000 | 2432.362 | 0.000 | -270.148 |
| base | FY2028E | 135.267 | 9447.198 | 23.336 | 22.400 | 0.000 | 2704.288 | 0.000 | -202.515 |
| base | FY2029E | 166.146 | 10625.919 | 23.368 | 22.012 | 0.000 | 3016.170 | 0.000 | -119.441 |
| base | FY2030E | 204.201 | 11971.855 | 23.599 | 21.824 | 0.000 | 3379.339 | 0.000 | -17.341 |
| downside | FY2026E | 69.274 | 7437.524 | 24.162 | 24.070 | 0.000 | 2084.652 | 0.000 | -324.111 |
| downside | FY2027E | 60.097 | 7971.999 | 23.805 | 23.466 | 0.000 | 2201.729 | 0.000 | -294.063 |
| downside | FY2028E | 53.826 | 8535.947 | 23.289 | 22.761 | 0.000 | 2318.870 | 0.000 | -267.150 |
| downside | FY2029E | 29.183 | 9113.088 | 22.351 | 21.749 | 0.000 | 2418.796 | 0.000 | -252.558 |
| downside | FY2030E | -1.559 | 9661.404 | 21.055 | 20.488 | 0.000 | 2486.652 | 0.000 | -254.117 |
| upside | FY2026E | 74.843 | 7567.395 | 23.870 | 23.755 | 0.000 | 2223.825 | 0.000 | -321.327 |
| upside | FY2027E | 126.008 | 8668.737 | 23.274 | 22.686 | 0.000 | 2534.625 | 0.000 | -258.323 |
| upside | FY2028E | 178.630 | 10038.925 | 23.079 | 21.975 | 0.000 | 2931.710 | 0.000 | -169.008 |
| upside | FY2029E | 246.686 | 11694.551 | 23.347 | 21.692 | 0.000 | 3428.815 | 0.000 | -45.665 |
| upside | FY2030E | 333.641 | 13726.458 | 23.964 | 21.740 | 0.000 | 4057.111 | 0.000 | 121.155 |

Capital screen below assumed minimum: 0/15. Negative securities: 0/15. Half-cash CRR gap positive: 0/15. These are diagnostics, not actual regulatory breaches.
Historical FY2025 and 9M2026 spot figures: assets 6484.459/7323.471, PAT 106.813/48.823, deposits 4151.503/5348.493; source register records source verification and limitations.
No independent review claimed. Model recomputes with shared macro.csv. The generated outputs were calculated by the same JS function used in model.mjs; full CLI replay requested from independent reviewer.

## Additional independent-review sensitivities

Frozen FY26 implied rates on FY24/FY25 average exposures: interest income 449.828 vs actual 648.996; interest expense 207.795 vs actual 295.187 GHS m. Different rate regimes, not a backtest.
Base FY2030 PAT: fast repricing 25% 212.279m, central 204.201m, 75% 196.233m. Recomputed using same engine and inputs, changing one estimated driver.
50% traded-asset earning exposure sensitivity (refit yield to same 9M interest): FY2030 base PAT 192.998m vs central 204.201m. No free liquidity assumed from pledged assets.

| Scenario | Year | CAR density +20% | Joint density/eligibility | 40%-eligible cash gap m | Alternative incremental dividend cap m |
|---|---|---:|---:|---:|---:|
| base | FY2026E | 19.983 | 19.893 | 157.116 | 0.000 |
| base | FY2027E | 19.619 | 19.192 | 177.344 | 0.000 |
| base | FY2028E | 19.447 | 18.667 | 201.108 | 0.000 |
| base | FY2029E | 19.473 | 18.343 | 227.623 | 0.000 |
| base | FY2030E | 19.666 | 18.187 | 257.632 | 0.000 |
| downside | FY2026E | 20.135 | 20.058 | 111.482 | 0.000 |
| downside | FY2027E | 19.838 | 19.555 | 119.653 | 0.000 |
| downside | FY2028E | 19.408 | 18.968 | 128.469 | 0.000 |
| downside | FY2029E | 18.626 | 18.124 | 137.976 | 0.000 |
| downside | FY2030E | 17.546 | 17.073 | 147.468 | 0.000 |
| upside | FY2026E | 19.892 | 19.796 | 158.387 | 0.000 |
| upside | FY2027E | 19.395 | 18.905 | 184.299 | 0.000 |
| upside | FY2028E | 19.233 | 18.313 | 216.010 | 0.000 |
| upside | FY2029E | 19.456 | 18.077 | 253.622 | 0.000 |
| upside | FY2030E | 19.970 | 18.116 | 299.122 | 0.000 |

The lower cash-eligibility payout screen is separate from the central case; no regulatory approval assumed. CAR estimates are diagnostic only.
