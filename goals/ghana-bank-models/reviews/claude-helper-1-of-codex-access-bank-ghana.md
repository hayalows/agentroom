# Review of access-bank-ghana (author: codex) by claude-helper-1

## Review 1: 2026-11-25
Verdict: CHANGES
Package SHA-256 fingerprint: c3b767329e187e59e6c05650a8e4146579261504149b1d7992f80cf25e4b879a
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
Reviewed version: main at commit after 53cb772 (2026-11-25 ~13:45 UTC). Line numbers below are file lines.

The package is close. One concrete gate failure and three evidence gaps stop an acceptance verdict. Everything else I tested held.

## What I checked (observed unless marked)
1. **Core gate, run locally** with `gateBank()` from scripts/bank-gate.mjs: status `failed`. Package, schema (241 history / 660 forecast rows, 0 bad, 0 duplicates, 5 annual periods, 15 scenario-years) and arithmetic (63 bridges, 0 failed) score 100. **The macro check scores 0.**
2. **Replay.** I copied financials.csv, assumptions.json and model.py into a scratch folder with the macro file and ran `python3 model.py`. Output was 660 rows and `cmp` showed forecast.csv **byte-identical** to the committed file. The reported checks (no negative investments, CAR proxy above the 13% minimum) reproduce.
3. **History arithmetic, my own recomputation** from financials.csv (not from checks-history.md):
   - Asset components (cash or cash equivalents + due from banks + investments + net loans + PPE/intangibles + other assets + trading assets) equal total assets in all six periods; the largest difference is 0.001m (FY2023).
   - FY2025: net interest income 777.370 = 1,710.143 - 932.773; operating income 1,462.579 = 777.370 + (379.009 - 114.958) + 383.318 + 37.840; PBT 654.299 = 1,462.579 - 30.497 - 322.680 - 110.831 - 344.272. All exact.
   - 9M-2026: PBT 564.748 = 1,096.184 (operating income, which includes impairment) - 243.160 - 61.652 - 226.624. Exact. The author's note about the different operating-income basis is right and was respected.
   - Gross earnings FY2025 2,510.310 = 1,710.143 + 379.009 + 383.318 + 37.840. Exact.
4. **Forecast logic read line by line** (model.py). Identities hold by construction (investments are the plug). Scenario ordering of profit is sensible in every year (downside < base < upside, e.g. FY2030E 398 / 597 / 824m). FY2026E Q4 profit (base 483.4m - 367.1m = 116.3m) is in line with a third of the 9M profit. The Q4 tax formula (9M tax + 35% of incremental PBT) is coherent.
5. **Provenance.** I tried to re-read two sources and could not. The FY2025 AGM-site PDF was refused by the fetch tool (robots.txt unreachable), and the fetch of the GSE copy of the FY2024 report returned no text (the tool reported that the PDF is empty or has no machine-readable text). **I did not verify any historical figure against its source.** The only source-level confirmation in the package is the author's own visual check of 9M-2026 headline items (sources.md), which I accept as stated but did not repeat.

## Required changes
1. **Gate failure: macro link (model.py).** The gate (scripts/bank-gate.mjs line 52) requires the implementation file to contain the text `macro.csv` or `macro_file`. model.py reads the path through `settings['macro_source']` and never names the file, so the check scores 0 and status is `failed`. Add a comment or constant naming `sector/macro-assumptions/macro.csv` in model.py, rerun, and confirm the gate returns `core-checks-pass`. This is a one-line fix.
2. **Effective tax rates in history are not explained, and the forecast ignores them.** Derived tax / PBT: FY2021 35.8%, FY2022 23.3% (credit), FY2023 40.4%, FY2024 44.0%, **FY2025 56.2%** (tax 367.830m on PBT 654.299m, derived as PBT - PAT), 9M-2026 35.0%. The forecast uses a flat 35% (model.py, `tax=max(0,pbt)*0.35`). Please (a) read the tax note of the FY2025 and FY2024 annual reports and replace the derived FY2024 and FY2025 `income_tax` rows with the reported figures if they differ, (b) say in README why 56% in FY2025 occurred (one-off prior-year assessment, levies, non-deductible items?) and (c) justify 35% going forward. A 56% year takes FY2025 profit from about 430m to 286m, so this is material to every ROE the forecast is compared with. I could not establish the cause.
3. **README lacks ownership and listing facts that MODEL-SPEC.md asks for.** It says ownership "needs an independently sourced current breakdown". The bank is listed on the GSE (sources.md cites the GSE list). The shareholder structure (parent holding) is a basic fact in the annual report's directors' or shareholders' section; please add it with a page, or mark it unavailable after looking.
4. **Reported ratios exist but are marked unavailable.** `car_pct` and `npl_pct` are "unavailable" for FY2021 to FY2025 ("not yet extracted from detailed notes"). Annual reports of Ghanaian banks print both in the risk or capital note. Without them the CAR proxy is calibrated on a single interim point (16.35% at 9M-2026) and the history cannot be checked against reported ratios. Extract them with page numbers or state that the note was read and does not contain them.

## Suggestions (not blocking)
- sources.md says the FY2025 AGM copy has a blank auditor signature line. The five-year summary pp.117-118 carry five years of history; a second source for FY2024 and FY2023 (the FY2024 report on the GSE) was listed but, per sources.md, not used for a cross-check. A consecutive-report comparison (FY2024 as printed in the FY2025 report vs the FY2024 report) would catch restatements, which SCB and Zenith both had.
- The half-rate interest sensitivity (`0.5 * policy_delta * (loan + investments)`) is disclosed as illustrative. It makes interest income move with the policy rate on the whole interest-earning book, but the cost side uses the 91-day bill on deposits only, with no link to the policy rate. State in assumptions.json why.
- Fee income and expense are unavailable for FY2021, FY2022 and 9M-2026 (net fee only). Acceptable and disclosed; the sector comparison will need the net figure.

## What I could not verify
- Any historical figure against its source PDF (see item 5 above).
- The 9M-2026 balance sheet beyond the headline items the author checked.
- Whether the FY2025 report on the AGM site is the final signed version.

## Request to the author
Fix items 1 to 4, set the claim to `needs-review` with `review_revision` and `review_macro` set to the new fingerprints, and post a TO claude-helper-1 message listing the changed files. I will re-review within the same session.
