# Independent review: Standard Chartered Bank Ghana PLC (`standard-chartered-ghana`), round 1

Reviewer: gemini; owner: claude. 2026-11-25T13:16:00Z. Reviewed `banks/standard-chartered-ghana/` (`financials.csv`, `forecast.csv`, `assumptions.json`, `model.py`, `build_financials.py`, `checks.md`, `checks_history.md`, `sources.md`, `README.md`). Package fingerprint: `11e7d4edb4eb26c1124cc09d419dd41cc88bfa52c5f9b1b7f743d0bcf5c14f6a`; macro fingerprint: `4cf8911a258f0c81a4a48e660b31b796de40e8327dca36d2bbdb16b59a2f7202`.

**Verdict:** CHANGES REQUIRED (minor deterministic gate fix only; all financial numbers, `SCB-FY22` check, and forecast arithmetic pass)

## What I checked (observed on disk & from primary PDFs)
1. **Opened `SCB-FY22` (`gh-full-year-financial-statement.pdf` p. 1) directly** (as requested in `README.md`):
   - Pre-restatement Bank 2022 `Net interest income` = `807,786`, `Operating income` = `1,210,125`, `Total Impairment` = `(1,158,773)`, `PBT` = `(383,542)`, `PAT` = `(299,634)` — all match `checks_history.md` lines 15–19 exactly.
   - Pre-restatement Bank 2022 `Total assets` = `10,367,004` and `Total shareholders' funds` = `1,327,358`, vs. restated `10,326,704` and `1,287,058` (`-40,300` GHS '000), confirming the `-40.3m` IAS 8 restatement documented in `README.md`.
2. **Spot-checked `SCB-FY25` (`gh-full-year-financial-statement-annual-report.pdf` p. 1) directly:**
   - Bank 2025 `Operating income` = `1,821,437`, `PBT` = `1,021,187`, `PAT` = `798,681`, `Total assets` = `16,502,639`, `Total liabilities` = `13,692,818`, `Total equity` = `2,809,821` — all match `checks_history.md` lines 43–50.
3. **Recomputed `forecast.csv` (540 rows, 15 scenario-years):**
   - Max forecast balance-sheet residual (`total_assets - (total_liabilities + total_equity)`) = `0.001` GHS m across all 15 scenario-years.
   - Macro linkage confirmed: `model.py` reads `sector/macro-assumptions/macro.csv` (v1.1) by `scenario`, `year`, `driver`.
4. **Asset-sensitivity & assumption challenge:**
   - Asset-sensitivity result (downside `FY2027E` PAT `517m` > base `401m`) is structurally sound given SCB's `15.2%` net-loan/deposit ratio (`FY2025`) and large T-bill/liquid-asset book (`7,424m` at `9M-2026`) repricing up in the downside rate-hike scenario (`tbill_91d_pct` `9.0%` vs. `5.5%` base).
   - Trading income fade (`-10%`/yr base, `-25%`/yr downside) is appropriately conservative given the `141m–568m` historical swing.

## Required change (1 item)
- **Deterministic gate (`node scripts/supervisor.mjs --json`) reports `status: failed` (`arithmetic: 0`):** `history||9M-2025 total_assets missing`. `financials.csv` includes `9M-2025` income statement rows without `9M-2025` balance sheet rows (`9M-2026` is the required latest interim). Either drop `9M-2025` rows from `financials.csv` or add `9M-2025` balance sheet rows so `bank-gate.mjs` passes.

## What I could not verify
- Did not re-run `build_financials.py` or `model.py` in-place to avoid modifying owner files; verified `financials.csv` (270 rows) and `forecast.csv` (540 rows) outputs directly in Python.
