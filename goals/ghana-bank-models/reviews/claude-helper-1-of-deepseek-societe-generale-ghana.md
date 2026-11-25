# Review of societe-generale-ghana (author: deepseek) by claude-helper-1

## Review 1: 2026-11-25
Verdict: CHANGES
Package SHA-256 fingerprint: 6a04f16b70d895e8cdbe490d2994facecd51c843445e450de762568cf044a18f
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
Reviewed version: main at commit e3f5fe1 (deepseek: societe-generale-ghana complete). Line numbers are file lines. Labels: observed = I ran or read it; inferred = my reasoning.

The package is internally sound and the history reconciles. Four forecast and disclosure issues stop an acceptance verdict. None needs new source data.

## What I checked
1. **Gate (observed).** `gateBank()` returned `core-checks-pass`: package, schema (294 history / 855 forecast rows, 0 bad, 0 duplicate, 5 annual periods, 15 scenario-years), arithmetic (63 core bridges, 0 failed) and macro all score 100.
2. **Replay (observed).** I copied financials.csv, assumptions.json and model.py plus the shared macro file to a scratch tree and ran `python3 -I model.py`. checks.md is byte-identical. forecast.csv differs only in line endings (the committed file uses LF, mine came out with CRLF from the csv writer); content is identical after stripping `\r`.
3. **History arithmetic (observed, my own recomputation from financials.csv).** Assets - liabilities - equity is 0.000 in all six periods. Effective tax FY2021 to 9M-2026 is 34.6, 35.4, 35.8, 34.2, 35.4, 35.4 percent, a stable pattern that supports the 35% forecast rate. Reported CAR and NPL series (22.38, 16.00, 18.71, 19.81, 23.39; 18.52 at 9M-2026) are present with source and page.
4. **Forecast read through (observed).** Accounting identities hold by construction. FY2026E interest income 1,000.559 equals 9M-2026 750.419 x 4/3 exactly, so the anchor is a plain run rate. Base ordering of profit (downside < base < upside) holds in every year (FY2030E -343 / 430 / 829).
5. **Source pages (not verified).** I tried to fetch the Q3-2026 PDF; the fetch tool returned only a noindex metadata block, so I did not verify any figure against a filing. Provenance rests on the author's page references.

## Required changes
1. **Allowance-build floor overrides the stated cost of risk (model.py line 231; assumptions.json cost_of_risk).** The assumptions say 0.8 / 1.5 / 3.5 percent (upside / base / downside) of average gross loans, but the model floors the charge at the allowance increase. Effective impairment over gross loans in FY2030E is **1.86% upside, 1.64% base, 3.36% downside**, and in dollar terms the upside charge (223m) exceeds the base charge (163m) in FY2029E and FY2030E. A stated 0.8% upside rate that produces the highest effective rate in the base-versus-upside pair is not what the assumptions file tells a reader. Either set the allowance ratio so the floor does not bind, or report the effective rate next to the input in checks.md and the README and say that the floor dominates in growth scenarios.
2. **Downside FY2026E Q4 and the tax line.** Downside profit before tax is 120.7m for the year against 232.1m already earned in 9M-2026, so Q4 is a loss of about 111m, driven by a Q4 impairment of about 122m (9M was 27.2m). Tax for the year is 82.1m, which is the 9M tax with no credit for the Q4 loss, an effective rate of 68%. Please either allow the Q4 loss to reverse part of the 9M tax or say this is the model's treatment (no deferred tax credit) in the README.
3. **Unexplained 9M-2026 equity movement and a Q4 dividend with no basis.** Equity fell 23.7m between FY2025 (2,601.8m) and 9M-2026 (2,578.1m) although 9M profit was +150.0m, so other movements are about -173.7m. That is close to a 44% payout on FY2025 profit of 397.0m (inferred, about 175m), which would be a FY2025 final dividend paid in 2026, but nothing in the package says so. The base case then adds a further 17.2m Q4 dividend (`x_model_dividends`, FY2026E) with the note "observed 9M retained earnings already include YTD equity movements". Please document what the -173.7m is (dividend, OCI or other) and justify or remove the 17.2m.
4. **Downside costs grow with inflation while revenue stays flat.** Opex growth is CPI plus 8 points in the downside. Staff costs go from 326m to 637m and total operating costs reach 107% of income in FY2030E, so the downside loss (-343m) is mostly cost pass-through, not credit losses, with no management response. The shared macro downside has higher inflation than base, so the effect is mechanical, but the README presents the loss as a CAR stress outcome. Please say which of the two drives it, and show the downside with base opex growth so a reader sees the credit and rate effect alone.

## Suggestions (not blocking)
- forecast.csv uses column order `bank,period,statement,...,notes,scenario` with `source_id` and `page` blank, while other banks use `bank,scenario,period,statement,line_item,value,unit,status,notes`. The gate reads by column name, but the sector roll-up may not; please align or confirm with the lead.
- All 855 forecast rows are `estimated`, including FY2026E lines that equal observed 9M figures plus a Q4 run rate. A note on those lines saying which part is observed would help.
- NPL is held flat at 12% (base) and 16% (downside) in every year, independent of the cost of risk. Say so in the README.
- The README states the 60.22% parent and 19.36% SSNIT holdings (SG25AR p.136); I did not verify them.

## What I could not verify
- Any historical figure against a filing (fetch refused). The author reports visual spot checks on three values; I did not repeat them.
- The preferred CAR basis (23.39% audited versus 17.5% excluding DDEP reliefs). The author flags this and asks a reviewer to confirm; I cannot.
- Whether the -173.7m equity movement is a dividend.

## Request to the author
Fix items 1 to 4, rerun model.py, set the claim to `needs-review` with the new `review_revision` and `review_macro`, and post a TO claude-helper-1 message listing the changed files.
