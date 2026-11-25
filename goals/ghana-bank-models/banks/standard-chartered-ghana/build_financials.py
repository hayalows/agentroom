#!/usr/bin/env python3
"""Builds financials.csv and history checks for Standard Chartered Bank Ghana (bank-only, GHS millions).

Run:  python build_financials.py     (writes financials.csv and checks_history.md next to this file)

Inputs are typed below in GH¢'000 exactly as printed in the bank's published summary statements
(BANK column, never the Group column). Every row in financials.csv is then:
  reported  = a number printed in the cited document
  derived   = computed here from reported numbers (formula in notes)
Nothing is estimated. Anything not printed is left out (listed in README as unavailable).
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = "standard-chartered-ghana"
rows = []
facts = {}  # facts[(period, item)] = value in GH¢'000, for checks


def put(period, stmt, item, thousands, src, page, status, notes=""):
    facts[(period, item)] = thousands
    rows.append([BANK, period, stmt, item, f"{thousands / 1000:.3f}", "GHS millions", src, page, status, notes])


def ratio(period, item, value, src, page, notes=""):
    rows.append([BANK, period, "ratios", item, f"{value:.2f}", "percent", src, page, "reported", notes])


# ---------------------------------------------------------------------------------- statements by period
# Each entry: dict of printed lines (GH¢'000), the source id, and the PDF page index of the statements.
P = {}

P["FY2021"] = dict(src="SCB-FY21", page="1", ncols="bank only (the bank had no consolidated statements in this report)", note_extra="As originally reported; not restated in later documents I read.",
    ii=819932, ie=173575, nii=646357, fee_i=170024, fee_e=14179, nti=268504, fvtpl=-378, oth=0, lease_mod=0, opinc=1070328,
    imp_total=-5892,  # printed as a GAIN of 5,892 -> cost sign negative
    staff=245459, dep=34608, othx=101656, pbt=694497, tax_total=257563, pat=436934,
    levies=[("x_national_fiscal_stabilisation_levy", 34725), ("x_financial_sector_cleanup_levy", 26472)], tax_only=196366,
    cash=3203097, deriv_a=10143, trading=361964, due_banks=241254, loans_net=1886799, secs=3761388, cur_tax=31649, ppe=242067, rou=0, eq_inv=1001, other_a=381214, def_tax_a=0, ta=10120576,
    deriv_l=9249, dep_banks=79690, dep_cust=7554457, borrow=240244, prov=86228, def_tax_l=11623, oth_l=495803, lease_l=0, tl=8477294,
    stated=400000, retained=553412, res_fund=568228, crr=144087, oth_res=-22445, te=1643282,
    ratios=[("car_pct", 33.42), ("x_cet1_pct", 33.21), ("x_leverage_ratio_pct", 11.58), ("npl_pct", 23.59), ("x_npl_ex_loss_pct", 2.56), ("x_liquid_ratio_pct", 71.05)],
    ratio_note="CAR on CRD basis as printed.")

P["FY2022"] = dict(src="SCB-FY23", page="1", ncols="bank column", note_extra="Income statement as originally reported in SCB-FY23 comparatives. Balance sheet is the RESTATED 1 January 2023 position from SCB-FY24 (equity cut by GHS 40.3m, loans and tax assets changed after the bank corrected booking of written-off loans).",
    ii=1008901, ie=201115, nii=807786, fee_i=191440, fee_e=22220, nti=239390, fvtpl=-1189, oth=3499, lease_mod=-8581, opinc=1210125,
    imp_total=1158773,  # printed as total impairment LOSS (1,158,773) -> cost positive
    imp_sec=602086, imp_loan=506438, imp_lease=50249,
    staff=298472, dep=32983, othx=103439, pbt=-383542, tax_total=-83908, pat=-299634, levies=[], tax_only=-83908,
    bs_src="SCB-FY24", bs_page="1",
    cash=3978479, deriv_a=69691, trading=4560, due_banks=0, loans_net=1988310, secs=3473154, cur_tax=96637, ppe=37958, rou=192667, eq_inv=1001, other_a=295723, def_tax_a=188524, ta=10326704,
    deriv_l=70338, dep_banks=114439, dep_cust=8183887, borrow=0, prov=98015, def_tax_l=0, oth_l=288470, lease_l=284497, tl=9039646,
    stated=400000, retained=108080, res_fund=568228, crr=0, oth_res=210750, te=1287058,
    ratios=[("car_pct", 22.90), ("x_cet1_pct", 22.75), ("x_leverage_ratio_pct", 11.52), ("npl_pct", 12.04), ("x_npl_ex_loss_pct", 1.68), ("x_liquid_ratio_pct", 62.91)],
    ratio_note="Capital ratio printed as 'Capital requirement directive (CRD)' in SCB-FY23.", ratio_src="SCB-FY23")

P["FY2023"] = dict(src="SCB-FY24", page="1", ncols="bank column, RESTATED", note_extra="RESTATED in SCB-FY24 (booking errors on written-off non-performing loans corrected under IAS 8). Original SCB-FY23 figures differ: net trading income 217.465m (restated 141.090m), profit before tax 1,351.319m (restated 1,274.944m), profit after tax 864.391m (restated 814.747m), total assets 13,920.755m (restated 13,830.811m), equity 1,924.793m (restated 1,834.849m).",
    ii=1421644, ie=155201, nii=1266443, fee_i=205166, fee_e=27391, nti=141090, fvtpl=2222, oth=42499, lease_mod=2556, opinc=1632585,
    imp_total=-220312,  # printed as total reversal 220,312 -> cost negative
    imp_sec=47964, imp_loan=-253876, imp_lease=-14400,
    staff=392348, dep=42879, othx=142726, pbt=1274944, tax_total=460197, pat=814747, levies=[], tax_only=460197,
    cash=4309599, deriv_a=8920, trading=17911, due_banks=0, loans_net=1965894, secs=6694890, cur_tax=239679, ppe=28357, rou=173502, eq_inv=1001, other_a=307794, def_tax_a=83264, ta=13830811,
    deriv_l=15045, dep_banks=202946, dep_cust=10818779, borrow=232860, prov=134802, def_tax_l=0, oth_l=225454, lease_l=366076, tl=11995962,
    stated=400000, retained=814778, res_fund=676277, crr=0, oth_res=-56206, te=1834849,
    ratios=[("car_pct", 27.48), ("x_cet1_pct", 27.35), ("x_leverage_ratio_pct", 12.79), ("npl_pct", 9.29), ("x_npl_ex_loss_pct", 0.43), ("x_liquid_ratio_pct", 92.84)],
    ratio_note="Restated ratios from SCB-FY24 (originally 27.74 CAR, 27.61 CET1, 12.82 leverage in SCB-FY23).")

P["FY2024"] = dict(src="SCB-FY25", page="1", ncols="bank column", note_extra="Taken from the comparative column of SCB-FY25; equal to SCB-FY24 on every line I compared (total assets, equity, profit before tax).",
    ii=1601737, ie=198415, nii=1403322, fee_i=273562, fee_e=43205, nti=149417, fvtpl=-8569, oth=14021, lease_mod=0, opinc=1788548,
    imp_total=80918,  # printed as total impairment charge (80,918) -> cost positive
    imp_sec=-62686, imp_loan=138880, imp_lease=4724,
    staff=489940, dep=48816, othx=159948, pbt=1008926, tax_total=300541, pat=708385, levies=[], tax_only=300541,
    cash=4593873, deriv_a=12551, trading=111486, due_banks=2532470, loans_net=2305886, secs=3680729, cur_tax=373524, ppe=24400, rou=132255, eq_inv=899, sub_inv=1001, other_a=498354, def_tax_a=32873, ta=14300301,
    deriv_l=14571, dep_banks=124582, dep_cust=11319902, borrow=0, prov=115652, def_tax_l=0, oth_l=263832, lease_l=423611, tl=12262150,
    stated=400000, retained=1016367, res_fund=764825, crr=18376, oth_res=-161417, te=2038151,
    ratios=[("car_pct", 24.01), ("x_cet1_pct", 23.91), ("x_leverage_ratio_pct", 12.73), ("npl_pct", 24.77), ("x_npl_ex_loss_pct", 1.75), ("x_liquid_ratio_pct", 90.0)],
    ratio_note="Leverage ratio is 12.73 in SCB-FY25 comparatives but 12.79 in SCB-FY24; liquid ratio 90 (SCB-FY25) vs 90.06 (SCB-FY24). SCB-FY25 values used.")

P["FY2025"] = dict(src="SCB-FY25", page="1", ncols="bank column", note_extra="",
    ii=1130790, ie=127846, nii=1002944, fee_i=294559, fee_e=58695, nti=555110, fvtpl=4403, oth=23084, lease_mod=32, opinc=1821437,
    imp_total=-37482,  # printed as total reversal 37,482 -> cost negative
    imp_sec=28840, imp_loan=-66109, imp_lease=-213,
    staff=561416, dep=39155, othx=237161, pbt=1021187, tax_total=222506, pat=798681, levies=[], tax_only=222506,
    cash=6106101, deriv_a=22490, trading=400168, due_banks=2833636, loans_net=1887422, secs=4049948, cur_tax=423022, ppe=21837, rou=143881, eq_inv=804, sub_inv=1001, other_a=410485, def_tax_a=201844, ta=16502639,
    deriv_l=2052, dep_banks=284215, dep_cust=12385298, borrow=0, prov=135183, def_tax_l=0, oth_l=563672, lease_l=322398, tl=13692818,
    stated=400000, retained=1481336, res_fund=864660, crr=24899, oth_res=38926, te=2809821,
    ratios=[("car_pct", 27.45), ("x_cet1_pct", 27.11), ("x_leverage_ratio_pct", 13.22), ("npl_pct", 25.82), ("x_npl_ex_loss_pct", 0.81), ("x_liquid_ratio_pct", 104.0)],
    ratio_note="")

P["9M-2025"] = dict(src="SCB-Q3-26", page="1", ncols="bank column, unaudited comparative, income statement only", note_extra="Unaudited comparative period shown in SCB-Q3-26.",
    ii=901514, ie=127242, nii=774272, fee_i=243706, fee_e=42419, nti=360235, fvtpl=1378, oth=24254, lease_mod=0, opinc=1361426,
    imp_total=-36227, staff=429089, dep=28496, othx=169181, pbt=770887, tax_total=277845, pat=493042, levies=[], tax_only=277845, is_only=True)

P["9M-2026"] = dict(src="SCB-Q3-26", page="1", ncols="bank column, UNAUDITED", note_extra="Unaudited interim to 30 September 2026. Includes a GHS 673.5m dividend paid in 2026.",
    ii=623186, ie=81948, nii=541238, fee_i=208679, fee_e=50599, nti=426206, fvtpl=-8388, oth=24642, lease_mod=0, opinc=1141778,
    imp_total=-73963, staff=454784, dep=29493, othx=176727, pbt=554737, tax_total=198219, pat=356518, levies=[], tax_only=198219,
    cash=2999277, deriv_a=161845, trading=367739, due_banks=4623733, loans_net=2538490, secs=2800050, cur_tax=411743, ppe=33864, rou=145109, eq_inv=870, sub_inv=1001, other_a=300832, def_tax_a=239919, ta=14624472,
    deriv_l=7572, dep_banks=305643, dep_cust=10477131, borrow=0, prov=153521, def_tax_l=0, oth_l=829725, lease_l=373856, tl=12147448,
    stated=400000, retained=1164372, res_fund=864660, crr=24899, oth_res=23093, te=2477024,
    ratios=[("car_pct", 23.12), ("x_cet1_pct", 21.02), ("tier1_pct", 21.12), ("x_leverage_ratio_pct", 10.34), ("npl_pct", 23.25), ("x_npl_ex_loss_pct", 0.76), ("x_liquid_ratio_pct", 99.21)],
    ratio_note="Unaudited, as published 29 Oct 2026.")

IS = "income_statement"
BS = "balance_sheet"
for per, d in P.items():
    s, pg = d["src"], d["page"]
    base = f"Bank-only ({d['ncols']}). {d['note_extra']}".strip()
    put(per, IS, "interest_income", d["ii"], s, pg, "reported", base)
    put(per, IS, "interest_expense", d["ie"], s, pg, "reported", "Printed in brackets (an expense); stored positive.")
    put(per, IS, "net_interest_income", d["nii"], s, pg, "reported")
    put(per, IS, "fee_commission_income", d["fee_i"], s, pg, "reported")
    put(per, IS, "fee_commission_expense", d["fee_e"], s, pg, "reported", "Stored positive.")
    put(per, IS, "net_trading_income", d["nti"], s, pg, "reported")
    other = d["fvtpl"] + d["oth"] + d["lease_mod"]
    parts = f"{d['fvtpl']} (FVTPL) + {d['oth']} (other income) + {d['lease_mod']} (lease modification gain/loss) in GH¢'000"
    put(per, IS, "other_operating_income", other, s, pg, "derived", "Sum of: " + parts)
    put(per, IS, "total_operating_income", d["opinc"], s, pg, "reported", "Printed as 'Operating income' (before impairment).")
    put(per, IS, "staff_costs", d["staff"], s, pg, "reported", "Stored positive.")
    put(per, IS, "depreciation_amortisation", d["dep"], s, pg, "reported", "Stored positive.")
    put(per, IS, "other_operating_expenses", d["othx"], s, pg, "reported", "Stored positive.")
    note_imp = "Total impairment, sign flipped to the room convention (cost positive, reversal negative). "
    if "imp_sec" in d:
        note_imp += f"Components in x_ rows: securities {d['imp_sec']}, loans {d['imp_loan']}, lease {d['imp_lease']} (GH¢'000, cost positive)."
    put(per, IS, "impairment_charge", d["imp_total"], s, pg, "derived", note_imp)
    if "imp_sec" in d:
        put(per, IS, "x_impairment_investment_securities", d["imp_sec"], s, pg, "derived", "Cost positive. 2022 contains the domestic debt exchange (DDEP) hit on securities; see README.")
        put(per, IS, "x_impairment_loans_and_advances", d["imp_loan"], s, pg, "derived", "Cost positive. Includes 'and others' in SCB-FY23 wording.")
        put(per, IS, "x_impairment_lease", d["imp_lease"], s, pg, "derived", "Cost positive.")
    put(per, IS, "profit_before_tax", d["pbt"], s, pg, "reported")
    tnote = "Total tax and levies as printed. Negative = tax credit." if d["levies"] or per in ("FY2021", "FY2022", "FY2023") else "Income tax expense; stored positive."
    put(per, IS, "income_tax", d["tax_total"], s, pg, "reported", tnote)
    for k, v in d["levies"]:
        put(per, IS, k, v, s, pg, "reported", "Levy included inside income_tax above; shown separately for information, do not add again.")
    put(per, IS, "profit_after_tax", d["pat"], s, pg, "reported", "Printed as 'Profit/(loss) for the year/period'.")
    if d.get("is_only"):
        continue
    # balance sheet
    bs_s, bs_pg = d.get("bs_src", s), d.get("bs_page", pg)
    bnote = f"Bank-only. {'Restated 1 Jan 2023 position; see README.' if per == 'FY2022' else ''}".strip()
    put(per, BS, "cash_and_bog_balances", d["cash"], bs_s, bs_pg, "reported", "Printed as 'Cash and cash equivalents'; includes mandatory reserve deposits at the Bank of Ghana (SCB-FY25 cash-flow note: reserves excluded from cash flow cash). " + bnote)
    put(per, BS, "due_from_banks", d["due_banks"], bs_s, bs_pg, "reported", "Printed as 'Due from other banks' (FY2021: 'Loans to other banks'). 0 where no line is printed.")
    put(per, BS, "investment_securities", d["secs"], bs_s, bs_pg, "reported")
    put(per, BS, "loans_and_advances_net", d["loans_net"], bs_s, bs_pg, "reported", "Printed 'Loans and advances to customers' (net of impairment).")
    put(per, BS, "property_equipment_intangibles", d["ppe"] + d["rou"], bs_s, bs_pg, "derived", f"Property and equipment {d['ppe']} + right-of-use asset {d['rou']} (GH¢'000). FY2021 prints one combined line.")
    oa_parts = [("derivative assets", d["deriv_a"]), ("non-pledged trading assets", d["trading"]), ("current tax assets", d["cur_tax"]), ("deferred tax asset", d["def_tax_a"]), ("equity investments", d["eq_inv"]), ("investment in subsidiaries", d.get("sub_inv", 0)), ("other assets", d["other_a"])]
    put(per, BS, "other_assets", sum(v for _, v in oa_parts), bs_s, bs_pg, "derived", "Sum of (GH¢'000): " + "; ".join(f"{n} {v}" for n, v in oa_parts))
    put(per, BS, "total_assets", d["ta"], bs_s, bs_pg, "reported")
    put(per, BS, "customer_deposits", d["dep_cust"], bs_s, bs_pg, "reported")
    put(per, BS, "due_to_banks", d["dep_banks"], bs_s, bs_pg, "reported", "Printed as 'Deposits from banks'.")
    put(per, BS, "borrowings", d["borrow"], bs_s, bs_pg, "reported" if d["borrow"] else "derived", "Short-term borrowings / borrowings. 0 where no line is printed in the statement of financial position.")
    ol_parts = [("derivative liabilities", d["deriv_l"]), ("provisions", d["prov"]), ("deferred tax liabilities", d["def_tax_l"]), ("other liabilities", d["oth_l"]), ("lease liabilities", d["lease_l"])]
    put(per, BS, "other_liabilities", sum(v for _, v in ol_parts), bs_s, bs_pg, "derived", "Sum of (GH¢'000): " + "; ".join(f"{n} {v}" for n, v in ol_parts))
    put(per, BS, "total_liabilities", d["tl"], bs_s, bs_pg, "reported")
    put(per, BS, "stated_capital", d["stated"], bs_s, bs_pg, "reported")
    put(per, BS, "retained_earnings", d["retained"], bs_s, bs_pg, "reported", "Printed as 'Retained earnings' or 'Income surplus'.")
    put(per, BS, "reserves_other", d["res_fund"] + d["crr"] + d["oth_res"], bs_s, bs_pg, "derived", f"Reserve fund {d['res_fund']} + credit risk reserve {d['crr']} + other reserves {d['oth_res']} (GH¢'000).")
    put(per, BS, "total_equity", d["te"], bs_s, bs_pg, "reported", "Printed as 'Total shareholders' funds'.")
    rsrc = d.get("ratio_src", s)
    for k, v in d["ratios"]:
        ratio(per, k, v, rsrc, "2" if s in ("SCB-FY25", "SCB-FY24") and rsrc == s else "1", d["ratio_note"])

# not printed in these summary statements
for per in ("FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "9M-2026"):
    for item in ("loans_and_advances_gross", "loan_loss_allowance"):
        rows.append([BANK, per, "balance_sheet", item, "", "GHS millions", "", "", "unavailable", "The published summary statements show loans only net of impairment. Gross loans and the allowance are in the notes to the full audited accounts, which I have not read."])
    rows.append([BANK, per, "ratios", "roe_pct", "", "percent", "", "", "unavailable", "Not printed in the summary statements. Recomputed in checks."])

with open(os.path.join(HERE, "financials.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bank", "period", "statement", "line_item", "value", "unit", "source_id", "page", "status", "notes"])
    w.writerows(rows)

# ---------------------------------------------------------------------------------- history checks
out = ["# History checks (generated by build_financials.py)", "", "All figures GH¢'000 unless stated. A check passes when the difference is within 1 (rounding).", "",
       "| Period | Check | Left | Right | Difference | Result |", "| --- | --- | --- | --- | --- | --- |"]
fails = 0
for per, d in P.items():
    def chk(name, left, right):
        global fails
        diff = left - right
        ok = abs(diff) <= 1
        fails += 0 if ok else 1
        out.append(f"| {per} | {name} | {left:,} | {right:,} | {diff:,} | {'PASS' if ok else 'FAIL'} |")
    chk("NII = interest income - interest expense", d["ii"] - d["ie"], d["nii"])
    other = d["fvtpl"] + d["oth"] + d["lease_mod"]
    chk("operating income = NII + net fees + trading + other", d["nii"] + d["fee_i"] - d["fee_e"] + d["nti"] + other, d["opinc"])
    chk("PBT = operating income - impairment - operating expenses", d["opinc"] - d["imp_total"] - (d["staff"] + d["dep"] + d["othx"]), d["pbt"])
    chk("PAT = PBT - total tax and levies", d["pbt"] - d["tax_total"], d["pat"])
    if "imp_sec" in d:
        chk("impairment components add to total", d["imp_sec"] + d["imp_loan"] + d["imp_lease"], d["imp_total"])
    if d.get("is_only"):
        continue
    ppe = d["ppe"] + d["rou"]
    oa = sum([d["deriv_a"], d["trading"], d["cur_tax"], d["def_tax_a"], d["eq_inv"], d.get("sub_inv", 0), d["other_a"]])
    chk("total assets = sum of asset lines", d["cash"] + d["due_banks"] + d["loans_net"] + d["secs"] + ppe + oa, d["ta"])
    ol = sum([d["deriv_l"], d["prov"], d["def_tax_l"], d["oth_l"], d["lease_l"]])
    chk("total liabilities = sum of liability lines", d["dep_cust"] + d["dep_banks"] + d["borrow"] + ol, d["tl"])
    chk("total equity = stated + retained + reserves", d["stated"] + d["retained"] + d["res_fund"] + d["crr"] + d["oth_res"], d["te"])
    chk("total assets = total liabilities + total equity", d["tl"] + d["te"], d["ta"])
out += ["", f"Failures: {fails}", ""]
out += ["## Ratios recomputed from the numbers (GH¢'000 inputs, annual periods only; ROE on closing equity)", "", "| Period | Loans/deposits (net loans / customer deposits) | Cost-to-income (opex / operating income) | ROE (PAT / closing equity) | ROA (PAT / closing assets) |", "| --- | --- | --- | --- | --- |"]
for per, d in P.items():
    if d.get("is_only") or per == "9M-2026":
        continue
    ldr = d["loans_net"] / d["dep_cust"] * 100
    cti = (d["staff"] + d["dep"] + d["othx"]) / d["opinc"] * 100
    roe = d["pat"] / d["te"] * 100
    roa = d["pat"] / d["ta"] * 100
    out.append(f"| {per} | {ldr:.1f}% | {cti:.1f}% | {roe:.1f}% | {roa:.1f}% |")
out += ["", "Note: a news item quoted a 2025 return on equity of 28 percent. My closing-equity recomputation gives 28.4 percent for FY2025, which is consistent, but I have not seen the bank's own definition (closing or average equity). Average equity (2,038 and 2,810) would give about 33 percent. The figures above are recomputations, not bank-reported ratios."]
with open(os.path.join(HERE, "checks_history.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("rows:", len(rows), "| failures:", fails)
