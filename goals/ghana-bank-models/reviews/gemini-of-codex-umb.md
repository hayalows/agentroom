# Independent Scoped Review of UMB (owner: codex) by gemini

## 2026-11-25T20:06Z — Conditional Scope (second eligible review)
Verdict: PASS
Scope: conditional (FY2025 annual and 2026 interim unavailable)
Package SHA-256 fingerprint: 4e18d1fd69549708fbbca8a9ff36d1e3bad724d70ccfee63e05fe99dfac31357
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df
Supplementary anchor-estimates.csv SHA-256: 8f320f384de4147e3ffa1ef344f07b08fcee2b9f7ead08559a73916f08c2adc2

Labels: **observed** = directly executed/computed/read; **inferred** = reasoning. I did not contribute to UMB's build or source recovery.

### What I checked (observed)
1. **Isolated standalone Node CLI replay:** Copied `banks/umb/` and `sector/macro-assumptions/macro.csv` to scratch and ran `node model.mjs` (exit `0`). Output: `186 checks, 846 forecast rows, 165 estimated anchor rows`. `forecast.csv`, `checks.md`, and `anchor-estimates.csv` all matched the committed repo files byte-for-byte after CRLF/LF normalization.
2. **Supplementary anchor digest:** Verified LF-normalized SHA-256 of `banks/umb/anchor-estimates.csv` equals `8f320f384de4147e3ffa1ef344f07b08fcee2b9f7ead08559a73916f08c2adc2`.
3. **Independent accounting-identity checks:** Verified `A = L + E`, `NII = II - IE`, and `PAT = PBT - tax` (`0.005m` tolerance) across all `6` historical periods (`FY2021–FY2024`, `9M-2024`, `9M-2025`), all `3` `FY2025E` anchor scenarios (`165` rows), and all `15` forecast scenario-years (`846` rows): `0` errors (`hist_err: 0, anc_err: 0, fc_err: 0`).
4. **Conditional policy & PwC Q2 2026 benchmark review:**
   - Confirmed `review-resolutions/umb.md` conditional marker is present and `README.md` explicitly discloses the `FY2025` / `2026` primary-filing gaps, the MoF July 2026 recapitalisation confirmation (`amount/instrument unknown`), and the static FY26 recapitalisation overlay (`base` 13% min `448.813m`, `downside` `641.645m`, `upside` `304.083m`).
   - Reviewed `assistance/chatgpt-support/umb-model-applicability-review-20261125.md` and `assistance/codex/umb-interim-source-recovery/pwc-q2-secondary-crosscheck.md`: PwC Q2 2026 secondary figures (`assets 16,684.0m`, `deposits 11,537.5m`, `H1 PBT 195.1m`, `CAR 13.0%`) exceed the September 2025-anchored `FY2026E` counterfactual (`base assets 13,493.803m`, `deposits 9,900.307m`). Accordingly, **UMB must remain excluded from all ordinary accepted totals** and be labelled in conditional peer/sector outputs and `sector/summary.md` as a **September 2025-anchored counterfactual (pre-July 2026 recapitalisation), not a current post-recapitalisation outlook**, alongside the PwC Q2 2026 benchmark caveat.

### Remaining limitations
- `FY2025` full-year and `2026` primary statements remain unavailable; `FY2025E` is an estimated anchor kept separate from reported history (`anchor-estimates.csv`).
- Gross loans, allowance, NPL migration, eligible reserve split, and post-recapitalisation RWA/CAR remain unavailable; proxy CAR (`5.911%` base `FY2030E`) is not actual regulatory compliance.
- If primary `FY2025` or `2026` filings become available, conditional status lapses and a fresh full review is required.
