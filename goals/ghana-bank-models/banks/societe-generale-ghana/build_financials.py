#!/usr/bin/env python3
"""Build banks/societe-generale-ghana/financials.csv (bank-only, GHS millions).

Sources (all official Societe Generale Ghana PLC filings, bank/separate statements):
  SG21AR  Annual Report 2021            (income printed p.51, BS p.52, IIS/allowance note p.76, CAR p.111)
  SG22AR  Annual Report 2022            (income p.54, BS p.55, loans note p.78, CAR p.115, stats p.79)
  SG23AR  Annual Report 2023            (income p.61, BS p.62, loans note p.90, stats p.91)
  SG24AR  Annual Report 2024            (income p.64, BS p.65, loans note p.96, stats p.97, CAR narrative p.14)
  SG25AR  Annual Report 2025            (income p.65, BS p.66, loans note p.95, stats p.95)
  SG25FIN 2025 Audited Financial Statements summary (quant disclosures: CAR/CET1)
  SG26Q3  9M-2026 Unaudited Financial Statements (income/BS/ratios)

Convention (MODEL-SPEC.md): costs/allowances stored POSITIVE; profits signed.
Every row is a reported figure copied from the cited page, or a derived row with its
formula in notes. Values unavailable in the summary statements are left blank.
"""
import csv, os

BANK = "societe-generale-ghana"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "financials.csv")

# ---------------------------------------------------------------- source data
# Income statement (GHS millions). Costs positive; impairment is a cost (negative = a gain).
INC = {
 "FY2021": dict(src="SG21AR", pg="51", ii=510.992929, ie=109.990417, nii=401.002512,  # printed p.51
   fci=77.475216, fce=27.252208, nt=40.793352, xfv=52.835645, ooi=91.439536, toi=636.294053,
   imp=33.407581, staff=135.516867, da=34.807599, ooe=150.595307, pbt=281.966699,
   tax=97.637066, pat=184.329633),
 "FY2022": dict(src="SG22AR", pg="54", ii=659.497229, ie=134.930676, nii=524.566553,  # printed p.54
   fci=105.172123, fce=36.313952, nt=95.734001, xfv=64.104688, ooi=48.318570, toi=801.581983,
   imp=284.737040, staff=171.621011, da=39.433935, ooe=137.405680, pbt=168.384317,
   tax=59.544391, pat=108.839926),
 "FY2023": dict(src="SG23AR", pg="61", ii=1088.895175, ie=215.486510, nii=873.408665,  # printed p.61
   fci=126.883065, fce=61.369992, nt=103.590162, xfv=126.748506, ooi=68.568937, toi=1237.829343,
   imp=99.213609, staff=216.591094, da=53.987350, ooe=206.448050, pbt=661.589240,
   tax=236.786258, pat=424.802981),
 "FY2024": dict(src="SG24AR", pg="64", ii=1357.215549, ie=234.148854, nii=1123.066695,  # printed p.64
   fci=158.644102, fce=83.272803, nt=59.933937, xfv=58.304970, ooi=138.874043, toi=1455.550944,
   imp=103.267026, staff=244.686798, da=71.057192, ooe=198.138976, pbt=838.400952,
   tax=287.101705, pat=551.299247),
 "FY2025": dict(src="SG25AR", pg="65", ii=1410.114120, ie=222.702856, nii=1187.411264,  # printed p.65
   fci=169.468925, fce=82.124280, nt=122.253401, xfv=18.789938, ooi=-59.763027, toi=1356.036221,
   imp=-33.641390, staff=275.643494, da=126.487549, ooe=372.781678, pbt=614.764890,
   tax=217.763590, pat=397.001300),
 "9M-2026": dict(src="SG26Q3", pg="1", ii=750.419, ie=126.427, nii=623.992,
   fci=135.216, fce=50.863, nt=59.697, xfv=14.295, ooi=14.762, toi=797.099,
   imp=27.165, staff=238.264, da=109.208, ooe=190.323, pbt=232.139,
   tax=82.136, pat=150.003),
}

