# Prudential Bank conditional forecast checks

PROVISIONAL: FY2025 only; 2026 interim inaccessible. Not accepted or current bank results.

Historical: 238 records and 44/44 exact bridges as recorded in sources.md. Forecast: 915 rows, 120 full precision arithmetic identities; max residual 0.0000000000m. Funding cost fit: FY24 6.265% observed / 28.552% average policy; FY25 5.798% / 25.129%; rate = max(1%, 2.3719 + 0.1363 × average policy), 2026 mean policy 14.136%. Inferred FY25 RWA 3049.111m (conditional shortfall method, not actual). Cash and capital gaps are proxy flags, not regulatory findings.

| Scenario | Year | PAT | CAR proxy % | Capital gap m | Cash m | Reserve proxy gap m | Cash eligibility stress gap m | 45% assets RWA CAR | 55% assets RWA CAR |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | FY2026E | -62.654 | 13.662 | 0.000 | 4104.585 | 0.000 | 47.040 | 11.533 | 9.436 |
| base | FY2027E | -48.425 | 11.185 | 65.464 | 4527.112 | 0.000 | 86.996 | 9.391 | 7.684 |
| base | FY2028E | -37.779 | 9.240 | 148.761 | 5044.776 | 0.000 | 127.124 | 7.701 | 6.301 |
| base | FY2029E | -25.176 | 7.834 | 224.420 | 5642.179 | 0.000 | 165.548 | 6.472 | 5.296 |
| base | FY2030E | -3.324 | 7.048 | 284.574 | 6346.212 | 0.000 | 200.120 | 5.762 | 4.714 |
| downside | FY2026E | -286.412 | 0.062 | 410.880 | 3690.056 | 0.000 | 105.173 | 0.054 | 0.044 |
| downside | FY2027E | -293.268 | -8.735 | 724.823 | 3662.063 | 0.000 | 208.394 | -7.798 | -6.380 |
| downside | FY2028E | -341.456 | -18.050 | 1088.465 | 3607.774 | 38.835 | 327.457 | -16.573 | -13.560 |
| downside | FY2029E | -435.065 | -28.949 | 1547.332 | 3483.334 | 198.275 | 476.942 | -27.546 | -22.538 |
| downside | FY2030E | -525.796 | -41.179 | 2096.708 | 3270.426 | 392.941 | 654.575 | -40.922 | -33.482 |
| upside | FY2026E | 52.558 | 16.724 | 0.000 | 4326.409 | 0.000 | 20.627 | 13.933 | 11.400 |
| upside | FY2027E | 68.123 | 16.749 | 0.000 | 4995.733 | 0.000 | 36.314 | 13.741 | 11.243 |
| upside | FY2028E | 93.648 | 17.020 | 0.000 | 5827.816 | 0.000 | 51.357 | 13.743 | 11.244 |
| upside | FY2029E | 135.253 | 17.776 | 0.000 | 6841.519 | 0.000 | 60.641 | 14.115 | 11.548 |
| upside | FY2030E | 185.007 | 18.873 | 0.000 | 8091.744 | 0.000 | 64.205 | 14.732 | 12.053 |

Capital recognition sensitivity (same assets, earnings and inferred RWA; not actual capital):

| Scenario | Year | 80% recognition CAR | 90% recognition CAR | 100% recognition CAR |
|---|---|---:|---:|---:|
| base | FY2026E | 6.827 | 10.245 | 13.662 |
| base | FY2030E | 2.322 | 4.685 | 7.048 |
| downside | FY2026E | 0.062 | 3.620 | 7.178 |
| downside | FY2030E | -41.179 | -38.259 | -35.339 |
| upside | FY2026E | 10.057 | 13.391 | 16.724 |
| upside | FY2030E | 14.807 | 16.840 | 18.873 |

No actual September statement, source loan/ECL for FY25, post-injection accounting split, true RWA or capital return. Statutory reserve tier proxy allocates positive annual PAT based on opening reserve relative to modeled paid-up capital; no dividends. No claimed PASS.
