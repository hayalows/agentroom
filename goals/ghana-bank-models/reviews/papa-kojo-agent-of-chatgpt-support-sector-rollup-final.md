# Independent final sector roll-up and peer comparison review

Reviewer: papa-kojo-agent (GPT-6.2)
Verdict: PASS — final sector roll-up and peer comparison, scoped to numerical reconciliation, membership and published output integrity.
Reviewed: 2026-11-25T21:10:08.717Z
Source commit: `b728a09ffd52393f98b97c14298544c139d1921f`
Published output commit: `11dffc9111b208dc896e2db05f0e65c18aa09179`
Input fingerprint: `b59a8526d5026b87a05f4a92784148fd1c8f801d2f5f637548dc2454e9f760e3`
Manifest macro fingerprint: `b3c4412d681469e8d974e0c067af8e28435f5669900a9f1b4c54b0178992b8df`

## Independent execution
I wrote a separate Python Decimal verifier, ran it on ICONKA, and read source and published bytes using git show at the exact commits above. No rollup/compare generator or owner's verifier was imported or executed. No shared worktree or bank package was edited. Process 28976 completed exit 0 in 11.51s. It read financials.csv and forecast.csv for all 23 banks, rejected duplicate keys, selected only reported/derived nonblank finite historical values and estimated nonblank finite forecasts, and recomputed aggregate values, reporting counts and membership, paired ratios, coverage, bank-level metrics, peer ROA/ROE/LDR and scenario cells. It checked exact pin, input fingerprint, output hashes and peer metadata against the manifest. Conditional banks were kept outside all ordinary sets.

| Check | Cells | Mismatches | Largest absolute numeric residual |
|---|---:|---:|---:|
| Ordinary roll-up | 258 | 0 | 0.000499 |
| Separate conditional diagnostics | 72 | 0 | 0 |
| Ordinary peer comparison (including metadata/status) | 440 | 0 | 0.000447 |
| Conditional peer comparison (including metadata/status) | 48 | 0 | 0 |
| Total | 818 | 0 | |

Tolerance: 0.000500001 million or 0.000050001 percentage points per formatted numeric cell. Every roll-up reporting membership and denominator count checked separately. Blank unavailable and non-comparable ratios preserved. Three manifest FY2025 totals reconciled to raw Decimal sums within 0.000001 million. 20 ordinary, 3 separate conditional: omnibsic-bank, prudential-bank, umb. UMB FY25 history remains blank and the diagnostic classification explicitly retains the September 2025-anchored counterfactual and PwC secondary caveat.

## Published byte integrity
- rollup.md SHA256: e79dcc600527c54c18ed9634f4cf4c2a577293b0ac4b8492289cb11aa590980b
- rollup.csv SHA256: 3c76380fac896e915121958c1665f0b0b5259846582a67cdf0594db539dda852
- provisional.csv SHA256: 1d6a979f5d38eb5b5adf38691149a812b4b98aebb6be4ed9cefe0aa9ec305477
- comparison.csv SHA256: ebc0966eaa6b5ba469c1b8660738d8a8c79d8d55aa910a6d3565277340dd9219
- conditional-comparison.csv SHA256: 12b5ab6d0e07d8b33fb87904b2843a1307ea9c56badaa7702b9704933413d242

All three roll-up hashes match manifest; both peer hashes match Support's publication announcement.

## Reconciled figures (GH¢m)
FY2025 assets 403776.743272; deposits 293234.914712; net loans 88845.932684; equity 56579.513135; PAT 14033.737959.
FY2030E PAT base 19285.178; downside 7237.121; upside 26476.585. No conditional estimates included.

## Scope limits
This is a fresh independent final output PASS, not a fresh review of issuer filings, individual model assumptions or regulatory compliance, not a new bank acceptance, and not an independent QA-sweep run. Bank-level eligibility decisions and package/macro fingerprints are taken from the published manifest and lead closures; peer metadata is checked against that manifest, not a fresh full package-fingerprint rebuild. The underlying source gaps remain, and the models are estimates. No findings requiring changes within the reviewed numerical/publication scope. Claude retains peer lead review, summary and human sign-off responsibility.

ACK Claude 21:01:51 all-hands. TO Claude / ChatGPT Support: my distinct PASS is recorded against the final exact pin and publication, alongside Helper's PASS. Please proceed to lead review and final summary under the existing closure rules.
