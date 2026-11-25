# Tasks: ghana-bank-models (lead edits only)

Work here is **self-organised**. Nobody is assigned a bank. Agents take pieces by creating claim files in `claims/` (see GOAL.md). To see who has what, run `node scripts/claims.mjs`, or read `STATUS-BANKS.md`, or just list `claims/`.

| ID | Piece | How it is owned |
| --- | --- | --- |
| B-* | One model per bank on the roster (`ROSTER.md`) | `claims/<bank-slug>.md` |
| S-1 | roster-verification | `claims/roster-verification.md` |
| S-2 | macro-assumptions | `claims/macro-assumptions.md` |
| S-3 | sector-rollup | `claims/sector-rollup.md` (after banks are finished) |
| S-4 | peer-comparison | `claims/peer-comparison.md` |
| S-5 | qa-sweep | `claims/qa-sweep.md` |

Reviews: each finished bank is reviewed by a different agent (`reviews/`). The lead (claude) breaks ties and merges the final summary.
