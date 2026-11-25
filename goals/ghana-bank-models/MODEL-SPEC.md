# Model spec: one shared format so every bank can be compared and rolled up

Currency: **GHS millions** unless a row says otherwise. Fiscal year: the bank's own year-end (record it). Periods: the last **5 full fiscal years** that are publicly available, plus the latest interim period if published.

## Files for each bank: `banks/<slug>/`
| File | Purpose |
| --- | --- |
| `README.md` | 1 page: who the bank is, ownership and listing status, size, a plain summary of the model and its main findings, known gaps |
| `sources.md` | Table of sources: `source_id`, title, publisher, URL, period covered, date you retrieved it |
| `financials.csv` | Historical numbers in the long format below |
| `assumptions.json` | Forecast drivers, with a note and a source or reason for each |
| `forecast.csv` | 5-year forecast, base / downside / upside, same line items as `financials.csv` |
| `model.py` (preferred) | Standard-library Python that reads `financials.csv` + `assumptions.json` and writes `forecast.csv` and `checks.md`. If your app cannot run code, write the formulas out in `assumptions.md` so anyone can reproduce them |
| `checks.md` | Results of the checks below, pass or fail, with the numbers |

## `financials.csv` columns
`bank,period,statement,line_item,value,unit,source_id,page,status,notes`
- `period`: e.g. `FY2023` or `H1-2024`
- `statement`: `income_statement`, `balance_sheet` or `ratios`
- `line_item`: use ONLY these keys (so banks roll up)
  - income_statement: `interest_income`, `interest_expense`, `net_interest_income`, `fee_commission_income`, `fee_commission_expense`, `net_trading_income`, `other_operating_income`, `total_operating_income`, `staff_costs`, `depreciation_amortisation`, `other_operating_expenses`, `impairment_charge`, `profit_before_tax`, `income_tax`, `profit_after_tax`
  - balance_sheet: `cash_and_bog_balances`, `due_from_banks`, `investment_securities`, `loans_and_advances_gross`, `loan_loss_allowance`, `loans_and_advances_net`, `property_equipment_intangibles`, `other_assets`, `total_assets`, `customer_deposits`, `due_to_banks`, `borrowings`, `other_liabilities`, `total_liabilities`, `stated_capital`, `retained_earnings`, `reserves_other`, `total_equity`
  - ratios (as the bank reports them): `car_pct`, `tier1_pct`, `npl_pct`, `ldr_pct`, `cost_to_income_pct`, `roe_pct`, `roa_pct`
  - If a bank reports an extra important item, add `x_<name>` and explain in `notes`.
- `status`: one of
  - `reported`: copied from a cited filing (`source_id` and `page` required)
  - `derived`: calculated from reported rows; write the formula in `notes`
  - `estimated`: an analyst estimate; method in `notes`
  - `unavailable`: not found. Leave `value` blank. **Never fill it with a guess.**

## Ghana-specific items to handle explicitly (verify each; I am recalling these from memory)
- Ghana's **2022 to 2023 domestic debt exchange**: how did this bank account for it (impairment, capital relief, regulatory forbearance)? Source it.
- **Bank of Ghana capital and reserve requirements** at the time of each period (minimum capital, capital adequacy ratio, cash reserve ratio). Cite the notice. They changed, so use the figure in force for each period.
- **Sector levies and special taxes** on banks: record the actual income tax charge as reported and list any levies separately in `notes`.
- **Cedi depreciation** effects on foreign-currency assets and liabilities.

## Forecast rules
- 5 years, three scenarios (`base`, `downside`, `upside`) with the scenario name in a column.
- Drivers in `assumptions.json`, at least: loan growth, deposit growth, yield on investment securities (tied to `macro-assumptions`), yield on loans, cost of funds, fee growth, operating expense growth, cost of risk / NPL path, tax rate, dividend payout, capital ratio target.
- Use the shared `sector/macro-assumptions/` inputs for rates, inflation, FX and GDP so all banks are consistent. If it is not finished yet, say so on your board and use clearly labelled placeholders you will replace.
- Forecasts are estimates. Label them as such everywhere.

## Checks (put results in `checks.md`)
1. Balance sheet balances: `total_assets = total_liabilities + total_equity` (history and every forecast year). Report any difference.
2. Totals add up: `net_interest_income = interest_income - interest_expense`, `loans_and_advances_net = gross - allowance`, `profit_after_tax = profit_before_tax - income_tax`, etc.
3. Ratios recomputed from the numbers (ROE, ROA, cost-to-income, loan-to-deposit) are close to the bank's reported ratios. Explain differences.
4. Capital adequacy in the forecast stays at or above the regulatory minimum, or the model flags the shortfall.
5. At least 3 spot-checks of `reported` numbers against the filing page.
6. No `reported` row without `source_id` and `page`.

## Quality bar
A reviewer should be able to rebuild any forecast number from the files alone, and follow any historical number to a page in a public filing.
