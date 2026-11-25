# UMB independent provisional review — 2026-11-25T16:52:57.461Z

Verdict: CHANGES (conditional model only; not a full-history acceptance decision)
Package SHA-256 fingerprint: 097d6f916f4d5cd870bdae43d63ef886ff34e034ce0ae470eaa9d28b5d1da3b0
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
Separate FY25 anchor SHA-256: 24e3922b9c1d5f2f0fdfa504abf95341a81bc8890644498144741e07b97e0db3

## Positive evidence
Independently executed the fetched model's pure JavaScript engine in isolated scratch against exact financials/config/macro; all three output strings (forecast, estimated anchors, checks) identical after LF normalization; 180 engine identities. This is an engine replay, not standalone CLI execution. Independently recomputed 174 rounded forecast/anchor accounting and rollforward identities, max 0.001m, zero failures at 0.005m; 24 history face checks pass (max <0.000001m), 280 historical rows, 825 forecast and 165 separate anchor rows, zero duplicate forecast/anchor keys. Separating unobserved annual and forecast data is correct. Prior source discovery and Codex extraction are acknowledged, but I did not repeat all source page verification. The September 2025 CAR is conditional on BoG approval of 264.247m deposits for shares; scenario recognition and RWA stress are transparent. The FY23 5m SoCE difference is disclosed.

## Bounded changes before provisional PASS
1. Rate vintage mismatch: actual 9M25 annualized blended asset yield 12.624% and funding cost 6.851% are calibrated to FY24/Sep25 balances, but code subtracts BASE FY2026E rates (11.01% 364d, 5.81% 91d), so the 2025→2026 market-rate decline is omitted from base yield/cost. Use same-period 2025 market-rate averages as calibration references, preferably Jan–Sep directly sourced; or explicitly justify locked-rate assumption with a repricing sensitivity. To quantify materiality I ran a scratch alternative using actual FY25 full-year proxy 17.48%/15.38% with unchanged betas .55/.35 and all other inputs. FY26 base PAT116.436→158.148m; FY30 base −121.185→1.991m, CAR proxy2.837→6.585%; downside FY30 PAT−504.397→−387.879m, CAR−14.842→−8.838%; upside FY30 PAT54.374→155.979m, CAR7.525→10.419%. These are sensitivity estimates, not preferred forecasts or actual rates. Show the anchor vintage and rate bridge in assumptions/checks, and update sensitivity and README after replay.
2. FY25 estimated-anchor capital and liquidity gap currently use FY26 statutory thresholds (13% CAR, uniform 20% CRR effective June 2026); actual FY25 CRR is unavailable/dynamic in macro. Explicitly label FY25 gaps as forward-2026-threshold stress only, or leave FY25 actual-compliance comparison unavailable. No misrepresentation of actual historical compliance.
3. Secondary B&FT context already recorded cites FY25 PAT267.2m/equity551.3m/deposits10.4bn versus conditional base 231.558m/483.463m/8.811bn. Do not substitute media numbers for actuals; include these approximate differences as a nowcast validation caveat and optional FY25 anchor sensitivity, alongside Q1 2026 media PAT81m. Primary FY25 and 2026 remain missing; these are not acceptance waivers.

No owner edits. Please address 1–2, disclose 3, and send exact revised fingerprint and CLI replay for independent provisional review. Keep UMB outside accepted-only totals regardless of arithmetic until coverage policy and reviewer requirements are met.

## 2026-11-25T17:20:38.451Z — conditional re-review
Verdict: BLOCK
Package SHA-256 fingerprint: 4e18d1fd69549708fbbca8a9ff36d1e3bad724d70ccfee63e05fe99dfac31357
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
Separate FY25 anchor SHA-256: 8f320f384de4147e3ffa1ef344f07b08fcee2b9f7ead08559a73916f08c2adc2

Conditional-scope arithmetic and prior repairs pass; ordinary acceptance remains blocked because actual FY25 annual and FY26 bank filings are missing. Exact fetched JS engine reproduced forecast, estimated anchors and checks strings; 174/174 independently computed rounded accounting and rollforward checks, max 0.001000m, 280 history/846 forecast/165 estimated anchor rows. Same-vintage Jan–Sep25 market rates now used; FY25 threshold stress labelled forward, media comparison caveat preserved. Official MoF July23 speech printed p16 paras209–210 confirms recapitalisation, amount/instrument unverified. Counterfactual no-quantified-event path and static estimated capital overlay explicitly distinguished from actual amounts; source uncertainty preserved. Owner reported standalone CLI exact; my current execution is pure engine replay, not independent CLI. No claim actual post-event capital, no ordinary PASS or waiver. Keep separate from accepted-only rollup.
