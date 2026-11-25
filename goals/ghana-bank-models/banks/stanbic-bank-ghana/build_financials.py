#!/usr/bin/env python3
"""Build banks/stanbic-bank-ghana/financials.csv (bank-only, GHS millions).

Sources (all official Stanbic Bank Ghana Ltd filings, bank/separate statements):
  SB22AR   2022 Annual Report (FY2022 income/BS + FY2021 comparatives; loan note 5.1 printed p.70)
  SB22SUM  2022 Summary financial statements (quantitative disclosures: CAR/CET1/NPL, FY2022/FY2021)
  SB23AR   2023 Annual Report (income/BS printed p.48; loan note p.85; capital note p.68; cash note p.40)
  SB23SUM  2023 Summary financial statements (ratios FY2023/FY2022)
  SB24AR   2024 Annual Report (BS printed p.49; loan note p.85; capital note p.137; cash note p.80)
  SB24SUM  2024 Summary financial statements (ratios FY2024/FY2023)
  SB25AR   2025 Annual Report (income p.47; BS p.46; loan note p.80; capital note p.132; cash note p.77)
  SB25SUM  2025 Summary financial statements (ratios FY2025/FY2024)
  SB26Q3   9M-2026 Unaudited Financial Statements (income/BS/ratios p.1)

Convention (MODEL-SPEC.md): costs/allowances stored POSITIVE; profits signed.
Stanbic reports an INDIRECT TAX line above the direct income tax; `profit_before_tax`
is the reported "Profit before indirect tax" and `income_tax` is the sum of indirect
and direct tax so that PAT = PBT - income_tax holds.
Every row is a reported figure copied from the cited page, or a derived/unavailable row
with its method in notes. Values unavailable in the summary statements are left blank.
"""
import csv, os

BANK = "stanbic-bank-ghana"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "financials.csv")

# ---------------------------------------------------------------- source data
# Income statement (GHS millions). Costs positive; impairment positive = a charge.
# pbt = reported "Profit before indirect tax"; tax = indirect + direct tax.
INC = {
 "FY2021": dict(src="SB22AR", pg="70", ii=886.625, ie=230.206, nii=656.419,
   fci=327.907, fce=43.242, netfee=284.665, nt=371.025, ooi=0.863, toi=1312.972,
   imp=39.273, staff=326.813, da=72.592, ooe=226.632, pbt=647.662,
   indtax=29.708, dirtax=212.764, tax=242.472, pat=405.190),
 "FY2022": dict(src="SB22AR", pg="70", ii=1504.110, ie=349.497, nii=1154.613,
   fci=440.795, fce=86.278, netfee=354.517, nt=225.549, ooi=-2.778, toi=1731.901,
   imp=965.937, staff=402.386, da=75.731, ooe=331.969, pbt=-44.122,
   indtax=36.549, dirtax=-18.076, tax=18.473, pat=-62.595),
 "FY2023": dict(src="SB23AR", pg="48", ii=2463.726, ie=498.256, nii=1965.470,
   fci=536.517, fce=113.447, netfee=423.070, nt=943.699, ooi=0.323, toi=3332.562,
   imp=31.876, staff=627.795, da=99.996, ooe=539.407, pbt=2033.488,
   indtax=71.869, dirtax=681.204, tax=753.073, pat=1280.415),
 "FY2024": dict(src="SB24AR", pg="48", ii=3154.821, ie=643.754, nii=2511.067,
   fci=700.025, fce=149.731, netfee=550.294, nt=591.788, ooi=0.097, toi=3653.246,
   imp=364.191, staff=745.741, da=112.464, ooe=655.040, pbt=1775.810,
   indtax=63.318, dirtax=549.890, tax=613.208, pat=1162.602),
 "FY2025": dict(src="SB25AR", pg="47", ii=3415.660, ie=578.935, nii=2836.725,
   fci=771.076, fce=167.997, netfee=603.079, nt=1011.641, ooi=12.047, toi=4463.492,
   imp=52.178, staff=943.984, da=130.582, ooe=729.216, pbt=2607.532,
   indtax=78.313, dirtax=920.552, tax=998.865, pat=1608.667),
 "9M-2026": dict(src="SB26Q3", pg="1", ii=1974.780, ie=282.424, nii=1692.356,
   fci=646.334, fce=125.730, netfee=520.604, nt=602.257, ooi=6.128, toi=2821.345,
   imp=102.757, staff=741.271, da=120.634, ooe=450.969, pbt=1405.714,
   indtax=36.323, dirtax=465.606, tax=501.929, pat=903.785),
}

