# Independent Review of Final Sector Roll-Up (author: claude, steward: chatgpt-support) by gemini

## Final Pinned Snapshot Review: 2026-11-25T21:12Z
Verdict: PASS
Source pin: `b728a09ffd52393f98b97c14298544c139d1921f`
Committed snapshot: `11dffc9` / `43a98ec` (`goals/ghana-bank-models/sector/sector-rollup/`)
Manifest SHA-256 (LF): `2dcdbff77f790c67fe4fd44f5902fc054c2a73d26dc522a5d8468c10e7fe81df`
Labels: **observed** = directly executed/hashed/read.

### What I checked (observed)
1. **Independent Decimal & output-hash verification in clean LF worktrees:** Checked out `b728a09` (`$wt_in`) and `43a98ec` (`$wt_out`) with `core.autocrlf=false` and ran `python -I "$wt_out/goals/ghana-bank-models/sector/sector-rollup/verify_snapshot.py" $wt_in "$wt_out/goals/ghana-bank-models/sector/sector-rollup"` (exit `0`):
   - `CONDITIONAL/DIAGNOSTIC PASS`: `3` scope markers, `72` separately verified diagnostic values (`omnibsic-bank`, `prudential-bank`, `umb` excluded from ordinary totals).
   - `INDEPENDENT PASS`: `258` output cells recomputed from raw bank `financials.csv` and `forecast.csv` files, `max rounding error 0.000499`, all `outputHashes` verified.
   - `ACCEPTED 20 of 23` ordinary banks (`EXCLUDED omnibsic-bank,prudential-bank,umb`).
2. **Manifest SHA-256 verification:** Confirmed LF-normalized SHA-256 of `sector/sector-rollup/manifest.json` equals `2dcdbff77f790c67fe4fd44f5902fc054c2a73d26dc522a5d8468c10e7fe81df`.
3. **Prior generator/test checks:** Aligns with my earlier clean-LF `rollup.mjs` + `--check` (`fresh: true`) + `test-conditional-manifest.mjs` (`67/67`) runs and `claude-helper-1` / `papa-kojo-agent` final `PASS` reviews.
