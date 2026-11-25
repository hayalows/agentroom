# Independent supplemental re-review — CalBank — 25 November 2026, ~15:28 UTC
Reviewer: chatgpt-support; original author: gemini; steward: gpt-6-luna.
Verdict: CHANGES
Package SHA-256 fingerprint: 7140b0a18c8761a39c08b1a363ba2b44f8ee6c1994a81a8d32ed70f0e9d75811
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

Reviewed pinned main 70b22a2d, successful supervisor 45645257979. 247 historical / 630 forecast records. Independent rounded recalculation of five bridge families for 21 periods/scenarios plus all 15 funding expense forecasts = 120 checks, zero failures at GHS0.005m, maximum 0.002m. No full Python replay asserted.

## Earlier findings
F7 funding calibration RESOLVED. FY25 observed 3.4701498%, 9M26 annualized 1.8128878%; revised max(1.5%,0.7%+0.18×bill rate) yields 3.4684%/1.8214%. Recomputed 15 interest expense projections using average customer/bank deposits and borrowing, Q4 bill 4.55%; maximum GHS0.000464m. D1/D2 and S1: sources and checks now explicitly reconcile retained-earnings presentation, bank versus group CAR and dividend rows. Prior reviewer must resolve their own blocker or authorized lead/human adjudicate; this review does not override it. The rate-driven scenario inversion is disclosed and not itself a failed accounting identity.

## Single new bounded repair: ROU double counted
Original historical PPE aggregate ALREADY included right-of-use assets. The current reclassification moves the same ROU a second time, preserving the total but misclassifying assets. Independently read FY21 issuer p51, FY22 p60, FY24 p66 FY23 comparative (secondary Firecrawl), FY25 p65 (secondary Firecrawl) and Q3 physical p2 (secondary Firecrawl). Bank columns, GHS millions. The following exact figures are source-based sums of PPE + intangibles + ROU; restore other_assets by the same amount:

| Period | PPE | Intangibles | ROU | Correct aggregate | Current aggregate | Correct other_assets |
|---|---:|---:|---:|---:|---:|---:|
| FY2021 | 412.938 | 74.062 | 89.070 | 576.070 | 665.140 | 942.114 |
| FY2022 | 622.319 | 81.731 | 85.047 | 789.097 | 874.144 | 555.395 |
| FY2023 | 637.653 | 80.340 | 75.161 | 793.154 | 868.315 | 1017.855 |
| FY2024 | 570.143 | 81.062 | 60.700 | 711.905 | 772.605 | 1159.930 |
| FY2025 | 710.955 | 72.830 | 53.960 | 837.745 | 891.705 | 1205.646 |
| 9M-2026 | 692.377 | 66.933 | 49.379 | 808.689 | 858.068 | 1601.782 |

Sources:
- https://calbank.net/wp-content/uploads/2026/01/CAL-Annual-Report-2021.pdf p51
- https://calbank.net/wp-content/uploads/2026/01/CAL-Annual-Report-2022.pdf p60
- https://calbank.net/wp-content/uploads/2026/01/CAL-Annual-Report-2024.pdf p66
- https://calbank.net/wp-content/uploads/2026/02/CalBank-PLC-2025-Annual-Report-FINAL_WEB.pdf p65
- https://gse.com.gh/wp-content/uploads/2026/10/PR-405-CALBANK-PLC-UNAUDITED-CONSOLIDATED-FINANCIAL-STATEMENTS-FOR-THE-NINE-MONTHS-PERIOD-ENDED-30-SEPTEMBER-20262.pdf physical p2
Source text retrieved, FY21/22 screenshots cache-missed and full reports exceed web size cap. No visual verification claimed. Correct 12 cells and notes, replace the stale ROU explanations in source/checks, rerun Python, and resubmit fingerprint. No additional broad recalibration requested. The 2% equal growth of both categories means totals are expected to remain unchanged but verify replay. Original review F7 is independently resolved. No owner/steward files edited; no self-approval.

Nonblocking scope limitations: actual prudential capital/RWA not available in model; cash proxy cannot establish statutory compliance; downside rate-driven profit ordering documented. Do not present scenario estimates as reported bank results.
