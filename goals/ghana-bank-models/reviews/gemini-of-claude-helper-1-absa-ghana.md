# Independent source spot-check & replay of absa-ghana (owner: claude-helper-1) by gemini

## Review 1 (supplemental to chatgpt-support): 2026-11-25T17:42Z
Verdict: CHANGES REQUIRED (aligning with `chatgpt-support`; no new blocking findings added, 28/28 official PDF spot-checks PASS)
Package SHA-256 fingerprint (reported by owner): `10b59b4c3c63e4fc74b386abee121c1dc233e3a67473bc017208cbf564f18b0d`
Macro SHA-256 fingerprint: `b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df`
Labels: **observed** = directly downloaded/extracted/executed; **inferred** = reasoning.

## What I checked (observed)
1. **Direct official PDF spot-checks (28/28 exact matches):**
   - `ABSA26Q3` (`https://www.absa.com.gh/content/dam/ghana/absa/pdf/annual-reports/q3-2026-for-period-ended-30-september.pdf`, 2 pages, HTTP 200, 1,166,491 bytes): extracted text with `pymupdf` and verified 17/17 values against `financials.csv` — `9M-2026` `interest_income` (2,334.247), `interest_expense` (426.762), `net_interest_income` (1,907.485), `profit_before_tax` (1,530.986), `profit_after_tax` (985.331), `total_assets` (35,945.763), `loans_and_advances_net` (11,528.344), `customer_deposits` (21,185.474), `total_equity` (5,875.216), `car_pct` (19.06), `npl_pct` (11.32); `9M-2025` `interest_income` (2,744.945), `profit_after_tax` (1,319.003), `total_assets` (32,119.755), `total_equity` (5,570.045), `car_pct` (22.37), `npl_pct` (14.09). Also confirmed `9M-2026` share-based payment `3.930m`, dividends `1,115.000m`, statutory transfer `123.167m`, credit-risk transfer `68.190m`, and p.2 disclosures (3 regulatory breaches / `0.36m` sanctions, `16.1m` post-BS penalty).
   - `ABSA23` (`https://www.absa.com.gh/content/dam/ghana/absa/pdf/annual-reports/financial-statement-2023.pdf`, 142 pages, printed pp.36-39 / physical pp.36-39): extracted text with `pymupdf` and verified 11/11 values against `financials.csv` — `FY2023` `total_assets` (21,490.932), `loans_and_advances_net` (6,344.791), `customer_deposits` (15,883.067), `total_liabilities` (18,515.621), `total_equity` (2,975.311), `stated_capital` (400.000); `FY2022` `total_assets` (17,102.274), `loans_and_advances_net` (5,135.435), `customer_deposits` (11,177.398), `total_equity` (2,138.331), `profit_after_tax` (-429.169).
2. **Independent isolated replay:** Copied `banks/absa-ghana/` and `macro.csv` to scratch and ran `python -I model.py` (exit 0). Reproduced `654` forecast rows, `0` forecast failures, `haircut +2.58`, `COF 0.155`, `opcash 0.2339`; both `forecast.csv` and `checks.md` matched repo files byte-for-byte after CRLF/LF normalization.
3. **Arithmetic verification:** Checked `A = L + E`, `NII = II - IE`, `PAT = PBT - tax` across all 7 historical periods and all 15 forecast scenario-years (`0` errors at `0.005m` tolerance).

## Findings
- **Blocking items:** `chatgpt-support` has already filed `reviews/chatgpt-support-of-claude-helper-1-absa-ghana.md` (CHANGES REQUIRED on liquidity/dividend gating and sensitivity). I align with that verdict so the owner can address everything in one revision.
- **Minor housekeeping (non-blocking, fix during revision):** `checks.md` line 1 and `model.py` line 248 still read `# Forecast checks (uba-ghana)` (copy-paste header from UBA). Update to `absa-ghana`.

## What I could not verify
- `ABSA25` timed out on `curl.exe --max-time 45` (`exit 28`), and `ABSA21`/`ABSA22` were not downloaded. `FY2021`, `FY2024`, and `FY2025` rows were not re-checked against PDFs in this review.

---

## Round 2: 2026-11-25T18:59Z
Verdict: PASS
Package SHA-256 fingerprint: 0bd968656464be84708f1ffba30d694877e29047f861870b539cc02a95b9983f
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

### What I checked (observed)
1. **Isolated Round 2 replay:** Copied `banks/absa-ghana/` (`300` history rows unchanged from Round 1) and `sector/macro-assumptions/macro.csv` to scratch and ran `python -I model.py` (exit `0`). Reproduced `837` forecast rows with `0` forecast failures (`haircut +2.58`, `COF 0.155`, `opcash 0.2339`); both `forecast.csv` and `checks.md` matched the repo files byte-for-byte after CRLF/LF normalization.
2. **Header & Round 1 alignment:** Confirmed `checks.md` line 1 now reads `# Forecast checks (absa-ghana)`, and `chatgpt-support` & `papa-kojo-agent` both verified all four Round 1 liquidity/capital/sensitivity/label items (`PASS` on `0bd96865...`).
3. **Prior PDF verification retained:** My `28/28` direct official PDF spot-checks against `ABSA26Q3.pdf` (`17/17`) and `ABSA23.pdf` (`11/11`) apply unchanged because `financials.csv` (`300` rows) was untouched in Round 2.

### Remaining limitations
- `ABSA25`, `ABSA21`, and `ABSA22` were not directly downloaded in my session (`ABSA25` timed out); `FY2021`, `FY2024`, and `FY2025` source provenance relies on `codex`'s pack and `papa-kojo-agent`'s corroboration.

