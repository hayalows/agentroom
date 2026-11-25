# Ghana banking models: accepted-only sector roll-up

Source commit: `3f6569746a996d4c64673579611cc14e92c8164e`
Input fingerprint: `76fe50c0973cad8f35c25bbd3b8e712b881b2c766350e302a1a9eea88b0a157f`

**16 of 23 licensed-bank models accepted.** These are partial coverage totals, not the whole banking sector.
Accepted banks: access-bank-ghana, adb, bank-of-africa-ghana, consolidated-bank-ghana, ecobank-ghana, fbnbank-ghana, fidelity-bank-ghana, first-atlantic-bank, first-national-bank-ghana, gcb, gtbank-ghana, nib, societe-generale-ghana, standard-chartered-ghana, uba-ghana, zenith-bank-ghana.
Provisional or otherwise excluded models appear only in the separate diagnostics and exclusion manifest.

## 1. Coverage against Bank of Ghana aggregates

| Measure | Period | Accepted banks (GHS bn; count) | BoG (GHS bn) | Indicative coverage |
|---|---|---:|---:|---:|
| total_assets | FY2025 | 311.374 (16/16) | 446.9 | 69.67% |
| total_assets | 9M-2026 | 344.112 (15/16) | 513.6 | 67.00% |
| customer_deposits | FY2025 | 233.010 (16/16) | 325.3 | 71.63% |
| customer_deposits | 9M-2026 | 256.993 (15/16) | 372.9 | 68.92% |

Bank-only values compared with same-month sector aggregates; definitions may differ. No net-loan versus gross-advance coverage comparison.

## 2. Historical totals (GHS millions; reporting/eligible banks)

| Item | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | 9M-2026 |
|---|---:|---:|---:|---:|---:|---:|
| total_assets | 124,490.651 (16/16) | 148,842.285 (16/16) | 193,721.414 (16/16) | 263,386.454 (16/16) | 311,374.255 (16/16) | 344,111.650 (15/16) |
| customer_deposits | 86,252.593 (16/16) | 114,124.657 (16/16) | 151,780.080 (16/16) | 203,578.550 (16/16) | 233,010.398 (16/16) | 256,993.441 (15/16) |
| loans_and_advances_net | 29,653.127 (16/16) | 39,405.180 (16/16) | 42,824.493 (16/16) | 52,681.169 (16/16) | 66,669.359 (16/16) | 87,900.080 (15/16) |
| total_equity | 17,993.314 (16/16) | 13,267.075 (16/16) | 20,715.313 (16/16) | 29,501.806 (16/16) | 42,104.436 (16/16) | 45,157.174 (15/16) |
| profit_after_tax | 3,316.416 (16/16) | -4,515.281 (16/16) | 4,952.264 (16/16) | 7,649.478 (16/16) | 10,101.658 (16/16) | 7,547.070 (15/16) |
| operating_income_pre_impairment | 11,626.915 (15/16) | 15,332.772 (15/16) | 23,645.673 (16/16) | 27,097.302 (16/16) | 31,289.334 (16/16) | 20,959.331 (14/16) |
| net_interest_income | 9,002.743 (16/16) | 11,118.894 (16/16) | 15,657.720 (16/16) | 19,130.394 (16/16) | 21,415.499 (16/16) | 14,113.224 (15/16) |

Only reported or derived historical observations are included; unavailable and estimated historical rows are excluded. Pre-impairment operating income is recomputed from net interest income + net fees + net trading + other operating income; incomplete components remain missing.

## 3. FY2025 bank comparison