# Balance sheet (GHS millions). Component buckets are defined so they sum to reported totals.
BS = {
 "FY2021": dict(src="SG21AR", pg="52", cash=963.960922, trading=143.156280, deriv_a=None,
   fvoci=87.240744, amc=1383.955004, loans_net=2504.366677, eqinv=2.923386, oth=54.130188,
   ppe=255.268418, intang=15.009794, dta=27.010706, cta=None,
   ta=5437.022119, dep_banks=1.916501, dep_cust=3391.140683, borrow=588.864628, deriv_l=40.509648,
   ctax=21.325184, dtl=None, othl=364.700138, tl=4408.456782,
   stated=404.245427, retained=207.312183, reval=123.670260, statutory=292.518632,
   resoth=0.818835, te=1028.565337),
 "FY2022": dict(src="SG22AR", pg="55", cash=1950.873066, trading=14.157407, deriv_a=188.780000,
   fvoci=43.784934, amc=796.556383, loans_net=3102.993067, eqinv=3.549552, oth=101.997533,
   ppe=292.785473, intang=10.499595, dta=89.859093, cta=None,
   ta=6595.836103, dep_banks=1.145398, dep_cust=4239.568200, borrow=642.585961, deriv_l=None,
   ctax=57.267488, dtl=None, othl=566.631231, tl=5507.198278,
   stated=404.245427, retained=240.555598, reval=123.670260, statutory=319.728614,
   resoth=0.437926, te=1088.637825),
 "FY2023": dict(src="SG23AR", pg="62", cash=2131.699314, trading=1.742074, deriv_a=None,
   fvoci=0.0, amc=1800.220862, loans_net=3987.842023, eqinv=3.503810, oth=163.193190,
   ppe=245.151386, intang=84.476574, dta=111.997320, cta=None,
   ta=8529.826553, dep_banks=1.798457, dep_cust=5087.136276, borrow=897.959701, deriv_l=0.060000,
   ctax=15.350102, dtl=None, othl=1014.519137, tl=7016.823673,
   stated=404.245427, retained=559.157834, reval=123.670260, statutory=425.929359,
   resoth=0.0, te=1513.002880),
 "FY2024": dict(src="SG24AR", pg="65", cash=3579.482591, trading=8.794742, deriv_a=2.021429,
   fvoci=None, amc=780.949308, loans_net=5011.684459, eqinv=5.513268, oth=93.914071,
   ppe=759.572915, intang=147.356438, dta=7.001472, cta=None,
   ta=10396.290693, dep_banks=30.764480, dep_cust=6219.856675, borrow=520.138679, deriv_l=None,
   ctax=54.866304, dtl=None, othl=1124.782632, tl=7950.408770,
   stated=404.245427, retained=1041.544676, reval=505.250055, statutory=494.841765,
   resoth=0.0, te=2445.881923),
 "FY2025": dict(src="SG25AR", pg="66", cash=2676.280210, trading=7.620583, deriv_a=None,
   fvoci=None, amc=1505.273694, loans_net=4491.826540, eqinv=9.368223, oth=77.558831,
   ppe=728.276952, intang=168.135948, dta=None, cta=11.759466,
   ta=9676.100447, dep_banks=1.396221, dep_cust=5843.182979, borrow=334.350011, deriv_l=None,
   ctax=None, dtl=2.699849, othl=892.696228, tl=7074.325288,
   stated=404.245427, retained=1147.812749, reval=505.250055, statutory=544.466928,
   resoth=0.0, te=2601.775159),
 "9M-2026": dict(src="SG26Q3", pg="1", cash=3958.763, trading=52.747, deriv_a=None,
   fvoci=None, amc=1305.391, loans_net=4674.926, eqinv=9.368, oth=122.860,
   ppe=709.128, intang=170.995, dta=2.097, cta=72.100,
   ta=11078.375, dep_banks=1.603, dep_cust=7156.119, borrow=314.740, deriv_l=None,
   ctax=None, dtl=None, othl=1027.804, tl=8500.266,
   stated=404.245, retained=1105.397, reval=505.250, statutory=563.217,
   resoth=None, te=2578.109),
}

# Loan detail (GHS millions): gross, amortised-cost adjustment, interest in suspense, allowance.
LOANS = {
 "FY2021": dict(src="SG21AR", pg="76", gross=2804.858737, amort=28.390451, iis=37.956512, allow=234.145097),
 "FY2022": dict(src="SG22AR", pg="78", gross=3635.008639, amort=45.950796, iis=52.331339, allow=433.733437),
 "FY2023": dict(src="SG23AR", pg="90", gross=4663.624839, amort=60.280870, iis=74.291811, allow=541.210135),
 "FY2024": dict(src="SG24AR", pg="96", gross=5840.974925, amort=71.229039, iis=103.492704, allow=654.568723),
 "FY2025": dict(src="SG25AR", pg="95", gross=5121.327682, amort=None, iis=None, allow=629.501142),
 "9M-2026": dict(src=None, pg="", gross=None, amort=None, iis=None, allow=None),
}

