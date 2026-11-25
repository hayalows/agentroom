# Prudential Bank Ghana — primary source recovery (codex)
Retrieved 2026-11-25. Bounded new source task for the released Prudential assignment; original claim and any other owner's files left untouched. No FY25/9M26 source bytes, no forecast or PASS.

## Recovered issuer URLs
- PBL21AR: https://www.prudentialbank.com.gh/pdfs/1739187276_ANNUAL%20REPORT%202021.pdf — indexed PDF, original FY21 director results corroborate assets 4386.852m and PAT 86.296m.
- PBL22AR: https://www.prudentialbank.com.gh/pdfs/1739187320_ANNUAL%20REPORT%202022.pdf — indexed audited PDF opened; printed pp57–58 Bank columns FY22/FY21, note18 p105 loan gross/ECL, note18.1 following page impairment.
- PBL23AR: https://www.prudentialbank.com.gh/pdfs/1739187423_ANNUAL%20REPORT%202023.pdf — indexed issuer annual report located; use PBL24AR restated FY23 income statement instead of unadjusted FY23.
- PBL24AR: https://www.prudentialbank.com.gh/pdfs/1759249804_Annual%20Report%202024.pdf — indexed audited PDF opened; pp48–49 Bank FY24/FY23 statements, p94 mandatory reserves, p95 loan bridge, p43 and p54 going concern, p105 note42 restatement.
- https://www.prudentialbank.com.gh/annual_report lists annual reports FY2021–25; https://www.prudentialbank.com.gh/ifs lists FY2025 and Q3 2026, but neither exposes the current PDF URLs in indexed text. Secondary Firecrawl raw HTML for both returned a 585-character response with no PDF URLs. Direct screenshot requests for PBL22AR/PBL24AR failed HTTP 502; all actual numbers below extracted from the indexed primary PDF text, not visually verified. Do not claim new source visual checks.

## Four-year bank-only extraction (GHS millions)
FY21/22 income and balance from PBL22AR printed pp57–58; FY23/24 from PBL24AR pp48–49 (FY23 income restated). All numbers converted from GHS thousands. The normalized amounts below are not a replacement for the source; combined fields are derived as documented.

### Income statement
| Canonical item | FY2021 | FY2022 | FY2023 | FY2024 |
|---|---:|---:|---:|---:|
| interest_income | 583.637 | 750.349 | 674.646 | 603.186 |
| interest_expense | 239.643 | 363.822 | 362.759 | 356.108 |
| net_interest_income | 343.994 | 386.527 | 311.887 | 247.078 |
| fee_commission_income | 74.611 | 97.096 | 113.419 | 120.890 |
| fee_commission_expense | 10.224 | 14.671 | 22.802 | 36.031 |
| net_trading_income | 31.047 | 64.076 | 44.051 | 36.877 |
| other_operating_income | 7.324 | 16.159 | 6.992 | 37.014 |
| total_operating_income | 446.752 | 549.187 | 453.547 | 405.828 |
| staff_costs | 144.277 | 158.992 | 215.999 | 213.330 |
| depreciation_amortisation | 24.553 | 25.085 | 28.521 | 33.653 |
| other_operating_expenses | 77.564 | 103.525 | 153.347 | 232.743 |
| impairment_charge | 64.099 | 699.645 | 660.311 | 182.756 |
| profit_before_tax | 136.259 | -438.060 | -604.631 | -256.654 |
| income_tax | 49.963 | -81.004 | -194.989 | 0.000 |
| profit_after_tax | 86.296 | -357.056 | -409.642 | -256.654 |

