#!/usr/bin/env python3
"""Forecast model for Guaranty Trust Bank (Ghana) Ltd (GHS millions). Standard library only.

Run:  python model.py          writes forecast.csv and checks.md in this folder.

Reads:  financials.csv (history), assumptions.json (owner estimates), ../../sector/macro-assumptions/macro.csv (shared macro, by scenario)
Every forecast number is an ESTIMATE. History is never changed.
Design lessons applied from the CalBank review: FY2026E is anchored on 9M-2026; interest legs are calibrated and disclosed;
growth is linked to macro nominal GDP and inflation; the capital proxy is calibrated to the reported ratio and out-of-sample tested.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, "assumptions.json"), encoding="utf-8"))
BANK = A["bank"]
YEARS = ["FY2026E", "FY2027E", "FY2028E", "FY2029E", "FY2030E"]
SCEN = ["base", "downside", "upside"]

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

R, G, C, K = A["rates"], A["growth"], A["credit"], A["capital_and_liquidity"]
LOAN_SPREAD = R["loan_yield_spread_over_tbill_364d_pct"]["value"] / 100
LIQ_SPREAD = R["liquid_yield_spread_over_tbill_364d_pct"]["value"] / 100
COF = R["cost_of_deposits_to_policy_rate"]["value"]
TAX = R["tax_rate"]["value"]
FEE_EXP = G["fee_expense_to_fee_income"]["value"]
RES_T = K["statutory_reserve_transfer_of_profit"]["value"]
OPCASH = K["operating_cash_to_customer_deposits"]["value"]
RW_L, RW_O = K["risk_weight_on_net_loans"]["value"], K["risk_weight_on_other_assets"]["value"]
BUF = K["capital_buffer_over_minimum_pp"]["value"]
LDR_CAP = 0.60
P9 = "9M-2026"
out = []


def emit(sc, per, stmt, item, val, note=""):
    out.append([BANK, sc, per, stmt, item, f"{val:.3f}", "percent" if item.endswith("_pct") else "GHS millions", "estimated", note])


def run(sc):
    res, prev = {}, {}
    f = 12 / 9
    for i, y in enumerate(YEARS):
        infl, gdp = M(sc, y, "inflation_cpi_pct") / 100, M(sc, y, "gdp_growth_pct") / 100
        pol, t364 = M(sc, y, "policy_rate_pct") / 100, M(sc, y, "tbill_364d_pct") / 100
        crr, minc = M(sc, y, "crr_pct") / 100, M(sc, y, "min_car_pct")
        r = {}
        if i == 0:
            r["loans"], r["dep"] = H(P9, "loans_and_advances_net"), H(P9, "customer_deposits")
            r["oth_l"], r["oth_a"], r["ppe"] = H(P9, "other_liabilities"), H(P9, "other_assets"), H(P9, "property_equipment_intangibles")
            ii, ie = H(P9, "interest_income") * f, H(P9, "interest_expense") * f
            fee_i, fee_e = H(P9, "fee_commission_income") * f, H(P9, "fee_commission_expense") * f
            nti, oth = H(P9, "net_trading_income") * f, H(P9, "other_operating_income") * f
            staff, dep_, othx = H(P9, "staff_costs") * f, H(P9, "depreciation_amortisation") * f, H(P9, "other_operating_expenses") * f
            imp, div = H(P9, "impairment_charge") * f, 604.370
        else:
            p = prev
            sp = G["customer_deposit_growth"]["spread"][sc][y]
            r["dep"] = p["dep"] * (1 + (1 + gdp) * (1 + infl) - 1 + sp)
            g_loan = G["net_loan_growth"]["rate"][sc][y]
            r["loans"] = min(p["loans"] * (1 + g_loan), LDR_CAP * r["dep"])
            r["oth_l"], r["oth_a"], r["ppe"] = p["oth_l"] * (1 + infl), p["oth_a"] * (1 + infl), p["ppe"]
            pol_prev = M(sc, YEARS[i - 1], "policy_rate_pct") / 100
            avg_loans = (p["loans"] + r["loans"]) / 2
            ii = (t364 + LOAN_SPREAD) * avg_loans + (t364 + LIQ_SPREAD) * p["earning_liquid"]
            ie = COF * (pol_prev + pol) / 2 * (p["dep"] + r["dep"]) / 2
            fee_i = p["fee_i"] * (1 + infl + G["fee_income_growth_over_inflation"]["value"])
            fee_e = fee_i * FEE_EXP
            nti = p["nti"] * (1 + G["net_trading_income_growth"][sc])
            oth = p["oth"]
            staff = p["staff"] * (1 + infl + G["staff_cost_growth_over_inflation"]["value"])
            dep_ = p["dep_"] * (1 + infl)
            othx = p["othx"] * (1 + infl + G["other_opex_growth_over_inflation"]["value"])
            imp = C["cost_of_risk_on_average_net_loans"][sc] * avg_loans
            div = K["dividend_payout_of_prior_year_profit"][sc] * p["pat"]
        nii = ii - ie
        opinc = nii + fee_i - fee_e + nti + oth
        pbt = opinc - imp - (staff + dep_ + othx)
        tax = TAX * pbt if pbt > 0 else 0.0
        pat = pbt - tax
        if i == 0:
            q4 = pat - H(P9, "profit_after_tax")
            te = H(P9, "total_equity") + q4
            res_other = H(P9, "reserves_other") + RES_T * q4
        else:
            te = prev["te"] + pat - div
            res_other = prev["res_other"] + RES_T * pat
        stated = H(P9, "stated_capital")
        ta = r["dep"] + r["oth_l"] + te
        liquid = ta - r["loans"] - r["oth_a"] - r["ppe"]
        cash = (crr + OPCASH) * r["dep"]
        secs = liquid - cash
        rwa = RW_L * r["loans"] + RW_O * (ta - r["loans"])
        car = te / rwa * 100
        # dividends are limited by the capital buffer (checked after the fact and flagged, never silently altered)
        r.update(dict(ii=ii, ie=ie, nii=nii, fee_i=fee_i, fee_e=fee_e, nti=nti, oth=oth, opinc=opinc, staff=staff, dep_=dep_, othx=othx,
                      imp=imp, pbt=pbt, tax=tax, pat=pat, div=div, te=te, stated=stated, res_other=res_other, retained=te - stated - res_other,
                      ta=ta, tl=r["dep"] + r["oth_l"], cash=cash, secs=secs, liquid=liquid, earning_liquid=liquid - crr * r["dep"],
                      car=car, min_car=minc, ldr=r["loans"] / r["dep"] * 100, cti=(staff + dep_ + othx) / opinc * 100))
        prior_te = H("FY2025", "total_equity") if i == 0 else prev["te"]
        r["roe"] = pat / ((prior_te + te) / 2) * 100
        prev = r
        res[y] = r
    return res


all_res = {sc: run(sc) for sc in SCEN}
for sc in SCEN:
    for y, r in all_res[sc].items():
        n_is = "Estimate. FY2026E = 9M-2026 x 12/9 (see assumptions.json)." if y == "FY2026E" else "Estimate from assumptions.json and the macro rows of this scenario."
        for item, key in [("interest_income", "ii"), ("interest_expense", "ie"), ("net_interest_income", "nii"), ("fee_commission_income", "fee_i"),
                          ("fee_commission_expense", "fee_e"), ("net_trading_income", "nti"), ("other_operating_income", "oth"),
                          ("total_operating_income", "opinc"), ("staff_costs", "staff"), ("depreciation_amortisation", "dep_"),
                          ("other_operating_expenses", "othx"), ("impairment_charge", "imp"), ("profit_before_tax", "pbt"),
                          ("income_tax", "tax"), ("profit_after_tax", "pat")]:
            emit(sc, y, "income_statement", item, r[key], n_is)
        emit(sc, y, "income_statement", "x_dividends_paid", r["div"], "Dividends paid in the year. FY2026E is the 604.370m actually paid in 9M-2026.")
        n_bs = "Estimate. FY2026E carries the 30 Sep 2026 balance sheet forward; equity adds Q4 profit." if y == "FY2026E" else "Estimate."
        for item, key in [("cash_and_bog_balances", "cash"), ("investment_securities", "secs"), ("loans_and_advances_net", "loans"), ("property_equipment_intangibles", "ppe"),
                          ("other_assets", "oth_a"), ("total_assets", "ta"), ("customer_deposits", "dep"), ("other_liabilities", "oth_l"), ("total_liabilities", "tl"),
                          ("stated_capital", "stated"), ("retained_earnings", "retained"), ("reserves_other", "res_other"), ("total_equity", "te")]:
            emit(sc, y, "balance_sheet", item, r[key], n_bs + (" Securities are the plug (liquid assets less cash and the central-bank reserve)." if key == "secs" else ""))
        for item in ("due_from_banks", "due_to_banks", "borrowings"):
            emit(sc, y, "balance_sheet", item, 0.0, "None assumed; no such line is printed.")
        emit(sc, y, "ratios", "x_car_proxy_pct", r["car"], "PROXY, not the regulatory ratio: book equity / (100% x loans + 38.1% x other assets), calibrated to the reported 24.08% at 30 Sep 2026.")
        emit(sc, y, "ratios", "x_roe_pct", r["roe"], "Profit after tax / average of opening and closing equity.")
        emit(sc, y, "ratios", "x_cost_to_income_pct", r["cti"], "Operating expenses / operating income before impairment.")
        emit(sc, y, "ratios", "x_ldr_pct", r["ldr"], "Net loans / customer deposits.")
with open(os.path.join(HERE, "forecast.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["bank", "scenario", "period", "statement", "line_item", "value", "unit", "status", "notes"])
    w.writerows(out)

# ---------------------------------------------------------------- checks
fails = 0
lines = ["# Checks: gtbank-ghana", "", "Generated by model.py. History checks are in `checks_history.md` (build_financials.py).", "",
         "## Forecast checks (all scenarios, all years)", "", "| Scenario | Year | Assets = liabilities + equity | Securities plug >= 0 | NII = II - IE | PAT = PBT - tax | CAR proxy vs minimum (+5pt buffer) | Dividend / PAT |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
for sc in SCEN:
    for y, r in all_res[sc].items():
        bal = abs(r["ta"] - (r["tl"] + r["te"])) < 0.001 and abs(r["cash"] + r["secs"] + r["loans"] + r["ppe"] + r["oth_a"] - r["ta"]) < 0.001
        sec = r["secs"] >= 0
        nii = abs(r["nii"] - (r["ii"] - r["ie"])) < 0.001
        pat = abs(r["pat"] - (r["pbt"] - r["tax"])) < 0.001
        ok = bal and sec and nii and pat
        fails += 0 if ok else 1
        flag = "ok" if r["car"] >= r["min_car"] + BUF else ("above minimum, inside buffer" if r["car"] >= r["min_car"] else "BELOW MINIMUM")
        lines.append(f"| {sc} | {y} | {'PASS' if bal else 'FAIL'} | {'PASS' if sec else 'FAIL'} | {'PASS' if nii else 'FAIL'} | {'PASS' if pat else 'FAIL'} | {r['car']:.1f}% vs {r['min_car']:.0f}% {flag} | {r['div'] / r['pat'] * 100:.0f}% |" if r["pat"] else f"| {sc} | {y} | {'PASS' if bal else 'FAIL'} | {'PASS' if sec else 'FAIL'} | {'PASS' if nii else 'FAIL'} | {'PASS' if pat else 'FAIL'} | {r['car']:.1f}% | n/a |")
lines += ["", f"Forecast failures: {fails}", ""]
# calibration disclosure
t364 = M("base", "FY2026E", "tbill_364d_pct") / 100
avg_loans = (H("FY2025", "loans_and_advances_net") + H(P9, "loans_and_advances_net")) / 2
eq_open = H("FY2025", "cash_and_bog_balances") + H("FY2025", "investment_securities") - 0.20 * H("FY2025", "customer_deposits")
formula_ii = (t364 + LOAN_SPREAD) * avg_loans + (t364 + LIQ_SPREAD) * eq_open
anch = H(P9, "interest_income") * 12 / 9
pol26, pol25 = M("base", "FY2026E", "policy_rate_pct") / 100, 0.18
formula_ie = COF * (pol25 + pol26) / 2 * (H("FY2025", "customer_deposits") + H(P9, "customer_deposits")) / 2
anch_ie = H(P9, "interest_expense") * 12 / 9
car_fy25 = H("FY2025", "total_equity") / (RW_L * H("FY2025", "loans_and_advances_net") + RW_O * (H("FY2025", "total_assets") - H("FY2025", "loans_and_advances_net"))) * 100
car_9m = H(P9, "total_equity") / (RW_L * H(P9, "loans_and_advances_net") + RW_O * (H(P9, "total_assets") - H(P9, "loans_and_advances_net"))) * 100
lines += ["## Calibration tests against reported data (honest disclosure)", "",
          f"- **Interest income.** FY2026E is anchored on 9M-2026 x 12/9 = {anch:,.1f}m. The forward formula (364-day bill + {LOAN_SPREAD*100:.1f} pts on average loans, 364-day bill + {LIQ_SPREAD*100:.1f} pts on opening earning liquid assets) gives {formula_ii:,.1f}m for FY2026E, a difference of {(formula_ii/anch-1)*100:+.1f}%. The spreads were chosen to land near the anchor, so this is a fit and not a validation.",
          f"- **Interest expense.** Anchor {anch_ie:,.1f}m; formula {formula_ie:,.1f}m ({(formula_ie/anch_ie-1)*100:+.1f}%), same caveat.",
          f"- **Capital ratio proxy.** Calibrated to the reported 24.08% at 30 Sep 2026 (formula gives {car_9m:.2f}%). **Out-of-sample:** the same weights give {car_fy25:.1f}% at FY2025 against 32.70% reported, so the proxy runs about {32.70-car_fy25:.1f} points low (conservative) at that date.",
          "- **Dividends** are 60% of prior-year profit in the base case; with capital above 24% there is no sign the buffer binds, but this is checked in the table above.", ""]
lines += ["## Scenario summary (GHS millions)", "", "| Scenario | Year | Net interest income | Net trading income | Profit after tax | Total equity | CAR proxy | ROE |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
for sc in SCEN:
    for y, r in all_res[sc].items():
        lines.append(f"| {sc} | {y} | {r['nii']:,.0f} | {r['nti']:,.0f} | {r['pat']:,.0f} | {r['te']:,.0f} | {r['car']:.1f}% | {r['roe']:.1f}% |")
lines += ["", "## Spot checks of reported history against filing text (done by the owner while building)", "",
          "1. FY2025 profit after tax 1,012,223 and total assets 21,201,620 (GH¢'000) match GTB-FY25 page 1.",
          "2. FY2023 profit after tax 725,786 and total equity 2,062,635 match GTB-FY24 and GTB-FY23 (both print the same).",
          "3. FY2021 total assets 5,035,451 and profit after tax 315,446 match GTB-FY21 page 1.",
          "4. 9M-2026 profit before tax 1,384,702 and total assets 25,972,432 match GTB-Q3-26 page 1.",
          "", "These spot checks are by the same agent that extracted the data, so they are NOT independent. A different agent must repeat them."]
with open(os.path.join(HERE, "checks.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("forecast rows:", len(out), "| forecast failures:", fails)
for sc in SCEN:
    r = all_res[sc]["FY2030E"]
    print(sc, "FY2030E PAT %.0f equity %.0f CAR %.1f ROE %.1f LDR %.0f securities %.0f" % (r["pat"], r["te"], r["car"], r["roe"], r["ldr"], r["secs"]))
print("FY2026E:", {k: round(all_res["base"]["FY2026E"][k], 1) for k in ("ii", "ie", "nii", "pat", "te", "car", "secs", "loans", "dep")})
