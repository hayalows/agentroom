# Review of qa-sweep (author: claude) by claude-helper-1

## Review 1: 2026-11-25
Verdict: CHANGES
Reviewed version: main after commit 618a75c; sector/qa-sweep/validate.py (280 lines), README.md, report.md. Line numbers are file lines of validate.py. Labels: observed = I ran it; inferred = my reasoning.

The sweep is a useful structural check and runs cleanly. It has one false FAIL, one bug that produces misleading FAILs, several checks that are too weak to catch real errors, and a stale committed report. This tool is a reviewer aid, so false results matter more than usual.

## What I checked
1. **Re-run (observed).** I copied validate.py to a scratch tree with symlinks to banks/ and claims/ and ran `python3 -I validate.py`. Result: 9 banks, FAIL 4, WARN 10. The committed report.md says FAIL 0, WARN 4 and lists societe-generale-ghana as in-progress ("missing README.md") and Zenith with 337 rows. It is stale: SG is now needs-review and Zenith has 346 history rows. Regenerate before anyone relies on it.
2. **Fault injection on a scratch copy of Zenith (observed).**
   - Changed one forecast status to `reported` and deleted only downside FY2030E. Result: a FAIL listing `base|FY2027E ... downside|FY2026E ...` as missing, though only one scenario-year was removed (see R2).
   - Set base FY2028E profit_after_tax to 1.0, renamed `loan_loss_allowance` to `bogus_item`, blanked every `unit` and removed the `bank` column from forecast.csv. Result: **FAIL 0, WARN 0** (see R3).
3. **Read of the logic (observed).** Every rule in the README exists in the code except where listed below.

## Required changes
1. **False FAIL on societe-generale-ghana (lines 151-157).** The gross-loans bridge allows only `x_interest_in_suspense` to explain the gap between gross less allowance and net loans. SG also reports an amortised-cost adjustment (`x_amortised_cost_adjustment`). The four "unexplained" amounts are 28.390, 45.951, 60.281 and 71.229 for FY2021 to FY2024, and these equal that adjustment to the third decimal (checked in SG's financials.csv). The bank reconciles exactly. Accept any `x_` loan reconciling item that the notes name, or include `x_amortised_cost_adjustment` in the bridge.
2. **A WARN `break` truncates the forecast read (about lines 190-194).** On the first forecast row whose status is not `estimated` or `unavailable`, the loop appends a WARN and executes `break`. That stops both the duplicate check and the loading of values into `fv`, so the later checks see an almost empty forecast: the scenario-year, balance-sheet and anchor tests then give false or misleading results (observed in test 2 above). Replace the `break` with a flag so the loop continues.
3. **Forecast checks are too weak to catch real errors (observed).**
   - Forecast line items are not tested against the spec list, so `bogus_item` passes. Apply the same `ALLOWED` or `x_` rule that history uses.
   - Only total assets = liabilities + equity and NII = income - expense are tested. A corrupted forecast profit after tax passed. Add PAT = PBT - tax, PBT = operating income - costs where all lines exist, and the sum of asset lines.
   - Required forecast columns are only scenario, period, line_item, value and status (lines 175-176). `bank`, `unit` and `notes` are not required, and column order is not checked, so SG's non-standard layout (scenario last, extra source_id and page) passes silently. At least require `bank` and `unit`, and WARN on a different order.
4. **Macro link test is a substring match (the final block).** `"macro" in a.lower()` accepts the word in any note. The core gate requires the text `macro.csv` or `macro_file` in the implementation file. Use the stricter rule so the two tools agree.

## Suggestions (not blocking)
- `SECTOR_ASSETS_DEC25` (line 33) is defined and never used; remove it or use it in the roll-up coverage.
- The asset-line WARN says "due_from_banks may be inside another line" but SG's gap is `x_trading_assets` and equity investments. Say "an x_ asset line may be missing from the sum" and name the shortfall.
- The anchor test reads only 9M-2026. A bank with H1-2026 as its interim period is skipped without a message.
- Tell the reader in report.md the date and commit it was generated at, so a stale report is visible.

## What I could not verify
- Whether `claim_status` correctly handles claims with several `status:` lines in the future; it takes the last one, which matched every claim today.
- That the thresholds (25% anchor gap, 30% asset CAGR, assets 500 to 150,000) suit all banks. I did not test them against banks other than the nine present.

## Request to the author
Fix items 1 to 4, regenerate report.md and report.json, set the claim to `needs-review` and post a TO claude-helper-1 message. I will re-run the same fault injections.
