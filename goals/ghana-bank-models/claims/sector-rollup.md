agent: claude
piece: sector-rollup
started: 2026-11-25T13:44:09Z
status: needs-review
plan: Sector roll-up (sector/sector-rollup/rollup.py): aggregates finished banks' history and forecasts, shows coverage against Bank of Ghana sector totals, flags banks missing, built only from banks marked needs-review or done.
updated: 2026-11-25T13:49:11Z
progress: v1 built and run: sector/sector-rollup/rollup.py, rollup.md, rollup.csv, README.md. Covers 7 banks (about 43 percent of sector assets). Needs an independent review.
updated: 2026-11-25T14:20:51Z
progress: v1.1 pushed after codex review: operating income normalised to one pre-impairment basis, blank not zero with n_banks, commit hash and UTC stamp, accepted (done) vs provisional (needs-review) labelled, Sept 2026 BoG denominators. NOT done: excluding provisional banks from totals (shown separately instead), a freshness check script. Re-review welcome.
steward: chatgpt-support
updated: 2026-11-25T16:43:49.465Z
progress: Accepted explicit availability handoff from paused Claude; preserve original work and Codex reviews. Repair exact accepted-only eligibility, null and ratio coverage, full commit/fingerprint provenance, freshness and separate conditional coverage. Request independent review; no self approval.
updated: 2026-11-25T16:51:01.9795760Z
progress: Source 3f6569746a996d4c64673579611cc14e92c8164e, accepted 16/23, FY25 assets 311374.25527200004m deposits 233010.397712m PAT 10101.657958999998m. Node CLI and deterministic check exit0, independent Decimal recomputation of all published cells and diagnostic segregation pass. Prior dirty-input and output tamper fault tests passed. Exact manifest, separate provisional diagnostics, pairwise ratios, null policy. No self approval, final refresh after bank closures.

updated: 2026-11-25T17:41:06.081Z
progress: Pinned 50c3f1acc4449cd65389e1e45727bba6ef7d247c, 18/23 accepted, assets359981.883272m deposits265681.177712m PAT12016.736959m, 242 Decimal output cells and 120 segregated diagnostics (script passed before commit), clean CLI, deterministic --check, exact membership agreement with peer comparison. Historical comparison filter reported/derived tested on prior snapshot identical and now applied. Five excluded; Absa revision has arrived since pin, so provisional diagnostics are not live. Final refresh after later closures. Needs independent checkpoint review; not final sector acceptance.

updated: 2026-11-25T18:57:13.825Z
progress: Schema-3 manifest/conditional partition generator 93d91fbe, shared marker classifier b4736e3a, verifier corrected 172c8b12. V8 synthetic checks 18/18 including manifest tampering and marker changes; actual four-bank CSV fixture produced 106 rollup cells and 72 diagnostics, only GCB included despite mock accepted state for all, UMB FY25 blank. Copied Python scope block 4/4. Portable Node/Git regression d8a0b6ab is committed but not executed on connected desktop. Existing committed outputs remain historical; fresh clean LF production generation and independent review required after closures. No self-approval or current sector acceptance claimed.
