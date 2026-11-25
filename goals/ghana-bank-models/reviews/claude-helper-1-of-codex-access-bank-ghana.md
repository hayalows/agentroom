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


## Review 2: 2026-11-25
Verdict: PASS
Package SHA-256 fingerprint: 579d12a3f8364d5bedef54f9c4c5d3e5168612d7d63420a9ca7bbe883bca3949
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
Reviewed version: main after commit 566046a (codex repair) as of 2026-11-25 ~13:55 UTC. Line numbers below are file lines. The package fingerprint equals the review_revision in the claim.

My four Review 1 items are closed. Two small presentation caveats remain and do not block acceptance of the package.

## What I checked (observed unless marked)
1. **Gate, run locally** with `gateBank()`: status `core-checks-pass`. Package, schema (241 history and 660 forecast rows, 0 bad, 0 duplicate, 5 annual periods, 15 scenario-years), arithmetic (63 core bridges, 0 failed) and macro all score 100. **Item 1 is fixed**: model.py now names `macro.csv` in its docstring (line 1) and assumptions.json points at `../../sector/macro-assumptions/macro.csv` (line 4).
2. **Replay.** I copied financials.csv, assumptions.json and model.py plus the shared macro file into a scratch tree and ran `python3 -I model.py`. It wrote 660 rows with no negative investments and no CAR below the scenario minimum. `cmp` showed forecast.csv and checks.md **byte-identical** to the committed files.
3. **Item 2 (tax).** README line 21 now explains the FY2025 rate of 56.22%: tax 367.830m includes a 127.231m change in prior-year estimates (ACCESS25AR note 14 pp.95-97), and the 35% forecast rate is tied to the 9M-2026 effective rate (35.0%, my own recomputation 197.662 / 564.748) and excludes a repeat of the prior-year item. That is an adequate disclosure. I did not open note 14 myself (see below).
4. **Item 3 (ownership).** README line 3 now states the bank is GSE-listed and that Access Bank Nigeria PLC held 93.40% at 31 December 2025 (ACCESS25AR p.115), with current ownership marked unverified. Adequate.
5. **Item 4 (ratios).** `car_pct` and `npl_pct` are now reported rows for all five years and 9M-2026 with source and page, for example CAR FY2021 35.68, FY2023 23.47, FY2025 17.70, 9M-2026 16.35 and NPL FY2021 9.90, FY2023 3.90, FY2025 9.16, 9M-2026 4.51. `tier1_pct` stays `unavailable` with no value, which is the correct status.
6. **Independent source evidence.** I did not re-retrieve the PDFs (the fetch tool refused them in Review 1). I relied on chatgpt-support's independent visual check posted on the board (37 exact comparisons against the source images, 2 FY2021 presentation differences, 3 CET1 supplement gaps). That check is theirs, not mine; I read its summary line, not the source pages.

## Remaining notes (not blocking)
- **N1. FY2021 balance sheet basis.** financials.csv takes FY2021 total assets 6,128.726 / 7,491.295 and total liabilities from the five-year series (ACCESS25AR pp.117-118). chatgpt-support found the FY2021 summary printed assets and liabilities each 35.874m lower, with equal equity, a possible gross-versus-net deferred-tax presentation that is unconfirmed. Neither README nor sources.md mentions it (a search for `35.874`, `presentation` and `deferred` found nothing). Please add one sentence stating which series was used and that the other differs by 35.874m on both sides. This does not change any ratio or the forecast, which starts from FY2025 and 9M-2026.
- **N2. CET1.** The 3 CET1 supplement gaps stay unresolved; Tier 1 is marked unavailable, which is honest.
- **N3. Core gate limits.** The gate checks link, schema and arithmetic only; it does not prove the numbers match the filings or that the capital proxy is prudential.

## What I could not verify
- Any historical figure against the source PDF myself (fetch refused). Provenance rests on codex's page references and chatgpt-support's independent visual check.
- The FY2025 signed report and the actual FY2025 dividend payment, which codex also flags as needing independent confirmation.
- Whether the 9M-2026 balance sheet matches the source beyond the headline lines.


## Review 3: 2026-11-25
Verdict: PASS
Package SHA-256 fingerprint: 735000270faf42f7ebeecf031d9006c710c6cdc6b358208a73987e782b4054ac
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
Reviewed version: main at commit 8143691. This covers the package changed after my Review 2 (fingerprint 579d12a3...).

**What changed (observed).** `git diff` from my Review 2 commit to this one touches one file in the package: `banks/access-bank-ghana/sources.md`, 4 added lines (a "FY2021 presentation discrepancy" section). financials.csv, assumptions.json, model.py, forecast.csv and checks.md are unchanged, so my replay result in Review 2 (byte-identical forecast and checks) still stands. The gate was run again: `core-checks-pass`, package fingerprint as above.

**Note N1 from Review 2 is closed.** The new section says the history uses the five-year series (ACCESS25AR pp.117-118: FY2021 assets 7,491.295m, liabilities 6,128.726m), that the FY2022 issuer summary (ACCESS22SUM p.1) gives 7,455.421m and 6,092.852m, and that the gap is 35.874m on both sides with equal equity of 1,362.569m. I recomputed both differences from those figures: 35.874 and 35.874, and equity 7,491.295 - 6,128.726 = 7,455.421 - 6,092.852 = 1,362.569. The note is consistent and honest that the cause is unverified.

**Is the five-year series the right choice? (inferred).** Yes, as a working basis: it is the later publication, it matches the FY2022 to FY2025 statements in the same series, and the difference affects only FY2021 gross-up (equity and profit are unchanged), so no ratio or forecast input moves. The owner should keep the "not reconciled" wording until the 2022 annual report detail is read.

**Still open (not blocking).** N2 (CET1 supplement gaps) and N3 (the gate checks structure and arithmetic only) from Review 2 stand. I did not re-read any source PDF.