# Balance sheet (GHS millions). cash = coins + balances with central bank; the
# "due from other banks" part of cash and cash equivalents is split out where the
# note discloses it. trading = non-pledged; pledged = separately reported pledged
# trading assets. Other assets include deferred/current tax assets.
BS = {
 "FY2021": dict(src="SB22AR", pg="70", cash=3316.768, due_from_banks=None,
   trading=1602.113, pledged=None, inv=2772.551, loans_net=5185.128,
   dta=36.513, oth=806.234, intang=69.948, ppe=253.842, ta=14043.097,
   dep_banks=1377.454, dep_cust=9936.698, borrow=None,
   trading_liab=95.104, ctax=19.180, othl_extra=661.860, tl=12090.296,
   stated=414.213, retained=960.512, statres=520.182, crim=57.894, others=None, te=1952.801),
 "FY2022": dict(src="SB22AR", pg="70", cash=4342.422, due_from_banks=4250.328,
   trading=1057.969, pledged=None, inv=1186.809, loans_net=6429.851,
   dta=287.572, oth=723.488, intang=55.284, ppe=263.728, ta=18597.451,
   dep_banks=741.714, dep_cust=14596.310, borrow=None,
   trading_liab=137.401, ctax=58.194, othl_extra=1356.040, tl=16889.659,
   stated=414.213, retained=773.397, statres=520.182, crim=0.0, others=0.0, te=1707.792),
 "FY2023": dict(src="SB23AR", pg="48", cash=7543.105, due_from_banks=1298.126,
   trading=2055.380, pledged=None, inv=6305.792, loans_net=5989.342,
   dta=228.587, oth=809.235, intang=46.850, ppe=357.121, ta=24633.538,
   dep_banks=794.725, dep_cust=18622.654, borrow=None,
   trading_liab=807.720, ctax=57.455, othl_extra=1374.114, tl=21656.668,
   stated=414.213, retained=1882.423, statres=680.234, crim=0.0, others=0.0, te=2976.870),
 "FY2024": dict(src="SB24AR", pg="49", cash=5887.649, due_from_banks=7913.420,
   trading=2165.532, pledged=150.990, inv=7165.362, loans_net=7846.716,
   dta=318.682, oth=708.313, intang=38.509, ppe=395.748, ta=32590.921,
   dep_banks=808.010, dep_cust=23172.209, borrow=573.179,
   trading_liab=2119.933, ctax=237.084, othl_extra=1549.842, tl=28460.257,
   stated=414.213, retained=2890.892, statres=825.559, crim=0.0, others=0.0, te=4130.664),
 "FY2025": dict(src="SB25AR", pg="46", cash=6743.970, due_from_banks=3402.728,
   trading=3783.127, pledged=1084.220, inv=11911.532, loans_net=7652.776,
   dta=332.736, oth=1374.749, intang=30.261, ppe=392.046, ta=36708.145,
   dep_banks=655.594, dep_cust=24013.184, borrow=1417.465,
   trading_liab=2950.742, ctax=222.323, othl_extra=1709.506, tl=30968.814,
   stated=414.213, retained=4298.476, statres=1026.642, crim=0.0, others=0.0, te=5739.331),
 "9M-2026": dict(src="SB26Q3", pg="1", cash=15778.120, due_from_banks=None,
   trading=3107.390, pledged=997.908, inv=12622.184, loans_net=9027.632,
   dta=241.918, oth=908.830, intang=18.296, ppe=541.356, ta=43243.634,
   dep_banks=636.076, dep_cust=29292.992, borrow=1768.066,
   trading_liab=3503.827, ctax=99.016, othl_extra=2426.875, tl=37726.852,
   stated=414.213, retained=3862.940, statres=1026.642, crim=212.987, others=0.0, te=5516.782),
}

# Loan detail (note 5.1; GHS millions): gross, credit impairment allowance,
# interest in suspense where separately reported.
LOANS = {
 "FY2021": dict(src="SB22AR", pg="70", gross=5388.433, allow=203.305, iis=None, net=5185.128),
 "FY2022": dict(src="SB22AR", pg="70", gross=7018.198, allow=588.347, iis=None, net=6429.851),
 "FY2023": dict(src="SB23AR", pg="85", gross=6767.842, allow=778.500, iis=0.0, net=5989.342),
 "FY2024": dict(src="SB24AR", pg="85", gross=9390.373, allow=1209.169, iis=334.488, net=7846.716),
 "FY2025": dict(src="SB25AR", pg="80", gross=9820.519, allow=1502.630, iis=665.113, net=7652.776),
 "9M-2026": dict(src=None, pg="", gross=None, allow=None, iis=None, net=None),
}

