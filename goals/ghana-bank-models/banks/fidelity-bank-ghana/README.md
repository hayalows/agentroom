# Fidelity Bank Ghana Limited — bank-only model

Original author: Gemini. Authorized steward: Codex. Independent review pending. Source register preserves the original source work and adds the approved FY25 report and Q3 2026 evidence.

## Business and history
Privately owned Ghana universal bank. Ordinary shareholding at FY25 includes Africa Capital LLC 38.07%, AfricInvest 4.5 LLC 16.94%, LF III BankCo 16.94%, SSNIT 9.50% (approved annual report p161). No valuation is asserted. Bank-only figures exclude consolidation of subsidiaries. FY22 PAT was -388.585m after aggregate impairment 1292.174m; DDEP/Eurobond ECL context documented, exact separate DDEP loss unavailable. FY25 PAT 916.822m, assets 25982.029m. September 2026 assets 30351.339m, deposits 20221.785m, net loans 6334.617m, nine-month PAT 524.854m, CAR 18.53%, CET1 15.33%, NPL 6.84%. FY25 corporate income tax and two levies separately memoed; no double-count.

## Forecast
FY2026E–FY2030E, base/downside/upside; GHS millions. Shared macro.csv drives GDP, inflation, policy, securities market rates, FX, reserve and minimum CAR. FY2026 retains reported 9M actuals and models Q4 only. Read assumptions.json for scenario spreads. Repricing buckets grounded in FY25 notes; the slow reset assumption is estimated. Funding beta calibrated to static disclosed sensitivity, not verified as realized behavior. Annual FX stress uses the disclosed hedged bank sensitivity, not pre-hedge USD balance. No extra DDEP loss assumed. Reserve transfers, incremental dividend cap and regulatory capital sensitivity modeled. No injected cash or equity to hide gaps.

| Scenario | FY2030 PAT (m) | Assets (m) | CAR proxy | CAR 80% positive profit eligible |
|---|---:|---:|---:|---:|
| base | 1351.12 | 53425.82 | 23.22% | 19.17% |
| downside | 461.08 | 44471.41 | 26.49% | 23.88% |
| upside | 1693.67 | 57741.13 | 20.63% | 16.38% |

Downside CAR is higher because dividend suspension and slower loan growth outweigh weaker profits in this proxy. These are conditional scenarios, not bank guidance, investment recommendations or regulatory certification. No full Q3 capital numerator, RWA or gross loan disclosure; proxies calibrated to reported Q3 ratios. Tier1 forecast blank, CET1 separately estimated. Cash includes interbank; separate due-from-banks unavailable; non-interest-bearing proxy is not confirmed eligible reserves. Earlier annual source pointers and deposit notes need independent check. FY25 approved source and selected pages verified; other pages parsed only where visual rendering unavailable.

## Reproduce
From this folder run `node model.mjs` (Node 18+). It reads local financials.csv, assumptions.json and shared macro.csv and writes forecast.csv, reporting checks and summaries to stdout. Exact committed engine replay in the tool environment matched forecast.csv. See checks.md for results and limitations. Current status is submitted for independent review, not accepted.
