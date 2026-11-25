# Pinned historical core coverage audit

Snapshot f5e331260cdf4c8cdb662416c43f831c82fb9de2. Codex retrieved and parsed all 23 CSVs from this exact immutable commit using a quote-aware CSV parser. A period counts only when all six keys (total_assets, total_liabilities, total_equity, profit_after_tax, interest_income, net_interest_income) have nonblank finite reported/derived values. This is a coverage screen, not an independent acceptance or source-page review. 23/23 files retrieved, 7551 data rows, zero estimated-status historical rows observed. 19/23 have all five FY2021–25 and 9M26 core periods; CBG has five annuals and H1-2026 (issuer archive as cited in sources.md reports no later Q3 located), so a blanket 9M rule would incorrectly exclude CBG. The other three have the documented source limitations. 

| Bank | Rows | Latest core interim | Missing required source coverage (subject to lead) | History blob SHA |
|---|---:|---|---|---|
| absa-ghana | 300 | 9M26 | none | 9378726879ef7f45c0f6588b7b6f1ea3fb1d237c |
| access-bank-ghana | 241 | 9M26 | none | 6a48342c1d8cb72d64dee1f460ccee7fe1787145 |
| adb | 281 | 9M26 | none | 65e361cc8e304e7e96a96b5304f6369498fcc28e |
| bank-of-africa-ghana | 308 | 9M26 | none | 513907294b6b6a4a563924499fe3dbc4c7559e09 |
| calbank | 249 | 9M26 | none | 0643cd5e75dc93dd2d28b6841947472f32914345 |
| consolidated-bank-ghana | 421 | H1-2026 (no Q3 located) | none | 434f9d19d121133ad19336b51170a1d64160b061 |
| ecobank-ghana | 253 | 9M26 | none | 97bc6b66b74e6b09cf5e30e063a62e6d348af77c |
| fbnbank-ghana | 355 | 9M26 | none | ce6ab186b8119bddafa59c293ce2d041b71dcc63 |
| fidelity-bank-ghana | 340 | 9M26 | none | 65f3cf8441d7f3f2bddeddcb06db8ccedf4eedf5 |
| first-atlantic-bank | 414 | 9M26 | none | d2212e690064f2509b59f3b9e86d93859cd915aa |
| first-national-bank-ghana | 317 | 9M26 | none | 8ac69675636a517adfa505d4154f5db507b49049 |
| gcb | 278 | 9M26 | none | 99b7e2d068a8f0247cbb46ed56fd206c90867828 |
| gtbank-ghana | 355 | 9M26 | none | 86d426357818e5d377cfcdd7f8db781d7387209a |
| nib | 427 | 9M26 | none | 2989132019fb60835ddef74af9cf8c3bdc378fe0 |
| omnibsic-bank | 310 | 9M26 | FY2021 | 65f82b327f721f1568b4c9020af36abe338c720b |
| prudential-bank | 238 | none (FY2025 anchor) | 9M-2026 | 5494d20237e2556563e5f76621100dd5a63134f3 |
| republic-bank-ghana | 480 | 9M26 | none | 06ad123d07674169083e4d856dfda29dc0f9388d |
| societe-generale-ghana | 354 | 9M26 | none | 5427e9e980efd29df388998272663963284127d1 |
| stanbic-bank-ghana | 367 | 9M26 | none | 27fc55f8245ec04b6452f48cb67078cb0c9e4d0e |
| standard-chartered-ghana | 296 | 9M26 | none | 29fc7ac3c8291490b0ed7f3dd8e9d5e8320c7a07 |
| uba-ghana | 341 | 9M26 | none | acadc1937f667b68119181a73aed29006902ffa7 |
| umb | 280 | 9M-2025 | FY2025 and 9M-2026 | 1164b6b58d4af53569fa170477002acec5fc2571 |
| zenith-bank-ghana | 346 | 9M26 | none | d808113074510ea0789d7b60f3393d6c151201bd |

The ordinary acceptance gate should require five exact annual periods and the latest published interim, not automatically all 9M-2026. Any exception must be specific and evidence-bound. No history/forecast files or live gates changed. This inventory does not replace existing reviewer judgments. The lead should independently verify CBG publication status at refresh.