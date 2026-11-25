# Absa Bank Ghana PLC (owner: claude-helper-1)

Status: **needs-review (round 1)**. Bank-only. GHS millions unless a percent is shown.

## READ FIRST: where the history came from
I could not open Absa's PDFs (automated access is refused, and I did not bypass it). The 300 history rows are the **independent transcription by agent `codex`** (`assistance/remaining-banks/absa-primary-source-pack-codex.csv`, official annual face pages checked visually by codex, Q3 2026 by text extraction). `build_financials.py` copies them unchanged and re-runs every statement identity (0 failures, `checks_history.md`). I did not re-read any row from the issuer's page. A reviewer should spot-check against the PDFs listed in `sources.md`.

## Who it is
Absa Group Ltd owns 100% (FY2023 directors' report, per codex; not confirmed against the current register). Stated capital 400m.

## Size and shape
| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | 9M-2026 |
| --- | --- | --- | --- | --- | --- | --- |
| Total assets | 16,038 | 17,102 | 21,491 | 27,342 | 31,530 | 35,946 |
| Customer deposits | 7,944 | 11,177 | 15,883 | 17,631 | 19,186 | 21,185 |
| Net loans | 4,785 | 5,135 | 6,345 | 8,345 | 9,995 | 11,528 |
| Profit after tax | 692.5 | -429.2 | 1,136.7 | 1,194.7 | 1,762.4 | 985.3 (9M) |
| Total equity | 2,298 | 2,138 | 2,975 | 4,178 | 5,973 | 5,875 |
| CAR / NPL (reported) | n/a | n/a | n/a | n/a | n/a | 19.06% / 11.32% |

- **Big and loan-heavy relative to the others modelled.** Loans are 54% of deposits; funding includes 5.75bn of borrowings.
- **FY2022 loss** is the domestic debt exchange (impairment 2,126.9m). **FY2025 profit of 1,762m had almost no impairment (3.3m)**; 9M-2026 impairment is 198.4m, so FY2025 is not a run rate.
- **1,115m dividend** was paid in 9M-2026 (63% of FY2025 profit), which is why equity fell from 5,973m to 5,875m despite 985m of profit.

## Forecast, base case (estimates)
| | FY2026E | FY2027E | FY2030E |
| --- | --- | --- | --- |
| Net interest income | 2,543 | 3,039 | 4,025 |
| Profit after tax | 1,311 | 1,489 | 1,657 |
| ROE | 21.5% | 22.5% | 18.3% |
| CAR proxy | 19.9% | 20.2% | 19.4% |

FY2030E profit after tax: base 1,657, downside 1,361, upside 1,811. Ordering is mixed in FY2027E and FY2028E because the shared macro file gives the downside higher rates (checks.md section 3). FY2026E is the same in all scenarios (nine months reported).

## Method and limits
- Same method as the accepted UBA model: FY2026E = 9M x 12/9 plus an implied Q4; from FY2027E loans earn the 364-day bill + 6 points, an earning pool (securities plus 3.6bn trading assets) earns a bill/bond blend plus a **fitted haircut of +2.58 points**, and funding cost is a solved ratio to the policy rate. **Both fitted constants match 9M-2026 by construction.** The positive haircut most likely means loans earn more than bill + 6 points; the statements cannot separate the two.
- Sensitivities (checks.md 2b, 2d): 1 point on the haircut moves FY2030E base profit by about 115m (7%). Section 2b changes FY2027E onward only; section 2d stresses the implied Q4 alone with the nine reported months frozen (yield, cost of risk, funding, a 16.1m penalty with no tax benefit).
- **The CAR figure is a weak proxy**: the reported 19.06% scaled by equity / total assets, because the pack has no annual CAR, RWA or regulatory capital. Regulatory CAR, NPL, gross loans and allowance are `unavailable` in the forecast.
- **Round-2 repairs (after two independent CHANGES reviews):** reserve-cash proxy and stresses (checks.md 2e), capital stress with shortfall rows, net LDR moved to `x_net_ldr_pct`, statutory reserve and credit-risk reserve balances plus a full-year and Q4 transfer memo (full-year requirement less the 123.2m already transferred), Q4-only sensitivities, no tax credit on a Q4 loss, a non-negative dividend target, corrected titles and wording.
- **Reserve-cash caveat:** the cash line is (CRR + a solved share) of deposits, so the calibrated reserve gap is zero by construction. Under the 20% eligibility stress the model would withhold every dividend (checks.md 2e). These are proxies, not regulatory calculations, and the issuer reports no liquidity breach.
- Statutory reserve uses the Act 930 s34 tiers (Absa is in the 12.5% tier, observed 123.2m on 985.3m profit).
- Not modelled: a Q3 2026 sanction of 0.36m and a 16.1m post-balance-sheet penalty (pack note).

## Files
`sources.md`, `financials.csv` (300 rows), `forecast.csv` (837 rows), `assumptions.json`, `build_financials.py`, `model.py`, `checks_history.md`, `checks.md`. A separate non-owner draft by papa-kojo-agent sits in `assistance/remaining-banks/absa-model-draft-papa-kojo-agent`; I did not copy it.
