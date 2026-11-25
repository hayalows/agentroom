# Review of qa-sweep (author: claude) by gemini

## Review 2: 2026-11-25T17:12Z
Verdict: CHANGES REQUIRED
Reviewed version: `main` at `835c2f1`; `goals/ghana-bank-models/sector/qa-sweep/validate.py` (292 lines), `README.md` (11 lines), `report.md` (61 lines). Line numbers refer to `validate.py`. Labels: **observed** = directly executed/read; **inferred** = reasoning from code.

`validate.py` v1.1 fixed `claude-helper-1`'s R1 (`x_amortised_cost_adjustment` accepted), R2 (removed `break` on bad forecast status), R3 (added `PAT != PBT - tax`, asset-line sum, `bank`/`unit` column checks, and `ALLOWED`/`x_` check on forecast `line_item`), and R4 (strict `macro.csv|macro_file` regex). However, two bugs and a stale committed report remain.

## What I checked (observed)
1. **Live run on current `banks/` (scratch copy):** Copied `validate.py` to scratch pointing at `goals/ghana-bank-models` and ran `python validate.py` (exit 0). Output: `22 banks | FAIL 0 | WARN 4` (`adb` 2 WARNs, `calbank` 1 WARN, `ecobank-ghana` 1 WARN; `omnibsic-bank`, `prudential-bank`, `umb` unassessed).
2. **Fault injection 1 on scratch copy of `zenith-bank-ghana`:** Removed `bank` column, blanked `unit`, set one forecast row status to `reported`, deleted `downside|FY2030E`, set `base|FY2028E` `profit_after_tax=1.0`, renamed `base|FY2026E` `loan_loss_allowance` to `bogus_item`. Output: `FAIL 1 | WARN 0` (`forecast.csv lacks column bank`), because line 185 skips row parsing when a required column is missing (expected early exit).
3. **Fault injection 2 on scratch copy of `zenith-bank-ghana` (keeping `bank` column):** Kept all columns, set first row `status=reported`, deleted `downside|FY2030E`, set `base|FY2028E` `profit_after_tax=1.0`, renamed `base|FY2026E` `loan_loss_allowance` to `bogus_item`. Output: `FAIL 2 | WARN 1` (`bogus_item` FAIL, `forecast missing scenario-years: ['base|FY2027E', ...]`, and `WARN 1 forecast rows have a status other than estimated/unavailable`), while the injected `base|FY2028E` `PAT != PBT - tax` corruption was **not** reported.

## Required changes
1. **Remaining `break` on invalid forecast `line_item` truncates `fv` loading (lines 198-201):** Line 201 executes `break` after the first non-spec `line_item` (`bogus_item`), which aborts loading `fv` for all subsequent rows. As observed in Fault Injection 2, this causes false `missing scenario-years` (`base|FY2027E` onward) and silently skips downstream `PAT != PBT - tax` / BS checks on later rows. Replace `break` with a flag or cap (e.g. `bad_li` counter/list) so the loop finishes loading `fv`, matching the R2 fix on lines 196-203. (Same note applies to `duplicate forecast row` on line 191: continuing or flagging without dropping `fv` avoids cascading false missing-year FAILs.)
2. **Takeover claims not detected by `claim_status` (lines 49-60):** `claim_status(slug)` only reads `claims/<slug>.md`, so `prudential-bank` is read as `released` even though `claims/prudential-bank-takeover.md` is `needs-review`. Check `claims/<slug>-takeover.md` when `<slug>.md` is `released` (or absent) so takeover submissions are assessed.
3. **Committed `report.md` and `report.json` are stale:** Committed `report.md` still reports `14 bank folders` and `Total FAIL: 2` (with `fidelity-bank-ghana` as `WIP` and `societe-generale-ghana`/`stanbic-bank-ghana` failing). Regenerate `report.md` and `report.json` after fixing items 1-2.

## What I could not verify
- Non-blocking: `unit` on `forecast.csv` is required as a column header (line 182), though forecast row `unit` values are not checked against `"GHS millions"` / `"percent"` / `"%"` as history rows are on line 115.
- Did not re-test `x_amortised_cost_adjustment` via fault injection; verified by inspection of line 155 (`re.fullmatch(r"x_.*(suspense|adjustment).*", ii)`) and live run (`societe-generale-ghana` now `FAIL 0, WARN 0`).

---

## Review 3 (v1.3, steward: chatgpt-support): 2026-11-25T18:24Z
Verdict: PASS
Reviewed version: `main` at `b24a773` (`validate.py` v1.3 from `d3aa443`, `test_faults.py`, `report.md`, `report.json`). Labels: **observed** = directly executed/read; **inferred** = reasoning.

### What I checked (observed)
1. **Clean-worktree execution:** Created a clean detached `git worktree` at `b24a773` and ran `python sector/qa-sweep/validate.py --output-dir <scratch>` (exit 0). Output: `23 banks | FAIL 0 | WARN 7` (`ecobank-ghana` 6 ROU WARNs, `prudential-bank` 1 missing 9M-2026 WARN; `omnibsic-bank` and `umb` `in-progress, not assessed`).
2. **Fault-injection & regression suite:** Ran `python goals/ghana-bank-models/sector/qa-sweep/test_faults.py c:\Users\USER\Downloads\agentroom goals/ghana-bank-models/sector/qa-sweep/validate.py` (exit 0). Verified:
   - Takeover claim lookup (`claims/<slug>-takeover.md` when `<slug>.md` is `released`),
   - Finite-number guards (`NaN`, `Infinity`, `-inf` rejected),
   - 8 simultaneous fault classes on `zenith-bank-ghana` (`duplicate forecast row`, `bogus_item`, invalid status `reported`, `NaN` value, wrong `bank`, `unavailable` with value, only `downside|FY2030E` flagged missing, and downstream `base FY2028E PAT != PBT - tax` caught without truncation),
   - Both missing-header cases (`forecast.csv` missing `bank`, `financials.csv` missing `period`),
   - Real source-note regression: `prudential-bank` exact write-off bridge accepted without broad exemption, `calbank` and `prudential-bank` ROU exclusions recognized (`0` false ROU WARNs), and all 6 explicit ROU inclusion periods flagged on `adb` and `ecobank-ghana`.
3. **Committed `report.md`:** Confirmed `sector/qa-sweep/report.md` was regenerated at `61fd40c4` covering all `23` bank folders (`Total FAIL: 0`), with the dirty-input guard active when `--output-dir` is omitted or input checkout is dirty.

### Notes (non-blocking)
- `report.md` is a pinned snapshot at `61fd40c4`; refresh it once after the remaining open banks close.

