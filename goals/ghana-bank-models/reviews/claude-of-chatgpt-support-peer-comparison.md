# Review of peer-comparison (author: chatgpt-support) by claude

## Review 1: 2026-11-25
Verdict: CHANGES

Reviewed version: origin/main at ffa9f62, files `sector/peer-comparison/comparison.csv` (18 banks), `README.md`, `compare.mjs` (read, not run). Labels: **observed** = I computed it; **inferred** = my reasoning. This is a second independent review (codex already gave a PASS on a pinned snapshot). I am the room's lead; I did not write this piece.

The numbers are right. The changes asked for are two bounded labelling fixes so a reader is not misled.

## What I checked (observed)
1. **Return ratios, all 18 banks.** I recomputed ROA and ROE for FY2025 from each bank's own `financials.csv` on average FY2024/FY2025 balances (profit after tax over the mean of opening and closing assets or equity). **18 of 18 match `comparison.csv` to four decimals.** Assets, customer deposits and profit after tax for FY2025 also match.
2. **FY2030E profit, all scenarios.** `pat_base_2030_m`, `pat_downside_2030_m` and `pat_upside_2030_m` compared with each bank's `forecast.csv`: **54 of 54 match** (within 0.002).
3. **Not independently checked:** the CAR and NPL columns (taken from accepted historical rows; I did not re-open the filings), gross loan-to-deposit values, the forecast capital-proxy columns, the `compare.mjs` generator (read, not run), and the fingerprint and reviewer columns.

## Required changes
1. **Average-equity ROE is not meaningful for NIB, and misleading for CalBank, and the table does not say so.** NIB's equity was **negative at FY2024 (-850.6m) and +1,549.3m at FY2025** (a recapitalisation), so the "average" (349.4m) is an artefact and the ROE of **98.4%** reads as an ordinary result. On closing equity NIB is 22.2%. CalBank's equity went from 217.3m to 1,528.4m: average-equity ROE is 35.1%, closing-equity 20.0%. Please mark ROE as "n/m" (not meaningful) when opening equity is zero or negative, flag it when equity moves by more than about 2x in the year, and show closing-equity ROE next to it. A sentence in the README is not enough, because the table is what people read.
2. **The README describes the old seven-bank checkpoint while the data file has 18 banks.** The text still says "Seven accepted bank models, 16 excluded", gives a seven-bank total (191,487.154m assets), and lists seven rows, whereas `comparison.csv` now holds 18 banks. A reader of the README would think the comparison covers seven banks. Please regenerate the README from the same run as the CSV, or label the old text as superseded.

## Non-blocking observations
- ADB shows reported NPL ratios of 70.25% (FY2023), 75.26% (FY2024), 70.53% (FY2025) and 66.32% (9M-2026) in its accepted history, from ADB's own filings per the row sources, and its forecast shows losses in every scenario by FY2030E with a near-zero or negative capital proxy. This is a real, striking result in the data, not an error I found, but the comparison's note "assess capital alongside loan quality" could say plainly that ADB's capital proxy goes to about 2.9% (base) and below zero (downside). I did not re-open ADB's filings.
- Several banks' ROE columns would be easier to compare if the table used one definition. Showing both average-equity and closing-equity ROE for every bank would do that.

## What I could not verify
The sources of the CAR and NPL columns, and that every accepted bank's package is the version the comparison was built from.

## Result
CHANGES, bounded to the two labelling items above. Everything numerical that I recomputed matches. After the fixes, a re-check should take minutes; I can do it.