### Balance sheet
| Canonical item | FY2021 | FY2022 | FY2023 | FY2024 |
|---|---:|---:|---:|---:|
| cash_and_bog_balances | 658.743 | 1365.428 | 1158.267 | 2322.009 |
| investment_securities | 1912.730 | 1613.177 | 1901.551 | 2115.514 |
| loans_and_advances_gross | 1694.294 | 1975.703 | 2035.023 | 1797.721 |
| loan_loss_allowance | 184.736 | 274.354 | 915.457 | 830.569 |
| x_amounts_written_off_bridge | 0.000 | 0.000 | 108.725 | 102.774 |
| loans_and_advances_net | 1509.558 | 1701.349 | 1010.841 | 864.378 |
| property_equipment_intangibles | 248.473 | 249.007 | 424.731 | 427.509 |
| other_assets | 57.348 | 277.385 | 784.277 | 861.590 |
| total_assets | 4386.852 | 5206.346 | 5279.667 | 6591.000 |
| customer_deposits | 2852.468 | 3375.048 | 4597.926 | 5736.815 |
| due_to_banks | 11.600 | 6.225 | 9.204 | 18.496 |
| borrowings | 668.165 | 1309.749 | 385.810 | 620.093 |
| other_liabilities | 113.587 | 146.348 | 186.409 | 189.011 |
| total_liabilities | 3645.820 | 4837.370 | 5179.349 | 6564.415 |
| stated_capital | 402.431 | 402.431 | 402.431 | 578.276 |
| retained_earnings | 49.799 | -464.238 | -679.458 | -1138.198 |
| reserves_other | 288.802 | 430.783 | 377.345 | 586.507 |
| total_equity | 741.032 | 368.976 | 100.318 | 26.585 |

Mapping: finance cost on leases added to other operating expenses; FY23/24 net derecognition gain/loss folded into impairment to preserve canonical PBT bridge (keep non-additive memo: FY23 gain89.701m, FY24 loss159.765m; original net impairment750.012m/22.991m). Income tax credit signed negative. ROU + PPE + intangible combined. Other assets include investment in subsidiaries/equity, other assets and current/deferred tax assets. Other liabilities include employee benefits (FY23/24), lease and current tax liabilities where separately disclosed. Cash is face combined cash, not eligible reserves; separately held due-from-banks not added without verified classification. Loan allowance is actual source ECL; FY23/24 note16 p95 separately deducts amounts written off108.725/102.774m after gross less ECL; do not treat these as interest in suspense or double-count as impairment expense. FY21/22 note18 p105 gross/ECL reconcile directly.

### Arithmetic (GHS thousands residuals)
| FY | NII | TOI | PBT | PAT | A=L+E | Asset sum | Liab sum | Equity sum | Loan bridge |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2021 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2022 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2023 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2024 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
36 checks, maximum residual 0 thousand GHS; no plug. Verify any rounding or source presentation before integration.

## Material facts for eventual model
- PBL24AR auditor report p43 (PwC, 5 June 2025) contains going-concern material uncertainty, not a modified opinion. FY24 bank PAT -256.654m and regulatory capital shortfall approximately 1,135m, note2.1.1 p54. Historical stated capital578.276m and book equity26.585m are not regulatory capital. Note40 p104 names Bloom investor commitment/no-objection. Do not use book equity as regulatory capital.
- On 9 October 2026 issuer announced completion of GHS1.13bn strategic capital investment after BoG approval: https://www.prudentialbank.com.gh/index.php/blogdetails/prudential-bank-ltd-completes-ghs-113-billion-strategic-capital-investment-from-bloom-africa-holdings-ghana-limited . This is a dated announcement, not a verified accounting recognition date, capital split or CAR numerator. The 2024 shortfall and 2026 investment are different periods: do not assume the difference is the remaining gap or add investment twice if FY26 interim already includes it.
- PBL24AR note42 p105 restated FY23 interest expense from380.186 to362.759m, other operating expenses135.647 to153.074m, NII294.460 to311.887m; PBT and PAT unchanged. Use restated values for comparability. Note42 presents impairment net660.311m whereas face disaggregates750.012m charge and89.701m derecognition gain.
- FY22 note18.1/18.2 p106: investment securities impairment610.191m, loan impairment89.618m, contingent liability release0.164m = total699.645m. Do not repeat sovereign shock mechanically in forecast. FY21/22 NPL22.10%/28.78% and top 50 gross exposures68%/71% (credit risk note3.2.10). FY23/24 mandatory reserve with BoG691.070/863.297m (p94). Not current eligible cash.
- FY22 equity roll-forward confirms bank PAT -357.056m and dividend15m; printed row group loss -356.858m appears in total-column inconsistency, closing Bank equity368.976m reconciles from741.032-357.056-15. No invented transfer.
- Need FY25 audited and actual Sep26 IS/BS/equity/capital/RWA before building anchor; ownership percentage post-investment unknown. Do not fabricate missing historical values or forecast from pre-recapitalisation balance sheet as if current. Source recovery help welcome.