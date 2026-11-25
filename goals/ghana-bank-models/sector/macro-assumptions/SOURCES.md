# Sources for macro-assumptions (all retrieved 2026-11-25 UTC by claude)

| source_id | Title | Publisher | URL | Period covered | How read |
| --- | --- | --- | --- | --- | --- |
| S-BOG-SUM-NOV26 | Summary of Economic and Financial Data, release 17 Nov 2026 | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2026/11/Summary-of-Economic-and-Financial-Data-November-2026-1.pdf | monthly Oct 2025 to Oct 2026 | Full PDF read (16 pages) |
| S-BOG-SUM-JAN26 | Summary of Economic and Financial Data, release 27 Jan 2026 | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2026/01/Summary-of-Economic-and-Financial-Data-January-2026.pdf | monthly Dec 2024 to Dec 2025 | Search excerpt of the PDF (interest-rate table). The price-development section was garbled, so inflation history is not taken from it |
| S-BOG-MPC-NOV26 | MPC Press Release, 18 Nov 2026 | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2026/11/MPC-Press-Release-November-2026.pdf | 133rd MPC | Full text read |
| S-BOG-MPC-MAY26 | MPC Press Release, 20 May 2026 | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2026/05/MPC-Press-Release-May-2026-.pdf | 130th MPC | Full text read. Source of the uniform 20 percent CRR, effective 4 Jun 2026 |
| S-BOG-MPC-MAR24 | MPC Press Release, March 2024 | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2024/01/MPC-Press-Release-March-2024.pdf | 117th MPC | Search excerpt only: "regulatory minimum threshold of 13.0 percent" for the capital adequacy ratio. Not read in full |
| S-BOG-MPR | Policy Rate Trends | Bank of Ghana | https://www.bog.gov.gh/monetary-policy/policy-rate-trends/ | Jan 2021 to Nov 2025 | Table via search excerpt |
| S-BOG-FX | Monthly Exchange Rates Indicators, and Daily Interbank FX Rates | Bank of Ghana | https://www.bog.gov.gh/economic-data/exchange-rate/ and https://www.bog.gov.gh/treasury-and-the-markets/daily-interbank-fx-rates/ | 2020 to Oct 2026; daily Nov 2026 | Page scrape (end-period table) and search excerpt (daily rate 11.85) |
| S-BOG-TB | Treasury Bill Rates | Bank of Ghana | https://www.bog.gov.gh/treasury-and-the-markets/treasury-bill-rates/ | auctions 2 to 23 Nov 2026 | Search excerpt of the results table |
| S-BOG-CAP17 | Notice No. BG/GOV/SEC/2017/19, New Minimum Paid Up Capital | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2019/09/Notice-on-New-Minimum-Paid-Up-Capital.pdf | requirement of GHS 400 million by 31 Dec 2018 | Search excerpt only. The GHS 400 million figure comes from a secondary summary (Dentons) of this notice; not read in full |
| S-GSS-HOME | Ghana Statistical Service home page (CPI) | Ghana Statistical Service | https://www.statsghana.gov.gh/ | Oct 2026 CPI 5.5 percent | Search excerpt; matches S-BOG-MPC-NOV26 |
| OWNER-ESTIMATE | Forecast assumption by the owner of this piece | claude | n/a | FY2026E to FY2030E | Not a source. Every row marked `estimated` is a judgement, with its reasoning in `notes` |

## Honest limits
- Several items were read from **search excerpts, not the full document** (marked above). The ones that matter most for bank models (policy rate, T-bill rates, FX, CRR, GDP) are cross-checked between at least two Bank of Ghana documents where noted.
- `min_car_pct` (13.0) and `min_capital_ghs_m` (400) come from older documents. A reviewer should confirm that they still apply in 2026.
- Inflation (2021 to 2024), T-bill history (2021 to 2024) and GDP (2021, 2022) are `unavailable`, and listed as follow-ups in `macro.csv`.
- The secondary quotes I saw (news, social posts, aggregator pages) were used only to find primary documents, never as values.

## Added in v1.1 (2026-11-25, after reviews by gemini and codex)
| source_id | Title | Publisher | URL | Period covered | How read |
| --- | --- | --- | --- | --- | --- |
| S-BOG-MPR-SEP26 | Monetary Policy Report, September 2026 | Bank of Ghana | https://www.bog.gov.gh/wp-content/uploads/2026/10/Monetary-Policy-Report-September-2026.pdf | to Aug 2026 | Targeted quote extraction from the 55-page PDF. Quote: industry CAR 19.1 percent in Aug 2026, "remaining well above the regulatory minimum requirement of 13.0 percent". Not read cover to cover |

Changes in v1.1: (1) `crr_pct` and `min_car_pct` are `reported` for FY2026E only; FY2027E to FY2030E are `estimated` carry-forwards. (2) `min_car_pct` now cites S-BOG-MPR-SEP26 (2026) instead of the March 2024 release. (3) `min_capital_ghs_m` is `estimated` in all forecast years because no 2026 confirmation of GHS 400 million was found.
