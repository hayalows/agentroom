# Ghana banking models: accepted-only sector roll-up

Source commit: `50c3f1acc4449cd65389e1e45727bba6ef7d247c`
Input fingerprint: `5d055a122d310c371f2ff2ff5c8cfc3d02c77a4476474098f2c561f42274117f`

**18 of 23 licensed-bank models accepted.** These are partial coverage totals, not the whole banking sector.
Accepted banks: access-bank-ghana, adb, bank-of-africa-ghana, calbank, consolidated-bank-ghana, ecobank-ghana, fbnbank-ghana, fidelity-bank-ghana, first-atlantic-bank, first-national-bank-ghana, gcb, gtbank-ghana, nib, societe-generale-ghana, stanbic-bank-ghana, standard-chartered-ghana, uba-ghana, zenith-bank-ghana.
Provisional or otherwise excluded models appear only in the separate diagnostics and exclusion manifest.

## 1. Coverage against Bank of Ghana aggregates

| Measure | Period | Accepted banks (GHS bn; count) | BoG (GHS bn) | Indicative coverage |
|---|---|---:|---:|---:|
| total_assets | FY2025 | 359.982 (18/18) | 446.9 | 80.55% |
| total_assets | 9M-2026 | 401.905 (17/18) | 513.6 | 78.25% |
| customer_deposits | FY2025 | 265.681 (18/18) | 325.3 | 81.67% |
| customer_deposits | 9M-2026 | 296.920 (17/18) | 372.9 | 79.62% |

Bank-only values compared with same-month sector aggregates; definitions may differ. No net-loan versus gross-advance coverage comparison.

## 2. Historical totals (GHS millions; reporting/eligible banks)

| Item | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | 9M-2026 |
|---|---:|---:|---:|---:|---:|---:|
| total_assets | 148,546.126 (18/18) | 176,658.990 (18/18) | 228,224.385 (18/18) | 307,636.069 (18/18) | 359,981.883 (18/18) | 401,904.984 (17/18) |
| customer_deposits | 101,351.224 (18/18) | 134,837.141 (18/18) | 177,348.361 (18/18) | 236,182.286 (18/18) | 265,681.178 (18/18) | 296,920.131 (17/18) |
| loans_and_advances_net | 37,077.775 (18/18) | 49,025.390 (18/18) | 51,568.614 (18/18) | 62,629.881 (18/18) | 75,393.015 (18/18) | 98,981.878 (17/18) |
| total_equity | 21,203.793 (18/18) | 15,471.376 (18/18) | 23,507.280 (18/18) | 33,849.806 (18/18) | 49,372.209 (18/18) | 52,524.068 (17/18) |
| profit_after_tax | 3,936.845 (18/18) | -5,393.076 (18/18) | 5,552.401 (18/18) | 9,068.473 (18/18) | 12,016.737 (18/18) | 8,772.525 (17/18) |
| operating_income_pre_impairment | 13,669.487 (17/18) | 17,832.777 (17/18) | 27,789.077 (18/18) | 31,523.924 (18/18) | 36,620.514 (18/18) | 24,752.443 (16/18) |
| net_interest_income | 10,124.495 (18/18) | 12,859.649 (18/18) | 18,158.547 (18/18) | 22,093.456 (18/18) | 24,751.926 (18/18) | 16,317.019 (17/18) |

Only reported or derived historical observations are included; unavailable and estimated historical rows are excluded. Pre-impairment operating income is recomputed from net interest income + net fees + net trading + other operating income; incomplete components remain missing.

## 3. FY2025 bank comparison

