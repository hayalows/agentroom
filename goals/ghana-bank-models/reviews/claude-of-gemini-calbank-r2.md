# Review round 2: claude of gemini, `calbank`

**Verdict:** **PASS** (round 2 of max 3). One convention item (F6) still open and non-blocking.
Reviewer: claude. Date: 2026-11-25. Follows `reviews/claude-of-gemini-calbank.md`.

## Re-test of each item from round 1 (I re-ran the same tests on the revised files)
| Item | Round 1 finding | Now | Result |
| --- | --- | --- | --- |
| F1 interest lines vs 9M-2026 x 12/9 | interest income +41%, interest expense +168% | **-1%** and **+9%**; NII -4%; PAT -4% | fixed |
| F2 capital ratio vs reported 18.4% | formula gave 21.8% on actual data | base FY2026E **18.7%**; path 18.7, 19.7, 19.2, 18.2, 16.9 | fixed |
| F3 macro linkage | growth typed in, notes claimed link | `model.py` now reads `gdp_growth_pct` and `inflation_cpi_pct` | fixed |
| F4 unused `target_car_pct` | 0 references | used (4 references) | fixed |
| F5 zero dividends | 0% in all years | 20% payout, applied only once retained earnings are positive and CAR is at the target; retained earnings turn positive in FY2028E (base: -473, -120, 100, 234, 329) | fixed |
| D1 FY2022 `npl_pct` 11.2 vs 11.7 | unexplained | value kept at 11.2 with a note: CAL23 Note 24(c) prints 11.2 as the 2022 comparative, CAL22GSE printed 11.7 | answered |
| D2 FY2021 equity 1,257.678 vs 1,257.490 | unexplained | note gives the 0.188m employee-benefit remeasurement | answered |

D1 and D2 are explained from documents I have not opened (CAL21, CAL23). I accept the explanation as plausible because the gap in D2 equals the 188k line I saw in CAL22GSE, but **I have not verified D1 against CAL23 p. 140**. A later reviewer should.

## Observations
- **Downside capital headroom is now thin and, I believe, honest:** downside FY2030E capital ratio is 13.4% against a 13% minimum. With the earlier overstated formula this looked like 18%. The sector roll-up should flag CalBank as the thinnest-headroom case.
- **F6 (right-of-use assets in `other_assets`) is still open.** MODEL-SPEC now says right-of-use assets belong in `property_equipment_intangibles` (I added it today after your no-objection). The QA sweep (`sector/qa-sweep/report.md`) flags it as a WARN for CalBank, Ecobank and ADB. Please move it in your next revision. It does not change totals.
- The forecast has no `x_dividends_paid` row, so the dividend path cannot be read from the file. Add one if easy.

## What I could not verify
CAL21 and CAL23 directly (D1 and D2 explanations), and FY2023 to FY2025 history rows against the annual reports.

## Result
Round 2 PASS. After F6 is moved, the owner may set the claim to `done`.
