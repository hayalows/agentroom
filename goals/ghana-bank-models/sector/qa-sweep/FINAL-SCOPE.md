# Final QA scope and publication evidence

Source commit: `b728a09ffd52393f98b97c14298544c139d1921f`

Roll-up input fingerprint: `b59a8526d5026b87a05f4a92784148fd1c8f801d2f5f637548dc2454e9f760e3`

All three reporting tools were run in one separate clean LF checkout on ICONKA with Node v24.16.0 and Python 3.14.6. Roll-up freshness passed; Decimal verification passed 258 ordinary cells and 72 separate diagnostics (max rounding 0.000499m). Peer verification passed 491 cells. These are steward execution results, not the required independent final agent reviews.

## Raw QA results and approved scope

- 20 ordinary accepted banks: 0 FAIL and 0 WARN.
- OmniBSIC: one raw FAIL, four annual periods (FY2021 unavailable).
- UMB: one raw FAIL, four annual periods (FY2025 unavailable), and one warning, 2026 interim unavailable.
- Prudential: one warning, 9M-2026 unavailable.
- The raw 2 FAIL and 2 WARN are retained. They correspond to documented scoped source gaps, not unresolved numerical defects. See [lead conditional closures](../../review-resolutions/CONDITIONAL-CLOSURES.md), including OmniBSIC's e5e6b3a0 rebind. Legacy gate and claim statuses do not override those closures.

All three conditional banks are excluded from ordinary totals. UMB is a September 2025-anchored counterfactual, not a current post-July 2026 recapitalisation outlook. PwC Q2 2026 secondary benchmarks (not primary history): assets GHS 16,684m, deposits GHS 11,537.5m, H1 PBT GHS 195.1m, CAR 13.0%. See [source cross-check](../../assistance/codex/umb-interim-source-recovery/pwc-q2-secondary-crosscheck.md) and the conditional scope rows in both reports.

The nine generated files are copied unedited from the external output directories. No bank package or generator was edited. Independent final reviews and human sign-off remain pending. QA checks structure, arithmetic and conventions, not original filings or regulatory compliance.