| Bank | Assets | Deposits | Net loans | Equity | PAT | Net LDR % | Closing-equity ROE % | Cost/income % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gcb | 52,398.519 | 41,048.267 | 16,038.002 | 6,008.709 | 2,043.968 | 39.07 | 34.02 | 46.87 |
| ecobank-ghana | 46,076.237 | 30,397.499 | 13,058.608 | 7,073.808 | 1,792.352 | 42.96 | 25.34 | 34.45 |
| stanbic-bank-ghana | 36,708.145 | 24,013.184 | 7,652.776 | 5,739.331 | 1,608.667 | 31.87 | 28.03 | 40.41 |
| zenith-bank-ghana | 26,702.820 | 20,825.728 | 7,210.226 | 3,049.986 | 997.714 | 34.62 | 32.71 | 30.40 |
| fidelity-bank-ghana | 25,982.029 | 17,212.890 | 4,743.015 | 2,769.753 | 916.822 | 27.56 | 33.10 | 44.29 |
| gtbank-ghana | 21,201.620 | 18,049.481 | 3,429.641 | 3,041.231 | 1,012.223 | 19.00 | 33.28 | 25.53 |
| first-atlantic-bank | 19,191.093 | 16,642.450 | 1,947.025 | 2,207.634 | 483.607 | 11.70 | 21.91 | 39.83 |
| access-bank-ghana | 19,022.897 | 14,542.546 | 5,057.262 | 2,044.432 | 286.469 | 34.78 | 14.01 | 53.18 |
| adb | 17,887.521 | 13,220.185 | 2,011.731 | 2,477.839 | 367.291 | 15.22 | 14.82 | 52.16 |
| consolidated-bank-ghana | 17,857.592 | 14,530.430 | 1,519.804 | 1,497.080 | 7.384 | 10.46 | 0.49 | 85.27 |
| standard-chartered-ghana | 16,502.639 | 12,385.298 | 1,887.422 | 2,809.821 | 798.681 | 15.24 | 28.42 | 45.99 |
| nib | 12,224.654 | 10,197.188 | 731.014 | 1,549.336 | 343.915 | 7.17 | 22.20 | 51.55 |
| calbank | 11,899.483 | 8,657.596 | 1,070.880 | 1,528.442 | 306.412 | 12.37 | 20.05 | 67.20 |
| uba-ghana | 11,541.568 | 8,590.385 | 1,277.050 | 1,895.745 | 407.104 | 14.87 | 21.47 | 39.74 |
| societe-generale-ghana | 9,676.100 | 5,843.183 | 4,491.827 | 2,601.775 | 397.001 | 76.87 | 15.26 | 57.15 |
| first-national-bank-ghana | 6,484.459 | 4,151.503 | 1,208.202 | 1,003.049 | 106.813 | 29.10 | 10.65 | 80.57 |
| fbnbank-ghana | 4,598.313 | 2,756.507 | 860.191 | 1,041.455 | 16.703 | 31.21 | 1.60 | 85.97 |
| bank-of-africa-ghana | 4,026.194 | 2,616.858 | 1,198.339 | 1,032.783 | 123.611 | 45.79 | 11.97 | 48.71 |

Combined ratios use only banks with both observations and positive denominators. Closing-equity ROE is not comparable to an average-equity or differently defined BoG ROE. No averages of individual bank ratios.

| Ratio | Matched-bank value % |
|---|---:|
| net_ldr | 28.38 (18/18) |
| closing_equity_roe | 24.34 (18/18) |
| cost_to_income | 45.75 (18/18) |

## 4. Scenario totals (GHS millions; reporting/eligible banks)

Forecasts are model estimates on shared macro paths, not audited results or guaranteed outcomes. Different calibration, capital proxies and unfunded stress cases limit interpretation.

### profit_after_tax

| Scenario | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| base | 11,409.757 (18/18) | 12,677.259 (18/18) | 13,833.341 (18/18) | 14,847.027 (18/18) | 16,709.192 (18/18) |
| downside | 9,008.658 (18/18) | 9,151.966 (18/18) | 8,539.685 (18/18) | 6,679.077 (18/18) | 5,121.921 (18/18) |
| upside | 12,022.944 (18/18) | 14,375.801 (18/18) | 16,705.245 (18/18) | 19,796.241 (18/18) | 23,702.145 (18/18) |

### total_assets

| Scenario | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| base | 433,064.479 (18/18) | 494,732.148 (18/18) | 566,684.873 (18/18) | 647,052.503 (18/18) | 738,591.609 (18/18) |
| downside | 417,872.748 (18/18) | 464,850.436 (18/18) | 515,331.346 (18/18) | 568,587.488 (18/18) | 623,219.002 (18/18) |
| upside | 441,082.200 (18/18) | 514,710.685 (18/18) | 604,314.636 (18/18) | 711,045.695 (18/18) | 839,975.774 (18/18) |

### total_equity

| Scenario | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| base | 56,383.662 (18/18) | 65,732.962 (18/18) | 76,121.794 (18/18) | 87,078.510 (18/18) | 99,404.601 (18/18) |
| downside | 54,151.999 (18/18) | 62,305.352 (18/18) | 69,661.108 (18/18) | 75,001.554 (18/18) | 78,868.517 (18/18) |
| upside | 56,860.137 (18/18) | 66,861.043 (18/18) | 78,793.058 (18/18) | 93,219.470 (18/18) | 110,513.219 (18/18) |

## 5. Excluded models

| Bank | Status | Review stage |
|---|---|---|
| absa-ghana | needs-review | re-review-required |
| omnibsic-bank | in-progress | in-progress |
| prudential-bank | needs-review | re-review-required |
| republic-bank-ghana | needs-review | repairs-required |
| umb | in-progress | in-progress |

See provisional.csv for separate non-accepted bank-level diagnostics. No provisional figures are added to accepted totals. See manifest.json for exact review, package and macro evidence and output hashes.

