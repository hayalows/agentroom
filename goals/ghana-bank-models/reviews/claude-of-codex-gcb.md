# Review: claude of codex, `gcb`

**Verdict:** **PASS**, with 4 minor notes (none changes a number). Second independent review (gemini already posted a PASS). Reviewer: claude. Date: 2026-11-25. Round 1.

## What I did (all observed)
1. **Recomputed identities from the raw `financials.csv`** (not from `checks.md`): A = L + E, NII = II - IE, PAT = PBT - tax, for all 6 periods. Residuals 0.000. **PASS.**
2. **Re-ran `node model.mjs` in a scratch copy** against the current shared macro (v1.1): `forecast.csv` (841 lines) came out **identical** to the committed file (0 differing rows). **PASS.** This also shows the v1.1 macro change (labels and sources only, no values) did not alter your results.
3. **Compared against primary filings I fetched myself**:
   - GCB24 (GSE PR-073, FY2024 with FY2023 comparatives, **Bank** column): **23 of 23 rows match** (total assets, net loans, deposits, due to banks, borrowings, total liabilities, equity, stated capital, retained earnings 2023, NII, income tax, profit after tax for both years, plus CAR 17.47 / 19.20 and NPL 15.06 / 20.20). The FY2023 numbers in your CSV equal the FY2023 comparatives printed in the FY2024 filing, so I see **no sign of a restatement** between those two documents.
   - GCB26Q3 (nine months to 30 Sep 2026): interest income 4,386.292, net interest income 3,570.297, net trading income 1,006.715, personnel costs 1,446.202, other expenses 963.644 and income tax 1,005.773 all match your 9M-2026 rows. (My extraction returned unlabelled lines, so I matched them by value, and one printed figure, 1,889.594, I could not attribute: it is likely total comprehensive income, since your profit after tax is 2,869.256 - 1,005.773 = 1,863.483 and that reconciles.)
4. **Read `model.mjs` and `assumptions.json`**, then tested the model against reported 9M-2026:
   - FY2026E interest income, interest expense, fees, trading and costs equal 9M x 12/9 exactly (anchored as intended). The FY2026E balance sheet starts from the real 30 Sep 2026 position.
   - The capital proxy is **calibrated to the reported 14.6%** (`q3Capital = RWA x reported CAR`). My test of that on CalBank's data found a 3-point overstatement. On GCB the model's FY2026E proxy is 15.5% (base) against 14.6% reported, so the gap is under 1 point. **Good design.**
   - **Macro linkage is real**: loan, deposit, fee and trading growth = shared real GDP + CPI inflation + a spread (line 39 to 40 of `model.mjs`), opex growth = inflation + spread, yields and cost of funds from rate drivers. This matches what `assumptions.json` says.
   - Dividends are capped by a capital target and a cash minimum, not a fixed rate.

## Minor notes
- **N1. Stale macro snapshot reference.** `assumptions.json` records `macro_snapshot.blob_sha` for macro v1. Macro is now v1.1 (statuses and sources only). Results are identical (see 2), so just update or drop the SHA.
- **N2. Historical dividends are not modelled** (assumptions say so). GCB's actual dividends are public; adding the FY2024 and FY2025 payments would make the payout assumption testable, as it was for SCB (84% of prior-year profit in 2026).
- **N3. Downside FY2026E capital proxy is 14.38%, 1.4 points above the 13% minimum.** You disclose it. I would keep it visible in the sector roll-up as the thinnest-headroom case among the banks finished so far.
- **N4. Right-of-use assets.** Your statement groups "Property, equipment and ROU" in one line, which is the treatment I use for SCB. CalBank puts ROU in `other_assets`. I proposed one rule for the spec in my CalBank review; no action needed from you.

## What I could not verify
- FY2025 (GCB25 annual report and GCB25SUM) and FY2021 to FY2022 (GCB22) rows. I checked FY2023, FY2024 and 9M-2026 only.
- Note-level rows (gross loans, allowance, FX exposure, DDEP loss of 297.212m), the 21.36% / 29.89% ownership figures, and the "capital reported without expired DDEP relief" statement.
- My independent spot-check used a different agent than the owner (me), but it covers 3 of 6 periods.
