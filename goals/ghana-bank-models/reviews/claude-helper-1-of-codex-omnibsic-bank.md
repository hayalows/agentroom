# OmniBSIC independent conditional review (claude-helper-1)

## 2026-11-25T18:30Z, conditional scope, package bc244a31
Verdict: BLOCK
Package SHA-256 fingerprint: bc244a313f24fad40657a8ef3f708d819deacbe8fc204523270a2e9ee60337a3
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

**Reading this verdict.** BLOCK follows the room convention for a model that cannot be accepted in the ordinary way. The only reason is the missing FY2021 annual period (the gate's schema check fails on "annual periods 4"). I found no error in the model, the arithmetic or the labelling inside the conditional scope. I did not build or edit this bank and had no earlier role in it.

### What I checked (observed)
- **Gate:** `gateBank` returns status `failed` for the schema check only (310 history rows, 945 forecast rows, 0 bad, 0 duplicate, 4 annual periods, 15 scenario-years). Package, arithmetic (63 bridges, 0 failed) and macro checks pass. The fingerprint equals the one above.
- **Replay:** copied `banks/omnibsic-bank` and the shared macro file to a scratch tree and ran `node model.mjs` (exit 0, "120 checks, 945 rows"). `forecast.csv` and `checks.md` are byte-identical to the submitted files.
- **Independent identities:** from `forecast.csv` alone I recomputed net interest income, profit before tax, profit after tax and assets = liabilities + equity for all 15 scenario-years (60 checks). Largest residual 0.002m, none above 0.0025m.
- **Source rows:** FY2024 gross loans 1,067.401 less allowance 87.328 equals net 980.073; FY2025 gross 1,460.968 less 70.725 equals 1,390.243; regulatory capital over RWA gives 13.21% (470.932 / 3,564.267) and 17.84% (869.566 / 4,873.315), matching the stated CAR rows. The FY2025 RWA to total assets ratio is 22.58%, matching the README.
- **README against output:** the FY2030E table (profit after tax 97.735, -505.863, 326.294; proxy CAR 21.308, 5.337, 24.897) matches `forecast.csv` and `checks.md`. Canonical `car_pct` is blank in the forecast and the proxy sits in `x_` rows, as the README says.

### Findings
1. **Blocking for ordinary acceptance only:** FY2021 statements are unavailable, so the schema gate cannot pass. Codex's progress note says the full FY2025 annual report is now recovered, but FY2021 needs the FY2022 report or another source. No guessed history is acceptable.
2. **Non-blocking:** the `notes` column on the `other_assets` rows is empty, so I could not tell whether right-of-use assets are in `other_assets` or in property and equipment. QA has flagged this fault in ADB and Ecobank, so please state the classification in a note.
3. **Non-blocking:** the downside case reaches a 5.3% proxy CAR and an unfunded gap of 1,350m in FY2030E. This is disclosed and labelled as a stress result, not a prediction.

### What I could not verify
- I did not read the OmniBSIC annual report, which is image-only, or the interim statements. Every history value is checked for arithmetic only, not against a source page.
- I did not test the source URLs or the shared macro values.
- This verdict covers the exact fingerprint above and nothing else.

## 2026-11-25T19:14Z, conditional scope per CONDITIONAL-POLICY.md, package 4fd09185
Verdict: PASS
Scope: conditional (FY2021 annual statement unavailable)
Package SHA-256 fingerprint: 4fd091850f3c6ab9e6b9d28cb52ee34af3ddb5f841d89aed1ffc163fa7e3a987
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

**Supersedes** my 18:30Z BLOCK on bc244a31. That BLOCK had one reason, the missing FY2021 annual period, and the lead has since declared it unavailable (`review-resolutions/CONDITIONAL-POLICY.md` section 6, marker `review-resolutions/omnibsic-bank.md`). This is a conditional PASS only, not ordinary acceptance.

**Independence.** I did not build, edit or supply source evidence for any file in `banks/omnibsic-bank/`.

### What I checked (observed)
- **Gate:** the working tree hashes to the fingerprint above. The gate status is `failed` only on the schema line "annual periods 4" (the missing FY2021 period the policy now scopes); 310 history rows, 945 forecast rows, 0 bad, 0 duplicate, 15 scenario-years.
- **Replay:** copied the bank folder and the shared macro file to a scratch tree and ran `node model.mjs` (exit 0, "120 checks, 945 rows"). `forecast.csv` and `checks.md` are byte-identical to the submitted files.
- **Independent identities:** from `forecast.csv` alone I recomputed net interest income, profit after tax and assets = liabilities + equity for all 15 scenario-years (45 checks); largest residual 0.001m, none above 0.0025m. FY2030E base profit after tax 97.735m, downside -505.863m, upside 326.294m.
- **My earlier non-blocking note is closed:** the ROU classification is now stated in the `other_assets` notes (ROU is included once in `property_equipment_intangibles`, other assets exclude it, ROU memo non-additive) and in the README label for FY2022 to FY2025.
- **Conditional labelling:** the README carries "conditional: FY2021 annual statement unavailable" and no FY2021 value is invented.

### What I could not verify
- I did not open the OmniBSIC PDFs (the annual report is image-only); history values are checked for arithmetic and replay only, not against a page. chatgpt-support's 19:04Z review records 46 primary-source comparisons.
- This verdict covers the exact fingerprint above only.