# Reported ratios (percent).
RATIO = {
 "FY2021": dict(src="SB22SUM", pg="1", car=19.2, tier1=17.2, npl=6.7),
 "FY2022": dict(src="SB22SUM", pg="1", car=12.3, tier1=12.3, npl=8.96),
 "FY2023": dict(src="SB23SUM", pg="1", car=19.6, tier1=16.6, npl=16.24),
 "FY2024": dict(src="SB24SUM", pg="1", car=19.0, tier1=16.0, npl=17.08),
 "FY2025": dict(src="SB25SUM", pg="1", car=23.2, tier1=21.2, npl=24.63),
 "9M-2026": dict(src="SB26Q3", pg="1", car=23.32, tier1=21.32, npl=9.54),
}

# Audited capital-adequacy note (GHS millions): Tier 1, Tier 2, total regulatory capital, RWA.
CAP = {
 "FY2021": dict(src=None, pg=None, t1=None, t2=None, cap=None, rwa=None),
 "FY2022": dict(src="SB23AR", pg="68", t1=1468.539, t2=0.0, cap=1468.539, rwa=11963.070),
 "FY2023": dict(src="SB23AR", pg="68", t1=1919.338, t2=345.918, cap=2265.256, rwa=11530.609),
 "FY2024": dict(src="SB24AR", pg="137", t1=2621.420, t2=491.453, cap=3112.873, rwa=16381.778),
 "FY2025": dict(src="SB25AR", pg="132", t1=3665.705, t2=346.290, cap=4011.995, rwa=17314.504),
 "9M-2026": dict(src=None, pg=None, t1=None, t2=None, cap=None, rwa=None),
}

