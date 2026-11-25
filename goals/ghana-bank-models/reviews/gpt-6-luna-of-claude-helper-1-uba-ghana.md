# Independent review: UBA Ghana (round 1)

Owner: claude-helper-1  
Reviewer: gpt-6-luna  
Reviewed against current claim `uba-ghana` and the exact files on main.

## Verdict

Verdict: PASS  
Package SHA-256 fingerprint: 1bd39e82a7410403b12c6ddf003fd8d9ab9590cc635af28e4f8d272c5d8ae27e  
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

The independently computed fingerprints match the claim's `review_revision` and `review_macro`. This verdict applies to those files only.

## Checks performed

- Rechecked the read-only package gate conditions: 341 historical rows, 671 forecast rows, 7 observed periods including five annual years, all 15 expected scenario-years, no duplicate keys, invalid status/value combinations, or missing source/page fields on reported rows. The assumptions and model both reference the shared macro file.
- Independently recomputed the historical statement identities across all 7 periods: NII, operating income, PBT, PAT, assets versus liabilities plus equity, asset totals, liability totals and equity totals. Maximum absolute residual was GHS 0.001m, consistent with rounded inputs.
- Recomputed the FY2021–FY2025 loan-note bridges: gross loans less allowance equals net loans, and the three loan stages sum to gross loans. Maximum absolute residual was GHS 0.001m.
- Independently recomputed all 15 scenario-year forecast balance, asset-total, NII, PAT and equity-roll checks. Maximum absolute residual was GHS 0.001m; no failures.
- Ran `model.py` in an isolated copy with the exact submitted inputs and current macro file. It generated 671 forecast rows with zero reported failures. The generated `forecast.csv` and `checks.md` matched the submitted files byte for byte.
- Checked reported numbers against the official UBA FY2025 audited statement and Q3 2026 statement. FY2025 PBT, PAT, assets, net loans and equity agree after conversion from GHS to GHS millions and rounding. Q3 2026 PBT, PAT, assets, deposits and equity agree after converting from GHS thousands to GHS millions.
- Visually checked the one-page FY2025 and Q3 2026 statement PDFs. The selected figures match the extracted text. Neither standalone PDF has printed page numbers; the row references `SoCI` and `SoFP` are appropriate. Detailed visual evidence is in `assistance/claude-helper-1/uba-visual-fy25/gpt-6-luna.md`.

## Limitations to keep visible

The forecast depends on fitted interest-income and funding-cost assumptions with no bank repricing schedule or deposit beta. The README and checks disclose this, including a material securities-yield sensitivity. The profit ordering across macro scenarios is not the conventional downside < base < upside order, and the model explains the rate-sensitive reason. The forecast CAR is an accounting proxy, not regulatory CAR; NPL, Tier 1 and gross loans are unavailable in the forecast. These are disclosed and do not invalidate the accounting model, but readers should not treat the proxies as prudential compliance measures.

This review covers the submitted rows, selected source figures, arithmetic and deterministic forecast replay. It is not a review of every note or every historical source row.
