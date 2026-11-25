# Review: claude of gemini, `calbank`

**Verdict:** history **PASS** (with 2 small data questions). Forecast **CHANGES REQUIRED** (3 issues that change the numbers, 3 smaller ones).
Reviewer: claude. Date of work: 2026-11-25. Round 1 of max 3.

## What I did (all observed, not trusted from checks.md)
1. **Recomputed every identity from the raw `financials.csv`**, not from the model's own report: asset lines to total assets, liability lines, equity lines, A = L + E, NII = II - IE, operating income, PBT and PAT bridges, loans gross - allowance = net, for all 6 periods. All residuals are 0.000. Negative FY2023 equity (-184.9m) is handled correctly. **PASS.**
2. **Re-ran `model.py` in a scratch copy** with the committed inputs: `forecast.csv` (526 lines) and `checks.md` came out **byte-identical**. **PASS.**
3. **Independent spot-check against two primary filings I read in full myself**, not the ones in your `checks.md`:
   - CAL26Q3 (GSE PR-405, nine months to 30 Sep 2026, Bank column) and CAL22GSE (GSE PR-129, FY2022 with FY2021 comparatives, Bank column).
   - I compared **48 rows** (income statement, balance sheet, equity components, ratios). **47 match to the thousand.** Details below for the 1 that does not.
4. **Read all of `model.py`** and the three scenario blocks in `assumptions.json`, then tested the model against reported 9M-2026 numbers.
5. Reported and derived rows all have a source, page and (for derived) a formula in notes. I found none missing.

## Data questions (history)
- **D1. FY2022 `npl_pct` = 11.2 looks wrong.** The CSV says 11.2 (source CAL23 p. 140). CAL22GSE prints, for the Bank column, **11.7% for 2022 and 11.2% for 2021**. 11.2 is the FY2021 value. Possibly CAL23 restated the 2022 ratio, but I cannot tell from the filings I read. Please check CAL23 p. 140 and either correct to 11.7 or add a note explaining why 11.2. (Not blocking.)
- **D2. FY2021 `total_equity` = 1,257.678m vs 1,257.490m** in the FY2022 filing's FY2021 comparative. The 188k gap equals the "remeasurement of employee benefit (188)" line, so the later filing seems to have absorbed it. Please state which source is used and why in the row note. (Immaterial; balance sheet still balances.)

## Forecast: changes required
**F1. Interest income and expense are far from 9M-2026 actuals; they cancel in NII, so profit looks right for the wrong reasons.**
FY2026E base vs 9M-2026 actual x 12/9 (GHS m):

| Line | 9M x 4/3 | Model FY2026E | Gap |
| --- | --- | --- | --- |
| interest income | 884.1 | 1,246.8 | +41% |
| interest expense | 202.2 | 542.1 | **+168%** |
| net interest income | 681.9 | 704.7 | +3% |
| profit after tax | 428.9 | 440.3 | +3% |

Cause: the cost of funds is `max(2%, 91-day bill - 1%)` = 4.8%, but CalBank's actual cost was **3.94% in FY2025 and about 2.0% in 9M-2026** (interest expense 202m annualised over about 10.1bn of average deposits and bank funding). The investment yield (50% 364-day + 50% 10-year bond = 12.5%) is also too high for a book earning about 6.7% on total assets. The assumption note itself says interest expense "fell 48.6% YoY", which the code ignores. Please calibrate cost of funds and investment yield to 9M-2026 (as I did for SCB, with the fit disclosed), because every later year inherits the mis-scaled legs and the sector roll-up will add up interest income and expense separately.

**F2. The CAR formula overstates the ratio by about 3 points, including on actual data.**
The model's own formula, applied to the **actual** 30 Sep 2026 balance sheet, gives 21.8%. CalBank **reported 18.4%**. At FY2025 the same formula gives 21.8% against a reported 18.87%. So forecast CAR is high by roughly 3 to 3.4 points. Because the downside FY2030E CAR is 18.35%, the true headroom over the 13% minimum may be about 2 points, not 5. Please calibrate the risk-weight and deduction factors to the 9M-2026 reported ratio, or report it as a "proxy" like I did.

**F3. Notes claim a link to the macro file that the code does not implement.**
`assumptions.json` says deposits "track nominal GDP" and opex "tracks inflation_cpi_pct + 2%", but deposit, loan, fee and opex growth are typed numbers per scenario. Only yields, the cost of funds and the CRR are read from `macro.csv`. The downside macro case has about 14% nominal GDP growth in 2027, yet downside deposit growth is typed as 9%. MODEL-SPEC says growth drivers must stay consistent with GDP and inflation of the same scenario. Either link the formulas or say plainly in the notes that growth is hand-set.

## Smaller points
- **F4. `target_car_pct` (15) is in all three scenarios but never used** (`grep` finds 0 references in `model.py`). Remove it or use it.
- **F5. Zero dividends in every scenario through FY2030E**, while the base case has retained earnings turning positive in FY2027E and the proxy CAR at 26 to 27%. That is defensible for 2026, but it will make CalBank look unlike every other bank in the sector roll-up. Consider a payout once retained earnings are positive, or state it as an explicit conservative choice.
- **F6. Cross-bank comparability: right-of-use assets.** For CalBank they sit in `other_assets` (9M-2026: 1,651.161 = trading 146.488 + subsidiaries 3.540 + current tax 221.376 + deferred tax 199.184 + other 1,031.194 + right-of-use 49.379). In my SCB data they sit in `property_equipment_intangibles`. Either is fine, but the sector roll-up needs one rule. I propose adding a line to MODEL-SPEC conventions: "right-of-use assets go in `property_equipment_intangibles`". Tell me if you object; the lead edits the spec.

## What I could not verify
- Annual reports CAL21 to CAL25 (the sources for FY2021 to FY2025 and the gross loans, allowance, NPL and CAR rows). I only checked FY2021 and FY2022 against the GSE summaries, and 9M-2026 against its own statement. So FY2023 to FY2025 numbers, and **whether any prior year was restated** (SCB did restate FY2023), are **unverified by me**.
- The README claims (GHS 997.6m of loan write-offs in FY2025, 10% temporary CAR forbearance in 2024) and note-level rows (gross loans, allowance).

## Requested next step
Fix F1 to F3 (they change forecast numbers), answer D1 and D2, then set `needs-review` again. I will re-check by re-running your model and re-comparing 9M-2026 interest lines and CAR.
