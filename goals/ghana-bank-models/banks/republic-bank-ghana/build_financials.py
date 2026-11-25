#!/usr/bin/env python3
"""Build goals/ghana-bank-models/banks/republic-bank-ghana/financials.csv
(bank-only / separate statements, GHS millions).

Sources (all official Republic Bank (Ghana) PLC filings, BANK/separate columns):
  RB21FS  2021 Audited Financial Statements  (income printed p.47, SoFP p.48,
          loans note 22 printed p.90, loan ratios 22h p.94, capital note p.151)
  RB23AR  2023 Annual Report  (income printed p.59, SoFP p.60, loans note p.104,
          loan ratios 22h p.110, capital note p.185)  -> FY2023 + FY2022 comparatives
  RB24AR  2024 Annual Report  (income printed p.66, SoFP p.67, loans note p.112,
          loan ratios 22h p.118, capital note p.194, 5-yr highlights p.18)
  RB25AR  2025 Annual Report (RFHL 2025 AR) (income/SCI printed p.76, SoFP p.77,
          loans note p.116, loan ratios 22h p.121, capital note p.189, 5-yr highlights p.35)
  RB26Q3  Q3-2026 unaudited summary  (income/BS/ratios printed pp.1-2)
  RB26Q2  Q2-2026 unaudited summary  (cross-check)
  RB24SUM 2024 audited summary       (cross-check)

Convention (MODEL-SPEC.md): costs/expenses/allowances stored POSITIVE; profits signed.
Bank (separate) column ONLY. The narrative "NET PROFIT" tables in the ARs are GROUP
level and are never used for the bank series; the Group column is used only as a
labelled cross-check and never mixed in.

Canonical buckets: the Bank reports extra asset components (pledged assets, investment
in subsidiaries, current and deferred tax assets, trading assets) that are folded into
other_assets, and intangibles folded into property_equipment_intangibles, so the
canonical asset bridge closes (cash + due_from_banks + investment_securities +
loans_net + ppe + other_assets = total_assets). The raw components are kept as
NONADDITIVE x_ memos. The income tax charge is stored as the TOTAL below-PBT charge
(levies + income tax expense = PBT - PAT) so PAT = PBT - income_tax holds; the levies
and the pure tax line are kept as x_ memos.
"""
import csv, os

BANK = "republic-bank-ghana"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "financials.csv")

# ---------------------------------------------------------------- income statement
# GHS thousands, BANK column. costs positive; impairment is a positive cost.
INC = {
 "FY2021": dict(src="RB21FS", pg="47", ii=467639, ie=180518, nii=287121,
   fci=50890, fce=2127, nt=27847, xfv=3572, ooi=7180, othinc=5487, toi=379970,
   imp=19549, staff=132464, lease=2793, da=21213, ooe=78302, pbt=125649,
   gsl=6260, fsr=4672, tax=33019, pat=81698),
 "FY2022": dict(src="RB23AR", pg="59", ii=604862, ie=234196, nii=370666,
   fci=52213, fce=1708, nt=34014, xfv=5098, ooi=18493, othinc=14807, toi=493583,
   imp=237662, staff=157498, lease=2374, da=24977, ooe=97177, pbt=-26105,
   gsl=0, fsr=0, tax=40732, pat=-66837),
 "FY2023": dict(src="RB24AR", pg="66", ii=947212, ie=420586, nii=526626,
   fci=66985, fce=3116, nt=55222, xfv=0, ooi=19164, othinc=13652, toi=678533,
   imp=66773, staff=196845, lease=767, da=32444, ooe=150154, pbt=231550,
   gsl=11577, fsr=11577, tax=77992, pat=130404),
 "FY2024": dict(src="RB24AR", pg="66", ii=1166325, ie=556098, nii=610227,
   fci=93477, fce=5075, nt=49924, xfv=3713, ooi=7376, othinc=10356, toi=769998,
   imp=31609, staff=237102, lease=2263, da=40381, ooe=162749, pbt=295894,
   gsl=14877, fsr=14877, tax=78438, pat=187702),
 "FY2025": dict(src="RB25AR", pg="76", ii=1246642, ie=538132, nii=708510,
   fci=107619, fce=5547, nt=55633, xfv=20070, ooi=21776, othinc=17650, toi=925711,
   imp=20696, staff=262116, lease=1415, da=54478, ooe=194156, pbt=392850,
   gsl=19642, fsr=19642, tax=98976, pat=254590),
 "9M-2026": dict(src="RB26Q3", pg="1", ii=725708, ie=283706, nii=442002,
   fci=91686, fce=4607, nt=49452, xfv=6742, ooi=7545, othinc=6608, toi=599428,
   imp=23987, staff=214092, lease=1098, da=43908, ooe=142089, pbt=174254,
   gsl=8935, fsr=8935, tax=37612, pat=118772),
 # 9M-2025 comparative column of RB26Q3 (bank).
 "9M-2025": dict(src="RB26Q3", pg="1", ii=901135, ie=392544, nii=508591,
   fci=73709, fce=4105, nt=45169, xfv=7865, ooi=16579, othinc=11679, toi=659487,
   imp=15000, staff=193183, lease=1100, da=39485, ooe=138616, pbt=272103,
   gsl=13458, fsr=13458, tax=68569, pat=176618),
}