# Reported ratios. car_pct primary value is the audited-statement disclosure where present,
# else the bank's own narrative; the alternative in notes is retained for transparency.
RATIO = {
 "FY2021": dict(src="SG21AR", pg="111", car=22.38, car_note="CAR 22.38% at 31 Dec 2021 per the audited capital-adequacy note (printed p.111).", npl=7.58, npl_pg="77"),
 "FY2022": dict(src="SG22AR", pg="113", car=16.00, car_note="CAR 16.00% at 31 Dec 2022 per the audited capital-adequacy note (printed p.113).", npl=13.48, npl_pg="79"),
 "FY2023": dict(src="SG23AR", pg="127", car=18.71, car_note="CAR 18.71% at 31 Dec 2023 per the audited capital-adequacy note (printed p.127). The FY2024 narrative separately quotes 13.9% with BoG DDEP reliefs / 8.3% without; different basis, noted.", npl=19.55, npl_pg="90"),
 "FY2024": dict(src="SG24AR", pg="133", car=19.81, car_note="CAR 19.81% at 31 Dec 2024 per the audited capital-adequacy note (printed p.133). FY2024 narrative separately quotes 14.0% with DDEP reliefs / 11.3% without; different basis, noted.", npl=16.56, npl_pg="96"),
 "FY2025": dict(src="SG25AR", pg="133", car=23.39, car_note="CAR 23.39% at 31 Dec 2025 per the audited capital-adequacy note (printed p.133); the 2025 narrative says 17.5% (DDEP reliefs excluded in 2025). The audited 2025 summary prints the same 23.39%.", npl=13.06, npl_pg="95"),
 "9M-2026": dict(src="SG26Q3", pg="1", car=18.52, car_note="CAR 18.52% at 30 Sep 2026 (unaudited).", npl=13.98, npl_pg="1"),
}

PERIODS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "9M-2026"]
BANKONLY = "Bank-only (separate) statements; costs/allowances positive, profits signed."

rows = []
def add(period, statement, line_item, value, unit, source_id, page, status, notes):
    rows.append([BANK, period, statement, line_item,
                 "" if value is None else f"{value:.6f}".rstrip("0").rstrip("."),
                 unit, source_id or "", page or "", status, notes])

