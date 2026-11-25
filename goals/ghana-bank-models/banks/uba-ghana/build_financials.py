#!/usr/bin/env python3
"""Build financials.csv and checks_history.md for United Bank for Africa (Ghana) Ltd (bank-only). Standard library only.

Run:  python build_financials.py
Every figure below was transcribed from the documents listed in sources.md. Annual statements are printed in whole Ghana cedis,
the interim statements in thousands of cedis; everything is converted to GHS millions on output. Nothing is estimated. Rows that
combine reported lines are marked 'derived' with the formula in notes.
Statement pages: the statement PDFs (FS) carry no printed page numbers in the text layer I could read, so their rows use the
statement name (SoCI, SoFP) as the page. Annual-report (AR) rows carry the printed page of the note.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = "uba-ghana"
ANNUAL = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
PERIODS = ANNUAL + ["9M-2025", "9M-2026"]
INTERIM = {"9M-2025", "9M-2026"}

SRC = {  # period -> source id for the primary statements
    "FY2021": "UBA22FS", "FY2022": "UBA22FS", "FY2023": "UBA23FS", "FY2024": "UBA24FS", "FY2025": "UBA25FS",
    "9M-2025": "UBA26Q3", "9M-2026": "UBA26Q3",
}

# ------------------------------------------------------------------ income statement (whole cedis; interim GHS'000), costs positive
# ii interest income, ie interest expense, nii, fi fee income, fe fee expense, nti net trading and revaluation income, oi other operating income,
# opinc net operating income (before impairment), imp allowance for credit losses on financial assets (positive = charge, negative = reversal),
# staff employee benefit expenses, da depreciation and amortisation, ox other operating expenses, pbt, tax, pat
IS = {
    "FY2021": dict(ii=506884566, ie=169547713, nii=337336853, fi=72937435, fe=18737068, nti=56982072, oi=931237, opinc=449450529, imp=95265683,
                   staff=65856828, da=11783794, ox=57730110, pbt=218814114, tax=77049377, pat=141764737),
    "FY2022": dict(ii=798611363, ie=261788406, nii=536822957, fi=75371769, fe=27551209, nti=97278555, oi=127895, opinc=682049967, imp=406630830,
                   staff=80753856, da=12590329, ox=90863133, pbt=91211819, tax=31617645, pat=59594174),
    "FY2023": dict(ii=1085374127, ie=310694532, nii=774679595, fi=93222993, fe=48134177, nti=84993942, oi=59936, opinc=904822289, imp=384075804,
                   staff=98839105, da=15448805, ox=130488201, pbt=275970374, tax=100127745, pat=175842629),
    "FY2024": dict(ii=1036453639, ie=438960110, nii=597493529, fi=168593873, fe=143421639, nti=68520782, oi=1222019, opinc=692408564, imp=180110176,
                   staff=114614924, da=16083359, ox=128017161, pbt=253582944, tax=89270965, pat=164311979),
    "FY2025": dict(ii=1125252471, ie=454948946, nii=670303525, fi=231804273, fe=153414223, nti=98759427, oi=482305, opinc=847935307, imp=-118985497,
                   staff=175503185, da=34744922, ox=126741256, pbt=629931441, tax=222827837, pat=407103604),
    "9M-2025": dict(ii=818197, ie=331750, nii=486447, fi=179081, fe=117085, nti=88103, oi=9, opinc=636555, imp=-54899,
                    staff=118415, da=22262, ox=120050, pbt=430727, tax=149489, pat=281238),
    "9M-2026": dict(ii=658248, ie=253623, nii=404625, fi=169451, fe=88513, nti=90114, oi=89, opinc=575766, imp=-47146,
                    staff=177038, da=11080, ox=98001, pbt=336793, tax=138950, pat=197843),
}

# ------------------------------------------------------------------ balance sheet
# cash cash and bank balances (includes balances with other banks); sec_ac / sec_fv investment securities at amortised cost / at FVOCI;
# loans net loans; oa other assets; ppe property and equipment; intg intangibles; ita income tax asset; dta deferred tax asset; ta total assets
# dep_c customer deposits; dep_b deposits from banks; bor borrowings; ol other liabilities; tl total liabilities
# sc stated capital; re retained earnings; fvr fair value reserve; crr credit risk reserve; sr statutory reserve; te total equity
BS = {
    "FY2021": dict(cash=1040251267, sec_ac=2717849080, sec_fv=64191145, loans=1032519321, oa=431298690, ppe=63388093, intg=1656104, ita=8594131, dta=13452036, ta=5373199867,
                   dep_c=4075498353, dep_b=59049587, bor=0, ol=105970684, tl=4240518624, sc=400000000, re=395669959, fvr=13612, crr=0, sr=336997672, te=1132681243),
    "FY2022": dict(cash=1855756294, sec_ac=2438908925, sec_fv=0, loans=1544688879, oa=176096466, ppe=72339376, intg=2051086, ita=30416193, dta=89804574, ta=6210061793,
                   dep_c=4736251611, dep_b=72940071, bor=0, ol=209603917, tl=5018795599, sc=400000000, re=439369978, fvr=0, crr=0, sr=351896216, te=1191266194),
    "FY2023": dict(cash=2615910993, sec_ac=3710843000, sec_fv=0, loans=1142142783, oa=162012449, ppe=73580706, intg=1863627, ita=34867378, dta=180204585, ta=7921425521,
                   dep_c=6338451000, dep_b=0, bor=0, ol=215865698, tl=6554316698, sc=400000000, re=486387853, fvr=0, crr=84864097, sr=395856873, te=1367108823),
    "FY2024": dict(cash=3752966689, sec_ac=4314251459, sec_fv=0, loans=1114365528, oa=256165210, ppe=115872666, intg=1702111, ita=46141650, dta=246370771, ta=9847836084,
                   dep_c=7285042974, dep_b=22872886, bor=785298475, ol=263200947, tl=8356415282, sc=400000000, re=654485934, fvr=0, crr=0, sr=436934868, te=1491420802),
    "FY2025": dict(cash=2907805813, sec_ac=6097113193, sec_fv=279624789, loans=1277049857, oa=594437094, ppe=118530458, intg=1856890, ita=56837091, dta=208313299, ta=11541568484,
                   dep_c=8590385384, dep_b=0, bor=807761561, ol=247676771, tl=9645823716, sc=400000000, re=994971587, fvr=12950362, crr=0, sr=487822819, te=1895744768),
    "9M-2025": dict(cash=3343804, sec_ac=6047141, sec_fv=0, loans=844994, oa=696700, ppe=104940, intg=1658, ita=28446, dta=246371, ta=11314054,
                    dep_c=8194116, dep_b=65739, bor=780449, ol=516821, tl=9557125, sc=400000, re=919994, fvr=0, crr=0, sr=436935, te=1756929),
    "9M-2026": dict(cash=2776062, sec_ac=7049417, sec_fv=106988, loans=1692697, oa=350300, ppe=320257, intg=1679, ita=54130, dta=207551, ta=12559081,
                    dep_c=8684740, dep_b=19925, bor=1690643, ol=372759, tl=10768067, sc=400000, re=887955, fvr=15236, crr=0, sr=487823, te=1791014),
}

# ------------------------------------------------------------------ loan notes (whole cedis): gross, allowance, stage gross
LOANS = {
    "FY2021": dict(gross=1135144224, allow=102624903, s1=801806334, s2=0, s3=333337890, src="UBA22AR", page="96"),
    "FY2022": dict(gross=1716210478, allow=171521599, s1=1445829967, s2=104682380, s3=165698131, src="UBA22AR", page="96"),
    "FY2023": dict(gross=1360046776, allow=217903993, s1=875272868, s2=149397394, s3=335376514, src="UBA24AR", page="135"),
    "FY2024": dict(gross=1316921454, allow=202555926, s1=1005512319, s2=146416526, s3=164992609, src="UBA25AR", page="137"),
    "FY2025": dict(gross=1339841064, allow=62791207, s1=1248370744, s2=63177410, s3=28292910, src="UBA25AR", page="136"),
}
# ------------------------------------------------------------------ reported ratios (percent): car, cet1, npl
RATIOS = {
    "FY2021": dict(car=22.8, cet1=22.8, npl=29.4, src="UBA22FS", page="Note 4"),
    "FY2022": dict(car=20.2, cet1=20.2, npl=15.8, src="UBA23FS", page="Note 4"),
    "FY2023": dict(car=15.0, cet1=15.0, npl=24.7, src="UBA24FS", page="Note 4"),
    "FY2024": dict(car=17.25, cet1=17.25, npl=12.5, src="UBA24FS", page="Note 4"),
    "FY2025": dict(car=26.11, cet1=26.10, npl=2.11, src="UBA25FS", page="Note 4"),
    "9M-2025": dict(car=20.4, cet1=None, npl=15.72, src="UBA26Q3", page="Regulatory ratios"),
    "9M-2026": dict(car=16.7, cet1=None, npl=1.57, src="UBA26Q3", page="Regulatory ratios"),
}
# regulatory capital note 5.1 (whole cedis): total regulatory capital, risk-weighted assets, tier 1 (CET1 after deductions)
CAPITAL = {
    "FY2023": dict(reg=709218197, rwa=4722209436, t1=709218197, src="UBA24AR", page="122"),
    "FY2024": dict(reg=891228373, rwa=5167704537, t1=891228373, src="UBA24AR", page="122"),
    "FY2025": dict(reg=1555839646, rwa=5958880637, t1=1555227698, src="UBA25AR", page="122"),
}
# other disclosed items (whole cedis)
STAT_TRANSFER = {"FY2022": 14898544, "FY2023": 43960657, "FY2024": 41077995, "FY2025": 50887951}   # statements of changes in equity
DIVIDENDS_PAID = {"FY2024": 40000000, "FY2025": 15730000, "9M-2026": 304860}
LEVIES = {"FY2023": 13798511 * 2, "FY2024": 12681918 * 2, "FY2025": 31496572 * 2}     # growth and sustainability + financial sector recovery levies (UBA24AR/25AR tax note)
OCI = {"FY2025": 12950362, "9M-2026": 2286}


def M(period, x):
    return round(x / (1e3 if period in INTERIM else 1e6), 3)


rows = []


def add(period, stmt, item, val, src, page, status, notes="", unit="GHS millions"):
    v = "" if val is None else (f"{val:.3f}" if isinstance(val, float) else str(val))
    rows.append([BANK, period, stmt, item, v, unit, src, page, status, notes])


for p in PERIODS:
    s = SRC[p]
    I, B = IS[p], BS[p]
    sp_i, sp_b = "SoCI", "SoFP"
    n_int = "Interim: thousands of cedis converted to millions." if p in INTERIM else ""
    for item, key in [("interest_income", "ii"), ("interest_expense", "ie"), ("net_interest_income", "nii"), ("fee_commission_income", "fi"),
                      ("fee_commission_expense", "fe"), ("net_trading_income", "nti"), ("other_operating_income", "oi"), ("total_operating_income", "opinc"),
                      ("staff_costs", "staff"), ("depreciation_amortisation", "da"), ("other_operating_expenses", "ox"),
                      ("impairment_charge", "imp"), ("profit_before_tax", "pbt"), ("income_tax", "tax"), ("profit_after_tax", "pat")]:
        note = n_int
        if item == "impairment_charge":
            note = ("Allowance for credit losses on financial assets (all financial assets, not loans only). Positive = charge, negative = reversal. " + n_int).strip()
        if item == "net_trading_income":
            note = ("Net trading and revaluation income. " + n_int).strip()
        if item == "total_operating_income":
            note = ("Net operating income before impairment (net interest income + net fees + net trading and other income). " + n_int).strip()
        add(p, "income_statement", item, M(p, I[key]), s, sp_i, "reported", note)
    # balance sheet
    add(p, "balance_sheet", "cash_and_bog_balances", M(p, B["cash"]), s, sp_b, "reported",
        "'Cash and bank balances'. Includes balances with other banks (due from other banks was 1,052.6m of the FY2024 figure per the cash note), so due_from_banks is not separable. " + n_int)
    if B["sec_fv"]:
        add(p, "balance_sheet", "investment_securities", M(p, B["sec_ac"] + B["sec_fv"]), s, sp_b, "derived",
            f"At amortised cost {M(p, B['sec_ac']):,.3f} + at FVOCI {M(p, B['sec_fv']):,.3f}. Net of allowance. " + n_int)
    else:
        add(p, "balance_sheet", "investment_securities", M(p, B["sec_ac"]), s, sp_b, "reported", "Investment securities (amortised cost; none at FVOCI). Net of allowance. " + n_int)
    add(p, "balance_sheet", "due_from_banks", None, "", "", "unavailable", "Not a separate line; balances with other banks sit inside cash and bank balances.")
    add(p, "balance_sheet", "loans_and_advances_net", M(p, B["loans"]), s, sp_b, "reported", "Loans and advances to customers (net). " + n_int)
    add(p, "balance_sheet", "property_equipment_intangibles", M(p, B["ppe"] + B["intg"]), s, sp_b, "derived",
        f"Property and equipment {M(p, B['ppe']):,.3f} + intangible assets {M(p, B['intg']):,.3f}. Right-of-use assets are not shown separately. " + n_int)
    add(p, "balance_sheet", "other_assets", M(p, B["oa"] + B["ita"] + B["dta"]), s, sp_b, "derived",
        f"Other assets {M(p, B['oa']):,.3f} + income tax asset {M(p, B['ita']):,.3f} + deferred tax asset {M(p, B['dta']):,.3f}. " + n_int)
    add(p, "balance_sheet", "total_assets", M(p, B["ta"]), s, sp_b, "reported", n_int)
    add(p, "balance_sheet", "customer_deposits", M(p, B["dep_c"]), s, sp_b, "reported", n_int)
    add(p, "balance_sheet", "due_to_banks", M(p, B["dep_b"]), s, sp_b, "reported", "Deposits from banks. " + n_int)
    add(p, "balance_sheet", "borrowings", M(p, B["bor"]), s, sp_b, "reported", ("None on the face of the balance sheet in this period. " if B["bor"] == 0 else "") + n_int)
    add(p, "balance_sheet", "other_liabilities", M(p, B["ol"]), s, sp_b, "reported", n_int)
    add(p, "balance_sheet", "total_liabilities", M(p, B["tl"]), s, sp_b, "reported", n_int)
    add(p, "balance_sheet", "total_equity", M(p, B["te"]), s, sp_b, "reported", n_int)
    add(p, "balance_sheet", "x_stated_capital", M(p, B["sc"]), s, sp_b, "reported", n_int)
    add(p, "balance_sheet", "x_retained_earnings", M(p, B["re"]), s, sp_b, "reported", n_int)
    add(p, "balance_sheet", "x_statutory_reserve", M(p, B["sr"]), s, sp_b, "reported", n_int)
    add(p, "balance_sheet", "x_credit_risk_reserve", M(p, B["crr"]), s, sp_b, "reported", "Credit risk reserve (regulatory); nil outside FY2023. " + n_int)
    add(p, "balance_sheet", "x_fair_value_reserve", M(p, B["fvr"]), s, sp_b, "reported", n_int)
    add(p, "balance_sheet", "x_investment_securities_fvoci", M(p, B["sec_fv"]), s, sp_b, "reported", "Included in investment_securities. " + n_int)

# loans
for p, L in LOANS.items():
    net = M(p, BS[p]["loans"])
    add(p, "balance_sheet", "loans_and_advances_gross", M(p, L["gross"]), L["src"], L["page"], "reported", "Gross carrying amount of loans and advances to customers (IFRS 9 note).")
    add(p, "balance_sheet", "loan_loss_allowance", M(p, L["allow"]), L["src"], L["page"], "reported", "Allowance for credit losses on loans and advances (positive). Gross - allowance = net loans.")
    for k, lab in (("s1", "stage_1"), ("s2", "stage_2"), ("s3", "stage_3")):
        add(p, "balance_sheet", f"x_loans_{lab}_gross", M(p, L[k]), L["src"], L["page"], "reported", f"Gross loans in IFRS 9 {lab.replace('_', ' ')}.")
    add(p, "ratios", "x_stage3_share_of_gross_pct", round(L["s3"] / L["gross"] * 100, 2), L["src"], L["page"], "derived", "Stage 3 gross / total gross loans x 100.", "percent")
for p in ("9M-2025", "9M-2026"):
    add(p, "balance_sheet", "loans_and_advances_gross", None, "", "", "unavailable", "The interim statement prints net loans only.")
    add(p, "balance_sheet", "loan_loss_allowance", None, "", "", "unavailable", "The interim statement prints net loans only.")
# ratios
for p, R in RATIOS.items():
    add(p, "ratios", "car_pct", R["car"], R["src"], R["page"], "reported", "Capital adequacy ratio as printed (interim: CRD basis).", "percent")
    add(p, "ratios", "npl_pct", R["npl"], R["src"], R["page"], "reported", "Gross non-performing loan ratio as printed.", "percent")
    if R["cet1"] is not None:
        add(p, "ratios", "x_cet1_pct", R["cet1"], R["src"], R["page"], "reported", "Common equity tier 1 ratio as printed. Not published as tier1_pct.", "percent")
    add(p, "ratios", "tier1_pct", None, "", "", "unavailable", "A Tier 1 ratio is not printed; the CET1 ratio is stored as x_cet1_pct.", "percent")
for p, C in CAPITAL.items():
    add(p, "balance_sheet", "x_regulatory_capital", M(p, C["reg"]), C["src"], C["page"], "reported", "Total regulatory capital (Note 5.1).")
    add(p, "balance_sheet", "x_tier1_capital", M(p, C["t1"]), C["src"], C["page"], "reported", "Tier 1 capital (CET1 after deductions) per Note 5.1.")
    add(p, "balance_sheet", "x_risk_weighted_assets", M(p, C["rwa"]), C["src"], C["page"], "reported", "Total risk-weighted assets (credit + operational + market risk).")
    add(p, "ratios", "x_rwa_to_total_assets", round(C["rwa"] / BS[p]["ta"], 4), C["src"], C["page"], "derived", "Risk-weighted assets / total assets (density).", "ratio")
# other disclosed flows
for p, v in STAT_TRANSFER.items():
    add(p, "income_statement", "x_statutory_reserve_transfer", M(p, v), SRC[p], "SoCE", "reported", "Transfer from retained earnings to the statutory reserve (statement of changes in equity).")
    add(p, "ratios", "x_statutory_transfer_share_of_pat_pct", round(v / IS[p]["pat"] * 100, 2), SRC[p], "SoCE", "derived", "Transfer / profit after tax x 100 (Act 930 s34 tiers: 50 / 25 / 12.5%).", "percent")
for p, v in DIVIDENDS_PAID.items():
    add(p, "income_statement", "x_dividends_paid", M(p, v), SRC[p], "SoCE", "reported", "Dividends paid to owners in the period (statement of changes in equity)." + (" The 9M-2025 comparative is 15.730m in the same statement." if p == "9M-2026" else ""))
add("FY2025", "income_statement", "x_dividend_recommended", 146.452, "UBA25FS", "Note 6", "reported", "Dividend recommended for 2025: GHS 146,452,341 (0.020 per share), subject to Bank of Ghana approval.")
for p, v in LEVIES.items():
    src = "UBA24AR" if p in ("FY2023", "FY2024") else "UBA25AR"
    add(p, "income_statement", "x_levies_in_income_tax", M(p, v), src, "129" if p != "FY2025" else "128", "reported", "Growth and Sustainability levy + Financial Sector Recovery levy, both inside the income tax charge (5% of profit before tax each).")
for p, v in OCI.items():
    add(p, "income_statement", "x_other_comprehensive_income", M(p, v), SRC[p], "SoCI", "reported", "Net change in fair value of FVOCI financial assets (net of tax).")

# derived ratios
for p in PERIODS:
    I, B = IS[p], BS[p]
    add(p, "ratios", "ldr_pct", round(B["loans"] / B["dep_c"] * 100, 2), "", "", "derived", "Net loans / customer deposits x 100.", "percent")
    add(p, "ratios", "cost_to_income_pct", round((I["staff"] + I["da"] + I["ox"]) / I["opinc"] * 100, 2), "", "", "derived",
        "(Staff + depreciation + other operating expenses) / net operating income x 100.", "percent")

with open(os.path.join(HERE, "financials.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["bank", "period", "statement", "line_item", "value", "unit", "source_id", "page", "status", "notes"])
    w.writerows(rows)

# ------------------------------------------------------------------ history checks
L = ["# Historical data checks (uba-ghana)", "",
     "Generated by `build_financials.py`. Whole-cedi figures are exact; interim figures are in thousands. Tolerance 0.001 GHS m annual, 0.0015 interim.", ""]
fails = 0


def chk(label, a, b, tol):
    global fails
    ok = abs(a - b) <= tol
    fails += 0 if ok else 1
    L.append(f"| {label} | {a:,.3f} | {b:,.3f} | {a - b:+.3f} | {'PASS' if ok else 'FAIL'} |")


L += ["## 1. Statement identities", "", "| Check | Computed | Reported | Difference | Result |", "| --- | --- | --- | --- | --- |"]
for p in PERIODS:
    I, B = IS[p], BS[p]
    t = 0.0015 if p in INTERIM else 0.001
    chk(f"{p}: NII = interest income - interest expense", M(p, I["ii"] - I["ie"]), M(p, I["nii"]), t)
    chk(f"{p}: operating income = NII + net fees + trading + other", M(p, I["nii"] + I["fi"] - I["fe"] + I["nti"] + I["oi"]), M(p, I["opinc"]), t)
    chk(f"{p}: PBT = operating income - impairment - staff - D&A - other", M(p, I["opinc"] - I["imp"] - I["staff"] - I["da"] - I["ox"]), M(p, I["pbt"]), t)
    chk(f"{p}: PAT = PBT - tax", M(p, I["pbt"] - I["tax"]), M(p, I["pat"]), t)
    chk(f"{p}: assets = liabilities + equity", M(p, B["tl"] + B["te"]), M(p, B["ta"]), t)
    chk(f"{p}: asset lines sum to total assets", M(p, B["cash"] + B["sec_ac"] + B["sec_fv"] + B["loans"] + B["oa"] + B["ppe"] + B["intg"] + B["ita"] + B["dta"]), M(p, B["ta"]), t)
    chk(f"{p}: liability lines sum to total liabilities", M(p, B["dep_c"] + B["dep_b"] + B["bor"] + B["ol"]), M(p, B["tl"]), t)
    chk(f"{p}: equity lines sum to total equity", M(p, B["sc"] + B["re"] + B["fvr"] + B["crr"] + B["sr"]), M(p, B["te"]), t)
L += ["", "## 2. Loan note bridges", "", "| Check | Computed | Reported | Difference | Result |", "| --- | --- | --- | --- | --- |"]
for p, Ln in LOANS.items():
    chk(f"{p}: gross - allowance = net loans on the balance sheet", M(p, Ln["gross"] - Ln["allow"]), M(p, BS[p]["loans"]), 0.001)
    chk(f"{p}: stage 1 + 2 + 3 = gross loans", M(p, Ln["s1"] + Ln["s2"] + Ln["s3"]), M(p, Ln["gross"]), 0.001)
L += ["", "## 3. Equity roll-forward (opening equity + comprehensive income - dividends = closing equity)", "",
      "| Check | Computed | Reported | Difference | Result |", "| --- | --- | --- | --- | --- |"]
chk("FY2024", M("FY2024", BS["FY2023"]["te"] + IS["FY2024"]["pat"] - DIVIDENDS_PAID["FY2024"]), M("FY2024", BS["FY2024"]["te"]), 0.001)
chk("FY2025", M("FY2025", BS["FY2024"]["te"] + IS["FY2025"]["pat"] + OCI["FY2025"] - DIVIDENDS_PAID["FY2025"]), M("FY2025", BS["FY2025"]["te"]), 0.001)
chk("9M-2026", M("FY2025", BS["FY2025"]["te"]) + M("9M-2026", IS["9M-2026"]["pat"] + OCI["9M-2026"] - DIVIDENDS_PAID["9M-2026"]), M("9M-2026", BS["9M-2026"]["te"]), 0.0015)
L += ["", "Exact roll-forwards in FY2024, FY2025 and 9M-2026 confirm the column orientation of the interim statement (current period first).", ""]

L += ["## 4. Statutory reserve transfer (Act 930 s34 tiers observed)", "",
      "| Year | Transfer / PAT | Opening reserve / stated capital | Tier implied |", "| --- | --- | --- | --- |"]
prev_sr = {"FY2022": 336997672, "FY2023": BS["FY2022"]["sr"], "FY2024": BS["FY2023"]["sr"], "FY2025": BS["FY2024"]["sr"]}
for p, v in STAT_TRANSFER.items():
    ratio = prev_sr[p] / 400000000
    tier = "50%" if ratio < 0.5 else "25%" if ratio < 1 else "12.5%"
    L.append(f"| {p} | {v / IS[p]['pat'] * 100:.2f}% | {ratio * 100:.1f}% | {tier} |")
L += ["", "Observed shares are 25.0% (reserve below stated capital of 400m) and 12.5% from FY2025 (opening reserve 436.9m, above stated capital).", ""]

L += ["## 5. Comparative columns agree across reports (observed)", "",
      "The same figures appear as the prior-year column in the next year's report for total assets, total liabilities, total equity, loans, customer deposits, profit before tax and profit after tax: FY2022 in UBA23FS, FY2023 in UBA24FS, FY2024 in UBA25FS. No restatement was seen. FY2021 rests on UBA22FS only.", ""]
L += ["## 6. Known source inconsistencies (disclosed, not fixed)", "",
      "- UBA24AR p.103 prints FY2023 stage carrying amounts that copy the FY2022 column (stage 1 net 1,423,497,088; total 1,544,688,879). Note 21 (pp.134-136) reconciles: gross 1,360.047m - allowance 217.904m = net 1,142.143m. The note values are used.",
      "- UBA25AR p.136 prints the FY2025 opening allowance as 202,555,426 in one table and 202,555,926 elsewhere (0.0005m). The balance-sheet note value 202,555,926 is used.",
      "- The reported FY2022 NPL ratio (15.8%) equals (stage 2 + stage 3) / gross loans (15.75%), while other years equal stage 3 / gross (FY2021 29.37% vs 29.4%; FY2023 24.66% vs 24.7%; FY2024 12.53% vs 12.5%; FY2025 2.11% vs 2.11%). The ratio is stored as printed.",
      "- UBA23FS prints an audit report date of 27 March 2023 against directors' approval on 27 March 2024; UBA25FS prints the audit signature as 31 March 2025 against 31 March 2026 in the text. Probable typographical errors; not verified.",
      "- 9M-2025 owner transactions are 15.73m in the equity statement but 1.057m dividends paid in the cash flow statement of UBA26Q3.",
      ""]
L += ["", f"**History check failures: {fails}**", ""]
with open(os.path.join(HERE, "checks_history.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print(f"financials.csv rows: {len(rows)} | history check failures: {fails}")
