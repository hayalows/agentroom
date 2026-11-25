# UMB independent conditional review (claude-helper-1)

## 2026-11-25T19:12Z, conditional scope per CONDITIONAL-POLICY.md, package 4e18d1fd
Verdict: PASS
Scope: conditional (FY2025 annual and 2026 interim statements unavailable)
Package SHA-256 fingerprint: 4e18d1fd69549708fbbca8a9ff36d1e3bad724d70ccfee63e05fe99dfac31357
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
Supplementary anchor-estimates.csv SHA-256: 8f320f384de4147e3ffa1ef344f07b08fcee2b9f7ead08559a73916f08c2adc2

**Scope.** Conditional PASS only, not ordinary acceptance. It rests on the lead's marker `review-resolutions/umb.md` and policy section 7.

**Independence.** I did not build, edit or supply source evidence for any file in `banks/umb/`. papa-kojo-agent and chatgpt-support supplied source evidence and are excluded; I am an eligible reviewer.

### What I checked (observed)
- **Fingerprints:** the gate hashes the working tree to the package fingerprint above. I hashed `anchor-estimates.csv` myself (sha256sum) and it equals the supplementary digest. The gate reports `failed` only on the schema line "annual periods 4" (FY2025 unavailable, scoped by the policy); 280 history rows, 846 forecast rows, 0 bad, 0 duplicate, 15 scenario-years, 63 core bridges, 0 failed.
- **Replay:** copied the bank folder and the shared macro file to a scratch tree and ran `node model.mjs` (exit 0, "186 checks, 846 forecast rows, 165 estimated anchor rows"). `forecast.csv`, `checks.md` and `anchor-estimates.csv` are byte-identical to the submitted files.
- **Independent identities:** from `forecast.csv` alone I recomputed net interest income, profit after tax and assets = liabilities + equity for all 15 scenario-years (45 checks): largest residual 0.001m, none above 0.0025m. The same balance identity holds in the three FY2025E anchor scenarios (residual at most 0.001m).
- **No invented actuals:** the history has periods FY2021 to FY2024, 9M-2024 and 9M-2025 only; there are no `reported` rows for FY2025 or 2026. Forecast rows carry status `estimated` or `unavailable`, and the FY2025E anchor rows are only `estimated` or `unavailable`.
- **Spot check against the owner's record:** 9M-2025 profit after tax 224.296m, total assets 11,820.441m and total equity 476.201m match the README figures and are marked `reported`.
- **Labelling:** the README title and opening state it is a conditional model with FY2025 and 2026 unavailable; the 2026 recapitalisation is shown as a confirmed event with an unknown amount and modelled only as labelled overlays (minimum 13% overlay, management target overlay, 60% incremental RWA stress).

### Findings (non-blocking)
1. The anchor file is outside the standard gate's hash. Anyone using it should verify the digest above, as the owner already says.
2. FY2030E base profit after tax is -17.7m and the base capital proxy is 5.911% with a 666.5m gap to the minimum; downside equity is negative. These are labelled stress results, not forecasts of an actual outcome.
3. The recapitalisation source is cited as the Ministry of Finance mid-year review (p16, paragraphs 209 to 210); the owner notes the PDF could not be fetched and relies on indexed official text.

### What I could not verify
- I did not open any UMB filing or the Ministry of Finance speech. History and 9M values are checked for arithmetic, replay and the three spot values above only, not against a page.
- This verdict covers the exact fingerprints above and nothing else.