for p in PERIODS:
    d = INC[p]
    for key, item in [("ii","interest_income"),("ie","interest_expense"),("nii","net_interest_income"),
                      ("fci","fee_commission_income"),("fce","fee_commission_expense"),
                      ("nt","net_trading_income"),
                      ("toi","total_operating_income"),("staff","staff_costs"),
                      ("da","depreciation_amortisation"),("ooe","other_operating_expenses"),
                      ("imp","impairment_charge"),("pbt","profit_before_tax"),("tax","income_tax"),
                      ("pat","profit_after_tax")]:
        note = BANKONLY
        if item == "impairment_charge" and d["imp"] < 0:
            note += " Impairment is a net credit (gain) this period; stored negative."
        add(p, "income_statement", item, d[key], "GHS millions", d["src"], d["pg"], "reported", note)
    # other operating income (bank's own line) and the FV-other-income line kept separately
    add(p, "income_statement", "other_operating_income", d["ooi"], "GHS millions", d["src"], d["pg"], "reported", BANKONLY)
    add(p, "income_statement", "x_fv_other_income", d["xfv"], "GHS millions", d["src"], d["pg"], "reported",
        BANKONLY + " Net income from other financial instruments carried at fair value.")

    b = BS[p]
    def rep(item, val, extra=""):
        add(p, "balance_sheet", item, val, "GHS millions", b["src"], b["pg"], "reported", BANKONLY + (" " + extra if extra else ""))
    rep("cash_and_bog_balances", b["cash"])
    if b["trading"] is not None:
        rep("x_trading_assets", b["trading"], "Non-pledged trading assets.")
    if b["deriv_a"] is not None:
        add(p, "balance_sheet", "x_derivative_assets", b["deriv_a"], "GHS millions", b["src"], b["pg"], "reported", BANKONLY + " Derivative financial assets.")
    else:
        add(p, "balance_sheet", "x_derivative_assets", None, "GHS millions", b["src"], b["pg"], "unavailable", "No derivative asset reported.")
    inv = (b["amc"] or 0) + (b["fvoci"] or 0)
    add(p, "balance_sheet", "investment_securities", inv, "GHS millions", b["src"], b["pg"], "derived",
        "Debt instruments at amortised cost plus debt instruments at FVOCI, as reported.")
    rep("loans_and_advances_net", b["loans_net"])
    if b["eqinv"] is not None:
        rep("x_equity_investments", b["eqinv"], "Unlisted equity investments at fair value.")
    oth = (b["oth"] or 0) + (b["dta"] or 0) + (b["cta"] or 0)
    add(p, "balance_sheet", "other_assets", oth, "GHS millions", b["src"], b["pg"], "derived",
        "Other assets plus deferred/current tax assets as reported.")
    ppe = (b["ppe"] or 0) + (b["intang"] or 0)
    add(p, "balance_sheet", "property_equipment_intangibles", ppe, "GHS millions", b["src"], b["pg"], "derived",
        "Property, plant and equipment plus intangible assets as reported.")
    rep("total_assets", b["ta"])
    rep("customer_deposits", b["dep_cust"])
    rep("due_to_banks", b["dep_banks"])
    rep("borrowings", b["borrow"])
    othl = (b["othl"] or 0) + (b["ctax"] or 0) + (b["dtl"] or 0) + (b["deriv_l"] or 0)
    add(p, "balance_sheet", "other_liabilities", othl, "GHS millions", b["src"], b["pg"], "derived",
        "Other liabilities plus current/deferred tax and derivative liabilities as reported.")
    rep("total_liabilities", b["tl"])
    rep("stated_capital", b["stated"])
    rep("retained_earnings", b["retained"])
    res = (b["reval"] or 0) + (b["statutory"] or 0) + (b["resoth"] or 0)
    add(p, "balance_sheet", "reserves_other", res, "GHS millions", b["src"], b["pg"], "derived",
        "Revaluation reserve plus statutory reserve plus other reserves as reported.")
    rep("total_equity", b["te"])

    l = LOANS[p]
    add(p, "balance_sheet", "loans_and_advances_gross", l["gross"], "GHS millions", l["src"], l["pg"],
        "reported" if l["gross"] is not None else "unavailable", BANKONLY + (" Gross loans and advances (note 20)." if l["gross"] is not None else " Not disclosed in the interim summary."))
    add(p, "balance_sheet", "loan_loss_allowance", l["allow"], "GHS millions", l["src"], l["pg"],
        "reported" if l["allow"] is not None else "unavailable", BANKONLY + (" Allowance for impairment on loans (note 20); positive balance." if l["allow"] is not None else " Not disclosed in the interim summary."))
    add(p, "balance_sheet", "x_amortised_cost_adjustment", l["amort"], "GHS millions", l["src"], l["pg"],
        "reported" if l["amort"] is not None else "unavailable", BANKONLY + " Amortised-cost adjustment to gross loans.")
    add(p, "balance_sheet", "x_interest_in_suspense", l["iis"], "GHS millions", l["src"], l["pg"],
        "reported" if l["iis"] is not None else "unavailable",
        BANKONLY + (" Interest in suspense (note 20); bridge: gross - amortised cost adjustment - interest in suspense - allowance = net." if l["iis"] is not None else " FY2025 net = gross - allowance exactly, so no interest-in-suspense adjustment was disclosed."))

    r = RATIO[p]
    add(p, "ratios", "car_pct", r["car"], "percent", r["src"], r["pg"], "reported", r["car_note"])
    add(p, "ratios", "npl_pct", r["npl"], "percent", r["src"], r["npl_pg"], "reported", "Gross non-performing loan ratio as reported.")
    for item in ["tier1_pct", "ldr_pct", "cost_to_income_pct", "roe_pct", "roa_pct"]:
        add(p, "ratios", item, None, "percent", "", "", "unavailable",
            "Not disclosed as a ratio in the bank's summary statements; recomputable in checks.md where inputs exist.")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bank","period","statement","line_item","value","unit","source_id","page","status","notes"])
    w.writerows(rows)

print(f"wrote {OUT} rows={len(rows)}")
