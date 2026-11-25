# Sector risk diagnostic (Codex, 25 November 2026)

**Snapshot only.** Source pin `67ff7c9a32bc6ab7f49b9904ccbc0ce0fccb5d6e`, clean-LF desktop supervisor confirmed 18 ordinary accepted at 19:14:40Z. Absa and ADB were pending ordinary, OmniBSIC, Prudential, UMB separately conditional. The roster subsequently changed (Absa accepted, Ecobank reopened); do not use this as final official roll-up. This is an interpretive supplement to Support's roll-up and not another acceptance register.

## Quantified downside

All 23 forecast packages: 19,493 rows, 345 scenario-years. For 18 then-accepted banks only (GHS m):

| Year | Base PAT | Downside PAT | Upside PAT | Base minus downside |
|---|---:|---:|---:|---:|
| 2026 | 11,264.790 | 8,723.676 | 11,924.938 | 2,541.114 |
| 2027 | 12,959.076 | 9,842.615 | 14,510.376 | 3,116.461 |
| 2028 | 14,409.122 | 9,723.814 | 17,012.325 | 4,685.308 |
| 2029 | 15,784.651 | 7,974.451 | 20,411.415 | 7,810.200 |
| 2030 | 17,936.419 | 6,560.068 | 24,585.746 | 11,376.351 |

The FY30 scenario gap is 63.42% of base PAT. GCB (4,231.126m), Stanbic (1,088.036m), CBG (893.148m) together explain 54.61% of the net gap. This is contribution to model sensitivity, not measured risk exposure, and includes negative contributions from nonmonotonic bank paths. FY30 downside: six loss-making banks, three with modeled CAR proxies below 13% (CBG, NIB, Societe Generale). CBG modeled negative equity. The three banks comprise 8.71% of the cohort's modeled downside assets. These are not actual capital violations. Capital proxy methods vary by bank.

## Profit gap drivers

90 bank-year bridges, signed contributions to base-minus-downside PAT. Values GHS m, rounded to .001m.

| Driver | FY2030 | FY2026–30 cumulative (undiscounted) |
|---|---:|---:|
| Net interest income | 5,761.918 | 9,999.131 |
| Non-interest income | 3,896.484 | 10,059.040 |
| Credit impairment | 1,936.469 | 10,584.394 |
| Other costs | 4,920.492 | 11,867.506 |
| Taxes and levies offset | -5,139.012 | -12,980.637 |
| PAT gap | 11,376.351 | 29,529.434 |

Higher gross interest income in downside in FY27–28 (-5,560.731/-6,761.615m contribution) is more than offset by higher funding costs (+5,648.630/+7,259.084m). The component convention is documented in earnings-drivers.mjs. 13 bank-years (23 individual scenario-order inversions) across CalBank, GTBank, Standard Chartered, UBA and Zenith traced to positive interest-income sensitivity. Individual bridges reconcile within .002m. Higher macro rates can help net interest income at individual banks; do not impose a mechanical scenario profit ranking or describe every downside scenario as a uniform earnings decline. The macro paths are assumed, not predictive probabilities.

## Reproducibility and limits

`diagnostic.mjs`, extracts 1–3 and `diagnostic-results.json` contain all raw contributions, explicit classification and source pin. `earnings-drivers.mjs`, driver extracts 1–3, and `earnings-drivers-results.json` contain individual bridges and aggregates. `scenario-inversions.json` contains the component comparisons. Run the scripts on the pinned inputs, not current main. `verify.py` is a separate Decimal verifier; its laptop execution could not be confirmed because desktop transport failed. Do not claim an independent CLI PASS. Executed extraction and arithmetic using exact fetched GitHub rows; the 2030 aggregate totals were independently matched by Support (c38767ca) and Claude Helper 1 (19:20:42Z board). No aggregate combines conditional and ordinary banks. This diagnostic is not a valuation, forecast probability or regulatory solvency finding. Final roster refresh belongs to the designated roll-up steward.


### Fixed-point aggregate recheck (19:27:56Z)
Re-fetched all three immutable extraction files plus both result JSONs. Independently aggregated GHS-thousand integer values (BigInt) for counts, annual PAT, annual gaps, asset totals, downside capital cohorts, each bank's FY30 and cumulative delta, annual component bridges and five-year component totals. 101 comparisons: 98 exact, three net-interest vs gross interest/funding component differences of 0.002m (FY26), 0.009m (FY27), and 0.002m (FY30). These are within the propagated tolerance of independent .001m rounded statement lines across 18 banks and two scenarios (up to .054m); no balancing adjustment made. All net PAT driver bridges and cohort totals reconcile exactly at .001m. This is an aggregate read-back check, not the independent native Decimal source-file verifier.
