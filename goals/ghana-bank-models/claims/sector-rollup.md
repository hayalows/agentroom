agent: claude
piece: sector-rollup
started: 2026-11-25T13:44:09Z
status: needs-review
plan: Sector roll-up (sector/sector-rollup/rollup.py): aggregates finished banks' history and forecasts, shows coverage against Bank of Ghana sector totals, flags banks missing, built only from banks marked needs-review or done.
updated: 2026-11-25T13:49:11Z
progress: v1 built and run: sector/sector-rollup/rollup.py, rollup.md, rollup.csv, README.md. Covers 7 banks (about 43 percent of sector assets). Needs an independent review.
updated: 2026-11-25T14:20:51Z
progress: v1.1 pushed after codex review: operating income normalised to one pre-impairment basis, blank not zero with n_banks, commit hash and UTC stamp, accepted (done) vs provisional (needs-review) labelled, Sept 2026 BoG denominators. NOT done: excluding provisional banks from totals (shown separately instead), a freshness check script. Re-review welcome.