# ---------------------------------------------------------------- balance sheet
# GHS thousands, BANK column. Component buckets defined so they sum to reported totals.
BS = {
 "FY2021": dict(src="RB21FS", pg="48", cash=946055, trading=17661, pledged=74406,
   fvoci=0, invsec=1243178, loans_net=1747995, subs=13543, cta=0, dta=19877,
   intang=9150, oth=17273, ppe=137121, ta=4226259,
   dep_banks=45016, dep_cust=3165079, borrow=136606, ctax=1078, dtl=9957,
   bonds=80849, othl=97742, tl=3536327,
   stated=401191, inesurp=24372, statres=192325, reval=24852, regcrr=46448,
   housing=744, te=689932),
 "FY2022": dict(src="RB23AR", pg="60", cash=1759927, trading=0, pledged=34148,
   fvoci=11185, invsec=1015786, loans_net=1958017, subs=13543, cta=14009, dta=26360,
   intang=6143, oth=22762, ppe=218412, ta=5080292,
   dep_banks=0, dep_cust=4090281, borrow=88123, ctax=0, dtl=24743,
   bonds=81681, othl=133940, tl=4418768,
   stated=401191, inesurp=-192890, statres=192325, reval=63281, regcrr=196873,
   housing=744, te=661524),
 # FY2023 balance sheet here is the RESTATED figure in the FY2024 report (DTA/DTL netting);
 # the 5-year summary total assets 6,924,025 matches the restated set. See sources.md.
 "FY2023": dict(src="RB24AR", pg="67", cash=2985556, trading=0, pledged=101019,
   fvoci=0, invsec=1065451, loans_net=2429756, subs=13543, cta=0, dta=4345,
   intang=9139, oth=27118, ppe=288098, ta=6924025,
   dep_banks=0, dep_cust=5868216, borrow=0, ctax=4014, dtl=0,
   bonds=81748, othl=178119, tl=6132097,
   stated=401191, inesurp=-143246, statres=257527, reval=63281, regcrr=212431,
   housing=744, te=791928),
 "FY2024": dict(src="RB24AR", pg="67", cash=4470741, trading=0, pledged=55403,
   fvoci=0, invsec=1591526, loans_net=3054049, subs=13543, cta=0, dta=3546,
   intang=10119, oth=46932, ppe=298737, ta=9544596,
   dep_banks=0, dep_cust=6114923, borrow=1732880, ctax=2575, dtl=0,
   bonds=81587, othl=633001, tl=8564966,
   stated=401191, inesurp=-20970, statres=304453, reval=63281, regcrr=230931,
   housing=744, te=979630),
 "FY2025": dict(src="RB25AR", pg="77", cash=6033188, trading=0, pledged=2140606,
   fvoci=0, invsec=251611, loans_net=3457667, subs=13543, cta=0, dta=7025,
   intang=13098, oth=33126, ppe=315149, ta=12265013,
   dep_banks=0, dep_cust=8368068, borrow=2091662, ctax=14860, dtl=0,
   bonds=81604, othl=474599, tl=11030793,
   stated=401191, inesurp=159229, statres=368101, reval=63281, regcrr=241674,
   housing=744, te=1234220),
 "9M-2026": dict(src="RB26Q3", pg="1", cash=3454660, trading=0, pledged=2801480,
   fvoci=0, invsec=849667, loans_net=4027925, subs=13543, cta=0, dta=7025,
   intang=13077, oth=141930, ppe=322580, ta=11631887,
   dep_banks=0, dep_cust=7222033, borrow=2767292, ctax=3965, dtl=0,
   bonds=77773, othl=250430, tl=10321493,
   stated=401191, inesurp=235403, statres=368101, reval=63281, regcrr=241674,
   housing=744, te=1310394),
 # 9M-2025 comparative column of RB26Q3 (bank).
 "9M-2025": dict(src="RB26Q3", pg="1", cash=4024490, trading=0, pledged=1790105,
   fvoci=0, invsec=230520, loans_net=3121579, subs=13542, cta=0, dta=3546,
   intang=10119, oth=274888, ppe=301175, ta=9769964,
   dep_banks=0, dep_cust=6105572, borrow=1790105, ctax=40605, dtl=0,
   bonds=81523, othl=595911, tl=8613716,
   stated=401191, inesurp=120243, statres=304453, reval=63281, regcrr=266336,
   housing=744, te=1156248),
}

