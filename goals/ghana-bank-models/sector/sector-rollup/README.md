# Ghana banking sector roll-up — accepted-only checkpoint
Original author: claude; authorized steward: chatgpt-support. Independent review required; this is not the final sector report.

## Run and replay
Requires Node.js (same runtime as the room supervisor) and Git. On Windows use an isolated LF checkout (core.autocrlf=false before checkout), not a CRLF-normalized working tree. The Python wrapper preserves the original command.
- From a clean checkout: `node goals/ghana-bank-models/sector/sector-rollup/rollup.mjs --output-dir /path/outside/repo`
- Exact historical replay: use the generator from this revision and pass `--input-root /path/to/clean/checkout-of-manifest-sourceCommit --output-dir /path/outside/repo`.
- Verify existing output: append `--check` with the same output directory. A changed accepted evidence set, excluded status/diagnostic input, context or generator invalidates it. Board-only changes that leave these inputs unchanged do not invalidate it. Output hashes and deterministic content are also checked.
- Independent Decimal verification: `python -I verify_snapshot.py /path/to/input-checkout /path/to/output`.
- Legacy invocation `python rollup.py` delegates to Node and accepts the same options. Default output is next to the generator; use an external output directory to avoid dirtying the input checkout. Committed results are a pinned snapshot, not a live dashboard.

## Definitions and evidence
Only the exact current supervisor acceptance set is included in rollup.md and rollup.csv. Claim status alone cannot admit a bank. manifest.json contains source commit, generation time, accepted package and macro fingerprints, review file/hash/reviewer, excluded model stages and diagnostics hashes, sector context and generator hashes, output hashes. Each CSV cell has reporting banks and coverage count. Historical totals include only reported/derived rows. No unavailable or estimated historical row is imputed; zero remains zero. Scenario totals are partial estimates, not guaranteed or probability weighted. Paired ratios require numerator and positive denominator from the same bank; combined ratios use the matched sample. Income is normalized before impairment using complete components. Net loans are not compared with gross sector advances. September 2026 compares with BoG September figures (513.6bn assets, 372.9bn deposits); FY25 denominators 446.9bn and 325.3bn. Bank-only vs sector scope may differ. Closing-equity ROE is not average-equity ROE.

provisional.csv contains isolated bank-level historical observations and scenario estimates from excluded work. It is not an aggregate, does not constitute acceptance, and never enters the accepted totals. Unavailable values are blank; malformed provisional tables are recorded in manifest diagnosticErrors rather than blocking accepted roll-up. Models lacking history/interim data remain excluded until the required review and gate pass or the lead/human explicitly defines a separate provisional policy.

## Validation
Tested on clean isolated LF input, replay via Node, independent Python Decimal recomputation of every reported aggregate, bank metric and paired ratio; tested rejection of modified output and dirty input. See the claim and board for exact tested snapshot and counts. Source bank packages and existing independent reviews were not edited. Final refresh after remaining bank closures.
