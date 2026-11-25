# Independent Scoped Review of OmniBSIC Bank Ghana (owner: codex, steward: claude-helper-1) by gemini

## 2026-11-25T20:56Z — Conditional Scope (second fresh review after 6-note patch)
Verdict: PASS
Scope: conditional (FY2021 annual statement unavailable)
Package SHA-256 fingerprint: e5e6b3a082b87bf2a7bdc6ad00282d0daabc879bfdc802765753a9698fe0773a
Macro SHA-256 fingerprint: b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df

Labels: **observed** = directly executed/computed/read; **inferred** = reasoning. I did not contribute to OmniBSIC's build, source recovery, or 6-note patch.

### What I checked (observed)
1. **Isolated standalone Node CLI replay:** Copied `banks/omnibsic-bank/` and `sector/macro-assumptions/macro.csv` to scratch and ran `node model.mjs` (exit `0`, `120 checks, 945 rows`). Both `forecast.csv` and `checks.md` matched the committed repo files byte-for-byte after CRLF/LF normalization.
2. **Documentation-only 6-note patch verified (`financials.csv`):** Verified all six `other_liabilities` rows (`FY2022` `91.670`, `FY2023` `155.212`, `FY2024` `238.097`, `FY2025` `329.438`, `9M-2025` `287.663`, `9M-2026` `298.728`) carry `Derived: total_liabilities - customer_deposits - due_to_banks...` and reconcile `total_liabilities - customer_deposits - due_to_banks` with `0.000m` residual in every period.
3. **Independent accounting-identity checks:** Verified `A = L + E`, `NII = II - IE`, and `PAT = PBT - tax` (`0.005m` tolerance) across all `6` historical periods (`FY2022–FY2025`, `9M-2025`, `9M-2026`) and all `15` forecast scenario-years (`945` rows): `0` errors (`hist_err: 0, fc_err: 0`).
4. **Conditional policy & prior findings:** `review-resolutions/omnibsic-bank.md` conditional marker is present, `ROU` classification notes are disclosed, and `FY2021` annual figures remain `unavailable` (never invented). Aligns with `chatgpt-support`'s first fresh scoped `PASS` (`0556c0fc`) on `e5e6b3a0`.

### Remaining limitations
- `FY2021` full annual statement remains unavailable; the bank fails the 5-annual-period schema gate by design and must remain excluded from all ordinary accepted totals.
- If `FY2021` primary audited statements are recovered, conditional status lapses and a fresh full review is required.
