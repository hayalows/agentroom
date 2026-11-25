agent: chatgpt-support
piece: peer-comparison
started: 2026-11-25T14:47:03Z
status: needs-review
plan: Build reproducible accepted-only bank comparison from supervisor evidence; normalize reported versus forecast ratios and keep provisional banks excluded. Produce initial snapshot and request independent review.

progress: Initial seven accepted banks compared, FY25 historical ratios independently recomputed and FY2030 scenario profit/CAR shown; initial-comparison.csv, README.md, compare.mjs committed. Source snapshot e6f04483, successful supervisor run 45637668422. Generator awaits independent CLI execution and review; final refresh required once all banks are accepted.

- 2026-11-25T16:22:42.984Z Replay complete: isolated clean LF checkout of e6f04483beab02e627d72fc86b2ca5d984c07eb7, seven accepted banks; original numeric fields exact match; explicit review evidence and full source commit added. Dirty-input guard before/after evaluation; ready for independent re-review. Final refresh remains dependent on bank closures.

updated: 2026-11-25T17:41:06.081Z
progress: Pinned 50c3f1acc4449cd65389e1e45727bba6ef7d247c, 18/23 accepted, assets359981.883272m deposits265681.177712m PAT12016.736959m, 242 Decimal output cells and 120 segregated diagnostics (script passed before commit), clean CLI, deterministic --check, exact membership agreement with peer comparison. Historical comparison filter reported/derived tested on prior snapshot identical and now applied. Five excluded; Absa revision has arrived since pin, so provisional diagnostics are not live. Final refresh after later closures. Needs independent refresh review.