# ---------------------------------------------------------------- loan detail (BANK)
# gross carrying amount and ECL allowance from loans note 22 (bank / group are identical).
LOANS = {
 "FY2021": dict(src="RB21FS", pg="90", gross=1892387, allow=144392),
 "FY2022": dict(src="RB23AR", pg="104", gross=2144579, allow=186562),
 "FY2023": dict(src="RB24AR", pg="112", gross=2639491, allow=209735),
 "FY2024": dict(src="RB24AR", pg="112", gross=3264377, allow=210328),
 "FY2025": dict(src="RB25AR", pg="116", gross=3690495, allow=232828),
 "9M-2026": dict(src=None, pg="", gross=None, allow=None),
 "9M-2025": dict(src=None, pg="", gross=None, allow=None),
}

# ---------------------------------------------------------------- reported ratios
RATIO = {
 "FY2021": dict(src="RB21FS", pg="151", car=27.63, car_note="Capital adequacy ratio 27.63% at 31 Dec 2021 per the audited capital-management note (printed p.151); Tier 1/RWA 25.63%.", npl=15.32, npl_pg="94"),
 "FY2022": dict(src="RB23AR", pg="185", car=21.25, car_note="Capital adequacy ratio 21.25% at 31 Dec 2022 per the audited capital-management note (printed p.185); Tier 1/RWA 18.25%. DDEP reliefs applied from 2022.", npl=19.85, npl_pg="110"),
 "FY2023": dict(src="RB24AR", pg="194", car=19.24, car_note="Capital adequacy ratio 19.24% at 31 Dec 2023 per the audited capital-management note (printed p.194); Tier 1/RWA 16.24%. On the BoG DDEP-relief basis (minimum held at 10%).", npl=15.95, npl_pg="118"),
 "FY2024": dict(src="RB24AR", pg="194", car=18.20, car_note="Capital adequacy ratio 18.20% at 31 Dec 2024 per the audited capital-management note (printed p.194); Tier 1/RWA 15.65%. On the BoG DDEP-relief basis (minimum held at 10%).", npl=15.64, npl_pg="118"),
 "FY2025": dict(src="RB25AR", pg="189", car=20.15, car_note="Capital adequacy ratio 20.15% at 31 Dec 2025 per the audited capital-management note (printed p.189); Tier 1/RWA 18.15%. Regulatory forbearances were withdrawn in December 2025, so FY2025 is stated WITHOUT the reliefs.", npl=14.15, npl_pg="121"),
 "9M-2026": dict(src="RB26Q3", pg="2", car=17.83, car_note="Capital adequacy ratio (CRD) 17.83% at 30 Sep 2026 (unaudited quantitative disclosures, printed p.2); NPL 11.60%, liquidity ratio 104.86%, leverage ratio 7.21%.", npl=11.60, npl_pg="2"),
 # 9M-2025 comparative column of RB26Q3.
 "9M-2025": dict(src="RB26Q3", pg="2", car=16.75, car_note="Capital adequacy ratio (CRD) 16.75% at 30 Sep 2025 (comparative quantitative disclosures); NPL 16.49%, liquidity ratio 121.23%, leverage ratio 6.32%.", npl=16.49, npl_pg="2"),
}

