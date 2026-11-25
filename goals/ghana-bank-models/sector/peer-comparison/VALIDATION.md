# Independent peer-comparison verification

Run `python goals/ghana-bank-models/sector/peer-comparison/test_verify_snapshot.py` for the self-contained regression fixture. Requires Python 3 and Git. No external packages.

Run `python goals/ghana-bank-models/sector/peer-comparison/verify_snapshot.py --help` for the production verification interface. Verify against the same clean, pinned source checkout used to produce both rollup and peer outputs. Keep generated outputs outside the pinned checkout so the original source stays clean.

The independent Python verifier recomputes membership and amounts from the source packages using Decimal. It checks reported/derived historical cells, forecast proxies, ROE caveats, separate conditional records, package and review digests, scope marker hashes, macro fingerprint, and agreement of the FY2025 accepted-only totals with the rollup manifest and CSV. It does not grant acceptance or replace a review of financial methodology.

## Test evidence

2026-11-25 19:10 UTC: exact verifier Git blob 42fd94f35f9238f841fd057dd8a1bdd59e4fce98 compiled and executed locally with Python and Git. Synthetic fixture checked 79 peer cells; valid case passed, all eleven corruptions rejected. Cases include false numeric ROE, omitted ROE caution, wrong reviewer, conditional contamination, wrong commit, unavailable historical data populated with an estimate, wrong scope digest, missing conditional row, stale review digest, wrong manifest total, and changed rollup CSV. Production replay remains a separate step and must be independently checked.
