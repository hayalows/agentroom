# Independent Absa assistance-draft review — chatgpt-support
2026-11-25T17:24:06.193Z. Snapshot b3cf92c74e00524d5fec16793e50fd4741c93448. Assistance draft, not a claimed bank package or ordinary PASS. Author Papa Kojo Agent, original source pack Codex. No bank owner files changed.

## What passed
- Isolated LF laptop `node model.mjs` exit0, 870 forecast rows, regenerated forecast.csv and checks.md byte-identical by SHA256; 300 historical rows. Separate Python recomputation 356/356 accounting and forecast rollforward, statutory reserve, dividends, RWA/CAR and liquidity identities, max rounding residual0.002m. Zero reported source/page omissions; no duplicate history/forecast keys. Macro exact b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df. Source draft model blob eaf1b78378f96cdb076a8ab77596a7b900737214, forecast544fe0ed131334b2fff67b0603daa8f71f898331.
- Official Q3 2026 issuer PDF fetched HTTP200 by secondary Firecrawl: https://www.absa.com.gh/content/dam/ghana/absa/pdf/annual-reports/q3-2026-for-period-ended-30-september.pdf (physical pp1–2, text extraction, no image verification). Verified Sep26/Sep25 IS and BS: 2026 II2334.247m, IE426.762m, NII1907.485m, TOI3042.475m, impairment198.435m, PBT1530.986m, tax545.655m, PAT985.331m; assets35945.763m, liabilities30070.547m, equity5875.216m, loans11528.344m, deposits21185.474m, stated capital400m, retained3896.887m, reserve1266.136m, credit risk317.614m, other reserves−5.421m. Sep25 PAT1319.003m, assets32119.755m, equity5570.045m. YTD dividend1115m and reserve transfer123.167m, OCI27.871m and share-based payment3.930m; equity bridge5973.084+985.331+27.871+3.930−1115=5875.216m. Reported CAR19.06% and NPL11.32%; Sep25 22.37%/14.09%. Full FY26 modeled PAT1313.250m, base FY30 PAT1632.697m, CAR proxy32.2562%. No independently accessed annual full report in this review, Codex's visual source work remains separate evidence.

## Material repair before adoption: reserve requirement calibration
Q3 source says no statutory liquidity breaches, mandatory reserve3264.904m, cash-flow cash5936.721m, balance-sheet cash9193.018m net ECL8.608m. Reconciliation: 9193.018+8.608−5936.721=3264.905m. At20% headline rate, implied reserve denominator16324.520m =77.0553% of stated customer deposits21185.474m (not a verified regulatory denominator). Current model instead compares 20% of all deposits with 35.5% combined cash; applying same model at actual anchor yields false-looking proxy gap973.573m even though no actual statutory breach was reported. This is a proxy convention, not evidence that Absa violated requirements. Retain current 100%-deposit basis as conservative stress, add calibrated illustrative denominator share and separate eligible-cash haircut. Recompute payout screening with explicitly chosen conservative or calibrated policy; no guarantee of permissible payout. Static unchanged-forecast sensitivity with 77.0553% denominator, same 35.5% cash share (and 28.4% haircut) yields:

| Scenario/year | Existing gap m | Calibrated gap m | Calibrated stress gap m |
|---|---:|---:|---:|
| Base FY26 | 952.714 | 0 | 634.280 |
| Base FY30 | 547.926 | 0 | 228.630 |
| Downside FY26 | 1012.509 | 64.623 | 688.355 |
| Downside FY30 | 910.980 | 0 | 555.518 |
| Upside FY26 | 985.924 | 0 | 657.729 |
| Upside FY30 | 680.349 | 0 | 305.194 |

These are static gap checks, not a regenerated dividend or earnings path. Forecast sensitivity needs model replay. Explain denominator inference caveat, actual cash eligibility unknown, no regulator-compliance claim.

## Adoption checklist and source gaps
- Existing paused owner claude-helper-1 retains bank claim. Lead/human must authorize named handoff. Adopt original source pack, add formal sources.md, use local financials.csv as engine input (currently reads adjacent assistance source CSV), rebase macro path to ../../sector/macro-assumptions/macro.csv; rerun bank gate and actual CLI. Preserve draft and source provenance. New bank-package independent review required; this is not approval of uncreated adopted files.
- Separate source annual FY25/26 capital numerator and RWA, FY25 gross/ECL, annual ratio and reserve basis when accessible. No imputation of actual ratios. Issuer Q3 note reports three other regulatory breaches and GHS0.36m sanctions; subsequent confirmed GHS16.1m penalty. Explicitly state whether modeled Q4 other expenses include or exclude an additional penalty scenario; avoid double-counting, do not assert IAS10 treatment without evidence. Illustrative incremental pretax expense16.1m could reduce FY26 earnings, tax effect uncertain. Retain dated issuer note.
- Current source-specific pledged/trading asset grouping avoids double-counting on BS; earn-yield split remains calibrated proxy. Credit-risk reserve unchanged, gross-loan migration unavailable. Actual tax and YTD payout preserved. No actual regulatory CAR or liquidity conclusion from forecast.

**Verdict: assistance draft arithmetic verified; bounded liquidity calibration improvement and formal authorized adoption required.** No ordinary bank acceptance claimed.
