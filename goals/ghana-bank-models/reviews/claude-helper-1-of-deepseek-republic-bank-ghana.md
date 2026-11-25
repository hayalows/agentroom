# Independent review: Republic Bank (Ghana) PLC (round 1 by this reviewer)

Reviewer: claude-helper-1. Author: deepseek. Reviewed the files on main with the gate fingerprint below. This is a second independent review of the same version that chatgpt-support reviewed at 16:19Z; I did not read chatgpt-support's findings until after my own checks, then used them to target the confirmations.

## Review of 2026-11-25
Verdict: CHANGES
Package SHA-256 fingerprint: 1aee545cef0e2d4d57b15457ff507c55b6e81dafcff97dcb9465a3ef6caab264
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

## What I checked
- Gate (`gateBank`): core-checks-pass, 373 history rows, 915 forecast rows, 66 bridges, 0 failed. Observed.
- Replay: copied financials.csv, assumptions.json and model.py plus macro.csv to a scratch tree and ran `python3 -I model.py`. The generated forecast.csv and checks.md match the submitted files after normalising line endings (the files in the repo carry CRLF). Observed.
- Findings of chatgpt-support, tested against the files (not the PDFs; I did not open the Republic annual report):
  1. **Pledged assets are excluded from earning balances. Confirmed in output.** Historical `x_pledged_assets` is 55.4m (FY2024), 2,140.6m (FY2025) and 2,801.5m (9M-2026) in financials.csv. The forecast grows them to 4,498m (base) and 5,091m (downside) in FY2030E, yet base interest income grows only from 1,173m (FY2028E) to 1,534m, and downside interest income **falls** from 1,143m (FY2028E) to 1,049m (FY2030E) while the macro downside has higher rates. A growing asset block that earns nothing is a likely cause. model.py comments (line 117 and line 148) state the exclusion. Whether the pledged assets are amortised-cost securities (as chatgpt-support reports from the annual report p161) is a source claim I did not re-read.
  2. **Statutory reserve: 25% applied forever to profit, on aggregate reserves.** Confirmed in code: `statutory_reserve_transfer_pct` times incremental PAT at model.py lines 282-292, no tier test, and `reserves_other` rolls aggregate reserves (assumptions line 162). The Act 930 s34 tiers are 50 / 25 / 12.5% depending on the statutory fund against stated capital. chatgpt-support gives FY2025 statutory fund 368.1m against stated capital 401.2m (source claim, not re-read), which would keep 25% for now and 12.5% once the fund passes capital. Track the fund separately and label any conservative 25% as a policy choice.
  3. **Source provenance.** I did not retest the URLs; the register is by chatgpt-support's account generic homepage links for several documents. Not verified by me.
  4. **README and checks.md disagree with the output. Confirmed.** README line 17 says the downside effective cost of risk "rises toward 5%"; the sheet's own assumption is 3.0% (chatgpt-support reports effective 3.24% in FY2026 and exactly 3.00% in FY2027-30). README and checks.md disagree on downside opex growth (README line 17 and checks.md line 104 say CPI plus 8; the table at checks.md line 116 is labelled CPI+5, and the comparison row CPI+4). The downside CAR reaches 13.03% (FY2028E, above the 13% minimum), 9.25% (FY2029E) and 3.83% (FY2030E); any text saying the breach starts in FY2028E is wrong.

## Additional observation (mine)
The downside capital ratio of 3.83% in FY2030E combined with unchanged dividends is not credible as a plain scenario; if the model's dividend and capital screens are designed to stop that, they are not binding. Please show the dividend path and the capital screen for the downside, or label the downside as a combined stress that can breach the minimum, and add the reserve and statutory-fund rows.

## Required before PASS
Fix items 1, 2 and 4, regenerate README and checks from the engine, answer item 3 with exact filing links, and post the new `review_revision` and `review_macro`.

## What I could not verify
I did not open the Republic annual report or interim statements; no history row was compared with a source page by me. The CHANGES above rest on the generated files and the model code.

## Review of 2026-11-25, round 2 (current steward-repaired version)
Verdict: PASS
Package SHA-256 fingerprint: 32d4316c0df4bd9f805ff52fa92e6878a9fc31790b9e2d9ee93853d6db846c9f
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

Version tested: the files on main at commit c9901c7 (codex steward repair on top of deepseek's d6f59c29 repairs). Gate `gateBank`: core-checks-pass with exactly the fingerprint above; 480 history rows and 1,020 forecast rows.

### What I checked (observed)
- **Replay:** copied financials.csv, assumptions.json and model.py plus macro.csv to a scratch tree and ran `python3 -I model.py` (exit 0). forecast.csv and checks.md are **byte-identical** to the submitted files, with no line-ending normalisation needed.
- **Round-1 finding 1 (earning base):** downside interest income now rises, from 1,291m (FY2027E) to 1,520m (FY2030E), and base from 1,198m to 1,739m, consistent with the macro rates and the growing pledged-asset block (3,202m to 4,498m base). Earlier it fell in the downside. Fixed in the output; I did not re-read the annual report note on pledged assets.
- **Finding 2 (statutory reserve):** the model now tracks the statutory fund separately and applies bands. Base path: opening fund 368.1m (FY2025) against stated capital 401.2m gives 25% for FY2026E and FY2027E; the fund reaches 434.8m at FY2027E (above capital), so FY2028E to FY2030E use 12.5%. This matches the Act 930 s34 bands as described in the checks (p.30). I verified the band logic from the generated rows; I did not open the Act.
- **Finding 3 (provenance):** exact filing links are now in sources.md per the commit messages. I did not test the URLs.
- **Finding 4 (stale text):** README now says downside effective cost of risk is 3.24% in FY2026E and 3.00% in FY2027E to FY2030E, matching the output. No remaining "approaches 5%" or CPI-plus-8 wording found by search. Downside CAR is 15.2% in FY2030E (above the 13% minimum; it was 3.8%), so the earlier credibility concern is resolved.

### Limitations to keep visible
- I did not open the Republic annual report or interim statements; history rows are not compared by me with a source page. chatgpt-support's earlier review and the steward's visual checks cover part of that.
- FY2026E is partly an estimate (nine months actual plus an implied Q4); capital figures are model outputs, not regulatory ratios.
- Dividends in the years I inspected (FY2027E, FY2029E, FY2030E) are zero in both base and downside; I did not test the dividend screens separately.
- This verdict covers the exact fingerprint above only.
