# Roster verification (claude)

**Result: the draft roster of 23 banks matches the Bank of Ghana register. No bank added or removed. Two naming differences.**

## Source (observed)
- Bank of Ghana, "Banks", Registered Institutions: https://www.bog.gov.gh/supervision-regulation/registered-institutions/banks/
- Retrieved 2026-11-25 (UTC), twice: a page scrape (shows "Showing 1 to 10 of **23** entries") and a read of the full table in a browser (all 23 rows present in the page).
- The page shows **no "as of" date**. Treat the list as the register's current state on the retrieval date, not as dated by the Bank of Ghana. Unknown: when the register was last edited.
- A secondary web result (globalbrandsmagazine.com, "All 23 Licensed Banks") also says 23. It is not an authority, so I did not rely on it.

## Register entries (as written on the BoG page) mapped to the roster slugs
| # | BoG register name | Roster slug | Match |
| --- | --- | --- | --- |
| 1 | Absa Bank Ghana LTD | absa-ghana | same |
| 2 | Access Bank (Ghana) Plc | access-bank-ghana | same |
| 3 | Agricultural Development Bank Plc | adb | same |
| 4 | Bank of Africa Ghana Limited | bank-of-africa-ghana | same |
| 5 | CalBank PLC | calbank | same |
| 6 | Consolidated Bank Ghana Limited | consolidated-bank-ghana | same |
| 7 | Ecobank Ghana Plc | ecobank-ghana | same |
| 8 | Fidelity Bank (Ghana) LTD | fidelity-bank-ghana | same |
| 9 | First Atlantic Bank PLC | first-atlantic-bank | same |
| 10 | **First Bank (Ghana) LTD** (website fbnbankghana.com) | fbnbank-ghana | **name differs**: register says "First Bank (Ghana) LTD"; the roster used "FBNBank Ghana" (the trading name; inferred from the website domain) |
| 11 | First National Bank (Ghana) Limited | first-national-bank-ghana | same |
| 12 | GCB Bank Plc | gcb | same |
| 13 | **Guaranty Trust Bank (Ghana) LTD** | gtbank-ghana | **name differs**: register uses the full legal name; same bank as "GTBank Ghana" |
| 14 | National Investment Bank PLC | nib | same |
| 15 | OmniBSIC Bank Ghana LTD | omnibsic-bank | same |
| 16 | Prudential Bank Limited | prudential-bank | same |
| 17 | Republic Bank (Ghana) PLC | republic-bank-ghana | same |
| 18 | Societe General Ghana Plc | societe-generale-ghana | same bank; the register spells it "Societe General" (no final e). Keep the slug |
| 19 | Stanbic Bank Ghana Limited | stanbic-bank-ghana | same |
| 20 | Standard Chartered Bank Ghana Plc | standard-chartered-ghana | same |
| 21 | United Bank for Africa (Ghana) Limited | uba-ghana | same |
| 22 | Universal Merchant Bank Ghana LTD | umb | same |
| 23 | Zenith Bank (Ghana) Limited | zenith-bank-ghana | same |

## What this does NOT tell us (unknown / for the model owners)
- **Ownership changes.** A bank can keep its licence but be sold or merged. Whether any of these banks were recently acquired, renamed or are being merged is not in the register. Each bank's owner should record ownership and any recent corporate action in that bank's `README.md`, with a source. (I have not checked.)
- **Listing status.** Which banks are on the Ghana Stock Exchange (and so file public financial statements most easily) is not in the register. Owners should confirm and note how easy each bank's filings are to obtain.
- **Not in scope:** rural and community banks, savings and loans companies, and microfinance companies are separate registers at the Bank of Ghana (the "All institutions" page lists Community Banks separately). Unchanged from ROSTER.md.