# FY2021 regulatory-basis loan detail (risk note 30) kept separate to avoid double counting.
REG21 = dict(src="SB21AR", pg="107", reg_gross=5466.710, iis=78.277)

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
                      ("nt","net_trading_income"),("ooi","other_operating_income"),
                      ("toi","total_operating_income"),("staff","staff_costs"),
                      ("da","depreciation_amortisation"),("ooe","other_operating_expenses"),
                      ("imp","impairment_charge"),("pbt","profit_before_tax"),("tax","income_tax"),
                      ("pat","profit_after_tax")]:
        note = BANKONLY
        if item == "profit_before_tax":
            note += " Reported 'Profit before indirect tax'; the indirect and direct tax below are combined into income_tax."
        if item == "income_tax":
            note += " Sum of the reported indirect tax and direct tax (see x_indirect_tax / x_direct_tax)."
        add(p, "income_statement", item, d[key], "GHS millions", d["src"], d["pg"], "reported", note)
    add(p, "income_statement", "x_indirect_tax", d["indtax"], "GHS millions", d["src"], d["pg"], "reported",
        BANKONLY + " Indirect tax, reported as a separate line above the direct income tax.")
    add(p, "income_statement", "x_direct_tax", d["dirtax"], "GHS millions", d["src"], d["pg"], "reported",
        BANKONLY + " Direct income tax charge/(credit).")

    b = BS[p]
    def rep(item, val, extra=""):
        add(p, "balance_sheet", item, val, "GHS millions", b["src"], b["pg"], "reported",
            BANKONLY + (" " + extra if extra else ""))
    rep("cash_and_bog_balances", b["cash"], "Coins and bank notes plus balances with central bank." if b["due_from_banks"] is not None
        else "Reported as a single cash-and-cash-equivalents line (split not disclosed in this filing).")
    add(p, "balance_sheet", "due_from_banks", b["due_from_banks"], "GHS millions", b["src"], b["pg"],
        "reported" if b["due_from_banks"] is not None else "unavailable",
        BANKONLY + (" Due from other banks and financial institutions (note 2/7)." if b["due_from_banks"] is not None
                    else " Cash and cash equivalents is reported as a single line in this filing; the inter-bank split is unavailable."))
    rep("x_trading_assets", b["trading"], "Non-pledged trading assets.")
    add(p, "balance_sheet", "x_pledged_assets", b["pledged"], "GHS millions", b["src"], b["pg"],
        "reported" if b["pledged"] is not None else "unavailable",
        BANKONLY + (" Pledged trading assets." if b["pledged"] is not None else " No pledged trading assets line in this filing."))
    rep("investment_securities", b["inv"])
    rep("loans_and_advances_net", b["loans_net"])
    oth = (b["oth"] or 0) + (b["dta"] or 0)
    add(p, "balance_sheet", "other_assets", oth, "GHS millions", b["src"], b["pg"], "derived",
        "Other assets plus deferred/current tax assets as reported.")
    ppe = (b["ppe"] or 0) + (b["intang"] or 0)
    add(p, "balance_sheet", "property_equipment_intangibles", ppe, "GHS millions", b["src"], b["pg"], "derived",
        "Property, equipment and right-of-use assets plus intangible assets as reported.")
    rep("total_assets", b["ta"])
    rep("customer_deposits", b["dep_cust"])
    rep("due_to_banks", b["dep_banks"])
    add(p, "balance_sheet", "borrowings", b["borrow"], "GHS millions", b["src"], b["pg"],
        "reported" if b["borrow"] is not None else "unavailable",
        BANKONLY + (" Borrowings (note 18.3)." if b["borrow"] is not None
                    else " Borrowings were not shown as a separate line before 2023; included within other liabilities."))
    othl = (b["trading_liab"] or 0) + (b["ctax"] or 0) + (b["othl_extra"] or 0)
    add(p, "balance_sheet", "other_liabilities", othl, "GHS millions", b["src"], b["pg"], "derived",
        "Trading liabilities plus current/deferred tax plus other liabilities as reported (borrowings are a separate line).")
    rep("total_liabilities", b["tl"])
    rep("stated_capital", b["stated"])
    rep("retained_earnings", b["retained"])
    res = (b["statres"] or 0) + (b["crim"] or 0) + (b["others"] or 0)
    add(p, "balance_sheet", "reserves_other", res, "GHS millions", b["src"], b["pg"], "derived",
        "Statutory reserve plus statutory credit risk reserve plus other reserves as reported.")
    rep("total_equity", b["te"])

    l = LOANS[p]
    add(p, "balance_sheet", "loans_and_advances_gross", l["gross"], "GHS millions", l["src"], l["pg"],
        "reported" if l["gross"] is not None else "unavailable",
        BANKONLY + (" Gross loans and advances to customers (note 5.1)." if l["gross"] is not None
                    else " Not disclosed in the interim summary."))
    add(p, "balance_sheet", "loan_loss_allowance", l["allow"], "GHS millions", l["src"], l["pg"],
        "reported" if l["allow"] is not None else "unavailable",
        BANKONLY + (" Credit impairment allowance on loans (note 5.1); positive balance." if l["allow"] is not None
                    else " Not disclosed in the interim summary."))
    add(p, "balance_sheet", "x_interest_in_suspense", l["iis"], "GHS millions", l["src"], l["pg"],
        "reported" if l["iis"] is not None else "unavailable",
        BANKONLY + (" Interest in suspense (note 5.1); bridge: gross - allowance - interest in suspense = net." if l["iis"] not in (None, 0.0)
                    else (" Net = gross - allowance exactly in this filing; no separate interest in suspense." if l["iis"] == 0.0
                          else " FY2022 interest in suspense is unresolved in the filing; left unavailable rather than guessed.")))

    r = RATIO[p]
    add(p, "ratios", "car_pct", r["car"], "percent", r["src"], r["pg"], "reported", "Total capital adequacy ratio as reported.")
    add(p, "ratios", "tier1_pct", r["tier1"], "percent", r["src"], r["pg"], "reported", "Reported Common Equity Tier 1 ratio (note 5.1 basis).")
    add(p, "ratios", "npl_pct", r["npl"], "percent", r["src"], r["pg"], "reported",
        "Gross non-performing loan ratio as reported by the Bank (the AR narrative separately quotes the industry NPL).")

    c = CAP[p]
    nreg = "Bank-only (separate) statements; audited capital-adequacy note."
    for key, item, lab in [("t1","x_tier1_capital","Tier 1 capital."),("t2","x_tier2_capital","Tier 2 capital."),
                           ("cap","x_regulatory_capital","Total regulatory capital (Tier 1 + Tier 2)."),
                           ("rwa","x_risk_weighted_assets","Total risk-weighted assets.")]:
        add(p, "balance_sheet", item, c[key], "GHS millions", c["src"], c["pg"],
            "reported" if c[key] is not None else "unavailable", nreg + " " + lab)

    for item in ["ldr_pct", "cost_to_income_pct", "roe_pct", "roa_pct"]:
        add(p, "ratios", item, None, "percent", "", "", "unavailable",
            "Not disclosed as a ratio in the bank's summary statements; recomputable in checks.md where inputs exist.")

# FY2021 regulatory-basis loan detail (kept in balance_sheet as x_ rows; not deducted again).
add("FY2021", "balance_sheet", "x_regulatory_gross_loans", REG21["reg_gross"], "GHS millions", REG21["src"], REG21["pg"],
    "reported", "Regulatory-basis gross loans (risk note 30). The note 5.1 gross of 5,388.433m is already net of the "
    "78.277m interest in suspense below, so this is disclosed for transparency and NOT used to re-derive net loans.")
add("FY2021", "balance_sheet", "x_iis_regulatory", REG21["iis"], "GHS millions", REG21["src"], REG21["pg"],
    "reported", "Interest in suspense on the regulatory basis (risk note 30): 5,466.710 - 78.277 - 203.305 = 5,185.128 net.")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bank","period","statement","line_item","value","unit","source_id","page","status","notes"])
    w.writerows(rows)

print(f"wrote {OUT} rows={len(rows)}")
