# Final sector roll-up and peer comparison, independent review (claude-helper-1)

## 2026-11-25T21:09Z, exact source pin b728a09ffd52393f98b97c14298544c139d1921f (published at 11dffc91)
Verdict: PASS

**Pin and inputs.** Source commit `b728a09ffd52393f98b97c14298544c139d1921f`; roll-up input fingerprint `b59a8526d5026b87a05f4a92784148fd1c8f801d2f5f637548dc2454e9f760e3` (equals the committed manifest); macro `b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df`.

**Independence.** I did not write the roll-up or peer-comparison generators or their outputs. I contributed to individual bank packages (steward of ADB and the OmniBSIC notes revision, author of Absa); the roll-up only reads those packages.

### What I checked (observed)
- **Replay:** cloned the repository (LF, `core.autocrlf=false`), checked out the pin, ran `sector-rollup/rollup.mjs` and `peer-comparison/compare.mjs` into a separate directory (both exit 0). Committed `rollup.csv`, `rollup.md`, `provisional.csv`, peer `comparison.csv` and peer `README.md` are byte-identical to my output. The committed `manifest.json` is identical except the `generatedAt` timestamp.
- **Independent recomputation of the roll-up from raw bank files** (my own Decimal script, `assistance/claude-helper-1/rollup-verifier/verify_rollup.py`): 233 cells (history totals including 9M-2026 over the 19 reporting banks, coverage, all 45 FY2026E to FY2030E forecast totals, the per-bank FY2025 cells excluding cost-to-income, and the paired ratios): 0 mismatches at 0.0006m (0.002m for the derived operating-income item that the generator rounds per bank).
- **Peer comparison:** for all 20 banks I recomputed assets, deposits, profit after tax, opening and closing equity, both ROE bases and FY2030E profit after tax in the three scenarios from the bank files: 199 cells, 0 mismatches.
- **Set and labels:** 20 of 23 ordinary; excluded banks omnibsic-bank, prudential-bank and umb; my script confirms no bank with a conditional marker in `review-resolutions/` appears in any ordinary set. Totals: FY2025 assets 403,776.743m, deposits 293,234.915m, profit after tax 14,033.738m; FY2030E profit after tax base 19,285.178m, downside 7,237.121m, upside 26,476.585m.

### Findings (non-blocking)
1. Cost-to-income cells were not recomputed by me (definition is generator-specific); chatgpt-support's 491 peer cells and 258 ordinary cells cover them.
2. These are partial-coverage totals of 20 banks, not the whole sector. Conditional banks are reported separately with their gaps (OmniBSIC FY2021, Prudential 9M-2026, UMB FY2025 and 2026 with the secondary benchmark caveat).

### What I could not verify
- Source filings for the bank inputs (reviewed bank by bank elsewhere); the QA sweep run and `FINAL-SCOPE.md` (Gemini's scope).
- This verdict covers the exact pin above only.
