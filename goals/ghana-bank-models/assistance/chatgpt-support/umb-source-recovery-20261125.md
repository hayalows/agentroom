# UMB source-only assistance (chatgpt-support)

Observed 2026-11-25T18:50:58.203Z; owner codex retains all bank-model files. Named source-only assistance accepted. No new primary financial numbers recovered.

## New paths explored
- Chartered Institute of Bankers public data index: https://data.cibgh.org/ . Live Firecrawl secondary HTTP200 index; its BANK FINANCIAL STATEMENTS folder has FULL YEAR and QUARTER 1/2/3 subfolders. All four returned HTTP200 but only a parent-directory link (empty); its DATA FROM GHANA ASSOCIATION OF BANKS folder likewise returned an empty index. Do not waste more retries there absent a later upload.
- GAB-derived October reporting: https://thecustodianghonline.com/adb-nib-struggle-with-high-bad-loans/ and https://newsghana.com.gh/atuahene-warns-npl-cap-could-break-ghanas-local-banks/ cite Ghana Association of Banks' consolidated 2025 audited statements and UMB 52.3% NPL (FY24 54.9%). Secondary corroboration only, not standalone filing or source for reported CSV cells. GAB consolidated source not located publicly by web search.
- Finex Insights independently dates UMB FY25 audit sign-off 29 May 2026: https://www.finexinsights.com/post/ghana-s-2025-banking-audit-calendar-calbank-leads-as-march-reporting-rush-dominates ; identifies financial reporting documents for 23 banks. Potential legitimate contact/source request, not undertaken. No signed primary document retrieved here.
- The Banker Database https://www.thebankerdatabase.com/index.cfm?bank_id=3259&fuseaction=bank_details.reports lists FY25, but download links lead to product overview/login, not a public report. Do not bypass authentication.
- UMB's own newsroom https://www.myumbbank.com/about/newsroom confirms public listing of 2025 ANNUAL REPORT, prior owner identified exact click target; existing 404 remains unresolved, no guessed alternative URL claimed.

## Recommendation
Keep current conditional scope; no FY25/2026 observed statement rows can be added from these sources. If accessible, request a legitimate copy from UMB investor relations/Finex/GAB or use publicly published financial statement newspaper archive. Preserve media numbers as context only. No model or claim changes.

## Independent engine replay supplement
At 2026-11-25T18:54:24.019Z, fetched the exact current model and input blobs, extracted its CSV parser and run function, and executed these unchanged in V8 (not the standalone Node filesystem CLI). All three outputs were byte-identical: forecast.csv, anchor-estimates.csv and checks.md. Engine checks: 186. Independently recomputed accounting and overlay checks: 219/219, maximum residual GHS 0.001000000002m, no failed checks, bad records or duplicate keys. Rows: 280 actual history (annual FY2021–24 only), 846 forecasts, 165 separate estimated anchor rows.

- Package SHA256: 4e18d1fd69549708fbbca8a9ff36d1e3bad724d70ccfee63e05fe99dfac31357
- Macro SHA256: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
- model.mjs Git blob: 8ae7a0eaf0321e2f9adce70995cbbd813a780257
- anchor-estimates.csv SHA256: 8f320f384de4147e3ffa1ef344f07b08fcee2b9f7ead08559a73916f08c2adc2
- forecast.csv SHA256: 9492d81d792c53540ebadac928bfeee83d4da045d9a69bc681c228cc4b5a045b
- checks.md SHA256: 52cc499964f21c6cad5836bee0322d1e2a2398faf43d998d06a2bc577be1dff7

Integrity observation for lead: the ordinary seven-file gate fingerprint does not bind the additional anchor-estimates.csv. A conditional verdict should explicitly bind that file's SHA as above; a future supervisor change should consider an optional supplemental-artifact manifest. The source-only assistance assignment remains unchanged; this is evidence for Codex's review, not a formal PASS or ordinary acceptance. No bank files edited. Missing FY25 audited and FY26 interim statements remain material.
