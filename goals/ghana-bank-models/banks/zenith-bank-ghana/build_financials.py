#!/usr/bin/env python3
"""Build financials.csv and checks_history.md for Zenith Bank (Ghana) Ltd (bank-only). Standard library only.

Run:  python build_financials.py
Every number below was transcribed (GH¢'000, as printed) from the documents in sources.md and is converted to
GHS millions on output. Nothing is estimated. Rows that are sums of reported lines are marked 'derived' with the formula.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = "zenith-bank-ghana"
PERIODS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "9M-2025", "9M-2026"]
ANNUAL = PERIODS[:5]

# ---------------------------------------------------------------- source / page map
# (income statement source, page), (balance sheet source, page)
SRC = {
    "FY2021": (("ZEN-FY21", "20"), ("ZEN-FY21", "21")),
    "FY2022": (("ZEN-FY22", "22"), ("ZEN-FY23", "29")),   # FY2022 balance-sheet page was not in the transcription; comparative column of ZEN-FY23
    "FY2023": (("ZEN-FY23", "28"), ("ZEN-FY23", "29")),
    "FY2024": (("ZEN-FY24", "35"), ("ZEN-FY24", "36")),
    "FY2025": (("ZEN-FY25", "38"), ("ZEN-FY25", "39")),
    "9M-2025": (("ZEN-Q3-25", "1"), ("ZEN-Q3-25", "1")),  # unnumbered statement pages; same figures appear as the comparative column of ZEN-Q3-26
    "9M-2026": (("ZEN-Q3-26", "1"), ("ZEN-Q3-26", "1")),
}

# ---------------------------------------------------------------- income statement, GH¢'000, as printed
# keys: ii interest income, ie interest expense (positive), nii, fi fee income, fe fee expense (positive), nti net trading income,
#       fv net income on FV instruments, oi other income, opinc operating income, imp impairment (positive = charge, negative = reversal),
#       staff, da, ox other expenses, pbt, tax (positive = expense, negative = credit), pat
IS = {
    "FY2021": dict(ii=949052, ie=308074, nii=640978, fi=100690, fe=13119, nti=-84272, fv=-18918, oi=11825, opinc=637184, imp=27971, staff=129781, da=21639, ox=123589, pbt=334204, tax=114099, pat=220105),
    "FY2022": dict(ii=1061427, ie=343759, nii=717668, fi=176208, fe=20427, nti=156749, fv=4977, oi=13765, opinc=1048940, imp=1193674, staff=178405, da=26921, ox=204524, pbt=-554584, tax=-134814, pat=-419770),
    "FY2023": dict(ii=1378663, ie=364870, nii=1013793, fi=225006, fe=29459, nti=332656, fv=433, oi=53121, opinc=1595550, imp=109351, staff=211740, da=32379, ox=219692, pbt=1022388, tax=346288, pat=676100),
    "FY2024": dict(ii=1725210, ie=634300, nii=1090910, fi=335824, fe=56977, nti=377835, fv=0, oi=37025, opinc=1784617, imp=143122, staff=254768, da=50087, ox=275475, pbt=1061165, tax=609187, pat=451978),
    "FY2025": dict(ii=2651880, ie=1082833, nii=1569047, fi=466550, fe=65213, nti=309332, fv=42, oi=112926, opinc=2392684, imp=140376, staff=317448, da=67215, ox=342719, pbt=1524926, tax=527212, pat=997714),
    "9M-2025": dict(ii=1900038, ie=774661, nii=1125377, fi=340808, fe=48560, nti=214620, fv=13, oi=74344, opinc=1706602, imp=32691, staff=239876, da=50060, ox=251454, pbt=1132521, tax=275697, pat=856824),
    "9M-2026": dict(ii=1669340, ie=553772, nii=1115568, fi=414831, fe=48315, nti=222224, fv=-47, oi=113361, opinc=1817622, imp=-32418, staff=244586, da=54200, ox=264047, pbt=1287207, tax=229474, pat=1057733),
}
# Income statement of each year as printed in the NEXT year's report (comparative), for the cross-report check. Only lines that differ are listed.
IS_COMPARATIVE_DIFF = {
    "FY2023": ("ZEN-FY24", dict(ox=219691, pbt=1022389, pat=676101)),   # 1 thousand rounding differences
    "FY2024": ("ZEN-FY25", {}),
    "FY2022": ("ZEN-FY23", {}),
    "FY2021": ("ZEN-FY22", {}),
}

# ---------------------------------------------------------------- balance sheet, GH¢'000, as printed
# cash (cash and bank balances), trd (non-pledged + pledged trading assets), sec (investment securities net), oth_inv (investments other than securities),
# der_a derivative assets, ctr current tax receivable, loans (net), ppe, intg, rou, dta, oa other assets, ta total assets
# dep_b deposits from banks and NBFIs, dep_c customer deposits, bor borrowings, ol other liabilities, lease, dtl, der_l derivative liabilities, tl
# sc stated capital, sr statutory reserve, crr credit risk reserve, re retained earnings, te total equity
BS = {
    "FY2021": dict(cash=1714699, trd=106690 + 485037, sec=4488707, oth_inv=66942, der_a=0, ctr=10611, loans=1498900, ppe=168837, intg=8201, rou=96608, dta=25281, oa=193753, ta=8864266,
                   dep_b=19300, dep_c=6391081, bor=154536, ol=600476, lease=100505, dtl=12370, der_l=31861, tl=7310129, sc=400000, sr=444899, crr=19439, re=689799, te=1554137),
    "FY2022": dict(cash=2963202, trd=15271 + 1951, sec=3419839, oth_inv=400699, der_a=0, ctr=11799, loans=1856211, ppe=187232, intg=9917, rou=94671, dta=325018, oa=373761, ta=9659571,
                   dep_b=17907, dep_c=8408201, bor=0, ol=124712, lease=108678, dtl=16089, der_l=1617, tl=8677204, sc=400000, sr=444899, crr=9704, re=127764, te=982367),
    "FY2023": dict(cash=4175590, trd=0, sec=5845900, oth_inv=252161, der_a=433, ctr=220608, loans=2246982, ppe=254352, intg=14073, rou=96479, dta=113421, oa=643500, ta=13863499,
                   dep_b=39247, dep_c=11702523, bor=170422, ol=155070, lease=119108, dtl=18661, der_l=0, tl=12205031, sc=400000, sr=529411, crr=0, re=729057, te=1658468),
    "FY2024": dict(cash=6611429, trd=0, sec=6174183, oth_inv=1212418, der_a=66791, ctr=64961, loans=3414019, ppe=249441, intg=28158, rou=92446, dta=26524, oa=1186763, ta=19127133,
                   dep_b=118976, dep_c=15630343, bor=952693, ol=240813, lease=111182, dtl=20854, der_l=0, tl=17074861, sc=1000000, sr=642405, crr=0, re=409867, te=2052272),
    "FY2025": dict(cash=7834422, trd=4148, sec=9146925, oth_inv=333996, der_a=24979, ctr=10849, loans=7210226, ppe=295797, intg=25355, rou=83809, dta=59877, oa=1672437, ta=26702820,
                   dep_b=147019, dep_c=20825728, bor=2132000, ol=412564, lease=107121, dtl=28402, der_l=0, tl=23652834, sc=1000000, sr=891834, crr=76140, re=1082012, te=3049986),
    # interim balance sheets print no right-of-use or lease lines (inside other lines); no derivative liabilities line
    "9M-2025": dict(cash=6456981, trd=5334, sec=9006394, oth_inv=1361263, der_a=13342, ctr=64961, loans=6079176, ppe=369299, intg=25057, rou=0, dta=26524, oa=632472, ta=24040803,
                    dep_b=124887, dep_c=18433230, bor=2187414, ol=365322, lease=0, dtl=20854, der_l=0, tl=21131707, sc=1000000, sr=642405, crr=0, re=1266691, te=2909096),
    "9M-2026": dict(cash=9519155, trd=15319, sec=8994067, oth_inv=117449, der_a=638, ctr=0, loans=9455377, ppe=418729, intg=16001, rou=0, dta=59877, oa=3394985, ta=31991597,
                    dep_b=144454, dep_c=25952603, bor=1345443, ol=412976, lease=0, dtl=28402, der_l=0, tl=27883878, sc=1000000, sr=891834, crr=177650, re=2038235, te=4107719),
}

# ---------------------------------------------------------------- notes and ratios (annual only unless stated), GH¢'000
LOANS = {  # gross (stage totals, before the allowance; written-off line excluded), allowance, stage 3 gross, stage 3 allowance, stage 2 gross
    "FY2021": dict(gross=1570493, allow=71593, s3=69071, s3a=42279 + 29314, s2=27228, page="84; 50-53"),
    "FY2022": dict(gross=1946036, allow=89825, s3=73854, s3a=40373, s2=120705, page="83-84; 53-54"),
    "FY2023": dict(gross=2336239, allow=89257, s3=15069, s3a=14886, s2=21392, page="58-61"),
    "FY2024": dict(gross=3475592, allow=61573, s3=58386, s3a=3017, s2=103, page="67-71"),
    "FY2025": dict(gross=7415927, allow=205701, s3=629804, s3a=84880, s2=273636, page="67-70"),
}
LOANS_SRC = {"FY2021": "ZEN-FY21", "FY2022": "ZEN-FY22", "FY2023": "ZEN-FY23", "FY2024": "ZEN-FY24", "FY2025": "ZEN-FY25"}
SEC = {  # investment securities gross, impairment (note), page
    "FY2021": (4494665, 5958, "83"), "FY2022": (4583273, 1163434, "82"), "FY2023": (6140288, 294388, "62"),
    "FY2024": (6174183, 0, "72"), "FY2025": (9146936, 11, "72"),
}
NOTE11 = {  # impairment charge by component (note 11), positive = charge: loans, off-balance sheet, securities, placements, written off, Eurobond haircut write-off
    "FY2021": dict(loans=35877, obs=-2251, sec=-6642, plc=-510, wo=1497, euro=0, page="78"),
    "FY2022": dict(loans=18444, obs=12399, sec=1157476, plc=0, wo=5355, euro=0, page="77"),
    "FY2024": dict(loans=-7953, obs=-18940, sec=18000, plc=0, wo=828, euro=151187, page="95"),
    "FY2025": dict(loans=144648, obs=-6598, sec=11, plc=0, wo=2315, euro=0, page="95"),
}
CASH_NOTE = {  # Bank of Ghana balances, balances with banks (as printed in the cash note), page
    "FY2021": (840417, 1371 + 491466 + 107549, "81"), "FY2022": (1621225, 59550 + 905885 + 148854, "80-81"),
    "FY2023": (2995933, 894557, "57"), "FY2024": (5195473, 1064266, "80"), "FY2025": (6314674, 1069025, "80"),
}
CAP = {  # CAR %, RWA, page
    "FY2021": (45.09, 3339214, "67-68"), "FY2022": (36.0, 4188858, "69-71"), "FY2023": (29.0, 6492583, "77"),
    "FY2024": (24.14, 9017179, "86-87"), "FY2025": (20.40, 14062231, "88"),
}
NPL_REPORTED = {"FY2021": (4.40, "54"), "FY2022": (3.80, "59"), "FY2023": (1.0, "65"), "FY2024": (1.0, "74"), "FY2025": (8.49, "74")}
INTERIM_RATIOS = {  # CAR, CET1, NPL, loan loss provision, liquid ratio
    "9M-2025": dict(car=21.55, cet1=18.55, npl=0.89, llp=1.50, liq=108.42),
    "9M-2026": dict(car=17.79, cet1=15.79, npl=8.91, llp=1.77, liq=92.92),
}
FIN_LEVIES = {"FY2024": 106116, "FY2025": 152493}   # Note 15(a): Financial Sector Recovery Levy & Growth and Sustainability levy charge (current-tax column)
NOT_RECOGNISED = {"FY2021": 4334, "FY2022": 6111}   # interest on impaired loans not recognised (note on interest income)

rows = []


def M(x):
    return f"{x / 1000:.3f}"


def add(period, stmt, item, val, src, page, status, notes="", unit="GHS millions"):
    v = "" if val is None else (val if isinstance(val, str) else M(val))
    rows.append([BANK, period, stmt, item, v, unit, src, page, status, notes])


def pct(period, item, val, src, page, status, notes=""):
    rows.append([BANK, period, "ratios", item, f"{val:.2f}", "percent", src, page, status, notes])


BASIS = "Bank-only (the bank has no subsidiaries)."
for p in PERIODS:
    (isrc, ipg), (bsrc, bpg) = SRC[p]
    d = IS[p]
    add(p, "income_statement", "interest_income", d["ii"], isrc, ipg, "reported", BASIS)
    add(p, "income_statement", "interest_expense", d["ie"], isrc, ipg, "reported", "Printed in brackets (an expense); stored positive.")
    add(p, "income_statement", "net_interest_income", d["nii"], isrc, ipg, "reported")
    add(p, "income_statement", "fee_commission_income", d["fi"], isrc, ipg, "reported")
    add(p, "income_statement", "fee_commission_expense", d["fe"], isrc, ipg, "reported", "Stored positive.")
    add(p, "income_statement", "net_trading_income", d["nti"], isrc, ipg, "reported", "Printed line 'Net trading income'." + (" Negative in FY2021." if p == "FY2021" else ""))
    add(p, "income_statement", "other_operating_income", d["fv"] + d["oi"], isrc, ipg, "derived",
        f"Net income on financial instruments at fair value ({M(d['fv'])}) + other income ({M(d['oi'])}).")
    add(p, "income_statement", "total_operating_income", d["opinc"], isrc, ipg, "reported", "Printed 'Operating income' (after net interest, net fees, trading and other income; before impairment).")
    add(p, "income_statement", "staff_costs", d["staff"], isrc, ipg, "reported", "Stored positive.")
    add(p, "income_statement", "depreciation_amortisation", d["da"], isrc, ipg, "reported", "Stored positive.")
    add(p, "income_statement", "other_operating_expenses", d["ox"], isrc, ipg, "reported", "Printed 'Other expenses'. Includes deposit-protection premium." + (" FY2024 comparative in ZEN-FY24 prints 219.691 (rounding)." if p == "FY2023" else ""))
    imp_note = "Impairment loss on financial assets, positive = charge."
    if p == "FY2022":
        imp_note += " Includes 1,157.476m on investment securities (Note 11), the domestic debt exchange effect."
    if p == "FY2024":
        imp_note += " Includes a 151.187m Eurobond haircut write-off (Note 11)."
    if p == "9M-2026":
        imp_note = "Net reversal (credit) of 32.418m, printed as a positive figure in a column where costs are in brackets; confirmed by the PBT identity. Stored negative = reversal."
    add(p, "income_statement", "impairment_charge", d["imp"], isrc, ipg, "reported", imp_note)
    add(p, "income_statement", "profit_before_tax", d["pbt"], isrc, ipg, "reported", "Loss in FY2022." if p == "FY2022" else "")
    tax_note = "Includes Growth and Sustainability Levy and Financial Sector Recovery Levy (5% each of PBT in FY2024 and FY2025, Note 15(b))."
    if p == "FY2022":
        tax_note = "Tax CREDIT of 134.814m (current 161.204m less deferred credit 296.018m); stored negative."
    if p == "FY2024":
        tax_note += " Effective rate 57.4% because of a 229.186m 'change in prior year estimate' after a GRA audit (Note 15(b))."
    add(p, "income_statement", "income_tax", d["tax"], isrc, ipg, "reported", tax_note)
    add(p, "income_statement", "profit_after_tax", d["pat"], isrc, ipg, "reported", "Loss in FY2022." if p == "FY2022" else "")

    b = BS[p]
    bs_note = "Comparative column of ZEN-FY23 (the FY2022 balance-sheet page was not in the transcription of ZEN-FY22)." if p == "FY2022" else ""
    add(p, "balance_sheet", "cash_and_bog_balances", b["cash"], bsrc, bpg, "reported",
        "Printed line 'Cash and bank balances': includes cash on hand, Bank of Ghana balances (incl. mandatory reserve), balances with other banks and items in course of collection. Not split here so every period uses one definition; see x_ rows. " + bs_note)
    add(p, "balance_sheet", "due_from_banks", b["oth_inv"], bsrc, bpg, "reported",
        "Printed line 'Investments (other than securities)'. INFERRED to be interbank/money-market placements because Note 11 reports 'Interbank placements' impairment on this balance; Note 20 text not read. Balances with banks sit inside cash_and_bog_balances.")
    add(p, "balance_sheet", "investment_securities", b["sec"] + b["trd"], bsrc, bpg, "derived",
        f"Investment securities (net) {M(b['sec'])} + non-pledged and pledged trading assets {M(b['trd'])}.")
    if p in ANNUAL:
        L = LOANS[p]
        add(p, "balance_sheet", "loans_and_advances_gross", L["gross"], LOANS_SRC[p], L["page"].split(";")[0], "reported", "Sum of IFRS 9 stages 1-3 gross (risk note); the loan note's separate 'loans written off' line is excluded.")
        add(p, "balance_sheet", "loan_loss_allowance", L["allow"], LOANS_SRC[p], L["page"].split(";")[0], "reported", "Allowance for impairment, positive balance.")
    else:
        add(p, "balance_sheet", "loans_and_advances_gross", None, bsrc, bpg, "unavailable", "Interim statements print net loans only.")
        add(p, "balance_sheet", "loan_loss_allowance", None, bsrc, bpg, "unavailable", "Interim statements print net loans only.")
    add(p, "balance_sheet", "loans_and_advances_net", b["loans"], bsrc, bpg, "reported", bs_note)
    add(p, "balance_sheet", "property_equipment_intangibles", b["ppe"] + b["intg"] + b["rou"], bsrc, bpg, "derived",
        f"Property and equipment {M(b['ppe'])} + intangible assets {M(b['intg'])} + right-of-use assets {M(b['rou'])}" + (" (interim statements print no separate right-of-use line)." if p.startswith("9M") else "."))
    other_assets = b["oa"] + b["der_a"] + b["ctr"] + b["dta"]
    add(p, "balance_sheet", "other_assets", other_assets, bsrc, bpg, "derived",
        f"Other assets {M(b['oa'])} + derivative assets {M(b['der_a'])} + current tax receivable {M(b['ctr'])} + deferred tax assets {M(b['dta'])}.")
    add(p, "balance_sheet", "total_assets", b["ta"], bsrc, bpg, "reported", bs_note)
    add(p, "balance_sheet", "customer_deposits", b["dep_c"], bsrc, bpg, "reported", bs_note)
    add(p, "balance_sheet", "due_to_banks", b["dep_b"], bsrc, bpg, "reported", "Printed 'Deposits from banks and non-bank financial institutions'.")
    add(p, "balance_sheet", "borrowings", b["bor"], bsrc, bpg, "reported", "None reported at FY2022." if b["bor"] == 0 and p == "FY2022" else "")
    other_liab = b["ol"] + b["lease"] + b["dtl"] + b["der_l"]
    add(p, "balance_sheet", "other_liabilities", other_liab, bsrc, bpg, "derived",
        f"Other liabilities {M(b['ol'])} + lease liabilities {M(b['lease'])} + deferred tax liabilities {M(b['dtl'])} + derivative liabilities {M(b['der_l'])}.")
    add(p, "balance_sheet", "total_liabilities", b["tl"], bsrc, bpg, "reported", bs_note)
    add(p, "balance_sheet", "stated_capital", b["sc"], bsrc, bpg, "reported", "Raised from 400m to 1,000m in FY2024 (bonus issue from retained earnings, inferred from the retained-earnings roll-forward)." if p == "FY2024" else "")
    add(p, "balance_sheet", "retained_earnings", b["re"], bsrc, bpg, "reported")
    add(p, "balance_sheet", "reserves_other", b["sr"] + b["crr"], bsrc, bpg, "derived", f"Statutory reserve {M(b['sr'])} + credit risk reserve {M(b['crr'])}.")
    add(p, "balance_sheet", "total_equity", b["te"], bsrc, bpg, "reported", bs_note)

# ---- annual notes: extra x_ rows
for p in ANNUAL:
    L = LOANS[p]
    ls = LOANS_SRC[p]
    pg = L["page"].split(";")[0]
    add(p, "balance_sheet", "x_loans_stage3_gross", L["s3"], ls, pg, "reported", "IFRS 9 stage 3 (credit-impaired) gross loans.")
    add(p, "balance_sheet", "x_loans_stage3_allowance", L["s3a"], ls, pg, "reported", "Stage 3 allowance" + (" (individual 42.279m + collective 29.314m)." if p == "FY2021" else "."))
    add(p, "balance_sheet", "x_loans_stage2_gross", L["s2"], ls, pg, "reported", "IFRS 9 stage 2 gross loans.")
    g, ia, pgs = SEC[p]
    add(p, "balance_sheet", "x_investment_securities_gross", g, ls, pgs, "reported", "Gross before impairment (note on investment securities).")
    add(p, "balance_sheet", "x_investment_securities_impairment", ia, ls, pgs, "reported", "Impairment allowance on investment securities, positive balance." + (" Domestic debt exchange: eligible bonds treated as credit-impaired." if p == "FY2022" else ""))
    bog, banks, cpg = CASH_NOTE[p]
    add(p, "balance_sheet", "x_cash_bog_balances", bog, ls, cpg, "reported", "Balances with the Bank of Ghana (cash note), including the mandatory reserve.")
    add(p, "balance_sheet", "x_cash_balances_with_banks", banks, ls, cpg, "reported" if p in ("FY2023", "FY2024", "FY2025") else "derived",
        "Balances with banks as printed." if p in ("FY2023", "FY2024", "FY2025") else "Balances with other local banks + other foreign banks + items in course of collection (sum of cash-note lines).")
    car, rwa, kpg = CAP[p]
    pct(p, "car_pct", car, ls, kpg, "reported", "Printed with no decimals ('36%' / '29%')." if p in ("FY2022", "FY2023") else "")
    add(p, "ratios", "x_risk_weighted_assets", rwa, ls, kpg, "reported", "Total risk-weighted assets.")
    npl, npg = NPL_REPORTED[p]
    pct(p, "npl_pct", npl, ls, npg, "reported",
        "Individually impaired gross NPLs to total gross loans. " + (f"Printed as '1%' (rounded); stage 3 / gross is {L['s3'] / L['gross'] * 100:.2f}% (see x_npl_stage3_to_gross_pct)." if p in ("FY2023", "FY2024") else ""))
    pct(p, "x_npl_stage3_to_gross_pct", L["s3"] / L["gross"] * 100, ls, pg, "derived", "x_loans_stage3_gross / loans_and_advances_gross.")
    pct(p, "ldr_pct", BS[p]["loans"] / BS[p]["dep_c"] * 100, SRC[p][1][0], SRC[p][1][1], "derived", "loans_and_advances_net / customer_deposits (the bank does not print a loan-to-deposit ratio in the text read).")
for p, d in NOTE11.items():
    s = LOANS_SRC[p]
    items = [("x_impairment_loans_and_advances", d["loans"]), ("x_impairment_off_balance_sheet", d["obs"]), ("x_impairment_investment_securities", d["sec"]),
             ("x_impairment_interbank_placements", d["plc"]), ("x_impairment_loans_written_off", d["wo"]), ("x_impairment_eurobond_haircut_writeoff", d["euro"])]
    for k, v in items:
        if k in ("x_impairment_interbank_placements", "x_impairment_eurobond_haircut_writeoff") and v == 0 and p in ("FY2022", "FY2025"):
            continue
        add(p, "income_statement", k, v, s, d["page"], "reported", "Note 11 component of impairment_charge; positive = charge, negative = release.")
for p in (2024, 2025):
    pp = f"FY{p}"
    add(pp, "income_statement", "x_financial_sector_levies_current", FIN_LEVIES[pp], "ZEN-FY25", "97", "reported",
        "Financial Sector Recovery Levy and Growth and Sustainability Levy charge for the year (Note 15(a)); included in income_tax.")
for pp, v in NOT_RECOGNISED.items():
    add(pp, "income_statement", "x_interest_not_recognised_impaired_loans", v, LOANS_SRC[pp], "77-78", "reported", "Interest on impaired loans not recognised; the bank calls it immaterial. This is the closest disclosure to interest in suspense.")
for pp in ("FY2023", "FY2024", "FY2025"):
    add(pp, "balance_sheet", "x_interest_in_suspense", None, LOANS_SRC[pp], "", "unavailable", "No interest-in-suspense figure found in the notes read.")

# ---- equity roll-forward (derived): other movements and dividends
EQ = {}
order = ANNUAL
open_te = 1456794  # FY2020 closing equity (ZEN-FY21 p.21 comparative)
for p in order:
    close = BS[p]["te"]
    other = close - (open_te + IS[p]["pat"])
    EQ[p] = (open_te, other)
    open_te = close
EQ["9M-2025"] = (BS["FY2024"]["te"], BS["9M-2025"]["te"] - (BS["FY2024"]["te"] + IS["9M-2025"]["pat"]))
EQ["9M-2026"] = (BS["FY2025"]["te"], BS["9M-2026"]["te"] - (BS["FY2025"]["te"] + IS["9M-2026"]["pat"]))
for p in PERIODS:
    o, other = EQ[p]
    src = SRC[p][1][0]
    add(p, "income_statement", "x_other_equity_movement", other, src, SRC[p][1][1], "derived",
        "Closing equity - (opening equity + profit after tax). Negative = outflow (dividend or other transfer out of equity)."
        + {"FY2021": " Likely the FY2020 dividend; not verified.", "FY2022": " Equals the GH¢152.0m dividend shown in the bank's own 9M-2022 statement.",
           "FY2024": " Equals the (58.174)m 'other transfers' in the statement of changes in equity (seen in the 9M-2024 report); not a dividend (directors: nil).",
           "FY2025": " Directors do not recommend a dividend for FY2025; roll-forward confirms no outflow.",
           "9M-2026": " No dividend paid in 9M-2026 (roll-forward exact)."}.get(p, ""))

for p, r in INTERIM_RATIOS.items():
    sc = SRC[p][1][0]
    pct(p, "car_pct", r["car"], sc, "1", "reported", "Regulatory disclosures table. Column orientation proven in checks_history.md.")
    pct(p, "tier1_pct", r["cet1"], sc, "1", "reported", "Printed as 'Common Equity Tier 1 Ratio'.")
    pct(p, "npl_pct", r["npl"], sc, "1", "reported", "Printed 'Non-performing loans to gross loans'.")
    pct(p, "x_loan_loss_provision_pct", r["llp"], sc, "1", "reported", "Printed 'Loan loss provision' ratio.")
    pct(p, "x_liquid_ratio_pct", r["liq"], sc, "1", "reported", "Printed 'Liquid Ratio'.")
    pct(p, "ldr_pct", BS[p]["loans"] / BS[p]["dep_c"] * 100, sc, "1", "derived", "loans_and_advances_net / customer_deposits.")

# ---------------------------------------------------------------- write financials.csv
with open(os.path.join(HERE, "financials.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bank", "period", "statement", "line_item", "value", "unit", "source_id", "page", "status", "notes"])
    w.writerows(rows)

# ---------------------------------------------------------------- checks
out = ["# History checks: zenith-bank-ghana", "", "Generated by build_financials.py from the same numbers that are written to financials.csv. All differences in GH¢'000 unless stated.", ""]
fails = 0


def chk(label, a, b, tol=1):
    global fails
    ok = abs(a - b) <= tol
    fails += 0 if ok else 1
    return f"| {label} | {a:,} | {b:,} | {a - b:+,} | {'PASS' if ok else 'FAIL'} |"


out += ["## 1. Income statement identities", "", "| Check | Computed | Printed | Diff | Result |", "| --- | --- | --- | --- | --- |"]
for p in PERIODS:
    d = IS[p]
    out.append(chk(f"{p} NII = II - IE", d["ii"] - d["ie"], d["nii"], 0))
    out.append(chk(f"{p} operating income = NII + (fee inc - fee exp) + trading + FV + other", d["nii"] + d["fi"] - d["fe"] + d["nti"] + d["fv"] + d["oi"], d["opinc"], 0))
    out.append(chk(f"{p} PBT = op income - impairment - staff - D&A - other", d["opinc"] - d["imp"] - d["staff"] - d["da"] - d["ox"], d["pbt"], 0))
    out.append(chk(f"{p} PAT = PBT - tax", d["pbt"] - d["tax"], d["pat"], 0))
out += ["", "## 2. Balance sheet identities", "", "| Check | Computed | Printed | Diff | Result |", "| --- | --- | --- | --- | --- |"]
for p in PERIODS:
    b = BS[p]
    out.append(chk(f"{p} sum of asset lines = total assets", b["cash"] + b["trd"] + b["sec"] + b["oth_inv"] + b["der_a"] + b["ctr"] + b["loans"] + b["ppe"] + b["intg"] + b["rou"] + b["dta"] + b["oa"], b["ta"], 0))
    out.append(chk(f"{p} sum of liability lines = total liabilities", b["dep_b"] + b["dep_c"] + b["bor"] + b["ol"] + b["lease"] + b["dtl"] + b["der_l"], b["tl"], 0))
    out.append(chk(f"{p} sum of equity lines = total equity", b["sc"] + b["sr"] + b["crr"] + b["re"], b["te"], 0))
    out.append(chk(f"{p} total assets = total liabilities + total equity", b["tl"] + b["te"], b["ta"], 0))
out += ["", "## 3. Loan note", "", "| Check | Computed | Printed | Diff | Result |", "| --- | --- | --- | --- | --- |"]
for p in ANNUAL:
    L = LOANS[p]
    out.append(chk(f"{p} gross - allowance = net loans on the balance sheet", L["gross"] - L["allow"], BS[p]["loans"], 0))
for p in ANNUAL:
    g, ia, _ = SEC[p]
    out.append(chk(f"{p} securities gross - impairment = net on the balance sheet", g - ia, BS[p]["sec"], 0))
out += ["", "## 4. Note 11 impairment components sum to the income-statement charge", "", "| Check | Computed | Printed | Diff | Result |", "| --- | --- | --- | --- | --- |"]
for p, d in NOTE11.items():
    out.append(chk(f"{p} sum of note 11 components = impairment_charge", d["loans"] + d["obs"] + d["sec"] + d["plc"] + d["wo"] + d["euro"], IS[p]["imp"], 0))
out += ["", "## 5. Same figure in two consecutive reports (current report vs next year's comparative column)", "",
        "Lines that are identical in both reports are not listed; they pass by construction of the table below. Differences are shown.", "",
        "| Period | Comparative source | Lines that differ | Result |", "| --- | --- | --- | --- |"]
for p, (cs, diff) in IS_COMPARATIVE_DIFF.items():
    if diff:
        txt = "; ".join(f"{k}: {IS[p][k]:,} vs {v:,}" for k, v in diff.items())
        ok = all(abs(IS[p][k] - v) <= 1 for k, v in diff.items())
        fails += 0 if ok else 1
        out.append(f"| {p} | {cs} | {txt} | {'PASS (1 thousand rounding)' if ok else 'FAIL'} |")
    else:
        out.append(f"| {p} | {cs} | none (all income-statement lines identical) | PASS |")
out += ["", "Balance-sheet totals FY2023 (ZEN-FY23 vs ZEN-FY24 comparative) and FY2024 (ZEN-FY24 vs ZEN-FY25 comparative) were identical as transcribed: total assets 13,863,499 and 19,127,133, total equity 1,658,468 and 2,052,272. The FY2022 balance sheet comes from the ZEN-FY23 comparative only, so it has no second source.", ""]
out += ["## 6. Equity roll-forward (opening equity + profit after tax vs closing equity)", "", "| Period | Opening | + PAT | Closing printed | Other movement (closing - opening - PAT) |", "| --- | --- | --- | --- | --- |"]
for p in PERIODS:
    o, other = EQ[p]
    out.append(f"| {p} | {o:,} | {IS[p]['pat']:,} | {BS[p]['te']:,} | {other:,} |")
out += ["", "FY2021 opening is FY2020 closing equity 1,456,794 (ZEN-FY21 p.21 comparative). Zero movements in FY2023, FY2025 and 9M-2026 mean no dividends or transfers out of equity in those periods.", ""]
o25, oth25 = EQ["9M-2025"]
o26, oth26 = EQ["9M-2026"]
out += ["## 7. Interim column orientation (the check that caught the transcription error)", "",
        "The fetch tool labelled the current-period column of ZEN-Q3-25 and ZEN-Q3-26 as the comparative. Proof of the orientation used in financials.csv:", "",
        f"- 9M-2025 equity {BS['9M-2025']['te']:,} = FY2024 equity {BS['FY2024']['te']:,} + 9M-2025 PAT {IS['9M-2025']['pat']:,} (other movement {oth25:,}).",
        f"- 9M-2026 equity {BS['9M-2026']['te']:,} = FY2025 equity {BS['FY2025']['te']:,} + 9M-2026 PAT {IS['9M-2026']['pat']:,} (other movement {oth26:,}).",
        f"- Retained earnings 9M-2026: FY2025 {BS['FY2025']['re']:,} + PAT {IS['9M-2026']['pat']:,} - credit risk reserve transfer {BS['9M-2026']['crr'] - BS['FY2025']['crr']:,} = {BS['FY2025']['re'] + IS['9M-2026']['pat'] - (BS['9M-2026']['crr'] - BS['FY2025']['crr']):,} (printed {BS['9M-2026']['re']:,}).",
        "- The wrong orientation would give 9M-2026 equity of 2,909,096, which is below the audited FY2025 closing equity of 3,049,986 even though the bank was profitable, so it is impossible.",
        "- Tax and statutory-reserve rows in the 9M-2025 column equal the FY2024 values and in the 9M-2026 column equal the FY2025 values (interim statements carry them forward), which also fixes the order.",
        "- 9M-2024 (ZEN-Q3-24 search snippet): PBT 881,953 and total equity and liabilities 19,174,160 sit in the comparative column of ZEN-Q3-25, so ZEN-Q3-25's current column is 9M-2025.",
        "- Supporting only (not proof): NPL ratio continuity. FY2025 audited 8.49% (stage 3 / gross 629,804 / 7,415,927) sits next to 9M-2026 8.91%, while the other orientation would put 0.89% at 9M-2026, a collapse from 8.49% in nine months that the loan book growth does not suggest.", ""]
fails += 0 if EQ["9M-2026"][1] == 0 else 1
out += ["## 8. Printed ratios vs recomputation (from the numbers above)", "", "| Period | CAR printed | NPL printed | NPL stage3/gross | Net loans / deposits | ROE on average equity | ROA on average assets | Cost-to-income |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
prev_b = None
for p in ANNUAL:
    d = IS[p]
    b = BS[p]
    ave = (b["te"] + (EQ[p][0])) / 2
    prev_ta = {"FY2021": 8034580}.get(p) or BS[ANNUAL[ANNUAL.index(p) - 1]]["ta"]
    ava = (b["ta"] + prev_ta) / 2
    cti = (d["staff"] + d["da"] + d["ox"]) / d["opinc"] * 100
    out.append(f"| {p} | {CAP[p][0]:.2f}% | {NPL_REPORTED[p][0]:.2f}% | {LOANS[p]['s3'] / LOANS[p]['gross'] * 100:.2f}% | {b['loans'] / b['dep_c'] * 100:.1f}% | {d['pat'] / ave * 100:.1f}% | {d['pat'] / ava * 100:.2f}% | {cti:.1f}% |")
out += ["", "The bank prints no ROE, ROA or cost-to-income in the text read, so there is nothing to compare these with; they are shown for context. FY2020 total assets 8,034,580 (ZEN-FY21 p.21 comparative) used for FY2021 average assets.", ""]
out += ["## Summary", "", f"Failures: {fails}", ""]
with open(os.path.join(HERE, "checks_history.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("rows:", len(rows), "| history check failures:", fails)
