# Model checks

History 308 rows; forecast 1035 rows; 176 accounting identities, max residual 2.000e-6 GHS m (before rounding). All pass at 0.005m.
Missing gross/allowance, actual regulatory capital numerator/RWA, and actual eligible CRR are not tested or assumed known.

## Calibration

- yieldS: 10.8325%
- yieldL: 15.8325%
- yieldC: 1.6249%
- funding: 1.6782%
- netCor: 6.7348%
- cashRatio: 45.8345%

## Scenario results (GHS m; CAR proxy %)

| Scenario | Year | PAT | Assets | CAR proxy | 80% eligibility | Half-cash CRR gap | Securities | Dividends | Retained earnings |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | 73.782 | 4636.524 | 26.967 | 26.831 | 0.000 | 1304.942 | 180.000 | 83.171 |
| base | FY2027E | 97.730 | 5175.126 | 26.404 | 25.776 | 0.000 | 1430.750 | 11.067 | 145.401 |
| base | FY2028E | 115.660 | 5805.617 | 25.867 | 24.773 | 0.000 | 1576.933 | 14.659 | 217.486 |
| base | FY2029E | 132.631 | 6510.021 | 25.440 | 23.919 | 0.000 | 1741.908 | 17.349 | 299.610 |
| base | FY2030E | 153.763 | 7308.722 | 25.113 | 23.195 | 0.000 | 1931.508 | 19.895 | 395.038 |
| downside | FY2026E | 64.421 | 4579.527 | 27.029 | 26.946 | 0.000 | 1228.056 | 180.000 | 76.150 |
| downside | FY2027E | 51.443 | 4894.646 | 26.696 | 26.337 | 0.000 | 1301.393 | 0.000 | 114.733 |
| downside | FY2028E | 52.499 | 5230.943 | 26.325 | 25.720 | 0.000 | 1378.366 | 0.000 | 154.107 |
| downside | FY2029E | 39.834 | 5576.030 | 25.652 | 24.893 | 0.000 | 1445.648 | 0.000 | 183.983 |
| downside | FY2030E | 26.126 | 5907.442 | 24.806 | 23.971 | 0.000 | 1500.216 | 0.000 | 203.577 |
| upside | FY2026E | 80.023 | 4670.351 | 26.951 | 26.780 | 0.000 | 1308.045 | 180.000 | 87.852 |
| upside | FY2027E | 130.564 | 5358.390 | 26.354 | 25.552 | 0.000 | 1446.360 | 16.005 | 169.770 |
| upside | FY2028E | 162.887 | 6195.218 | 25.751 | 24.354 | 0.000 | 1606.165 | 26.113 | 265.822 |
| upside | FY2029E | 204.341 | 7194.810 | 25.372 | 23.407 | 0.000 | 1797.055 | 32.577 | 386.500 |
| upside | FY2030E | 255.972 | 8408.172 | 25.137 | 22.641 | 0.000 | 2026.639 | 40.868 | 569.608 |

Capital screen below assumed minimum: 0/15. Negative securities: 0/15. Half-cash CRR gap positive: 0/15. These are diagnostics, not actual regulatory breaches.
Historical FY2025 and 9M2026 spot figures: assets 4026.194/4512.378, PAT 123.611/50.242, deposits 2616.858/3206.582; source register records source verification and limitations.
No independent review claimed. Model recomputes with shared macro.csv. The generated outputs were calculated by the same JS function used in model.mjs; full CLI replay requested from independent reviewer.

## Additional independent-review sensitivities

Frozen FY26 implied rates on FY24/FY25 average exposures: interest income 314.575 vs actual 463.031; interest expense 54.494 vs actual 92.136 GHS m. Different rate regimes, not a backtest.
Base FY2030 PAT: fast repricing 25% 158.167m, central 153.763m, 75% 149.413m. Recomputed using same engine and inputs, changing one estimated driver.

| Scenario | Year | CAR density +20% | Joint density/eligibility | 40%-eligible cash gap m | Alternative incremental dividend cap m |
|---|---|---:|---:|---:|---:|
| base | FY2026E | 22.472 | 22.359 | 55.008 | 0.000 |
| base | FY2027E | 22.003 | 21.480 | 62.090 | 0.000 |
| base | FY2028E | 21.555 | 20.644 | 70.410 | 0.000 |
| base | FY2029E | 21.200 | 19.932 | 79.693 | 0.000 |
| base | FY2030E | 20.928 | 19.329 | 90.200 | 0.000 |
| downside | FY2026E | 22.524 | 22.455 | 28.197 | 0.000 |
| downside | FY2027E | 22.247 | 21.948 | 30.264 | 0.000 |
| downside | FY2028E | 21.937 | 21.433 | 32.494 | 0.000 |
| downside | FY2029E | 21.377 | 20.745 | 34.898 | 0.000 |
| downside | FY2030E | 20.671 | 19.976 | 37.299 | 0.000 |
| upside | FY2026E | 22.459 | 22.316 | 55.453 | 0.000 |
| upside | FY2027E | 21.962 | 21.294 | 64.525 | 0.000 |
| upside | FY2028E | 21.460 | 20.295 | 75.627 | 0.000 |
| upside | FY2029E | 21.143 | 19.506 | 88.796 | 0.000 |
| upside | FY2030E | 20.948 | 18.867 | 104.726 | 0.000 |

The lower cash-eligibility payout screen is separate from the central case; no regulatory approval assumed. CAR estimates are diagnostic only.