| Bank | Assets | Deposits | Net loans | Equity | PAT | Net LDR % | Closing-equity ROE % | Cost/income % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gcb | 52,398.519 | 41,048.267 | 16,038.002 | 6,008.709 | 2,043.968 | 39.07 | 34.02 | 46.87 |
| ecobank-ghana | 46,076.237 | 30,397.499 | 13,058.608 | 7,073.808 | 1,792.352 | 42.96 | 25.34 | 34.45 |
| zenith-bank-ghana | 26,702.820 | 20,825.728 | 7,210.226 | 3,049.986 | 997.714 | 34.62 | 32.71 | 30.40 |
| fidelity-bank-ghana | 25,982.029 | 17,212.890 | 4,743.015 | 2,769.753 | 916.822 | 27.56 | 33.10 | 44.29 |
| gtbank-ghana | 21,201.620 | 18,049.481 | 3,429.641 | 3,041.231 | 1,012.223 | 19.00 | 33.28 | 25.53 |
| first-atlantic-bank | 19,191.093 | 16,642.450 | 1,947.025 | 2,207.634 | 483.607 | 11.70 | 21.91 | 39.83 |
| access-bank-ghana | 19,022.897 | 14,542.546 | 5,057.262 | 2,044.432 | 286.469 | 34.78 | 14.01 | 53.18 |
| adb | 17,887.521 | 13,220.185 | 2,011.731 | 2,477.839 | 367.291 | 15.22 | 14.82 | 52.16 |
| consolidated-bank-ghana | 17,857.592 | 14,530.430 | 1,519.804 | 1,497.080 | 7.384 | 10.46 | 0.49 | 85.27 |
| standard-chartered-ghana | 16,502.639 | 12,385.298 | 1,887.422 | 2,809.821 | 798.681 | 15.24 | 28.42 | 45.99 |
| nib | 12,224.654 | 10,197.188 | 731.014 | 1,549.336 | 343.915 | 7.17 | 22.20 | 51.55 |
| uba-ghana | 11,541.568 | 8,590.385 | 1,277.050 | 1,895.745 | 407.104 | 14.87 | 21.47 | 39.74 |
| societe-generale-ghana | 9,676.100 | 5,843.183 | 4,491.827 | 2,601.775 | 397.001 | 76.87 | 15.26 | 57.15 |
| first-national-bank-ghana | 6,484.459 | 4,151.503 | 1,208.202 | 1,003.049 | 106.813 | 29.10 | 10.65 | 80.57 |
| fbnbank-ghana | 4,598.313 | 2,756.507 | 860.191 | 1,041.455 | 16.703 | 31.21 | 1.60 | 85.97 |
| bank-of-africa-ghana | 4,026.194 | 2,616.858 | 1,198.339 | 1,032.783 | 123.611 | 45.79 | 11.97 | 48.71 |

Combined ratios use only banks with both observations and positive denominators. Closing-equity ROE is not comparable to an average-equity or differently defined BoG ROE. No averages of individual bank ratios.

| Ratio | Matched-bank value % |
|---|---:|
| net_ldr | 28.61 (16/16) |
| closing_equity_roe | 23.99 (16/16) |
| cost_to_income | 45.91 (16/16) |

## 4. Scenario totals (GHS millions; reporting/eligible banks)

Forecasts are model estimates on shared macro paths, not audited results or guaranteed outcomes. Different calibration, capital proxies and unfunded stress cases limit interpretation.

### profit_after_tax

| Scenario | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| base | 9,811.980 (16/16) | 11,282.232 (16/16) | 12,396.599 (16/16) | 13,369.476 (16/16) | 15,076.204 (16/16) |
| downside | 8,369.645 (16/16) | 7,642.884 (16/16) | 7,061.454 (16/16) | 5,671.680 (16/16) | 4,492.685 (16/16) |
| upside | 10,283.826 (16/16) | 12,954.280 (16/16) | 15,114.081 (16/16) | 17,883.704 (16/16) | 21,398.924 (16/16) |

### total_assets

| Scenario | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| base | 373,165.241 (16/16) | 427,014.363 (16/16) | 489,911.532 (16/16) | 560,288.713 (16/16) | 640,499.276 (16/16) |
| downside | 360,929.298 (16/16) | 401,197.556 (16/16) | 444,496.104 (16/16) | 490,414.649 (16/16) | 537,731.058 (16/16) |
| upside | 379,521.019 (16/16) | 443,287.457 (16/16) | 520,888.713 (16/16) | 613,110.297 (16/16) | 724,300.000 (16/16) |

### total_equity

| Scenario | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| base | 48,751.183 (16/16) | 57,114.681 (16/16) | 66,488.755 (16/16) | 76,481.943 (16/16) | 87,744.482 (16/16) |
| downside | 47,371.547 (16/16) | 54,015.819 (16/16) | 59,949.836 (16/16) | 64,334.581 (16/16) | 67,622.616 (16/16) |
| upside | 49,183.498 (16/16) | 58,310.297 (16/16) | 69,279.396 (16/16) | 82,381.364 (16/16) | 97,967.742 (16/16) |

## 5. Excluded models

| Bank | Status | Review stage |
|---|---|---|
| absa-ghana | in-progress | in-progress |
| calbank | needs-review | re-review-required |
| omnibsic-bank | in-progress | in-progress |
| prudential-bank | needs-review | peer-review-required |
| republic-bank-ghana | needs-review | repairs-required |
| stanbic-bank-ghana | needs-review | lead-resolution-required |
| umb | in-progress | in-progress |

See provisional.csv for separate non-accepted bank-level diagnostics. No provisional figures are added to accepted totals. See manifest.json for exact review, package and macro evidence and output hashes.

