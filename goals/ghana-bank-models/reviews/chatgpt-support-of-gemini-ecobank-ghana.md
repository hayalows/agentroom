# Ecobank Ghana — independent round 4 review

## 2026-11-25T19:31:18.620Z — ROU reclassification
Verdict: PASS
Package SHA-256 fingerprint: cdd36f7645e10123d95ccd9735c27e6be3a0633c183594f654108c0d52359138
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

Scope: bounded independent re-review of the round 4 repair of the previously accepted bank. I did not build, edit or supply the ROU repair or its source table. I worked on the shared QA checks which flagged classification issues, not the bank package. Owner closure and lead review decision remain separate.

- Pin 872f8f3dcee07f9805f4126d66675417b25a9ce9; comparison 67ff7c9a32bc6ab7f49b9904ccbc0ce0fccb5d6e. Recomputed ordered seven-file package and macro fingerprints on fetched contents with independent SHA256 implementation verified against standard abc vector; matches Codex and Helper current exact fingerprints. Model.py and assumptions.json are unchanged between pins.
- Inspected EGH22 p1 original text (screenshot cache miss), EGH24 p1 visual screenshot, EGH25 and EGH26Q3 p1 original PDFs via fresh secondary Firecrawl HTTP200 application/pdf (scrape IDs 01a21430-178a-77cc-9786-6e5b2c6ad652 / 01a21430-1877-7129-934b-40f7dce62e72; no visual confirmation for these two). Sources in banks/ecobank-ghana/sources.md. Confirmed standalone Bank columns; amounts in thousands /1000 to GHS m. The Sep26 PDF metadata says June but table explicitly says Bank Sep-26.
- Independently obtained PPE+intangibles+ROU amounts from filings, then checked new canonical total and equal/opposite movement against old CSV for all six periods.

| Period | ROU m | Intangibles m | PPE m | Corrected combined m |
|---|---:|---:|---:|---:|
| FY2021 |45.530|41.143|570.888|657.561|
| FY2022 |38.670|20.690|1253.410|1312.770|
| FY2023 |62.472|5.988|1258.760|1327.220|
| FY2024 |92.353|6.540|1255.082|1353.975|
| FY2025 |90.823|3.553|1295.250|1389.626|
| 9M-2026 |73.725|1.803|1286.203|1361.731|

- All 253 historical rows and 615 forecast rows parsed with width validation; no duplicate keys or invalid numeric/status/source/page observations. Exactly twelve history values changed, the two intended rows for each period. 178 forecast values change. Total historical assets and PAT unchanged.
- Independently recomputed 186/186 checks: 18 source/reclass checks with tolerance .00001m; 168 core financial bridges (NII, operating income, PBT including separate lease finance costs and modification loss, PAT, asset/liability/equity compositions, balance) across six history and fifteen forecast groups, tolerance .005m, max .002m. FY30 PAT base/down/up 1910.075/1351.485/2641.818m. No failures.
- Native Python replay not newly run by me; model and assumptions unchanged, prior Codex round3 exact replay and Helper current round4 scratch replay with CR normalization are recorded. Codex's independent round4 603/603 driver/core checks complement my source/reclass review. This is not a second claim of fresh native execution or of actual regulatory CAR/CRR.

Conclusion: intended correction is complete, no additional model revision required by this bounded review. The previous accepted package's regulatory and source limitations remain. Owner Gemini should bind current review_revision and close after lead confirms eligible reviews. This is an ordinary scoped repair PASS, not a self-close.