# ------------------------------------------------- regulatory capital (BANK), GHS thousands
CAP = {
 "FY2021": dict(src="RB21FS", pg="151", t1=585679, t2=45705, cap=631384, rwa=2285257, t1_pct=25.63),
 "FY2022": dict(src="RB23AR", pg="185", t1=482402, t2=80099, cap=562501, rwa=2669957, t1_pct=18.25),
 "FY2023": dict(src="RB24AR", pg="194", t1=564520, t2=104302, cap=668822, rwa=3476721, t1_pct=16.24),
 "FY2024": dict(src="RB24AR", pg="194", t1=695947, t2=113229, cap=809176, rwa=4446499, t1_pct=15.65),
 "FY2025": dict(src="RB25AR", pg="189", t1=882894, t2=97281, cap=980175, rwa=4864037, t1_pct=18.15),
 "9M-2026": dict(src=None, pg=None, t1=None, t2=None, cap=None, rwa=None, t1_pct=None),
 "9M-2025": dict(src=None, pg=None, t1=None, t2=None, cap=None, rwa=None, t1_pct=None),
}

PERIODS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025", "9M-2025", "9M-2026"]
BANKONLY = "Bank-only (separate) statements; costs/allowances positive, profits signed."

rows = []
def add(period, statement, line_item, value, unit, source_id, page, status, notes):
    # Raw inputs above are GHS thousands (as printed); convert to GHS millions.
    if value is not None and unit == "GHS millions":
        value = value / 1000.0
    rows.append([BANK, period, statement, line_item,
                 "" if value is None else f"{value:.6f}".rstrip("0").rstrip("."),
                 unit, source_id or "", page or "", status, notes])

