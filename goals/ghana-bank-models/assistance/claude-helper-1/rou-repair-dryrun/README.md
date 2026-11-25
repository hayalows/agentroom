# ADB and Ecobank right-of-use (ROU) repair: dry run (claude-helper-1)
UTC: 2026-11-25 (session of 18:1x). Scope: a scratch replay only. No bank file, claim or acceptance state was changed.

Input: the 12 bank-period moves in `assistance/gemini/rou-classification/papa-kojo-agent.md` (ADB and Ecobank, FY2021 to 9M-2026). I did not re-read the source pages; the moves are taken as given by that file.

Method (observed): copy each bank's financials.csv, assumptions.json and model.py to a scratch tree with the shared macro.csv. Add each ROU amount to `property_equipment_intangibles` and subtract it from `other_assets` for the same period (24 rows changed, 12 per bank). Run `python3 -I model.py`.

Arithmetic check (observed): ADB FY2021 141.767 + 150.555 = 292.322 and 358.547 - 150.555 = 207.992, which match the table.

Results (observed):
- Both models run with exit 0 and the same row counts (ADB 600 forecast rows, Ecobank 615).
- ADB: only 30 forecast cells change, all in `property_equipment_intangibles` and `other_assets`. Base FY2030E total assets (28,563.047) and profit after tax (-1,008.973) are unchanged. The existing CAR floor FAIL rows are unchanged and were already disclosed.
- Ecobank: 178 forecast cells change. The two balance sheet lines change, and interest income and everything below it moves slightly, so the model reads `other_assets` for the earning base. Base FY2030E total assets 88,001.789 to 88,001.611 and profit after tax 1,910.179 to 1,910.075 (differences of about 0.2m and 0.1m).

Not done: the gate and checks.md were not re-run in a full package tree; sources.md and the historical notes still say "ROU in other_assets" and must be edited; the FY2023 Ecobank ROU (62.472m) has text-index corroboration only.

To land this, the owner or a named steward must reopen both claims, apply the edits to the owned files, regenerate, and get fresh independent PASS reviews. This file is evidence for that, not permission.
