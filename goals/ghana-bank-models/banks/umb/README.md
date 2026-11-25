# Universal Merchant Bank — conditional model

Standalone Ghana bank. Actual coverage FY21–24 and 9M24/25. FY25 full-year and 2026 primary filings unavailable. Sep25 actual assets11820.441m, equity476.201m, PAT224.296m including impairment reversal205.833m, CAR6.46% conditional on approval of deposits for shares264.247m. No current CAR or approved capital inferred. Fortiz 52.6% issuer website undated, current ownership unverified. Conditional FY25 anchor separate from history; full-year 2026 estimates, no actual 2026 or Q3 nowcast asserted. No quantified new capital or dividends included in the counterfactual projection. This is not a claim that recapitalisation did not occur. Forecasts use shared macro, loan and deposit growth, blended rate calibration, normalized credit costs rather than extrapolated recoveries, positive annual reserve transfers and explicit cash/ capital proxy stress. Estimated capital recognition 0/50/100% in downside/base/upside; no actual approval implied. Missing gross loans, NPL migration, eligible reserve split and regulatory RWA remain unavailable. FY23 5m SoCE discrepancy flagged.

The rate vintage correction uses Jan–Sep 2025 BoG monthly averages (16.8800% 91-day and 18.9911% 364-day), same period as the observed income calibration. This captures the subsequent rate decline; no contractual repricing assumed. FY25 estimated-anchor gaps are forward FY26 screening thresholds only, not historical compliance. Media FY25 PAT267.2m/equity551.3m/deposits10400m differ from base estimates231.558m/483.463m/8811.238m by35.642/67.837/1588.762m; Q1 2026 media PAT81m, not used as actual. These differences emphasize uncertainty, not validation of primary results.

| FY2030E | PAT m | Assets m | Equity m | CAR proxy % | Capital gap m |
|---|---:|---:|---:|---:|---:|
| base | -17.744 | 20891.947 | 820.386 | 5.911 | 666.497 |
| downside | -400.579 | 15034.218 | -264.534 | -9.776 | 1540.864 |
| upside | 141.362 | 25831.560 | 1284.283 | 9.908 | 359.444 |

Reproduce node model.mjs. 846 forecast rows, 165 separate anchor rows, 186 identities. Conditional reviewer CHANGES addressed; fresh independent review requested after exact replay. 280 history rows unchanged; FY25 and 2026 actuals unavailable. Not accepted, no investment advice.

## Confirmed 2026 recapitalisation; unknown amount
MoF's 23 July 2026 Mid-Year Fiscal Policy Review speech, printed p16 paragraphs 209–210, confirms GAT completed UMB recapitalisation the preceding week. Indexed official text corroborated; PDF exceeds web fetch limit, screenshot unavailable. No transaction amount, instrument, regulatory recognition or actual post-event balance sheet verified. Existing projections are explicitly counterfactual without a quantified injection, not a prediction of current CAR. Static FY26 closing alternative solves X=max(0,(target*RWA-cap)/(1-target*incremental RWA density)); full hypothetical equity recognition, cash addition, no P&L; not a forecast of actual proceeds. No 2027+ post-event earnings effect modeled.

| Scenario | Min 13% overlay m | Management target overlay m | 60% incremental RWA stress m |
|---|---:|---:|---:|
| base | 448.813 | 651.642 | 458.306 |
| downside | 641.645 | 949.422 | 655.216 |
| upside | 304.083 | 517.570 | 310.515 |