for p in PERIODS:
    d = INC[p]
    # core income item -> (source key, canonical key)
    core = [("ii","interest_income"),("ie","interest_expense"),("nii","net_interest_income"),
            ("fci","fee_commission_income"),("fce","fee_commission_expense"),
            ("nt","net_trading_income"),("toi","total_operating_income"),
            ("staff","staff_costs"),("da","depreciation_amortisation"),
            ("imp","impairment_charge"),("pbt","profit_before_tax")]
    for key, item in core:
        add(p, "income_statement", item, d[key], "GHS millions", d["src"], d["pg"], "reported", BANKONLY)
    # other_operating_expenses = lease expenses + other expenses (both reported cost lines)
    add(p, "income_statement", "other_operating_expenses", (d["lease"] + d["ooe"]), "GHS millions",
        d["src"], d["pg"], "derived",
        BANKONLY + " Operating lease expenses plus other expenses, as reported.")
    # canonical other_operating_income folds FVTPL income, other operating income and other income
    ooi = d["xfv"] + d["ooi"] + d["othinc"]
    add(p, "income_statement", "other_operating_income", ooi, "GHS millions", d["src"], d["pg"],
        "derived", BANKONLY + " Net income from investments at fair value through P&L plus other operating income plus other income; folded so the operating-income bridge closes.")
    add(p, "income_statement", "x_fv_other_income", d["xfv"], "GHS millions", d["src"], d["pg"],
        "reported" if d["xfv"] else "reported",
        BANKONLY + " Net income from financial instruments carried at fair value through P&L. Memo only; already folded into canonical other_operating_income, so do not add again.")
    add(p, "income_statement", "x_other_income", d["othinc"], "GHS millions", d["src"], d["pg"], "reported",
        BANKONLY + " The Bank's separate 'Other income' line. Memo only; already folded into canonical other_operating_income, so do not add again.")
    # income tax stored as TOTAL below-PBT charge so PAT = PBT - income_tax holds.
    total_tax = d["gsl"] + d["fsr"] + d["tax"]
    add(p, "income_statement", "income_tax", total_tax, "GHS millions", d["src"], d["pg"], "derived",
        BANKONLY + " Total below-profit-before-tax charge: growth & sustainability levy plus financial sector recovery levy plus income tax expense (PBT - PAT). The levies and the pure tax line are kept as x_ memos for the tax fork.")
    add(p, "income_statement", "profit_after_tax", d["pat"], "GHS millions", d["src"], d["pg"], "reported", BANKONLY)
    add(p, "income_statement", "x_growth_sustainability_levy", d["gsl"], "GHS millions", d["src"], d["pg"],
        "reported", BANKONLY + " Growth and Sustainability Levy, reported separately below profit before tax.")
    add(p, "income_statement", "x_financial_sector_recovery_levy", d["fsr"], "GHS millions", d["src"], d["pg"],
        "reported", BANKONLY + " Financial Sector Recovery Levy, reported separately below profit before tax.")
    add(p, "income_statement", "x_income_tax_expense", d["tax"], "GHS millions", d["src"], d["pg"],
        "reported", BANKONLY + " Income tax expense line as reported (excludes the two levies).")

    b = BS[p]
    def rep(item, val, extra=""):
        add(p, "balance_sheet", item, val, "GHS millions", b["src"], b["pg"], "reported",
            BANKONLY + (" " + extra if extra else ""))
    rep("cash_and_bog_balances", b["cash"])
    add(p, "balance_sheet", "due_from_banks", None, "GHS millions", b["src"], b["pg"], "unavailable",
        "The Bank reports no separate asset-side 'due from banks' balance in the summary statements; interbank assets sit inside cash and cash equivalents. Deposits from banks (a liability) appear as due_to_banks where reported.")
    if b["trading"]:
        add(p, "balance_sheet", "x_trading_assets", b["trading"], "GHS millions", b["src"], b["pg"], "reported",
            BANKONLY + " Non-pledged trading assets. Memo only; already folded into canonical other_assets, so do not add again.")
    else:
        add(p, "balance_sheet", "x_trading_assets", None, "GHS millions", b["src"], b["pg"], "unavailable", "No non-pledged trading assets reported.")
    inv = (b["fvoci"] or 0) + (b["invsec"] or 0)
    add(p, "balance_sheet", "investment_securities", inv, "GHS millions", b["src"], b["pg"], "derived",
        "Investment securities at FVOCI plus investment securities at amortised cost, as reported. Pledged investment securities are NOT included here; they are folded into other_assets (see x_pledged_assets).")
    add(p, "balance_sheet", "x_pledged_assets", b["pledged"], "GHS millions", b["src"], b["pg"], "reported",
        BANKONLY + " Pledged assets (investment securities pledged as collateral). Memo only; already folded into canonical other_assets, so do not add again.")
    rep("loans_and_advances_net", b["loans_net"])
    if b["subs"] is not None:
        add(p, "balance_sheet", "x_investment_in_subsidiaries", b["subs"], "GHS millions", b["src"], b["pg"], "reported",
            BANKONLY + " Investment in subsidiaries (Republic Investments, Securities, Boafo, HFC Realty, HFC Venture Capital, Republic Trust). Memo only; already folded into canonical other_assets, so do not add again.")
    else:
        add(p, "balance_sheet", "x_investment_in_subsidiaries", None, "GHS millions", b["src"], b["pg"], "unavailable", "No investment in subsidiaries reported.")
    if b["cta"]:
        add(p, "balance_sheet", "x_current_tax_assets", b["cta"], "GHS millions", b["src"], b["pg"], "reported",
            BANKONLY + " Current tax assets. Memo only; already folded into canonical other_assets, so do not add again.")
    else:
        add(p, "balance_sheet", "x_current_tax_assets", None, "GHS millions", b["src"], b["pg"], "unavailable", "No current tax asset reported.")
    # canonical other_assets folds other assets + deferred/current tax assets + investment in
    # subsidiaries + pledged assets + trading assets so the asset bridge closes.
    oth = ((b["oth"] or 0) + (b["dta"] or 0) + (b["cta"] or 0) + (b["subs"] or 0)
           + (b["pledged"] or 0) + (b["trading"] or 0))
    add(p, "balance_sheet", "other_assets", oth, "GHS millions", b["src"], b["pg"], "derived",
        "Other assets plus deferred and current tax assets, investment in subsidiaries, pledged assets and trading assets, as reported.")
    ppe = (b["ppe"] or 0) + (b["intang"] or 0)
    add(p, "balance_sheet", "property_equipment_intangibles", ppe, "GHS millions", b["src"], b["pg"], "derived",
        "Property and equipment plus intangible assets and goodwill, as reported.")
    rep("total_assets", b["ta"])
    rep("customer_deposits", b["dep_cust"])
    rep("due_to_banks", b["dep_banks"])
    rep("borrowings", b["borrow"])
    othl = (b["othl"] or 0) + (b["ctax"] or 0) + (b["dtl"] or 0) + (b["bonds"] or 0)
    add(p, "balance_sheet", "other_liabilities", othl, "GHS millions", b["src"], b["pg"], "derived",
        "Other liabilities plus current/deferred tax liabilities plus bonds, as reported.")
    rep("total_liabilities", b["tl"])
    rep("stated_capital", b["stated"])
    rep("retained_earnings", b["inesurp"])
    res = (b["statres"] or 0) + (b["reval"] or 0) + (b["regcrr"] or 0) + (b["housing"] or 0)
    add(p, "balance_sheet", "reserves_other", res, "GHS millions", b["src"], b["pg"], "derived",
        "Statutory reserve fund plus revaluation reserve plus regulatory credit risk reserve plus housing development assistance reserve, as reported.")
    rep("total_equity", b["te"])

    l = LOANS[p]
    add(p, "balance_sheet", "loans_and_advances_gross", l["gross"], "GHS millions", l["src"], l["pg"],
        "reported" if l["gross"] is not None else "unavailable",
        BANKONLY + (" Gross loans and advances at amortised cost (loans note 22)." if l["gross"] is not None else " Not disclosed in the interim summary."))
    add(p, "balance_sheet", "loan_loss_allowance", l["allow"], "GHS millions", l["src"], l["pg"],
        "reported" if l["allow"] is not None else "unavailable",
        BANKONLY + (" ECL allowance on loans and advances (loans note 22c); positive balance." if l["allow"] is not None else " Not disclosed in the interim summary."))

    if p == "9M-2026":
        add(p, "balance_sheet", "x_ytd_dividends", 42598, "GHS millions", "RB26Q3", "1", "reported",
            "Dividend paid in the nine months to 30 September 2026 (statement of changes in equity, bank).")
    elif p == "9M-2025":
        add(p, "balance_sheet", "x_ytd_dividends", 0, "GHS millions", "RB26Q3", "1", "reported",
            "No dividend paid in the nine months to 30 September 2025 (comparative statement of changes in equity, bank).")

    r = RATIO[p]
    add(p, "ratios", "car_pct", r["car"], "percent", r["src"], r["pg"], "reported", r["car_note"])
    add(p, "ratios", "npl_pct", r["npl"], "percent", r["src"], r["npl_pg"], "reported",
        "Gross non-performing loans ratio as reported.")

    c = CAP[p]
    nreg = "Bank-only (separate) statements; capital-management note."
    add(p, "balance_sheet", "x_tier1_capital", c["t1"], "GHS millions", c["src"], c["pg"],
        "reported" if c["t1"] is not None else "unavailable", nreg + " Tier 1 regulatory capital.")
    add(p, "balance_sheet", "x_tier2_capital", c["t2"], "GHS millions", c["src"], c["pg"],
        "reported" if c["t2"] is not None else "unavailable", nreg + " Tier 2 regulatory capital.")
    add(p, "balance_sheet", "x_total_regulatory_capital", c["cap"], "GHS millions", c["src"], c["pg"],
        "reported" if c["cap"] is not None else "unavailable", nreg + " Total regulatory capital (Tier 1 + Tier 2).")
    add(p, "balance_sheet", "x_risk_weighted_assets", c["rwa"], "GHS millions", c["src"], c["pg"],
        "reported" if c["rwa"] is not None else "unavailable", nreg + " Total risk-weighted assets.")
    add(p, "ratios", "tier1_pct", c["t1_pct"], "percent", c["src"], c["pg"],
        "reported" if c["t1_pct"] is not None else "unavailable",
        nreg + " Tier 1 / RWA as reported. The Bank discloses Tier 1 (which is predominantly CET1) rather than a separate CET1 ratio, so this is used as tier1_pct.")

    for item in ["ldr_pct", "cost_to_income_pct", "roe_pct", "roa_pct"]:
        add(p, "ratios", item, None, "percent", "", "", "unavailable",
            "Not disclosed as a ratio in the Bank's summary statements; recomputed from the numbers in checks.md.")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bank","period","statement","line_item","value","unit","source_id","page","status","notes"])
    w.writerows(rows)

print(f"wrote {OUT} rows={len(rows)}")
