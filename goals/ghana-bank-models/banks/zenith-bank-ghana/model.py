#!/usr/bin/env python3
"""Forecast model for Zenith Bank (Ghana) Ltd (bank-only, GHS millions). Standard library only.

Run:  python model.py          writes forecast.csv and checks.md in this folder.

Reads:  financials.csv (history, from build_financials.py)
        assumptions.json (owner estimates)
        ../../sector/macro-assumptions/macro.csv (shared macro drivers by scenario)
Every forecast number is an ESTIMATE. History is never changed.
Structure follows banks/standard-chartered-ghana/model.py; differences are listed in assumptions.json.
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
FAST_SHARE = H("FY2025", "x_securities_repricing_under_3m") / (H("FY2025", "x_securities_repricing_under_3m") + H("FY2025", "x_securities_repricing_6_12m") + H("FY2025", "x_securities_repricing_1_5y") + H("FY2025", "x_securities_repricing_over_5y"))
FAST_SPREAD = R["fast_bucket_spread_over_tbill_91d_pct"]["value"] / 100
SLOW_YIELD0 = R["slow_bucket_yield_fy2026e_pct"]["value"] / 100
SLOW_PASS = R["slow_bucket_pass_through_of_bond_yield_change"]["value"]
COF = R["cost_of_funds_to_policy_rate"]["value"]
TAX = R["tax_rate"]["value"]
FEE_EXP = G["fee_expense_to_fee_income"]["value"]
OPCASH = K["operating_cash_to_customer_deposits"]["value"]
DFB = K["due_from_banks_share_of_liquid_assets"]["value"]
RWD_FY25 = H("FY2025", "x_risk_weighted_assets") / H("FY2025", "total_assets")
REG_ADJ = H("FY2025", "x_regulatory_capital_adjustment")   # book equity minus regulatory capital at FY2025 (181.041m), held constant
RWD_REG = (H("9M-2026", "total_equity") - REG_ADJ) / (H("9M-2026", "car_pct") / 100) / H("9M-2026", "total_assets")
RWD = RWD_REG   # risk-weight density calibrated to the reported 9M-2026 CAR on regulatory-capital proxy (book equity - 181.041m)
TARGET_CAR = A["capital_and_liquidity"]["target_car_pct_for_dividends"]["value"]
STATED = H("FY2025", "stated_capital")
# reserves_other in financials.csv = statutory reserve + credit risk reserve. Statutory reserve 891.834m at FY2025 and at 30 Sep 2026 (ZEN-FY25 p.39, ZEN-Q3-26); the split is read from those statements.
STAT_RES_FY25 = 891.834
CRR_RESERVE = H("9M-2026", "reserves_other") - STAT_RES_FY25   # credit risk reserve at 30 Sep 2026 (177.650m)
P9 = "9M-2026"

out = []


def emit(sc, per, stmt, item, val, note=""):
    unit = "percent" if item.endswith("_pct") else "GHS millions"
    out.append([BANK, sc, per, stmt, item, f"{val:.3f}", unit, "estimated", note])


def stat_transfer(prior_reserve, pat):
    """Banks and SDI Act 2016 (Act 930) s.34 (read by the independent reviewer): transfer >= 50% of net profit if the reserve is below 50% of stated
    capital, >= 25% if 50% to <100%, >= 12.5% at or above 100%. Observed in this bank: FY2023 12.5% (reserve above the then 400m capital),
    FY2024 and FY2025 25.0%."""
    if pat <= 0:
        return 0.0
    ratio = prior_reserve / STATED
    return (0.50 if ratio < 0.5 else 0.25 if ratio < 1.0 else 0.125) * pat


def run(sc):
    res = {}
    prev = {}
    f = 12 / 9
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
            r["slow_y"] = SLOW_YIELD0
            r["loans"] = H(P9, "loans_and_advances_net")
            r["dep_c"] = H(P9, "customer_deposits")
            r["dep_b"] = H(P9, "due_to_banks")
            r["bor"] = H(P9, "borrowings")
            r["oth_l"] = H(P9, "other_liabilities")
            r["oth_a"] = H(P9, "other_assets")
            r["ppe"] = H(P9, "property_equipment_intangibles")
            ii = H(P9, "interest_income") * f
            ie = H(P9, "interest_expense") * f
            fee_i = H(P9, "fee_commission_income") * f
            fee_e = H(P9, "fee_commission_expense") * f
            nti = H(P9, "net_trading_income") * f
            oth = H(P9, "other_operating_income") * f
            staff = H(P9, "staff_costs") * f
            dep = H(P9, "depreciation_amortisation") * f
            othx = H(P9, "other_operating_expenses") * f
            q4_charge = C["cost_of_risk_on_average_net_loans"]["base"] * H(P9, "loans_and_advances_net") / 4
            imp = H(P9, "impairment_charge") + q4_charge
            div = 0.0
            equity_open = H("FY2025", "total_equity")
            prior_res = STAT_RES_FY25
        else:
            p = prev
            r["dep_c"] = p["dep_c"] * (1 + (1 + gdp) * (1 + infl) - 1 + G["customer_deposit_adjustment"][sc])
            g_dep = r["dep_c"] / p["dep_c"] - 1
            r["loans"] = p["loans"] * (1 + G["net_loan_growth"][sc][y])
            r["dep_b"] = p["dep_b"] * (1 + g_dep)
            r["bor"] = p["bor"]
            r["oth_l"] = p["oth_l"] * (1 + infl)
            r["oth_a"] = p["oth_a"] * (1 + infl)
            r["ppe"] = p["ppe"] * (1 + infl)
            pol_prev = M(sc, YEARS[i - 1], "policy_rate_pct") / 100
            avg_loans = (p["loans"] + r["loans"]) / 2
            slow_y = p["slow_y"] + SLOW_PASS * (M(sc, y, "govt_bond_yield_pct") - M(sc, YEARS[i - 1], "govt_bond_yield_pct")) / 100
            r["slow_y"] = slow_y
            ii = (t364 + LOAN_SPREAD) * avg_loans + p["liquid"] * (FAST_SHARE * (t91 + FAST_SPREAD) + (1 - FAST_SHARE) * slow_y)
            avg_fund = (p["dep_c"] + r["dep_c"]) / 2 + (p["dep_b"] + r["dep_b"]) / 2 + (p["bor"] + r["bor"]) / 2
            ie = COF * (pol_prev + pol) / 2 * avg_fund
            fee_i = p["fee_i"] * (1 + infl + G["fee_income_growth_over_inflation"]["value"])
            fee_e = fee_i * FEE_EXP
            nti = p["nti"] * (1 + G["net_trading_income_growth"][sc])
            oth = p["oth"]
            staff = p["staff"] * (1 + infl + G["staff_cost_growth_over_inflation"]["value"])
            dep = p["dep"] * (1 + infl)
            othx = p["othx"] * (1 + infl + G["other_opex_growth_over_inflation"]["value"])
            imp = C["cost_of_risk_on_average_net_loans"][sc] * avg_loans
            div_target = K["dividend_payout_of_prior_year_profit"][sc] * p["pat"]
            equity_open = p["te"]
            prior_res = p["stat_res"]
        nii = ii - ie
        opinc = nii + fee_i - fee_e + nti + oth
        pbt = opinc - imp - (staff + dep + othx)
        tax = TAX * pbt if pbt > 0 else 0.0
        pat = pbt - tax
        transfer = stat_transfer(prior_res, pat)
        stat_res = prior_res + transfer
        tl = r["dep_c"] + r["dep_b"] + r["bor"] + r["oth_l"]
        div_flag = ""
        if i == 0:
            div = 0.0
            te = H(P9, "total_equity") + (pat - H(P9, "profit_after_tax"))
        else:
            # dividends are capped by (a) distributable retained earnings after the statutory transfer and (b) a CAR-proxy buffer after payment
            distributable = max(0.0, p["retained"] + pat - transfer)
            div = min(div_target, distributable)
            if div < div_target:
                div_flag = "capped by distributable retained earnings"
            te_after = equity_open + pat - div
            if (te_after - REG_ADJ) / (RWD * (tl + te_after)) * 100 < TARGET_CAR and div > 0:
                div, div_flag = 0.0, "withheld: CAR proxy would fall below the dividend buffer"
            te = equity_open + pat - div
        r["div_flag"] = div_flag
        r["div_target"] = 0.0 if i == 0 else div_target
        res_other = stat_res + CRR_RESERVE
        retained = te - STATED - res_other
        ta = tl + te
        cash = (crr + OPCASH) * r["dep_c"]
        liquid = ta - cash - r["loans"] - r["oth_a"] - r["ppe"]
        r.update(dict(ii=ii, ie=ie, nii=nii, fee_i=fee_i, fee_e=fee_e, nti=nti, oth=oth, opinc=opinc, staff=staff, dep=dep, othx=othx,
                      imp=imp, pbt=pbt, tax=tax, pat=pat, div=div, te=te, stat_res=stat_res, res_other=res_other, retained=retained,
                      tl=tl, ta=ta, cash=cash, liquid=liquid, due=liquid * DFB, secs=liquid * (1 - DFB)))
        r["car_proxy"] = (te - REG_ADJ) / (RWD * ta) * 100
        r["car_proxy_fy25_density"] = (te - REG_ADJ) / (RWD_FY25 * ta) * 100
        r["min_car"] = minc
        r["ldr"] = r["loans"] / r["dep_c"] * 100
        r["cti"] = (staff + dep + othx) / opinc * 100
        prior_te = H("FY2025", "total_equity") if i == 0 else prev["te"]
        r["roe"] = pat / ((prior_te + te) / 2) * 100
        prior_ta = H("FY2025", "total_assets") if i == 0 else prev["ta"]
        r["roa"] = pat / ((prior_ta + ta) / 2) * 100
        prev = r
        res[y] = r
    return res


def write_rows(sc, res):
    IS, BS, RT = "income_statement", "balance_sheet", "ratios"
    for y, r in res.items():
        note_is = "Estimate. FY2026E = 9M-2026 x 12/9 (see assumptions.json)." if y == "FY2026E" else "Estimate from assumptions.json and the macro rows of this scenario."
        for item, key in [("interest_income", "ii"), ("interest_expense", "ie"), ("net_interest_income", "nii"), ("fee_commission_income", "fee_i"),
                          ("fee_commission_expense", "fee_e"), ("net_trading_income", "nti"), ("other_operating_income", "oth"),
                          ("total_operating_income", "opinc"), ("staff_costs", "staff"), ("depreciation_amortisation", "dep"),
                          ("other_operating_expenses", "othx"), ("impairment_charge", "imp"), ("profit_before_tax", "pbt"),
                          ("income_tax", "tax"), ("profit_after_tax", "pat")]:
            n = note_is
            if key == "imp" and y == "FY2026E":
                n = "Estimate. 9M-2026 actual (a 32.418m reversal) plus a Q4 charge at the base cost of risk on 30 Sep 2026 net loans / 4."
            if key == "tax" and y == "FY2026E":
                n = "Estimate. 34% of full-year profit before tax (9M-2026 effective rate was 17.8%; see assumptions.json tax_rate)."
            emit(sc, y, IS, item, r[key], n)
        emit(sc, y, IS, "x_dividends_paid", r["div"], "Dividends paid in the year. FY2026E is 0: none was paid in 9M-2026." if y == "FY2026E" else "Payout x prior-year profit after tax (assumptions.json).")
        note_bs = "Estimate. FY2026E carries the 30 Sep 2026 balance sheet forward; equity adds Q4 profit." if y == "FY2026E" else "Estimate."
        for item, key in [("cash_and_bog_balances", "cash"), ("due_from_banks", "due"), ("investment_securities", "secs"), ("loans_and_advances_net", "loans"),
                          ("property_equipment_intangibles", "ppe"), ("other_assets", "oth_a"), ("total_assets", "ta"), ("customer_deposits", "dep_c"),
                          ("due_to_banks", "dep_b"), ("borrowings", "bor"), ("other_liabilities", "oth_l"), ("total_liabilities", "tl"),
                          ("retained_earnings", "retained"), ("reserves_other", "res_other"), ("total_equity", "te")]:
            emit(sc, y, BS, item, r[key], note_bs + (" Due from banks and securities are the plug (liquid assets) split at the 30 Sep 2026 mix." if key in ("due", "secs") else ""))
        emit(sc, y, BS, "stated_capital", STATED, "Held at 1,000m; no issue or bonus issue assumed.")
        emit(sc, y, RT, "x_car_proxy_pct", r["car_proxy"], "PROXY, not the regulatory ratio: (book equity - 181.041m FY2025 regulatory adjustment) / (risk-weight density x total assets). Density calibrated so the proxy equals the reported 17.79% at 30 Sep 2026. Not a prudential calculation.")
        emit(sc, y, RT, "x_car_proxy_fy25_density_pct", r["car_proxy_fy25_density"], "PROXY with the FY2025 audited density (reported RWA / total assets = 0.527); a high case. Interim reported CAR is lower than this implies, so treat as an upper bound of the proxy, not of actual CAR.")
        emit(sc, y, RT, "roe_pct", r["roe"], "Estimate. Profit after tax / average of opening and closing equity.")
        emit(sc, y, RT, "roa_pct", r["roa"], "Estimate. Profit after tax / average of opening and closing total assets.")
        emit(sc, y, RT, "cost_to_income_pct", r["cti"], "Estimate. (Staff + depreciation + other expenses) / operating income before impairment.")
        emit(sc, y, RT, "ldr_pct", r["ldr"], "Estimate. NET loans / customer deposits (gross loans are not forecast).")
        for stmt_, item_, why in [("balance_sheet", "loans_and_advances_gross", "Gross loans not forecast; interim statements do not print them."),
                                  ("balance_sheet", "loan_loss_allowance", "Allowance not forecast. Impairment is driven by a cost of risk on net loans, not a stage 3 path."),
                                  ("ratios", "npl_pct", "No NPL path is forecast. Reported NPL was 8.49% (FY2025) and 8.91% (Sep 2026); the cost of risk is an independent assumption."),
                                  ("ratios", "car_pct", "Regulatory CAR is not forecast; see x_car_proxy_pct (accounting proxy)."),
                                  ("ratios", "tier1_pct", "Tier 1 is not forecast.")]:
            out.append([BANK, sc, y, stmt_, item_, "", "percent" if stmt_ == "ratios" else "GHS millions", "unavailable", why])
        if r["div_flag"]:
            emit(sc, y, IS, "x_dividend_target_before_cap", r["div_target"], "Payout x prior-year profit before the caps; actual dividend is lower: " + r["div_flag"] + ".")
    q = res["FY2026E"]
    emit(sc, "FY2026E", "income_statement", "x_q4_implied_profit_before_tax", q["pbt"] - H(P9, "profit_before_tax"), "FY2026E profit before tax less 9M-2026 actual.")
    emit(sc, "FY2026E", "income_statement", "x_q4_implied_income_tax", q["tax"] - H(P9, "income_tax"), "FY2026E tax (34% of full-year PBT) less 9M-2026 actual tax; implies a very high Q4 tax rate (see checks.md).")
    emit(sc, "FY2026E", "income_statement", "x_q4_implied_impairment", q["imp"] - H(P9, "impairment_charge"), "Q4 charge at the base cost of risk on 30 Sep 2026 net loans / 4.")


all_res = {sc: run(sc) for sc in SCEN}
for sc in SCEN:
    write_rows(sc, all_res[sc])
with open(os.path.join(HERE, "forecast.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["bank", "scenario", "period", "statement", "line_item", "value", "unit", "status", "notes"])
    w.writerows(out)

# ---------------------------------------------------------------- checks
fails = 0
L = ["# Checks: zenith-bank-ghana", "", "Generated by model.py. History checks are in `checks_history.md` (build_financials.py).", "",
     "## 1. Forecast identities (all scenarios, all years)", "",
     "| Scenario | Year | Assets = liabilities + equity | Liquid assets >= 0 | NII = II - IE | PAT = PBT - tax | Equity roll-forward | CAR proxy (Sep-26 density) | CAR proxy (FY25 density) | Minimum |",
     "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for sc in SCEN:
    for i, (y, r) in enumerate(all_res[sc].items()):
        bal = abs(r["ta"] - (r["tl"] + r["te"])) < 0.001
        sumA = abs(r["cash"] + r["due"] + r["secs"] + r["loans"] + r["ppe"] + r["oth_a"] - r["ta"]) < 0.001
        sumE = abs(STATED + r["res_other"] + r["retained"] - r["te"]) < 0.001
        liq = r["liquid"] >= 0
        nii = abs(r["nii"] - (r["ii"] - r["ie"])) < 0.001
        pat = abs(r["pat"] - (r["pbt"] - r["tax"])) < 0.001
        prior = all_res[sc][YEARS[i - 1]]["te"] if i else H("FY2025", "total_equity")
        roll = abs(prior + r["pat"] - r["div"] - r["te"]) < 0.001 if i else abs(H(P9, "total_equity") + (r["pat"] - H(P9, "profit_after_tax")) - r["te"]) < 0.001
        ok = bal and sumA and sumE and liq and nii and pat and roll
        fails += 0 if ok else 1
        low = r["car_proxy"] < r["min_car"]
        L.append(f"| {sc} | {y} | {'PASS' if bal and sumA and sumE else 'FAIL'} | {'PASS' if liq else 'FAIL'} | {'PASS' if nii else 'FAIL'} | {'PASS' if pat else 'FAIL'} | {'PASS' if roll else 'FAIL'} | {r['car_proxy']:.1f}%{' BELOW MINIMUM' if low else ''} | {r['car_proxy_fy25_density']:.1f}% | {r['min_car']:.0f}% |")
L += ["", f"Forecast failures: {fails}", ""]

# calibration disclosure
avg_loans = (H("FY2025", "loans_and_advances_net") + H(P9, "loans_and_advances_net")) / 2
liq_open = H("FY2025", "due_from_banks") + H("FY2025", "investment_securities")
t364 = macro[("base", "FY2026E", "tbill_364d_pct")] / 100
t91 = macro[("base", "FY2026E", "tbill_91d_pct")] / 100
f_ii = (t364 + LOAN_SPREAD) * avg_loans + liq_open * (FAST_SHARE * (t91 + FAST_SPREAD) + (1 - FAST_SHARE) * SLOW_YIELD0)
anch = H(P9, "interest_income") * 12 / 9
avg_fund = (sum(H("FY2025", k) for k in ("customer_deposits", "due_to_banks", "borrowings")) + sum(H(P9, k) for k in ("customer_deposits", "due_to_banks", "borrowings"))) / 2
f_ie = COF * 0.143 * avg_fund
anch_ie = H(P9, "interest_expense") * 12 / 9
L += ["## 2. Calibration disclosure (a fit, not a validation)", "",
      f"- FY2026E interest income is **anchored** on 9M-2026 x 12/9 = {anch:,.1f}m. The forward formula is: 364-day bill + {LOAN_SPREAD*100:.1f} pts on average net loans, plus on opening liquid assets a fast bucket ({FAST_SHARE*100:.2f}% of securities repricing within 3 months in the FY2025 schedule) at the 91-day bill + {FAST_SPREAD*100:.1f} pts and a slow bucket at {SLOW_YIELD0*100:.1f}%. It gives {f_ii:,.1f}m for FY2026E, a difference of {f_ii - anch:+,.1f}m ({(f_ii / anch - 1) * 100:+.1f}%). The slow yield was solved to land on the anchor, so this match is by construction; the fast share is observed (FY2025 audited repricing schedule, as read by an independent reviewer).",
      f"- FY2026E interest expense is anchored on 9M-2026 x 12/9 = {anch_ie:,.1f}m. The cost-of-funds ratio {COF} x an assumed 14.3% 2026 average policy rate x average funding {avg_fund:,.1f}m gives {f_ie:,.1f}m ({(f_ie / anch_ie - 1) * 100:+.1f}%). The 14.3% average is taken from SCB's assumptions basis and was not re-verified.",
      "- The macro file's FY2026E bill rates (91-day 5.81%, 364-day 11.01%) are lower than rates earlier in 2026, so yields from FY2027E depend on the fitted spreads staying stable. That is untested.", ""]

# sensitivity of the base case to the repricing and funding assumptions (F1 of the independent review)
def _variant(label, fast_share=None, fast_spread=None, slow_y0=None, cof_mult=1.0):
    global FAST_SHARE, FAST_SPREAD, SLOW_YIELD0, COF
    saved = (FAST_SHARE, FAST_SPREAD, SLOW_YIELD0, COF)
    if fast_share is not None:
        FAST_SHARE = fast_share
    if fast_spread is not None:
        FAST_SPREAD = fast_spread
    if slow_y0 is not None:
        SLOW_YIELD0 = slow_y0
    COF = COF * cof_mult
    res_ = {sc_: run(sc_) for sc_ in ("base", "downside")}
    FAST_SHARE, FAST_SPREAD, SLOW_YIELD0, COF = saved
    return label, res_


variants = [_variant("As modelled (58.35% of securities fast, rest at a fitted slow yield)"),
            _variant("Previous draft: whole pool reprices with the 91-day bill + 2.7 pts", fast_share=1.0, fast_spread=0.027),
            _variant("Cost-of-funds ratio +25%", cof_mult=1.25),
            _variant("Cost-of-funds ratio -25%", cof_mult=0.75)]
L += ["## 2b. Sensitivity of net interest income and profit to the repricing and funding assumptions", "",
      "Base and downside, GHS millions. The first row is the published forecast; the others rerun the model with one assumption changed (FY2026E is anchored, so differences start in FY2027E).", "",
      "| Variant | Base NII FY2027E | Base NII FY2030E | Base PAT FY2030E | Downside NII FY2027E | Downside PAT FY2028E | Downside PAT FY2030E |", "| --- | --- | --- | --- | --- | --- | --- |"]
for lab_, rs_ in variants:
    L.append(f"| {lab_} | {rs_['base']['FY2027E']['nii']:,.0f} | {rs_['base']['FY2030E']['nii']:,.0f} | {rs_['base']['FY2030E']['pat']:,.0f} | {rs_['downside']['FY2027E']['nii']:,.0f} | {rs_['downside']['FY2028E']['pat']:,.0f} | {rs_['downside']['FY2030E']['pat']:,.0f} |")
L += ["", "Reading: the repricing schedule does not give exact interest sensitivity (maturity assumptions and deposit betas are unknown). The table shows how much the conclusions rest on the assumption.", ""]
q_ = all_res["base"]["FY2026E"]
L += ["## 2c. Q4-2026 implied by the FY2026E anchor (same in all scenarios)", "",
      "| Item | 9M-2026 actual | FY2026E | Implied Q4 |", "| --- | --- | --- | --- |",
      f"| Profit before tax | {H(P9, 'profit_before_tax'):,.1f} | {q_['pbt']:,.1f} | {q_['pbt'] - H(P9, 'profit_before_tax'):,.1f} |",
      f"| Income tax | {H(P9, 'income_tax'):,.1f} | {q_['tax']:,.1f} | {q_['tax'] - H(P9, 'income_tax'):,.1f} ({(q_['tax'] - H(P9, 'income_tax')) / (q_['pbt'] - H(P9, 'profit_before_tax')) * 100:.0f}% of Q4 PBT) |",
      f"| Impairment | {H(P9, 'impairment_charge'):,.1f} | {q_['imp']:,.1f} | {q_['imp'] - H(P9, 'impairment_charge'):,.1f} |",
      f"| Profit after tax | {H(P9, 'profit_after_tax'):,.1f} | {q_['pat']:,.1f} | {q_['pat'] - H(P9, 'profit_after_tax'):,.1f} |", "",
      "The implied Q4 tax rate is high by design (Q4-2025 was 64%); the 2026 tax law is not established by the FY2025 report, so see the 28% sensitivity in section 3b.", ""]

# scenario bridge
L += ["## 3. Scenario bridge: why base, downside and upside differ in FY2030E", "",
      "| Item (GHS m, FY2030E) | Downside | Base | Upside |", "| --- | --- | --- | --- |"]
for lab, key in [("Net loans", "loans"), ("Customer deposits", "dep_c"), ("Net interest income", "nii"), ("Net trading income", "nti"), ("Impairment charge", "imp"),
                 ("Profit after tax", "pat"), ("Total equity", "te")]:
    L.append(f"| {lab} | {all_res['downside']['FY2030E'][key]:,.0f} | {all_res['base']['FY2030E'][key]:,.0f} | {all_res['upside']['FY2030E'][key]:,.0f} |")
L += ["", "Drivers: loan growth and deposit growth (assumptions.json), policy and bill rates, inflation and GDP (macro.csv), trading income growth, cost of risk and the dividend payout. The bridge is a summary of outputs; it does not attribute the gap to each driver.", ""]

# scenario ordering and tax sensitivity
L += ["## 3b. Scenario ordering and a tax sensitivity", "",
      "| Year | PAT downside | PAT base | PAT upside | Ordered downside < base < upside? |", "| --- | --- | --- | --- | --- |"]
inv = []
for y in YEARS:
    d_, b_, u_ = (all_res[s][y]["pat"] for s in ("downside", "base", "upside"))
    ok = d_ <= b_ <= u_
    if not ok:
        inv.append(y)
    L.append(f"| {y} | {d_:,.0f} | {b_:,.0f} | {u_:,.0f} | {'yes' if ok else 'NO (inverted)'} |")
if inv:
    L += ["", f"Profit is not ordered downside < base < upside in {', '.join(inv)}. This is a property of the shared macro file, not an error in the arithmetic: the downside has higher policy and bill rates (policy rate 14% in FY2027E-FY2028E vs 10% in base and 9% in upside), so the upside earns slightly less than the base on rate-sensitive assets, and Zenith holds about 9,000m of liquid assets that reprice with bills while the cost-of-funds ratio is 0.204 of the policy rate, so higher rates lift net interest income more than funding cost. The downside still carries a cost of risk of 4% and zero dividends, so equity is highest in the downside by FY2030E. Reviewers should challenge whether a rate-rise scenario deserves this asset sensitivity (it is the same formula as in banks/standard-chartered-ghana)."]
L += ["", f"Tax sensitivity (unverified alternative): if the FY2026E tax rate were 28% (9M-2026 17.8% plus the 10.3-point step seen between 9M-2025 and FY2025), FY2026E profit after tax would be {all_res['base']['FY2026E']['pbt'] * 0.72:,.0f}m instead of {all_res['base']['FY2026E']['pat']:,.0f}m.", ""]

# summary
L += ["## 4. Scenario summary (GHS millions)", "",
      "| Scenario | Year | Net interest income | Impairment | Profit after tax | Dividends | Total equity | CAR proxy (Sep-26 density) | ROE | LDR |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for sc in SCEN:
    for y, r in all_res[sc].items():
        L.append(f"| {sc} | {y} | {r['nii']:,.0f} | {r['imp']:,.0f} | {r['pat']:,.0f} | {r['div']:,.0f} | {r['te']:,.0f} | {r['car_proxy']:.1f}% | {r['roe']:.1f}% | {r['ldr']:.0f}% |")

# reasonableness vs history
b = all_res["base"]
L += ["", "## 5. Reasonableness against history (observed history, estimated forecast)", "",
      f"- FY2026E profit after tax {b['FY2026E']['pat']:,.0f}m against 9M-2026 actual {H(P9, 'profit_after_tax'):,.0f}m and FY2025 {H('FY2025', 'profit_after_tax'):,.0f}m. FY2026E is below the 9M-2026 x 12/9 run rate ({H(P9, 'profit_after_tax') * 12 / 9:,.0f}m) because of the 34% full-year tax rate and the Q4 impairment charge (see assumptions.json).",
      f"- Base ROE {b['FY2026E']['roe']:.1f}% (FY2026E) and {b['FY2030E']['roe']:.1f}% (FY2030E) against reported-basis history of 39.1% (FY2025), 24.4% (FY2024), 51.2% (FY2023) in checks_history.md.",
      f"- Base cost-to-income {b['FY2026E']['cti']:.1f}% (FY2026E) against 30.4% (FY2025) and 32.5% (FY2024).",
      f"- Base net loans {b['FY2026E']['loans']:,.0f}m -> {b['FY2030E']['loans']:,.0f}m; loan-to-deposit ratio {b['FY2026E']['ldr']:.0f}% -> {b['FY2030E']['ldr']:.0f}%.", ""]

# spot checks (history), by the same agent
L += ["## 6. Spot checks of reported history against the filing text (owner's own, NOT independent)", "",
      "Each figure below was read from the PDF text returned by the fetch tool and compared with financials.csv. The same agent extracted and checked them, so a different agent must repeat them.", "",
      "1. FY2025 profit after tax 997,714 and total assets 26,702,820 (GH¢'000): ZEN-FY25, income statement p.38 and balance sheet p.39.",
      "2. FY2024 customer deposits 15,630,343 and total equity 2,052,272: ZEN-FY24 p.36, and identical in the FY2025 comparative column.",
      "3. FY2023 profit after tax 676,100: ZEN-FY23 p.28 (the FY2024 report prints 676,101, a rounding difference noted in checks_history.md).",
      "4. 30 Sep 2026 total assets 31,991,597 and total equity 4,107,719: ZEN-Q3-26 (page not numbered); equity is also proven by 3,049,986 + 1,057,733.",
      "5. FY2025 Note 11 impairment components sum to the charge: 144,648 - 6,598 + 11 + 2,315 = 140,376.", "",
      "## 7. Known limits", "",
      "- Gross loans and the allowance are not in the interim statements, so the stage 3 coverage used in the cost-of-risk basis is the FY2025 figure.",
      "- The gate requires full balance sheets for 9M-2025 and 9M-2026: both are in financials.csv.",
      "- The CAR proxy is not the regulatory ratio. The two density choices bracket it.", ""]
with open(os.path.join(HERE, "checks.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(L) + "\n")
print("forecast rows:", len(out), "| forecast failures:", fails)
for sc in SCEN:
    for y in ("FY2026E", "FY2030E"):
        r = all_res[sc][y]
        print(sc, y, "PAT %.0f equity %.0f CAR %.1f/%.1f ROE %.1f LDR %.0f liquid %.0f II %.0f IE %.0f" % (r["pat"], r["te"], r["car_proxy"], r["car_proxy_fy25_density"], r["roe"], r["ldr"], r["liquid"], r["ii"], r["ie"]))
