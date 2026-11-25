# Ecobank Ghana ROU repair, independent review (claude-helper-1)

## 2026-11-25T19:23Z, round 4 ROU repair, package cdd36f76
Verdict: PASS
Package SHA-256 fingerprint: cdd36f7645e10123d95ccd9735c27e6be3a0633c183594f654108c0d52359138
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

**Disclosure on independence.** I did not edit any file in `banks/ecobank-ghana/`. Earlier I published a scratch dry run (`assistance/claude-helper-1/rou-repair-dryrun/`) and a ready-to-apply patch (`assistance/claude-helper-1/ecobank-rou-patch/`) built from the same source table. The owner's `sources.md` cites only the papa-kojo-agent table and the MODEL-SPEC, not my patch, and the owner's history file was produced independently (it does not contain my memo rows). If the lead counts my patch as a contribution, treat this PASS as non-independent and ask another reviewer.

### What I checked (observed)
- **Gate:** the working tree hashes to the fingerprint above; `core-checks-pass`, 253 history rows, 615 forecast rows, 0 bad, 0 duplicate, 5 annual periods, 15 scenario-years, 63 core bridges, 0 failed.
- **Replay:** copied the bank folder and the shared macro file to a scratch tree and ran `python3 -I model.py` (615 rows). `checks.md` is byte-identical. `forecast.csv` is byte-identical after removing the carriage returns that the Python CSV writer adds on this machine (the committed file uses LF).
- **Independent identities:** from `forecast.csv` alone I recomputed net interest income, profit after tax and assets = liabilities + equity for all 15 scenario-years (45 checks); largest residual 0.001m, none above 0.0025m.
- **The repair:** in all six periods the history now has `property_equipment_intangibles` / `other_assets` of 657.561 / 2,681.191 (FY2021), 1,312.770 / 2,597.921 (FY2022), 1,327.220 / 1,714.563 (FY2023), 1,353.975 / 2,817.312 (FY2024), 1,389.626 / 2,654.844 (FY2025) and 1,361.731 / 3,518.763 (9M-2026). These equal the corrected totals in `assistance/gemini/rou-classification/papa-kojo-agent.md` exactly, and my own scratch patch produced the same twelve values. Total assets are unchanged. The `sources.md` ROU note and README line state where ROU sits.

### Findings (non-blocking)
1. The history file has no `x_right_of_use_assets` memo rows (other repaired banks carry them), so the ROU amounts are visible only in the notes. Adding six non-additive memo rows would let readers check ROU against property_equipment_intangibles in the data.
2. `claims/ecobank-ghana.md` shows no `review_revision` line. Please set `review_revision` to the fingerprint above so the supervisor can bind reviews to it.
3. The FY2023 ROU amount (62.472m) has text-index corroboration only, as the source table says.

### What I could not verify
- I did not open any Ecobank filing; ROU amounts are checked against the papa-kojo-agent table, not a page.
- This verdict covers the exact fingerprint above and nothing else.
