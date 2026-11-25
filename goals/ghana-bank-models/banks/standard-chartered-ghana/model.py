#!/usr/bin/env python3
"""Forecast model for Standard Chartered Bank Ghana (bank-only, GHS millions). Standard library only.

Run:  python model.py          writes forecast.csv and checks.md in this folder.

Reads:  financials.csv (history, from build_financials.py)
        assumptions.json (owner estimates)
        ../../sector/macro-assumptions/macro.csv (shared macro drivers by scenario)
Every forecast number is an ESTIMATE. History is never changed.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, "assumptions.json"), encoding="utf-8"))
BANK = A["bank"]
YEARS = ["FY2026E", "FY2027E", "FY2028E", "FY2029E", "FY2030E"]
SCEN = ["base", "downside", "upside"]

# ---------------------------------------------------------------- inputs
hist = {}
for r in csv.DictReader(open(os.path.join(HERE, "financials.csv"), encoding="utf-8")):
    if r["value"] != "":
        hist[(r["period"], r["line_item"])] = float(r["value"])
H = lambda p, k: hist[(p, k)]

macro = {}
for r in csv.DictReader(open(os.path.join(HERE, A["macro_file"]), encoding="utf-8")):
    if r["value"] != "":
        macro[(r["scenario"], r["year"], r["driver"])] = float(r["value"])
M = lambda sc, y, d: macro[(sc, y, d)]

R, G, C, K, OB = A["rates"], A["growth"], A["credit"], A["capital_and_liquidity"], A["other_balance_sheet"]
LOAN_SPREAD = R["loan_yield_spread_over_tbill_364d_pct"]["value"] / 100
LIQ_SPREAD = R["liquid_yield_spread_over_tbill_91d_pct"]["value"] / 100
COF = R["cost_of_funds_to_policy_rate"]["value"]
TAX = R["tax_rate"]["value"]
FEE_EXP = G["fee_expense_to_fee_income"]["value"]
RES_T = K["statutory_reserve_transfer_of_profit"]["value"]
OPCASH = K["operating_cash_to_customer_deposits"]["value"]
DFB = K["due_from_banks_share_of_liquid_assets"]["value"]
RWD = K["risk_weight_density_of_total_assets"]["value"]

P9 = "9M-2026"
out = []   # forecast rows
chk = []   # check rows
state = {}


def emit(sc, per, stmt, item, val, note=""):
    out.append([BANK, sc, per, stmt, item, "" if val is None else f"{val:.3f}", "GHS millions" if not item.endswith("_pct") else "percent", "unavailable" if val is None else "estimated", note])


def run(sc):
    s = {}
    # ---------------------------------------------------- FY2026E anchored on 9M-2026
    f = 12 / 9
    s["ii"] = H(P9, "interest_income") * f
    s["ie"] = H(P9, "interest_expense") * f
    s["fee_i"] = H(P9, "fee_commission_income") * f
    s["fee_e"] = H(P9, "fee_commission_expense") * f
    s["nti"] = H(P9, "net_trading_income") * f
    s["oth"] = H(P9, "other_operating_income") * f
    s["staff"] = H(P9, "staff_costs") * f
    s["dep"] = H(P9, "depreciation_amortisation") * f
    s["othx"] = H(P9, "other_operating_expenses") * f
    s["imp"] = H(P9, "impairment_charge")
    s["div"] = 673.482
    prev = {}
    res = {}
    for i, y in enumerate(YEARS):
        infl = M(sc, y, "inflation_cpi_pct") / 100
        gdp = M(sc, y, "gdp_growth_pct") / 100
        pol = M(sc, y, "policy_rate_pct") / 100
        t91 = M(sc, y, "tbill_91d_pct") / 100
        t364 = M(sc, y, "tbill_364d_pct") / 100
        crr = M(sc, y, "crr_pct") / 100
        minc = M(sc, y, "min_car_pct")
        r = {}
        if i == 0:
            # balance sheet at 30 Sep 2026 carried forward; Q4 earnings added to equity
            r["loans"] = H(P9, "loans_and_advances_net")
            r["dep_c"] = H(P9, "customer_deposits")
            r["dep_b"] = H(P9, "due_to_banks")
            r["oth_l"] = H(P9, "other_liabilities")
            r["oth_a"] = H(P9, "other_assets")
            r["ppe"] = H(P9, "property_equipment_intangibles")
            ii, ie, fee_i, fee_e, nti, oth = s["ii"], s["ie"], s["fee_i"], s["fee_e"], s["nti"], s["oth"]
            staff, dep, othx, imp = s["staff"], s["dep"], s["othx"], s["imp"]
            div = s["div"]
            equity_open = H("FY2025", "total_equity")
        else:
            p = prev
            r["dep_c"] = p["dep_c"] * (1 + (1 + gdp) * (1 + infl) - 1 + G["customer_deposit_adjustment"][sc])
            g_dep = r["dep_c"] / p["dep_c"] - 1
            r["loans"] = p["loans"] * (1 + G["net_loan_growth"][sc][y])
            r["dep_b"] = p["dep_b"] * (1 + g_dep)
            r["oth_l"] = p["oth_l"] * (1 + infl)
            r["oth_a"] = p["oth_a"] * (1 + infl)
            r["ppe"] = p["ppe"]
            pol_prev = M(sc, YEARS[i - 1], "policy_rate_pct") / 100
            avg_loans = (p["loans"] + r["loans"]) / 2
            ii = (t364 + LOAN_SPREAD) * avg_loans + (t91 + LIQ_SPREAD) * p["liquid"]
            ie = COF * (pol_prev + pol) / 2 * ((p["dep_c"] + r["dep_c"]) / 2 + (p["dep_b"] + r["dep_b"]) / 2)
            fee_i = p["fee_i"] * (1 + infl + G["fee_income_growth_over_inflation"]["value"])
            fee_e = fee_i * FEE_EXP
            nti = p["nti"] * (1 + G["net_trading_income_growth"][sc])
            oth = p["oth"]
            staff = p["staff"] * (1 + infl + G["staff_cost_growth_over_inflation"]["value"])
            dep = p["dep"] * (1 + infl)
            othx = p["othx"] * (1 + infl + G["other_opex_growth_over_inflation"]["value"])
            imp = C["cost_of_risk_on_average_net_loans"][sc] * avg_loans
            div = K["dividend_payout_of_prior_year_profit"][sc] * p["pat"]
            equity_open = p["te"]
        nii = ii - ie
        opinc = nii + fee_i - fee_e + nti + oth
        pbt = opinc - imp - (staff + dep + othx)
        tax = H(P9,"income_tax") + TAX*max(0,pbt-H(P9,"profit_before_tax")) if i==0 else TAX*max(0,pbt)
        pat = pbt - tax
        stated = H(P9,"stated_capital")
        # Opening reserve 864.660 exceeds stated capital 400; actual YTD transfer zero.
        transfer = RES_T * max(0,pat)
        incpat = pat-H(P9,"profit_after_tax") if i==0 else pat
        res_other = (H(P9,"reserves_other") if i==0 else prev["res_other"]) + transfer
        tl = r["dep_c"] + r["dep_b"] + r["oth_l"]
        cash = (crr + OPCASH) * r["dep_c"]
        if i==0:
            te = H(P9,"total_equity") + incpat
            incdiv = 0.0
        else:
            incdiv = max(0,min(div,prev["retained"]+pat-transfer))
            te = equity_open+pat-incdiv
            # Hypothetical buffer and eligible cash screen, not a regulatory return.
            if te/(RWD*(tl+te))*100 < minc+2 or .7*cash < crr*r["dep_c"] or tl+te-cash-r["loans"]-r["oth_a"]-r["ppe"]<0:
                incdiv=0.0
                te=equity_open+pat
            div=incdiv
        retained=te-stated-res_other
        ta=tl+te
        liquid=ta-cash-r["loans"]-r["oth_a"]-r["ppe"]
        assert abs(minc-13)<1e-9
        r.update(dict(ii=ii, ie=ie, nii=nii, fee_i=fee_i, fee_e=fee_e, nti=nti, oth=oth, opinc=opinc, staff=staff, dep=dep, othx=othx,
                      imp=imp, pbt=pbt, tax=tax, pat=pat, div=div, te=te, stated=stated, res_other=res_other, retained=retained,
                      tl=tl, ta=ta, cash=cash, liquid=liquid, due=liquid * DFB, secs=liquid * (1 - DFB)))
        r["car_proxy"] = te / (RWD * ta) * 100
        r["min_car"] = minc
        r["transfer"] = transfer
        r["incdiv"] = incdiv
        r["reserve"] = (864.660 if i==0 else prev["reserve"])+transfer
        r["cash_gap_stress"] = max(0,crr*r["dep_c"]-.6*cash)
        r["roa"] = pat/((H("FY2025","total_assets") if i==0 else prev["ta"])+ta)*200
        r["ldr"] = r["loans"] / r["dep_c"] * 100
        r["cti"] = (staff + dep + othx) / opinc * 100
        prior_te = H("FY2025", "total_equity") if i == 0 else prev["te"]
        r["roe"] = pat / ((prior_te + te) / 2) * 100
        prev = r
        res[y] = r
    return res


def write_rows(sc, res):
    for y, r in res.items():
        IS, BS, RT = "income_statement", "balance_sheet", "ratios"
        note_is = "Estimate. FY2026E = actual 9M plus estimated Q4; actual 9M impairment/tax retained." if y == "FY2026E" else "Estimate from assumptions.json and the macro rows of this scenario."
        for item, key in [("interest_income", "ii"), ("interest_expense", "ie"), ("net_interest_income", "nii"), ("fee_commission_income", "fee_i"),
                          ("fee_commission_expense", "fee_e"), ("net_trading_income", "nti"), ("other_operating_income", "oth"),
                          ("total_operating_income", "opinc"), ("staff_costs", "staff"), ("depreciation_amortisation", "dep"),
                          ("other_operating_expenses", "othx"), ("impairment_charge", "imp"), ("profit_before_tax", "pbt"),
                          ("income_tax", "tax"), ("profit_after_tax", "pat")]:
            emit(sc, y, IS, item, r[key], note_is)
        emit(sc, y, IS, "x_dividends_paid", r["div"], "Actual YTD 673.482m, no further Q4 payout." if y=="FY2026E" else "Estimated payout after reserve transfer and retained earnings/capital/cash screens.")
        note_bs = "Estimate. FY2026E carries the 30 Sep 2026 balance sheet forward; equity adds Q4 profit." if y == "FY2026E" else "Estimate."
        for item, key in [("cash_and_bog_balances", "cash"), ("due_from_banks", "due"), ("investment_securities", "secs"), ("loans_and_advances_net", "loans"),
                          ("property_equipment_intangibles", "ppe"), ("other_assets", "oth_a"), ("total_assets", "ta"), ("customer_deposits", "dep_c"),
                          ("due_to_banks", "dep_b"), ("other_liabilities", "oth_l"), ("total_liabilities", "tl"), ("stated_capital", "stated"),
                          ("retained_earnings", "retained"), ("reserves_other", "res_other"), ("total_equity", "te")]:
            emit(sc, y, BS, item, r[key], note_bs + (" Due from banks and securities are the plug (liquid assets) split at the 30 Sep 2026 mix." if key in ("due", "secs") else ""))
        emit(sc, y, BS, "borrowings", 0.0, "None assumed.")
        emit(sc, y, RT, "x_car_proxy_pct", r["car_proxy"], "PROXY, not the regulatory ratio: book equity / (risk-weight density x total assets). Density is the 30 Sep 2026 implied value.")
        emit(sc, y, RT, "x_roe_pct", r["roe"], "Profit after tax / average of opening and closing equity.")
        emit(sc, y, RT, "x_cost_to_income_pct", r["cti"], "Operating expenses / operating income before impairment.")
        emit(sc, y, RT, "x_ldr_pct", r["ldr"], "Net loans / customer deposits.")
        for k in ("loans_and_advances_gross","loan_loss_allowance"):
            emit(sc,y,BS,k,None,"Separate gross/allowance unavailable; no fabricated forecast.")
        for k in ("car_pct","tier1_pct","npl_pct","ldr_pct"):
            emit(sc,y,RT,k,None,"Regulatory or gross basis unavailable; separate proxy or net LDR where available.")
        for k,v in (("roe_pct",r["roe"]),("roa_pct",r["roa"]),("cost_to_income_pct",r["cti"])):
            emit(sc,y,RT,k,v,"Estimated, average balance ROE/ROA or pre-impairment cost/income.")
        for k,v in (("x_statutory_reserve",r["reserve"]),("x_statutory_reserve_transfer",r["transfer"]),("x_cash_reserve_gap_60pct",r["cash_gap_stress"])):
            emit(sc,y,BS,k,v,"Nonadditive memo; statutory transfer internal, cash gap hypothetical.")
        emit(sc,y,IS,"x_incremental_dividend",r["incdiv"],"Q4 incremental payout zero; subsequent annual forecast.")
        emit(sc,y,BS,"x_capital_target_gap",max(0,(r["min_car"]+2)/100*RWD*r["ta"]-r["te"]),"15% management proxy target, not regulation.")



all_res = {sc: run(sc) for sc in SCEN}
for sc in SCEN:
    write_rows(sc, all_res[sc])

with open(os.path.join(HERE, "forecast.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bank", "scenario", "period", "statement", "line_item", "value", "unit", "status", "notes"])
    w.writerows(out)

# ---------------------------------------------------------------- checks
fails = 0
lines = ["# Checks: standard-chartered-ghana", "", "Generated by model.py. History checks are in `checks_history.md` (build_financials.py).", "",
         "## Forecast checks (all scenarios, all years)", "", "| Scenario | Year | Assets = liabilities + equity | Liquid assets >= 0 | Net interest income = II - IE | PAT = PBT - tax | CAR proxy vs minimum |", "| --- | --- | --- | --- | --- | --- | --- |"]
for sc in SCEN:
    for y, r in all_res[sc].items():
        bal = abs(r["ta"] - (r["tl"] + r["te"])) < 0.001
        sumA = abs(r["cash"] + r["due"] + r["secs"] + r["loans"] + r["ppe"] + r["oth_a"] - r["ta"]) < 0.001
        liq = r["liquid"] >= 0
        nii = abs(r["nii"] - (r["ii"] - r["ie"])) < 0.001
        pat = abs(r["pat"] - (r["pbt"] - r["tax"])) < 0.001
        car = r["car_proxy"] >= r["min_car"]
        extra = max(abs(r["te"]-r["stated"]-r["retained"]-r["res_other"]),abs(r["tl"]-r["dep_c"]-r["dep_b"]-r["oth_l"]),abs(r["opinc"]-r["nii"]-r["fee_i"]+r["fee_e"]-r["nti"]-r["oth"]),abs(r["pbt"]-r["opinc"]+r["staff"]+r["dep"]+r["othx"]+r["imp"]))
        ok = bal and sumA and liq and nii and pat and extra<.001 and r["transfer"]>=0 and (r["incdiv"]==0 or (r["retained"]>=0 and r["car_proxy"]>=15))
        assert ok,(sc,y,extra)
        fails += 0 if ok else 1
        lines.append(f"| {sc} | {y} | {'PASS' if bal and sumA else 'FAIL'} | {'PASS' if liq else 'FAIL'} | {'PASS' if nii else 'FAIL'} | {'PASS' if pat else 'FAIL'} | {r['car_proxy']:.1f}% vs {r['min_car']:.0f}% {'ok' if car else 'BELOW MINIMUM'} |")
lines += ["", f"Forecast failures: {fails}", "", "Additional equity/liability/TOI/PBT bridges and payout gates asserted for all 15 scenario-years.", "", "FY2026 retains actual 9M tax198.219m and taxes positive Q4 PBT at 34%; no Q4 payout. Annual 12.5% statutory reserve transfer, actual 9M transfer zero; internal equity only. Future payout tested against retained earnings, 15% proxy CAR and hypothetical 70%-eligible cash; no regulatory permission inferred.", "", "| Scenario | Year | Reserve transfer | Annual payout | 60%-eligible cash gap |", "|---|---|---:|---:|---:|"]
for sc in SCEN:
    for y,r in all_res[sc].items():
        lines.append(f"| {sc} | {y} | {r['transfer']:.3f} | {r['div']:.3f} | {r['cash_gap_stress']:.3f} |")
lines += [""]

# calibration line: does the yield formula reproduce 9M-2026 annualised interest income?
avg_loans = (H("FY2025", "loans_and_advances_net") + H(P9, "loans_and_advances_net")) / 2
liq_open = H("FY2025", "due_from_banks") + H("FY2025", "investment_securities")
t364_26 = macro[("base", "FY2026E", "tbill_364d_pct")] / 100
t91_26 = macro[("base", "FY2026E", "tbill_91d_pct")] / 100
formula_ii = (t364_26 + LOAN_SPREAD) * avg_loans + (t91_26 + LIQ_SPREAD) * liq_open
anch = H(P9, "interest_income") * 12 / 9
lines += ["## Calibration of the interest-income formula (honest disclosure)", "",
          f"- FY2026E interest income is **anchored** on 9M-2026 x 12/9 = {anch:,.1f}m.",
          f"- Applying the forward formula (364-day bill + {LOAN_SPREAD*100:.1f} pts on average loans, 91-day bill + {LIQ_SPREAD*100:.1f} pts on opening liquid assets) to FY2026E gives {formula_ii:,.1f}m, a difference of {formula_ii - anch:+,.1f}m ({(formula_ii/anch-1)*100:+.1f}%).",
          "- The spreads were chosen by me to land near the anchor, so this is a fit, not a validation. Forward years from FY2027E rely on them.", ""]

# scenario summary
lines += ["## Scenario summary (GHS millions)", "", "| Scenario | Year | Net interest income | Net trading income | Profit after tax | Total equity | CAR proxy | ROE |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
for sc in SCEN:
    for y, r in all_res[sc].items():
        lines.append(f"| {sc} | {y} | {r['nii']:,.0f} | {r['nti']:,.0f} | {r['pat']:,.0f} | {r['te']:,.0f} | {r['car_proxy']:.1f}% | {r['roe']:.1f}% |")
lines += ["", "## Spot checks of reported history against the filing text (done by the owner while building)", "",
          "1. FY2025 profit after tax 798,681 and total assets 16,502,639 (GH¢'000) match SCB-FY25 page 1. compared with the scraped text of the PDF.",
          "2. FY2021 total assets 10,120,576 matches SCB-FY21 page 1.",
          "3. 9M-2026 profit before tax 554,737 matches SCB-Q3-26 page 1.",
          "4. FY2023 restated profit after tax 814,747 matches SCB-FY24 page 1 (original 864,391 in SCB-FY23).",
          "", "These spot checks are by the same agent that extracted the data, so they are NOT independent. A different agent must repeat them (see the review request in the claim file)."]
with open(os.path.join(HERE, "checks.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("forecast rows:", len(out), "| forecast failures:", fails)
for sc in SCEN:
    r = all_res[sc]["FY2030E"]
    print(sc, "FY2030E PAT %.0f equity %.0f CARproxy %.1f ROE %.1f" % (r["pat"], r["te"], r["car_proxy"], r["roe"]))
