#!/usr/bin/env python3
"""Forecast model for United Bank for Africa (Ghana) Ltd (bank-only, GHS millions). Standard library only.

Run:  python model.py          writes forecast.csv and checks.md in this folder.

Reads:  financials.csv (history, from build_financials.py)
        assumptions.json (owner estimates, each with a basis)
        ../../sector/macro-assumptions/macro.csv (shared macro drivers by scenario; named in assumptions.json as macro_file)
Every forecast number is an ESTIMATE. History is never changed.
Method follows banks/zenith-bank-ghana/model.py after its round-2 repairs (calibrated capital proxy, Act 930 reserve tiers,
Q4 implied rows, sensitivities), adapted to this bank: no repricing schedule is available, so securities earn a blended yield with one fitted haircut.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, "assumptions.json"), encoding="utf-8"))
BANK = A["bank"]
YEARS = ["FY2026E", "FY2027E", "FY2028E", "FY2029E", "FY2030E"]
SCEN = ["base", "downside", "upside"]
P9 = "9M-2026"

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
BILL_WEIGHT = R["tbill_share_of_securities"]["value"]
TAX = R["tax_rate"]["value"]
AVG_POLICY_2026 = R["avg_policy_rate_2026_pct"]["value"] / 100
FEE_EXP = H(P9, "fee_commission_expense") / H(P9, "fee_commission_income")      # 9M-2026 ratio held
STATED = H("FY2025", "x_stated_capital")
STAT_RES = H(P9, "x_statutory_reserve")        # unchanged from FY2025 (transfer is booked at year end)
FVR = H(P9, "x_fair_value_reserve")
REG_ADJ = H("FY2025", "total_equity") - H("FY2025", "x_regulatory_capital")      # deductions from book equity, held constant
RWD_FY25 = H("FY2025", "x_risk_weighted_assets") / H("FY2025", "total_assets")
RWD = (H(P9, "total_equity") - REG_ADJ) / (H(P9, "car_pct") / 100) / H(P9, "total_assets")   # calibrated to the reported 30 Sep 2026 CAR
TARGET_CAR = K["target_car_pct_for_dividends"]["value"]
OPCASH = H(P9, "cash_and_bog_balances") / H(P9, "customer_deposits") - M("base", "FY2026E", "crr_pct") / 100   # calibrated at 30 Sep 2026
COF_ANCHOR_RATE = AVG_POLICY_2026


def sec_yield(sc, y, haircut, bill_weight=None):
    w = BILL_WEIGHT if bill_weight is None else bill_weight
    bills = (M(sc, y, "tbill_91d_pct") + M(sc, y, "tbill_364d_pct")) / 2
    return (w * bills + (1 - w) * M(sc, y, "govt_bond_yield_pct") + haircut) / 100


# --- calibration of two constants to 9M-2026 x 12/9 (disclosed; a fit, not a validation)
_f = 12 / 9
_avg_loans26 = (H("FY2025", "loans_and_advances_net") + H(P9, "loans_and_advances_net")) / 2
_loan_part26 = (M("base", "FY2026E", "tbill_364d_pct") / 100 + LOAN_SPREAD) * _avg_loans26
_ii_anchor = H(P9, "interest_income") * _f
_sec_open = H("FY2025", "investment_securities")
_needed_yield = (_ii_anchor - _loan_part26) / _sec_open * 100
_unadj = sec_yield("base", "FY2026E", 0.0) * 100
HAIRCUT = _needed_yield - _unadj                    # percentage points, negative = securities earn less than the macro blend
_avg_fund26 = (sum(H("FY2025", k) for k in ("customer_deposits", "due_to_banks", "borrowings")) + sum(H(P9, k) for k in ("customer_deposits", "due_to_banks", "borrowings"))) / 2
COF = H(P9, "interest_expense") * _f / (COF_ANCHOR_RATE * _avg_fund26)

out = []


def emit(sc, per, stmt, item, val, note=""):
    unit = "percent" if item.endswith("_pct") else "GHS millions"
    out.append([BANK, sc, per, stmt, item, f"{val:.3f}", unit, "estimated", note])


def stat_transfer(prior_reserve, pat):
    """Act 930 s34: transfer 50% of net profit if the reserve is below 50% of stated capital, 25% from 50% to below 100%, 12.5% at or above 100%.
    Observed here: 25.0% FY2022 to FY2024, 12.5% FY2025."""
    if pat <= 0:
        return 0.0
    ratio = prior_reserve / STATED
    return (0.50 if ratio < 0.5 else 0.25 if ratio < 1.0 else 0.125) * pat


def run(sc, haircut=None, cof_mult=1.0, bill_weight=None, tax=None, loan_growth_scale=1.0):
    hc = HAIRCUT if haircut is None else haircut
    cof = COF * cof_mult
    tx = TAX if tax is None else tax
    res, prev = {}, {}
    for i, y in enumerate(YEARS):
        infl = M(sc, y, "inflation_cpi_pct") / 100
        gdp = M(sc, y, "gdp_growth_pct") / 100
        pol = M(sc, y, "policy_rate_pct") / 100
        t364 = M(sc, y, "tbill_364d_pct") / 100
        crr = M(sc, y, "crr_pct") / 100
        minc = M(sc, y, "min_car_pct")
        r = {}
        if i == 0:
            r.update(loans=H(P9, "loans_and_advances_net"), dep_c=H(P9, "customer_deposits"), dep_b=H(P9, "due_to_banks"), bor=H(P9, "borrowings"),
                     oth_l=H(P9, "other_liabilities"), oth_a=H(P9, "other_assets"), ppe=H(P9, "property_equipment_intangibles"))
            ii = _ii_anchor * (1 if hc == HAIRCUT else 1)
            if hc != HAIRCUT:   # sensitivity: re-price the securities part of the anchor
                ii = _loan_part26 + _sec_open * sec_yield(sc, y, hc, bill_weight)
            ie = H(P9, "interest_expense") * _f * (cof / COF)
            fee_i = H(P9, "fee_commission_income") * _f
            fee_e = H(P9, "fee_commission_expense") * _f
            nti = H(P9, "net_trading_income") * _f
            oth = H(P9, "other_operating_income") * _f
            staff = H(P9, "staff_costs") * _f
            dep = H(P9, "depreciation_amortisation") * _f
            othx = H(P9, "other_operating_expenses") * _f
            q4_imp = C["cost_of_risk_on_average_net_loans"]["base"] * H(P9, "loans_and_advances_net") / 4
            imp = H(P9, "impairment_charge") + q4_imp
            equity_open = H("FY2025", "total_equity")
            prior_res = H("FY2025", "x_statutory_reserve")
        else:
            p = prev
            r["dep_c"] = p["dep_c"] * ((1 + gdp) * (1 + infl) + G["customer_deposit_adjustment"][sc])
            g_dep = r["dep_c"] / p["dep_c"] - 1
            r["loans"] = p["loans"] * (1 + G["net_loan_growth"][sc][y] * loan_growth_scale)
            r["dep_b"] = p["dep_b"] * (1 + g_dep)
            r["bor"] = p["bor"]
            r["oth_l"] = p["oth_l"] * (1 + infl)
            r["oth_a"] = p["oth_a"] * (1 + infl)
            r["ppe"] = p["ppe"] * (1 + infl)
            pol_prev = M(sc, YEARS[i - 1], "policy_rate_pct") / 100
            avg_loans = (p["loans"] + r["loans"]) / 2
            ii = (t364 + LOAN_SPREAD) * avg_loans + p["liquid"] * sec_yield(sc, y, hc, bill_weight)
            avg_fund = (p["dep_c"] + r["dep_c"]) / 2 + (p["dep_b"] + r["dep_b"]) / 2 + (p["bor"] + r["bor"]) / 2
            ie = cof * (pol_prev + pol) / 2 * avg_fund
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
        if i == 0:   # nine months of tax are already booked at the observed rate; Q4 profit is taxed at the statutory blend
            tax_amt = H(P9, "income_tax") + tx * max(0.0, pbt - H(P9, "profit_before_tax")) + min(0.0, (pbt - H(P9, "profit_before_tax")) * tx)
        else:
            tax_amt = tx * pbt if pbt > 0 else 0.0
        pat = pbt - tax_amt
        transfer = stat_transfer(prior_res, pat)
        stat_res = prior_res + transfer
        tl = r["dep_c"] + r["dep_b"] + r["bor"] + r["oth_l"]
        div_flag = ""
        if i == 0:
            div = 0.0
            te = H(P9, "total_equity") + (pat - H(P9, "profit_after_tax"))
        else:
            distributable = max(0.0, p["retained"] + pat - transfer)
            div = min(div_target, distributable)
            if div < div_target:
                div_flag = "capped by distributable retained earnings"
            te_after = equity_open + pat - div
            if (te_after - REG_ADJ) / (RWD * (tl + te_after)) * 100 < TARGET_CAR and div > 0:
                div, div_flag = 0.0, "withheld: CAR proxy would fall below the dividend buffer"
            te = equity_open + pat - div
        res_other = stat_res + FVR
        retained = te - STATED - res_other
        ta = tl + te
        cash = (crr + OPCASH) * r["dep_c"]
        liquid = ta - cash - r["loans"] - r["oth_a"] - r["ppe"]
        r.update(dict(ii=ii, ie=ie, nii=nii, fee_i=fee_i, fee_e=fee_e, nti=nti, oth=oth, opinc=opinc, staff=staff, dep=dep, othx=othx, imp=imp, pbt=pbt,
                      tax=tax_amt, pat=pat, div=div, te=te, stat_res=stat_res, res_other=res_other, retained=retained, tl=tl, ta=ta, cash=cash,
                      liquid=liquid, secs=liquid, div_flag=div_flag, div_target=0.0 if i == 0 else div_target, transfer=transfer))
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
        first = y == "FY2026E"
        note_is = "Estimate. FY2026E = 9M-2026 x 12/9 (see assumptions.json)." if first else "Estimate from assumptions.json and the macro rows of this scenario."
        for item, key in [("interest_income", "ii"), ("interest_expense", "ie"), ("net_interest_income", "nii"), ("fee_commission_income", "fee_i"),
                          ("fee_commission_expense", "fee_e"), ("net_trading_income", "nti"), ("other_operating_income", "oth"),
                          ("total_operating_income", "opinc"), ("staff_costs", "staff"), ("depreciation_amortisation", "dep"),
                          ("other_operating_expenses", "othx"), ("impairment_charge", "imp"), ("profit_before_tax", "pbt"),
                          ("income_tax", "tax"), ("profit_after_tax", "pat")]:
            n = note_is
            if key == "imp" and first:
                n = "Estimate. 9M-2026 actual (a reversal) plus a Q4 loan charge at the base cost of risk on 30 Sep 2026 net loans / 4."
            if key == "tax" and first:
                n = "Estimate. 9M-2026 tax actually booked (41.3% of 9M profit before tax) plus 35% of implied Q4 profit before tax."
            emit(sc, y, IS, item, r[key], n)
        emit(sc, y, IS, "x_dividends_paid", r["div"], "Dividends paid in the year. FY2026E adds none in Q4 (304.9m was already paid in 9M-2026 and sits in the equity base)." if first else "Payout x prior-year profit after tax (assumptions.json), capped as flagged.")
        emit(sc, y, IS, "x_statutory_reserve_transfer", r["transfer"], "Act 930 s34 tiers on profit after tax (see model.py stat_transfer).")
        note_bs = "Estimate. FY2026E carries the 30 Sep 2026 balance sheet forward; equity adds Q4 profit." if first else "Estimate."
        for item, key in [("cash_and_bog_balances", "cash"), ("investment_securities", "secs"), ("loans_and_advances_net", "loans"),
                          ("property_equipment_intangibles", "ppe"), ("other_assets", "oth_a"), ("total_assets", "ta"), ("customer_deposits", "dep_c"),
                          ("due_to_banks", "dep_b"), ("borrowings", "bor"), ("other_liabilities", "oth_l"), ("total_liabilities", "tl"),
                          ("x_retained_earnings", "retained"), ("x_reserves_other", "res_other"), ("total_equity", "te")]:
            emit(sc, y, BS, item, r[key], note_bs + (" Securities are the plug (liquid assets) after cash, loans, other assets and property." if key == "secs" else ""))
        emit(sc, y, BS, "x_stated_capital", STATED, "Held at 400m; no issue assumed. Matches the shared minimum paid-up capital.")
        emit(sc, y, RT, "x_car_proxy_pct", r["car_proxy"], "PROXY, not the regulatory ratio: (book equity - deductions held at the FY2025 gap between book equity and regulatory capital) / (risk-weight density x total assets). Density calibrated so the proxy equals the reported 16.7% at 30 Sep 2026.")
        emit(sc, y, RT, "x_car_proxy_fy25_density_pct", r["car_proxy_fy25_density"], "PROXY with the FY2025 audited density (RWA / total assets = 0.516), a high case.")
        emit(sc, y, RT, "roe_pct", r["roe"], "Estimate. Profit after tax / average of opening and closing equity.")
        emit(sc, y, RT, "roa_pct", r["roa"], "Estimate. Profit after tax / average of opening and closing total assets.")
        emit(sc, y, RT, "cost_to_income_pct", r["cti"], "Estimate. (Staff + depreciation + other expenses) / operating income before impairment.")
        emit(sc, y, RT, "ldr_pct", r["ldr"], "Estimate. NET loans / customer deposits (gross loans are not forecast).")
        for stmt_, item_, why in [("balance_sheet", "due_from_banks", "Not a separate balance sheet line (inside cash and bank balances)."),
                                  ("balance_sheet", "loans_and_advances_gross", "Gross loans not forecast; interim statements do not print them."),
                                  ("balance_sheet", "loan_loss_allowance", "Allowance not forecast; impairment is driven by a cost of risk on net loans."),
                                  ("ratios", "npl_pct", "No NPL path is forecast. Reported NPL was 2.11% (FY2025) and 1.57% (Sep 2026); cost of risk is an independent assumption."),
                                  ("ratios", "car_pct", "Regulatory CAR is not forecast; see x_car_proxy_pct (accounting proxy)."),
                                  ("ratios", "tier1_pct", "Tier 1 is not forecast.")]:
            out.append([BANK, sc, y, stmt_, item_, "", "percent" if stmt_ == "ratios" else "GHS millions", "unavailable", why])
        if r["div_flag"]:
            emit(sc, y, IS, "x_dividend_target_before_cap", r["div_target"], "Payout x prior-year profit before the caps; actual dividend is lower: " + r["div_flag"] + ".")
    q = res["FY2026E"]
    emit(sc, "FY2026E", "income_statement", "x_q4_implied_profit_before_tax", q["pbt"] - H(P9, "profit_before_tax"), "FY2026E profit before tax less 9M-2026 actual.")
    emit(sc, "FY2026E", "income_statement", "x_q4_implied_income_tax", q["tax"] - H(P9, "income_tax"), "FY2026E tax less 9M-2026 actual tax (35% of implied Q4 profit).")
    emit(sc, "FY2026E", "income_statement", "x_q4_implied_impairment", q["imp"] - H(P9, "impairment_charge"), "Q4 charge at the base cost of risk on 30 Sep 2026 net loans / 4.")


all_res = {sc: run(sc) for sc in SCEN}
for sc in SCEN:
    write_rows(sc, all_res[sc])

with open(os.path.join(HERE, "forecast.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["bank", "scenario", "period", "statement", "line_item", "value", "unit", "status", "notes"])
    w.writerows(out)

# ------------------------------------------------------------------ checks.md
L = ["# Forecast checks (uba-ghana)", "",
     "Generated by `model.py` from `financials.csv`, `assumptions.json` and the shared macro file. GHS millions; ratios in percent. Every forecast value is an estimate.", "",
     "## 1. Forecast identities (all scenarios, all years)", "",
     "| Scenario | Year | Balance (A = L + E) | Asset lines = total | NII = II - IE | PAT = PBT - tax | Equity roll | CAR proxy | CAR proxy (FY25 density) | Min CAR |",
     "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
fails = 0
for sc in SCEN:
    for i, y in enumerate(YEARS):
        r = all_res[sc][y]
        prev = all_res[sc][YEARS[i - 1]] if i else None
        bal = abs(r["ta"] - r["tl"] - r["te"]) < 0.001
        sumA = abs(r["cash"] + r["secs"] + r["loans"] + r["oth_a"] + r["ppe"] - r["ta"]) < 0.001
        nii = abs(r["nii"] - (r["ii"] - r["ie"])) < 0.001
        pat = abs(r["pat"] - (r["pbt"] - r["tax"])) < 0.001
        if i == 0:
            roll = abs(r["te"] - (H(P9, "total_equity") + r["pat"] - H(P9, "profit_after_tax"))) < 0.001
        else:
            roll = abs(r["te"] - (prev["te"] + r["pat"] - r["div"])) < 0.001
        ok = bal and sumA and nii and pat and roll and r["secs"] > 0
        fails += 0 if ok else 1
        low = r["car_proxy"] < r["min_car"]
        L.append(f"| {sc} | {y} | {'PASS' if bal else 'FAIL'} | {'PASS' if sumA and r['secs'] > 0 else 'FAIL'} | {'PASS' if nii else 'FAIL'} | {'PASS' if pat else 'FAIL'} | {'PASS' if roll else 'FAIL'} | {r['car_proxy']:.1f}%{' BELOW MINIMUM' if low else ''} | {r['car_proxy_fy25_density']:.1f}% | {r['min_car']:.0f}% |")
L += ["", f"Forecast failures: {fails}", ""]

f26 = all_res["base"]["FY2026E"]
L += ["## 2. Calibration disclosure (a fit, not a validation)", "",
      f"- FY2026E interest income is **anchored** on 9M-2026 x 12/9 = {_ii_anchor:,.1f}m. The forward formula is: 364-day bill + {LOAN_SPREAD*100:.1f} pts on average net loans ({_loan_part26:,.1f}m for 2026), plus on opening securities of {_sec_open:,.1f}m a blended yield: {BILL_WEIGHT*100:.1f}% weight on the average of the 91- and 364-day bills and {(1-BILL_WEIGHT)*100:.1f}% on the government bond yield (an ASSUMED weight, not observed), plus a haircut of **{HAIRCUT:+.2f} pts solved so the formula lands on the anchor**. The match is by construction. The haircut is negative because the macro blend ({_unadj:.2f}%) is above the yield the bank earned ({_needed_yield:.2f}%); the older, lower-yield holdings and any non-earning balances are not separately visible.",
      f"- FY2026E interest expense is anchored on 9M-2026 x 12/9 = {H(P9, 'interest_expense') * _f:,.1f}m. The cost-of-funds ratio ({COF:.3f}) is solved so that ratio x an assumed {AVG_POLICY_2026*100:.1f}% 2026 average policy rate x average funding {_avg_fund26:,.1f}m gives that figure. The 14.3% average policy rate is taken from the SCB and Zenith bases and was not re-verified.",
      f"- Capital proxy: book equity less {REG_ADJ:,.1f}m (FY2025 book equity 1,895.7m minus regulatory capital 1,555.8m) over density {RWD:.3f} x total assets, density solved so the proxy equals the reported 16.7% at 30 Sep 2026 (FY2025 audited density {RWD_FY25:.3f}). Whether the interim CAR includes the unaudited 9M profit is unknown.",
      f"- Cash is modelled at (macro CRR 20% + {OPCASH*100:.2f}%) of customer deposits, the extra share solved from 30 Sep 2026 balances. The 20% is a constructed floor, not a tested statutory eligibility.",
      "- The macro file's FY2026E bill rates (91-day 5.81%, 364-day 11.01%) are lower than rates earlier in 2026, so yields from FY2027E depend on the fitted haircut staying stable. That is untested.", ""]

# sensitivity
variants = [("As modelled", run("base"), run("downside")),
            ("Securities haircut 1 pt worse", run("base", haircut=HAIRCUT - 1.0), run("downside", haircut=HAIRCUT - 1.0)),
            ("Securities haircut 1 pt better", run("base", haircut=HAIRCUT + 1.0), run("downside", haircut=HAIRCUT + 1.0)),
            ("Cost-of-funds ratio +25%", run("base", cof_mult=1.25), run("downside", cof_mult=1.25)),
            ("Cost-of-funds ratio -25%", run("base", cof_mult=0.75), run("downside", cof_mult=0.75)),
            ("Loan growth halved", run("base", loan_growth_scale=0.5), run("downside", loan_growth_scale=0.5)),
            ("Tax rate 41% (9M-2026 effective)", run("base", tax=0.41), run("downside", tax=0.41))]
L += ["## 2b. Sensitivity of net interest income and profit to the main assumptions", "",
      "Base and downside, GHS millions. FY2026E is anchored, so most differences start in FY2027E.", "",
      "| Variant | Base NII FY2027E | Base NII FY2030E | Base PAT FY2030E | Downside NII FY2027E | Downside PAT FY2030E |", "| --- | --- | --- | --- | --- | --- |"]
for lab, b, d in variants:
    L.append(f"| {lab} | {b['FY2027E']['nii']:,.0f} | {b['FY2030E']['nii']:,.0f} | {b['FY2030E']['pat']:,.0f} | {d['FY2027E']['nii']:,.0f} | {d['FY2030E']['pat']:,.0f} |")
L += ["", "Reading: no repricing schedule or deposit beta is available for this bank, so these ranges show how much the conclusions rest on the fitted haircut and the cost-of-funds ratio.", ""]

q = f26
L += ["## 2c. Q4-2026 implied by the FY2026E anchor (same in all scenarios)", "",
      "| Item | 9M-2026 actual | FY2026E | Implied Q4 |", "| --- | --- | --- | --- |",
      f"| Profit before tax | {H(P9, 'profit_before_tax'):,.1f} | {q['pbt']:,.1f} | {q['pbt'] - H(P9, 'profit_before_tax'):,.1f} |",
      f"| Income tax | {H(P9, 'income_tax'):,.1f} | {q['tax']:,.1f} | {q['tax'] - H(P9, 'income_tax'):,.1f} ({(q['tax'] - H(P9, 'income_tax')) / (q['pbt'] - H(P9, 'profit_before_tax')) * 100:.0f}% of Q4 PBT) |",
      f"| Impairment | {H(P9, 'impairment_charge'):,.1f} | {q['imp']:,.1f} | {q['imp'] - H(P9, 'impairment_charge'):,.1f} |",
      f"| Profit after tax | {H(P9, 'profit_after_tax'):,.1f} | {q['pat']:,.1f} | {q['pat'] - H(P9, 'profit_after_tax'):,.1f} |", "",
      f"Q4 profit before tax is the 9M run rate for every line except impairment (9M was a 47.1m reversal; Q4 gets a small charge). The 9M-2026 tax rate was 41.3% against 35% in FY2024 and FY2025 so the full-year rate comes out at {q['tax'] / q['pbt'] * 100:.1f}%.", ""]

# scenario ordering
L += ["## 3. Scenario ordering of profit after tax", "", "| Year | Downside | Base | Upside | Ordered downside < base < upside? |", "| --- | --- | --- | --- | --- |"]
for y in YEARS:
    d, b, u = (all_res[s][y]["pat"] for s in ("downside", "base", "upside"))
    L.append(f"| {y} | {d:,.0f} | {b:,.0f} | {u:,.0f} | {'equal (FY2026E is anchored on reported nine months)' if d == b == u else 'yes' if d < b < u else 'NO'} |")
L += ["", "Where the order is broken it follows the shared macro file: the downside has higher policy and bill rates, and this bank holds far more securities than loans (securities are about 57% of assets at 30 Sep 2026), so higher yields lift income. Please challenge it.", ""]

# summary
L += ["## 4. Scenario summary (GHS millions)", "", "| Scenario | Year | Net interest income | Impairment | PAT | Dividends | Equity | CAR proxy | ROE | LDR |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for sc in SCEN:
    for y in YEARS:
        r = all_res[sc][y]
        L.append(f"| {sc} | {y} | {r['nii']:,.0f} | {r['imp']:,.0f} | {r['pat']:,.0f} | {r['div']:,.0f} | {r['te']:,.0f} | {r['car_proxy']:.1f}% | {r['roe']:.1f}% | {r['ldr']:.0f}% |")
L += ["", "## 5. Reasonableness against history (observed history, estimated forecast)", "",
      f"- ROE history: FY2022 {H('FY2022', 'profit_after_tax') / H('FY2022', 'total_equity') * 100:.1f}%, FY2023 {H('FY2023', 'profit_after_tax') / H('FY2023', 'total_equity') * 100:.1f}%, FY2024 {H('FY2024', 'profit_after_tax') / H('FY2024', 'total_equity') * 100:.1f}%, FY2025 {H('FY2025', 'profit_after_tax') / H('FY2025', 'total_equity') * 100:.1f}% (year-end equity). Base forecast ROE is in the table above.",
      f"- FY2025 profit after tax of 407.1m included a 118.99m reversal of expected credit losses; 9M-2026 includes a 47.1m reversal. The forecast has no further reversals, so base profit after tax in FY2026E (about 256m) is well below FY2025 (407m); the base case then grows with net interest income.",
      "- Loan-to-deposit ratio was 19.6% at 30 Sep 2026 (net loans / customer deposits). Base loan growth in assumptions.json starts from that low base.", "",
      "## 6. Known limits", "",
      "- The shared macro rate paths (policy, bills, bonds) drive securities yields; deposit pricing uses a single ratio to the policy rate. There is no deposit beta, no maturity ladder and no FX translation (the statements do not give a net FX position).",
      "- Securities are a plug (liquid assets); if loan growth exceeds deposit growth the plug falls, and a negative plug would fail check 1.",
      "- Borrowings (1,690.6m at 30 Sep 2026, up from 807.8m at FY2025) are held flat; the reason for the increase is not stated.",
      "- Property and equipment rose from 122.3m (30 Jun 2026) to 320.3m (30 Sep 2026); the forecast carries the September level and grows it with inflation. The cause is unknown.",
      "- The FY2025 dividend recommended (146.5m) needed Bank of Ghana approval; 304.9m was paid in 9M-2026. Future dividends use a payout on prior-year profit with caps.",
      "- The CAR figures are proxies; the regulatory ratio, Tier 1 and NPL are not forecast.", ""]
with open(os.path.join(HERE, "checks.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print(f"forecast rows: {len(out)} | forecast failures: {fails} | haircut {HAIRCUT:+.2f} | COF {COF:.3f} | RWD {RWD:.3f} | opcash {OPCASH:.4f}")
for sc in ("base", "downside", "upside"):
    for y in ("FY2026E", "FY2030E"):
        r = all_res[sc][y]
        print(sc, y, f"PAT {r['pat']:.0f} equity {r['te']:.0f} CAR {r['car_proxy']:.1f}/{r['car_proxy_fy25_density']:.1f} ROE {r['roe']:.1f} LDR {r['ldr']:.0f} secs {r['secs']:.0f} II {r['ii']:.0f} IE {r['ie']:.0f} div {r['div']:.0f}")
