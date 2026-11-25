#!/usr/bin/env python3
"""Builds financials.csv and checks_history.md for Guaranty Trust Bank (Ghana) Ltd (bank-only, GHS millions).

Run:  python build_financials.py     (writes financials.csv and checks_history.md next to this file)

Inputs are typed below in GH¢'000 exactly as printed in the bank's published statements. GTBank Ghana
publishes a single set of statements (it has no group). Every output row is:
  reported = a number printed in the cited document (lines are never changed)
  derived  = computed here from printed numbers (formula in notes)
Nothing is estimated. Latest published classification is used where a later report re-presented an earlier year.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = "gtbank-ghana"
rows = []

IS, BS, RT = "income_statement", "balance_sheet", "ratios"


def put(period, stmt, item, thousands, src, page, status, notes=""):
    rows.append([BANK, period, stmt, item, f"{thousands / 1000:.3f}", "GHS millions", src, page, status, notes])


def ratio(period, item, value, src, page, notes=""):
    rows.append([BANK, period, RT, item, f"{value:.2f}", "percent", src, page, "reported", notes])


P = {}
# ------------------------------------------------------------------ income statement inputs (printed, GH¢'000)
# ii_a = interest income (EIR), ii_b = other interest and similar income (0 if no line), ie = interest expense (positive),
# fv = net income from other financial instruments at fair value, oth_inc = other income, imp = net impairment charge (cost positive),
# staff, amort_lease, dep, fin (separate lease finance charge, FY2021-FY2022 only), othx, pbt, tax (total tax incl. levies), pat
P["FY2021"] = dict(src="GTB-FY21", page="1", sp=None, note="As originally reported in GTB-FY21; FY2022 report not read, so any later re-presentation of 2021 is not applied.",
    ii_a=421028, ii_b=60548, ie=140110, nii=341466, fee_i=149901, fee_e=32836, nti=133954, fv=55192, oth_inc=436,
    imp=14826, staff=63297, amort_lease=1924, dep=19595, fin=4178, othx=67051, pbt=477242, tax=161796, pat=315446,
    tax_parts=[("x_income_tax_before_levies", 120037), ("x_national_fiscal_stabilisation_levy", 23862), ("x_financial_sector_recovery_levy", 17897)],
    cash=894167, trading=764426, pledged=160121, loans=1647641, secs=1013537, cur_tax_a=0, def_tax_a=4132, other_a=424970, ppe=117208, intang=9249, ta=5035451,
    dep_c=3725427, cur_tax_l=2740, def_tax_l=2705, prov=1396, oth_l=82705, tl=3814973,
    stated=404895, retained=375870, crr=37241, stat=403861, oth_res=-1389, te=1220478,
    ratios=[("car_pct", 38.80), ("npl_pct", 1.59), ("x_loan_loss_provision_ratio_pct", 0.47), ("x_liquidity_ratio_pct", 60.60), ("x_leverage_ratio_pct", 21.79)])
P["FY2022"] = dict(src="GTB-FY23", page="1", sp=None, note="Income statement and balance sheet as printed in the FY2022 comparatives of GTB-FY23 (the FY2022 report itself was not read).",
    ii_a=649145, ii_b=0, ie=176232, nii=472913, fee_i=244472, fee_e=57464, nti=304813, fv=1771, oth_inc=269,
    imp=557020, staff=81809, amort_lease=1676, dep=20885, fin=3776, othx=110570, pbt=191038, tax=76058, pat=114980,
    tax_parts=[("x_income_tax_before_levies", 56954), ("x_national_fiscal_stabilisation_levy", 9552), ("x_financial_sector_recovery_levy", 9552)],
    cash=1779276, trading=142756, pledged=158628, loans=2026345, secs=2134382, cur_tax_a=44370, def_tax_a=137422, other_a=560523, ppe=138662, intang=4981, ta=7127345,
    dep_c=5629807, cur_tax_l=0, def_tax_l=0, prov=521, oth_l=161395, tl=5791723,
    stated=404895, retained=473113, crr=26233, stat=432606, oth_res=-1225, te=1335622,
    ratios=[("car_pct", 33.42), ("npl_pct", 2.42), ("x_loan_loss_provision_ratio_pct", 0.86), ("x_liquidity_ratio_pct", 57.51), ("x_leverage_ratio_pct", 21.83)])
P["FY2023"] = dict(src="GTB-FY24", page="1", sp=None, note="Taken from the FY2023 comparatives in GTB-FY24 (the bank re-presented 2023: the lease finance charge of 3.927m moved into interest expense; profit before tax 1,118.498m is unchanged from GTB-FY23).",
    ii_a=1341301, ii_b=2977, ie=313113, nii=1031166, fee_i=281228, fee_e=85993, nti=297364, fv=-3411, oth_inc=2133,
    imp=115364, staff=87279, amort_lease=2284, dep=23314, fin=0, othx=175748, pbt=1118498, tax=392712, pat=725786,
    tax_parts=[], imp_parts=[("x_impairment_reversal_financial_assets", -295067), ("x_modification_loss_investment_securities", 410431)],
    cash=3094740, trading=60897, pledged=156831, loans=1790422, secs=5516067, cur_tax_a=11892, def_tax_a=166671, other_a=277577, ppe=144070, intang=5186, ta=11224353,
    dep_c=9011566, cur_tax_l=0, def_tax_l=0, prov=1025, oth_l=149127, tl=9161718,
    stated=404895, retained=997000, crr=46687, stat=614053, oth_res=0, te=2062635,
    ratios=[("car_pct", 41.84), ("npl_pct", 3.95), ("x_loan_loss_provision_ratio_pct", 2.26), ("x_liquidity_ratio_pct", 73.18), ("x_leverage_ratio_pct", 18.03)],
    ratio_src="GTB-FY24")
P["FY2024"] = dict(src="GTB-FY25", page="1", sp=None, note="Taken from the FY2024 comparatives in GTB-FY25; equal to GTB-FY24 on every statement line I compared.",
    ii_a=1828378, ii_b=277, ie=630424, nii=1198231, fee_i=364278, fee_e=129307, nti=281748, fv=1555, oth_inc=7171,
    imp=185805, staff=117054, amort_lease=2120, dep=27826, fin=0, othx=219479, pbt=1171391, tax=427369, pat=744022,
    tax_parts=[], imp_parts=[("x_impairment_reversal_financial_assets", -157167), ("x_modification_loss_investment_securities", 342972)],
    cash=5660310, trading=158697, pledged=283000, loans=2553795, secs=5609497, cur_tax_a=23728, def_tax_a=199619, other_a=600719, ppe=272198, intang=4587, ta=15366150,
    dep_c=12741124, cur_tax_l=0, def_tax_l=0, prov=1025, oth_l=130155, tl=12872304,
    stated=404895, retained=1348501, crr=33394, stat=707056, oth_res=0, te=2493846,
    ratios=[("car_pct", 36.94), ("npl_pct", 2.42), ("x_loan_loss_provision_ratio_pct", 1.14), ("x_liquidity_ratio_pct", 69.52), ("x_leverage_ratio_pct", 15.41)],
    ratio_note="CAR 36.94 and leverage 15.41 are the FY2024 values printed in GTB-FY25; GTB-FY24 itself printed 37.01 and 15.30.")
P["FY2025"] = dict(src="GTB-FY25", page="1", sp=None, note="",
    ii_a=2194220, ii_b=12032, ie=843730, nii=1362522, fee_i=469380, fee_e=161805, nti=426243, fv=16833, oth_inc=8667,
    imp=15684, staff=152305, amort_lease=2898, dep=45492, fin=0, othx=341057, pbt=1564405, tax=552182, pat=1012223,
    tax_parts=[], imp_parts=[("x_impairment_charge_financial_assets", 1088), ("x_modification_loss_investment_securities", 896), ("x_impairment_non_financial_assets", 13700)],
    cash=9545853, trading=107406, pledged=260402, loans=3429641, secs=6363569, cur_tax_a=112448, def_tax_a=159999, other_a=833988, ppe=353454, intang=34860, ta=21201620,
    dep_c=18049481, cur_tax_l=0, def_tax_l=0, prov=1025, oth_l=109883, tl=18160389,
    stated=404895, retained=1686279, crr=116473, stat=833583, oth_res=0, te=3041231,
    ratios=[("car_pct", 32.70), ("npl_pct", 7.13), ("x_loan_loss_provision_ratio_pct", 0.91), ("x_liquidity_ratio_pct", 77.48), ("x_leverage_ratio_pct", 12.35)],
    ratio_note="The Q3-2026 statement prints December 2025 CAR as 32.37 and leverage 12.35; the audited FY2025 report prints CAR 32.70. 32.70 is used.", ratio_page="2")
P["9M-2025"] = dict(src="GTB-Q3-26", page="1", sp=None, note="Unaudited comparative (nine months to 30 Sep 2025) printed in GTB-Q3-26.",
    ii_a=1586385, ii_b=209, ie=622138, nii=964456, fee_i=393026, fee_e=117355, nti=299476, fv=21777, oth_inc=1355,
    imp=20571, staff=112628, amort_lease=2832, dep=23317, fin=0, othx=211957, pbt=1191430, tax=417000, pat=774430,
    tax_parts=[], imp_parts=[("x_impairment_loans_and_advances", 7975), ("x_impairment_other_financial_assets", 12596)],
    cash=6426068, trading=153451, pledged=446073, loans=3344440, secs=7069029, cur_tax_a=0, def_tax_a=199619, other_a=1121183, ppe=355274, intang=10966, ta=19126103,
    dep_c=15988217, cur_tax_l=173210, def_tax_l=0, prov=1025, oth_l=160213, tl=16322665,
    stated=404895, retained=1561289, crr=33394, stat=803859, oth_res=0, te=2803438,
    ratios=[("car_pct", 33.33), ("npl_pct", 1.63), ("x_loan_loss_provision_ratio_pct", 1.10), ("x_liquidity_ratio_pct", 73.56), ("x_leverage_ratio_pct", 11.53)],
    ratio_note="Unaudited comparative as printed in GTB-Q3-26.")
P["9M-2026"] = dict(src="GTB-Q3-26", page="1", sp=None, note="UNAUDITED interim to 30 September 2026. Includes dividends paid of 604.370m in 2026.",
    ii_a=1656601, ii_b=5167, ie=429953, nii=1231815, fee_i=462787, fee_e=141093, nti=257197, fv=4441, oth_inc=1440,
    imp=6499, staff=126850, amort_lease=2071, dep=61247, fin=0, othx=235218, pbt=1384702, tax=484646, pat=900056,
    tax_parts=[], imp_parts=[("x_impairment_loans_and_advances", 1275), ("x_impairment_other_financial_assets", 5224)],
    cash=11747476, trading=232853, pledged=88416, loans=6406184, secs=5123287, cur_tax_a=0, def_tax_a=159999, other_a=1839312, ppe=345522, intang=29381, ta=25972432,
    dep_c=22496810, cur_tax_l=802, def_tax_l=0, prov=1025, oth_l=136878, tl=22635515,
    stated=404895, retained=1869458, crr=116473, stat=946091, oth_res=0, te=3336918,
    ratios=[("car_pct", 24.08), ("npl_pct", 3.67), ("x_loan_loss_provision_ratio_pct", 0.51), ("x_liquidity_ratio_pct", 69.15), ("x_leverage_ratio_pct", 10.30)],
    ratio_note="Unaudited, as published.")

for per, d in P.items():
    s, pg = d["src"], d["page"]
    base = f"Bank-only (GTBank Ghana publishes a single set of statements). {d['note']}".strip()
    ii = d["ii_a"] + d["ii_b"]
    put(per, IS, "interest_income", ii, s, pg, "derived" if d["ii_b"] else "reported",
        (f"Interest income by effective interest method {d['ii_a']} + other interest and similar income {d['ii_b']} (GH¢'000). " if d["ii_b"] else "As printed. ") + base)
    put(per, IS, "interest_expense", d["ie"], s, pg, "reported", "Stored positive. " + ("FY2023 onward includes the lease finance charge; FY2021 and FY2022 print it as a separate expense, which I show inside other_operating_expenses." if per in ("FY2021", "FY2022") else ""))
    put(per, IS, "net_interest_income", d["nii"], s, pg, "reported")
    put(per, IS, "fee_commission_income", d["fee_i"], s, pg, "reported")
    put(per, IS, "fee_commission_expense", d["fee_e"], s, pg, "reported", "Stored positive.")
    put(per, IS, "net_trading_income", d["nti"], s, pg, "reported")
    other = d["fv"] + d["oth_inc"]
    put(per, IS, "other_operating_income", other, s, pg, "derived", f"Net income from other financial instruments at fair value {d['fv']} + other income {d['oth_inc']} (GH¢'000).")
    net_fee = d["fee_i"] - d["fee_e"]
    toi = d["nii"] + net_fee + d["nti"] + other
    put(per, IS, "total_operating_income", toi, s, pg, "derived", "Net interest income + net fee and commission income + net trading income + other operating income (before impairment). The bank's own 'Net operating income' line excludes 'Other income'.")
    put(per, IS, "staff_costs", d["staff"], s, pg, "reported", "Printed as personnel expenses; stored positive.")
    da = d["dep"] + d["amort_lease"]
    put(per, IS, "depreciation_amortisation", da, s, pg, "derived", f"Depreciation and amortisation {d['dep']} + amortisation of prepaid leases {d['amort_lease']} (GH¢'000).")
    ox = d["othx"] + d["fin"]
    put(per, IS, "other_operating_expenses", ox, s, pg, "reported" if not d["fin"] else "derived", "Other operating expenses." if not d["fin"] else f"Other operating expenses {d['othx']} + lease finance charge {d['fin']} (printed separately in this period; later reports put it in interest expense).")
    inote = "Net impairment cost (positive = cost). "
    if "imp_parts" in d:
        inote += "Components shown in x_ rows (cost positive; a reversal is negative). "
    else:
        inote += "Printed as one line 'Net impairment on financial instruments'. "
    if per == "FY2022":
        inote += "FY2022 is the year of the domestic debt exchange (DDEP)."
    put(per, IS, "impairment_charge", d["imp"], s, pg, "derived" if "imp_parts" in d else "reported", inote)
    for k, v in d.get("imp_parts", []):
        put(per, IS, k, v, s, pg, "reported", "Cost positive; reversal negative. Part of impairment_charge.")
    put(per, IS, "profit_before_tax", d["pbt"], s, pg, "reported")
    tnote = "Total income tax and levies (profit before tax minus profit after tax)." if d["tax_parts"] else "Income tax expense as printed (levies included in the printed charge)."
    put(per, IS, "income_tax", d["tax"], s, pg, "derived" if d["tax_parts"] else "reported", tnote)
    for k, v in d["tax_parts"]:
        put(per, IS, k, v, s, pg, "reported", "Printed separately; already inside income_tax above, do not add again.")
    put(per, IS, "profit_after_tax", d["pat"], s, pg, "reported", "Printed as 'Profit for the year/period'.")
    # balance sheet
    other_a = d["trading"] + d["pledged"] + d["cur_tax_a"] + d["def_tax_a"] + d["other_a"]
    put(per, BS, "cash_and_bog_balances", d["cash"], s, pg, "reported", "Printed 'Cash and cash equivalents'; includes balances at the Bank of Ghana and with other banks (no separate due-from-banks line). " + base)
    put(per, BS, "due_from_banks", 0, s, pg, "derived", "No separate line is printed; balances with other banks are inside cash and cash equivalents.")
    put(per, BS, "investment_securities", d["secs"], s, pg, "reported", "Printed 'Investment securities' only. Pledged assets and non-pledged trading assets are in other_assets (memo x_ rows below).")
    put(per, BS, "loans_and_advances_net", d["loans"], s, pg, "reported", "Printed 'Loans and advances to customers' (net of impairment).")
    put(per, BS, "property_equipment_intangibles", d["ppe"] + d["intang"], s, pg, "derived", f"Property and equipment {d['ppe']} + intangible assets {d['intang']} (GH¢'000). No separate right-of-use line is printed.")
    put(per, BS, "other_assets", other_a, s, pg, "derived", f"Non-pledged trading assets {d['trading']} + pledged assets {d['pledged']} + current tax assets {d['cur_tax_a']} + deferred tax assets {d['def_tax_a']} + other assets {d['other_a']} (GH¢'000).")
    put(per, BS, "x_pledged_assets", d["pledged"], s, pg, "reported", "Memo only: inside other_assets above, do not add again.")
    put(per, BS, "x_non_pledged_trading_assets", d["trading"], s, pg, "reported", "Memo only: inside other_assets above, do not add again.")
    put(per, BS, "total_assets", d["ta"], s, pg, "reported")
    put(per, BS, "customer_deposits", d["dep_c"], s, pg, "reported")
    put(per, BS, "due_to_banks", 0, s, pg, "derived", "No line printed for deposits from banks.")
    put(per, BS, "borrowings", 0, s, pg, "derived", "No borrowings line is printed.")
    ol = d["cur_tax_l"] + d["def_tax_l"] + d["prov"] + d["oth_l"]
    put(per, BS, "other_liabilities", ol, s, pg, "derived", f"Current tax liabilities {d['cur_tax_l']} + deferred tax liabilities {d['def_tax_l']} + provision on off-balance-sheet items {d['prov']} + other liabilities {d['oth_l']} (GH¢'000).")
    put(per, BS, "total_liabilities", d["tl"], s, pg, "reported")
    put(per, BS, "stated_capital", d["stated"], s, pg, "reported")
    put(per, BS, "retained_earnings", d["retained"], s, pg, "reported", "Printed as 'Retained earnings' or 'Income surplus'.")
    put(per, BS, "reserves_other", d["crr"] + d["stat"] + d["oth_res"], s, pg, "derived", f"Credit risk reserve {d['crr']} + statutory reserve fund {d['stat']} + other reserves {d['oth_res']} (GH¢'000).")
    put(per, BS, "total_equity", d["te"], s, pg, "reported")
    rs = d.get("ratio_src", s)
    rp = d.get("ratio_page", "2" if rs in ("GTB-FY25", "GTB-FY24", "GTB-FY23") else "1")
    for k, v in d["ratios"]:
        ratio(per, k, v, rs, rp, d.get("ratio_note", ""))

for per in P:
    if per == "FY2021" or per in P:
        for item in ("loans_and_advances_gross", "loan_loss_allowance"):
            rows.append([BANK, per, BS, item, "", "GHS millions", "", "", "unavailable", "The summary statements print loans net only. Gross loans and the allowance are in the annual-report notes (GTB-AR24, GTB-AR22), which I have not read."])
        rows.append([BANK, per, RT, "tier1_pct", "", "percent", "", "", "unavailable", "Not printed. The bank prints a 'Tier 1 leverage ratio' (x_leverage_ratio_pct), which is a different measure."])

with open(os.path.join(HERE, "financials.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bank", "period", "statement", "line_item", "value", "unit", "source_id", "page", "status", "notes"])
    w.writerows(rows)

# ------------------------------------------------------------------ checks
out = ["# History checks (generated by build_financials.py)", "", "GH¢'000 unless stated. A check passes within 2 (the bank's published statements carry rounding differences of 1 to 2 thousand).", "",
       "| Period | Check | Left | Right | Difference | Result |", "| --- | --- | --- | --- | --- | --- |"]
fails = 0
for per, d in P.items():
    def chk(name, left, right, tol=2):
        global fails
        diff = left - right
        ok = abs(diff) <= tol
        fails += 0 if ok else 1
        out.append(f"| {per} | {name} | {left:,} | {right:,} | {diff:,} | {'PASS' if ok else 'FAIL'} |")
    ii = d["ii_a"] + d["ii_b"]
    chk("NII = interest income - interest expense", ii - d["ie"], d["nii"])
    other = d["fv"] + d["oth_inc"]
    toi = d["nii"] + d["fee_i"] - d["fee_e"] + d["nti"] + other
    opex = d["staff"] + d["dep"] + d["amort_lease"] + d["othx"] + d["fin"]
    chk("PBT = total operating income - impairment - operating expenses", toi - d["imp"] - opex, d["pbt"])
    chk("PAT = PBT - total tax and levies", d["pbt"] - d["tax"], d["pat"])
    if d["tax_parts"]:
        chk("tax parts add to total tax", sum(v for _, v in d["tax_parts"]), d["tax"])
    if "imp_parts" in d:
        chk("impairment components add to impairment_charge", sum(v for _, v in d["imp_parts"]), d["imp"])
    other_a = d["trading"] + d["pledged"] + d["cur_tax_a"] + d["def_tax_a"] + d["other_a"]
    chk("total assets = sum of asset lines", d["cash"] + d["secs"] + d["loans"] + d["ppe"] + d["intang"] + other_a, d["ta"])
    ol = d["cur_tax_l"] + d["def_tax_l"] + d["prov"] + d["oth_l"]
    chk("total liabilities = sum of liability lines", d["dep_c"] + ol, d["tl"])
    chk("total equity = stated + retained + reserves", d["stated"] + d["retained"] + d["crr"] + d["stat"] + d["oth_res"], d["te"])
    chk("total assets = total liabilities + total equity", d["tl"] + d["te"], d["ta"])
out += ["", f"Failures: {fails}", ""]
out += ["## Ratios recomputed from the numbers (annual periods; ROE on closing equity)", "", "| Period | Loans/deposits | Cost-to-income | ROE (closing equity) | ROA (closing assets) | Net interest margin proxy (NII / closing assets) |", "| --- | --- | --- | --- | --- | --- |"]
for per, d in P.items():
    if not per.startswith("FY"):
        continue
    other = d["fv"] + d["oth_inc"]
    toi = d["nii"] + d["fee_i"] - d["fee_e"] + d["nti"] + other
    opex = d["staff"] + d["dep"] + d["amort_lease"] + d["othx"] + d["fin"]
    out.append(f"| {per} | {d['loans'] / d['dep_c'] * 100:.1f}% | {opex / toi * 100:.1f}% | {d['pat'] / d['te'] * 100:.1f}% | {d['pat'] / d['ta'] * 100:.1f}% | {d['nii'] / d['ta'] * 100:.1f}% |")
out += ["", "These are my recomputations, not bank-reported ratios."]
with open(os.path.join(HERE, "checks_history.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("rows:", len(rows), "| failures:", fails)
