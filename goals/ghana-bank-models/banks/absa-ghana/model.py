#!/usr/bin/env python3
"""Forecast model for Absa Bank Ghana PLC (bank-only, GHS millions). Standard library only.

Run:  python model.py          writes forecast.csv and checks.md in this folder.

Reads:  financials.csv (history, from build_financials.py)
        assumptions.json (owner estimates, each with a basis)
        ../../sector/macro-assumptions/macro.csv (shared macro drivers by scenario; named in assumptions.json as macro_file)
Every forecast number is an ESTIMATE. History is never changed.
Method follows banks/uba-ghana/model.py (accepted after independent review), adapted to Absa: the earning pool is investment securities plus trading assets
(held flat), there is no regulatory-capital history, so the capital figure is a ratio-scaled proxy of the reported 19.06% CAR.
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
BILL_WEIGHT = R["tbill_share_of_earning_pool"]["value"]
TAX = R["tax_rate"]["value"]
AVG_POLICY_2026 = R["avg_policy_rate_2026_pct"]["value"] / 100
FEE_EXP = H(P9, "fee_commission_expense") / H(P9, "fee_commission_income")      # 9M-2026 ratio held
STATED = H("FY2025", "stated_capital")
TRADING = H(P9, "x_nonpledged_trading_assets") + H(P9, "x_pledged_trading_assets")   # held flat inside other_assets
DFB_SHARE = H(P9, "due_from_banks") / H(P9, "customer_deposits")
RES_BASE_SHARE = H(P9, "x_mandatory_cash_reserves") / (M("base", "FY2026E", "crr_pct") / 100 * H(P9, "customer_deposits"))   # 0.7706: share of deposits that carries the reserve requirement (inferred, not observed)
ELIG_SHARE = H(P9, "x_mandatory_cash_reserves") / H(P9, "cash_and_bog_balances")   # 0.3551: share of cash held as mandatory reserves (observed at 30 Sep 2026)
ELIG_HAIRCUT = 0.20   # stress: eligible reserve cash 20% lower than observed share
STRESS_NUM_HAIRCUT, STRESS_RWA_UP = 0.10, 0.10   # capital stress: numerator -10%, risk-weighted assets +10% (hypothetical)
Q4 = 0.25   # one quarter of the annualised FY2026E anchor
RES_OTHER_FIXED = H(P9, "x_credit_risk_reserve") + H(P9, "x_other_reserves")   # held
CAR0 = H(P9, "car_pct")
EQA0 = H(P9, "total_equity") / H(P9, "total_assets")   # proxy = reported CAR x (equity/assets) / (equity/assets at 30 Sep 2026)
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
_sec_open = H("FY2025", "investment_securities") + H("FY2025", "x_nonpledged_trading_assets") + H("FY2025", "x_pledged_trading_assets")   # earning pool at FY2025
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


def run(sc, haircut=None, cof_mult=1.0, bill_weight=None, tax=None, loan_growth_scale=1.0, q4_yield_pts=0.0, q4_cor=None, q4_cof_mult=1.0, penalty=0.0, stress_gate=False):
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
                     oth_l=H(P9, "other_liabilities"), oth_a=H(P9, "other_assets") - TRADING, ppe=H(P9, "property_equipment_intangibles"), dfb=H(P9, "due_from_banks"))
            # Nine months are reported and frozen. Sensitivities change the implied Q4 only (one quarter of the annualised anchor).
            F = lambda h: _loan_part26 + _sec_open * sec_yield(sc, y, h, bill_weight)
            ii = _ii_anchor + Q4 * (F(hc) - F(HAIRCUT)) + Q4 * _sec_open * q4_yield_pts / 100
            ie = H(P9, "interest_expense") * _f * (1 + Q4 * ((cof / COF - 1) + (q4_cof_mult - 1)))
            fee_i = H(P9, "fee_commission_income") * _f
            fee_e = H(P9, "fee_commission_expense") * _f
            nti = H(P9, "net_trading_income") * _f
            oth = H(P9, "other_operating_income") * _f
            staff = H(P9, "staff_costs") * _f
            dep = H(P9, "depreciation_amortisation") * _f
            othx = H(P9, "other_operating_expenses") * _f
            q4_imp = (C["cost_of_risk_on_average_net_loans"]["base"] if q4_cor is None else q4_cor) * H(P9, "loans_and_advances_net") / 4
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
            r["dfb"] = r["dep_c"] * DFB_SHARE
            r["ppe"] = p["ppe"] * (1 + infl)
            pol_prev = M(sc, YEARS[i - 1], "policy_rate_pct") / 100
            avg_loans = (p["loans"] + r["loans"]) / 2
            ii = (t364 + LOAN_SPREAD) * avg_loans + (p["liquid"] + TRADING) * sec_yield(sc, y, hc, bill_weight)
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
            div_target = max(0.0, K["dividend_payout_of_prior_year_profit"][sc] * p["pat"])
            equity_open = p["te"]
            prior_res = p["stat_res"]
        nii = ii - ie
        opinc = nii + fee_i - fee_e + nti + oth
        pbt = opinc - imp - (staff + dep + othx)
        if i == 0:   # nine months of tax are already booked at the observed rate; Q4 profit is taxed at the tax rate; no tax credit is taken on a Q4 loss
            tax_amt = H(P9, "income_tax") + tx * max(0.0, pbt - H(P9, "profit_before_tax"))
            pbt -= penalty   # post-balance-sheet penalty stress: charged with no tax benefit (tax computed before it)
        else:
            tax_amt = tx * pbt if pbt > 0 else 0.0
        pat = pbt - tax_amt
        transfer = stat_transfer(prior_res, pat)   # full-year requirement on full-year profit
        q4_transfer = max(0.0, transfer - H(P9, "x_ytd_statutory_transfer")) if i == 0 else 0.0   # full-year requirement less the 123.2m actually transferred in 9M-2026
        stat_res = (H(P9, "x_statutory_reserve") + q4_transfer) if i == 0 else prior_res + transfer
        req_cal = crr * RES_BASE_SHARE * r["dep_c"]
        elig = ELIG_SHARE * (crr + OPCASH) * r["dep_c"]
        gap_cal = max(0.0, round(req_cal - elig, 6))
        gap_full = max(0.0, crr * r["dep_c"] - elig)
        gap_hair = max(0.0, req_cal - (1 - ELIG_HAIRCUT) * elig)
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
            if (gap_hair if stress_gate else gap_cal) > 0 and div > 0:
                div, div_flag = 0.0, "withheld: reserve-cash gap" + (" under the 20% eligibility stress" if stress_gate else "")
            elif CAR0 * (te_after / (tl + te_after)) / EQA0 < TARGET_CAR and div > 0:
                div, div_flag = 0.0, "withheld: CAR proxy would fall below the dividend buffer"
            te = equity_open + pat - div
        res_other = stat_res + RES_OTHER_FIXED
        retained = te - STATED - res_other
        ta = tl + te
        cash = (crr + OPCASH) * r["dep_c"]
        liquid = ta - cash - r["dfb"] - r["loans"] - r["oth_a"] - TRADING - r["ppe"]
        r["oth_a_total"] = r["oth_a"] + TRADING
        r.update(dict(ii=ii, ie=ie, nii=nii, fee_i=fee_i, fee_e=fee_e, nti=nti, oth=oth, opinc=opinc, staff=staff, dep=dep, othx=othx, imp=imp, pbt=pbt,
                      tax=tax_amt, pat=pat, div=div, te=te, stat_res=stat_res, res_other=res_other, retained=retained, tl=tl, ta=ta, cash=cash,
                      req_cal=req_cal, elig=elig, gap_cal=gap_cal, gap_full=gap_full, gap_hair=gap_hair, q4_transfer=q4_transfer,
                      liquid=liquid, secs=liquid, div_flag=div_flag, div_target=0.0 if i == 0 else div_target, transfer=transfer))
        r["car_proxy"] = CAR0 * (te / ta) / EQA0
        r["car_stress"] = r["car_proxy"] * (1 - STRESS_NUM_HAIRCUT) / (1 + STRESS_RWA_UP)
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
                n = "Estimate. 9M-2026 actual plus a Q4 loan charge at the base cost of risk on 30 Sep 2026 net loans / 4."
            if key == "tax" and first:
                n = "Estimate. 9M-2026 tax actually booked (35.6% of 9M profit before tax) plus the tax rate on implied Q4 profit before tax."
            emit(sc, y, IS, item, r[key], n)
        emit(sc, y, IS, "x_dividends_paid", H(P9, "x_dividends_paid") if first else r["div"], "FY2026E: 1,115m actually paid in 9M-2026 (in the equity base); none is added for Q4." if first else "Payout x prior-year profit after tax (assumptions.json), capped as flagged.")
        emit(sc, y, IS, "x_statutory_reserve_transfer", r["transfer"], "Act 930 s34 tiers on profit after tax (see model.py stat_transfer).")
        note_bs = "Estimate. FY2026E carries the 30 Sep 2026 loans, deposits, borrowings, other assets and property forward; equity adds Q4 profit, and cash, due from banks and the securities plug are recomputed." if first else "Estimate."
        for item, key in [("cash_and_bog_balances", "cash"), ("investment_securities", "secs"), ("loans_and_advances_net", "loans"),
                          ("property_equipment_intangibles", "ppe"), ("due_from_banks", "dfb"), ("other_assets", "oth_a_total"), ("total_assets", "ta"), ("customer_deposits", "dep_c"),
                          ("due_to_banks", "dep_b"), ("borrowings", "bor"), ("other_liabilities", "oth_l"), ("total_liabilities", "tl"),
                          ("retained_earnings", "retained"), ("reserves_other", "res_other"), ("total_equity", "te")]:
            emit(sc, y, BS, item, r[key], note_bs + (" Securities are the plug (liquid assets) after cash, loans, other assets and property." if key == "secs" else ""))
        emit(sc, y, BS, "stated_capital", STATED, "Held at 400m; no issue assumed. Matches the shared minimum paid-up capital.")
        emit(sc, y, RT, "x_car_proxy_pct", r["car_proxy"], "PROXY, not the regulatory ratio: the reported 19.06% CAR at 30 Sep 2026 scaled by the change in equity / total assets since then (no regulatory-capital history was available).")
        emit(sc, y, RT, "roe_pct", r["roe"], "Estimate. Profit after tax / average of opening and closing equity.")
        emit(sc, y, RT, "roa_pct", r["roa"], "Estimate. Profit after tax / average of opening and closing total assets.")
        emit(sc, y, RT, "cost_to_income_pct", r["cti"], "Estimate. (Staff + depreciation + other expenses) / operating income before impairment.")
        emit(sc, y, RT, "x_net_ldr_pct", r["ldr"], "Estimate. NET loans / customer deposits. The canonical ldr_pct is unavailable because gross loans are not in the source pack.")
        emit(sc, y, BS, "x_statutory_reserve", r["stat_res"], "Statutory reserve balance after the Act 930 s34 transfer (FY2026E: 9M-2026 balance plus the Q4 top-up).")
        emit(sc, y, BS, "x_credit_risk_reserve", H(P9, "x_credit_risk_reserve"), "Held at the 30 Sep 2026 balance.")
        emit(sc, y, IS, "x_statutory_transfer_full_year", r["transfer"], "Full-year Act 930 s34 requirement on full-year profit after tax." + (" 123.167m of it was already transferred in 9M-2026." if first else ""))
        if first:
            emit(sc, y, IS, "x_q4_statutory_transfer", r["q4_transfer"], "Full-year requirement less the 123.167m actually transferred in 9M-2026 (never negative).")
        emit(sc, y, BS, "x_reserve_requirement_calibrated", r["req_cal"], "ILLUSTRATIVE PROXY, not the regulatory calculation: macro CRR x 77.06% x customer deposits, where 77.06% = 3,264.9m mandatory reserves / (20% x 21,185.5m deposits) at 30 Sep 2026 (inferred).")
        emit(sc, y, BS, "x_eligible_reserve_cash", r["elig"], "Mandatory-reserve share of cash (35.51%, observed at 30 Sep 2026) x modelled cash and bank balances. Proxy.")
        emit(sc, y, BS, "x_reserve_gap_calibrated", r["gap_cal"], "max(0, calibrated requirement - eligible reserve cash). Proxy; the issuer reports no liquidity breach.")
        emit(sc, y, BS, "x_reserve_gap_full_deposit_stress", r["gap_full"], "STRESS: max(0, CRR x all customer deposits - eligible reserve cash). Not a regulatory result.")
        emit(sc, y, BS, "x_reserve_gap_eligibility_stress", r["gap_hair"], "STRESS: calibrated requirement against eligible reserve cash 20% lower than observed. Not a regulatory result.")
        emit(sc, y, RT, "x_car_stress_pct", r["car_stress"], "HYPOTHETICAL stress: capital proxy with the numerator 10% lower and risk-weighted assets 10% higher. Not a regulatory result.")
        emit(sc, y, RT, "x_car_stress_shortfall_vs_min_pct", max(0.0, r["min_car"] - r["car_stress"]), "max(0, shared minimum CAR - stressed proxy), percentage points. Zero means no shortfall in this stress.")
        emit(sc, y, RT, "x_car_stress_shortfall_vs_target_pct", max(0.0, TARGET_CAR - r["car_stress"]), "max(0, 15% dividend target - stressed proxy), percentage points.")
        for stmt_, item_, why in [("balance_sheet", "loans_and_advances_gross", "Gross loans are not in the source pack (annual note not extracted) and are not forecast."),
                                  ("balance_sheet", "loan_loss_allowance", "Allowance is not in the source pack and is not forecast; impairment is driven by a cost of risk on net loans."),
                                  ("ratios", "npl_pct", "No NPL path is forecast. Reported NPL was 14.09% (Sep 2025) and 11.32% (Sep 2026); cost of risk is an independent assumption."),
                                  ("ratios", "ldr_pct", "Gross loans are not in the source pack; the net ratio is stored as x_net_ldr_pct."),
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
L = ["# Forecast checks (absa-ghana)", "",
     "Generated by `model.py` from `financials.csv`, `assumptions.json` and the shared macro file. GHS millions; ratios in percent. Every forecast value is an estimate.", "",
     "## 1. Forecast identities (all scenarios, all years)", "",
     "| Scenario | Year | Balance (A = L + E) | Asset lines = total | NII = II - IE | PAT = PBT - tax | Equity roll | CAR proxy | Min CAR |",
     "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
fails = 0
for sc in SCEN:
    for i, y in enumerate(YEARS):
        r = all_res[sc][y]
        prev = all_res[sc][YEARS[i - 1]] if i else None
        bal = abs(r["ta"] - r["tl"] - r["te"]) < 0.001
        sumA = abs(r["cash"] + r["dfb"] + r["secs"] + r["loans"] + r["oth_a_total"] + r["ppe"] - r["ta"]) < 0.001
        nii = abs(r["nii"] - (r["ii"] - r["ie"])) < 0.001
        pat = abs(r["pat"] - (r["pbt"] - r["tax"])) < 0.001
        if i == 0:
            roll = abs(r["te"] - (H(P9, "total_equity") + r["pat"] - H(P9, "profit_after_tax"))) < 0.001
        else:
            roll = abs(r["te"] - (prev["te"] + r["pat"] - r["div"])) < 0.001
        ok = bal and sumA and nii and pat and roll and r["secs"] > 0
        fails += 0 if ok else 1
        low = r["car_proxy"] < r["min_car"]
        L.append(f"| {sc} | {y} | {'PASS' if bal else 'FAIL'} | {'PASS' if sumA and r['secs'] > 0 else 'FAIL'} | {'PASS' if nii else 'FAIL'} | {'PASS' if pat else 'FAIL'} | {'PASS' if roll else 'FAIL'} | {r['car_proxy']:.1f}%{' BELOW MINIMUM' if low else ''} | {r['min_car']:.0f}% |")
L += ["", f"Forecast failures: {fails}", ""]

f26 = all_res["base"]["FY2026E"]
L += ["## 2. Calibration disclosure (a fit, not a validation)", "",
      f"- FY2026E interest income is **anchored** on 9M-2026 x 12/9 = {_ii_anchor:,.1f}m. The forward formula is: 364-day bill + {LOAN_SPREAD*100:.1f} pts on average net loans ({_loan_part26:,.1f}m for 2026), plus on opening securities of {_sec_open:,.1f}m a blended yield: {BILL_WEIGHT*100:.1f}% weight on the average of the 91- and 364-day bills and {(1-BILL_WEIGHT)*100:.1f}% on the government bond yield (an ASSUMED weight, not observed), plus a haircut of **{HAIRCUT:+.2f} pts solved so the formula lands on the anchor**. The match is by construction. The haircut is positive here: the pool earned more than the macro blend ({_unadj:.2f}%), which means either the pool yields more than assumed or, more likely, the 364-day bill + 6 points understates what Absa earns on loans (its loan book is 11.5bn, so a 1 point loan-yield error is about 0.1bn). The split between loans and the pool cannot be identified from the statements; only the total is fitted.",
      f"- FY2026E interest expense is anchored on 9M-2026 x 12/9 = {H(P9, 'interest_expense') * _f:,.1f}m. The cost-of-funds ratio ({COF:.3f}) is solved so that ratio x an assumed {AVG_POLICY_2026*100:.1f}% 2026 average policy rate x average funding {_avg_fund26:,.1f}m gives that figure. The 14.3% average policy rate is taken from the SCB and Zenith bases and was not re-verified.",
      f"- Capital proxy: the reported 19.06% CAR at 30 Sep 2026 scaled by equity / total assets relative to its 30 Sep 2026 level ({EQA0*100:.2f}%). It assumes risk-weighted assets grow with total assets and no change in regulatory deductions. No annual CAR or RWA history exists in the source pack, so this is weaker than the Zenith and UBA proxies.",
      f"- Cash is modelled at (macro CRR 20% + {OPCASH*100:.2f}%) of customer deposits, the extra share solved from 30 Sep 2026 balances. The 20% is a constructed floor, not a tested statutory eligibility.",
      "- The macro file's FY2026E bill rates (91-day 5.81%, 364-day 11.01%) are lower than rates earlier in 2026, so yields from FY2027E depend on the fitted haircut staying stable. That is untested.", ""]

# sensitivity
variants = [("As modelled", run("base"), run("downside")),
            ("Securities haircut 1 pt worse", run("base", haircut=HAIRCUT - 1.0), run("downside", haircut=HAIRCUT - 1.0)),
            ("Securities haircut 1 pt better", run("base", haircut=HAIRCUT + 1.0), run("downside", haircut=HAIRCUT + 1.0)),
            ("Cost-of-funds ratio +25%", run("base", cof_mult=1.25), run("downside", cof_mult=1.25)),
            ("Cost-of-funds ratio -25%", run("base", cof_mult=0.75), run("downside", cof_mult=0.75)),
            ("Loan growth halved", run("base", loan_growth_scale=0.5), run("downside", loan_growth_scale=0.5)),
            ("Tax rate 41% (hypothetical, +5.5 pts)", run("base", tax=0.41), run("downside", tax=0.41))]
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
      f"| Income tax | {H(P9, 'income_tax'):,.1f} | {q['tax']:,.1f} | {q['tax'] - H(P9, 'income_tax'):,.1f} ({(q['tax'] - H(P9, 'income_tax')) / (q['pbt'] - H(P9, 'profit_before_tax')) * 100:.1f}% of Q4 PBT, the 35.5% tax rate) |",
      f"| Impairment | {H(P9, 'impairment_charge'):,.1f} | {q['imp']:,.1f} | {q['imp'] - H(P9, 'impairment_charge'):,.1f} |",
      f"| Profit after tax | {H(P9, 'profit_after_tax'):,.1f} | {q['pat']:,.1f} | {q['pat'] - H(P9, 'profit_after_tax'):,.1f} |", "",
      f"Q4 profit before tax is the 9M run rate for every line except impairment (9M impairment was 198.4m; Q4 gets a charge at the base cost of risk). The 9M-2026 tax rate was 35.6% against 35.7% in FY2025, so the full-year rate comes out at {q['tax'] / q['pbt'] * 100:.1f}%.", ""]

# Q4-only sensitivities (nine months frozen)
b0 = run("base")["FY2026E"]
q4v = [("As modelled", b0), ("Q4 securities yield -2 pts", run("base", q4_yield_pts=-2.0)["FY2026E"]), ("Q4 securities yield +2 pts", run("base", q4_yield_pts=2.0)["FY2026E"]),
       ("Q4 cost of risk 5% (annualised, on net loans)", run("base", q4_cor=0.05)["FY2026E"]), ("Q4 funding cost +25%", run("base", q4_cof_mult=1.25)["FY2026E"]),
       ("Q4 funding cost -25%", run("base", q4_cof_mult=0.75)["FY2026E"]), ("Confirmed 16.1m post-balance-sheet penalty, no tax benefit", run("base", penalty=16.1)["FY2026E"])]
L += ["## 2d. Q4-only sensitivities of FY2026E (nine months frozen at the reported figures)", "", "| Variant | FY2026E PBT | FY2026E tax | FY2026E PAT | Change in PAT |", "| --- | --- | --- | --- | --- |"]
for lab, r_ in q4v:
    L.append(f"| {lab} | {r_['pbt']:,.1f} | {r_['tax']:,.1f} | {r_['pat']:,.1f} | {r_['pat'] - b0['pat']:+,.1f} |")
L += ["", "The 16.1m penalty is the Q3 2026 statement's post-balance-sheet note (via the source pack); whether and when it is recognised is unknown, so it is a stress and not in the base. The 0.36m sanction is immaterial and not modelled.", ""]
alt = {sc: run(sc, stress_gate=True) for sc in SCEN}
L += ["## 2e. Reserve-cash and capital stresses (illustrative proxies, not regulatory calculations)", "",
      f"Reserve proxy calibration: at 30 Sep 2026 mandatory reserves were 3,264.9m; that is {ELIG_SHARE*100:.2f}% of cash and bank balances (observed) and implies the requirement applies to {RES_BASE_SHARE*100:.2f}% of customer deposits at a 20% rate (inferred). The issuer reports no liquidity breach. The cash line itself is modelled as (CRR + a solved share) of deposits, so the calibrated gap is zero by construction; the two stress columns show how much reserve cash the bank would need if the requirement applied to all deposits or if eligible cash were 20% lower.", "",
      "| Scenario | Year | Calibrated gap | Full-deposit stress gap | Eligibility stress gap (20% lower) | Dividend in model | Dividend if eligibility stress withholds | CAR proxy | CAR stress (num -10%, RWA +10%) | Shortfall vs 13% minimum |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for sc in SCEN:
    for y in YEARS:
        r_, a_ = all_res[sc][y], alt[sc][y]
        L.append(f"| {sc} | {y} | {r_['gap_cal']:,.0f} | {r_['gap_full']:,.0f} | {r_['gap_hair']:,.0f} | {r_['div']:,.0f} | {a_['div']:,.0f} | {r_['car_proxy']:.1f}% | {r_['car_stress']:.1f}% | {max(0.0, r_['min_car'] - r_['car_stress']):.1f} pts |")
L += ["", "Reading: under the eligibility stress the model would withhold the dividends shown in the 'if withheld' column. The base dividend uses the calibrated screen, which cannot bind by construction. The stressed capital proxy stays above the minimum in every scenario-year unless a shortfall is shown. None of this is a statement of actual compliance.", ""]

# scenario ordering
L += ["## 3. Scenario ordering of profit after tax", "", "| Year | Downside | Base | Upside | Ordered downside < base < upside? |", "| --- | --- | --- | --- | --- |"]
for y in YEARS:
    d, b, u = (all_res[s][y]["pat"] for s in ("downside", "base", "upside"))
    L.append(f"| {y} | {d:,.0f} | {b:,.0f} | {u:,.0f} | {'equal (FY2026E is anchored on reported nine months)' if d == b == u else 'yes' if d < b < u else 'NO'} |")
L += ["", "Where the order is broken it follows the shared macro file: the downside has higher policy and bill rates, and the bank's earning pool of securities and trading assets (about 11.6bn) is similar in size to its loans (11.5bn), so higher yields lift income. Please challenge it.", ""]

# summary
L += ["## 4. Scenario summary (GHS millions)", "", "| Scenario | Year | Net interest income | Impairment | PAT | Dividends | Equity | CAR proxy | ROE | LDR |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
for sc in SCEN:
    for y in YEARS:
        r = all_res[sc][y]
        L.append(f"| {sc} | {y} | {r['nii']:,.0f} | {r['imp']:,.0f} | {r['pat']:,.0f} | {r['div']:,.0f} | {r['te']:,.0f} | {r['car_proxy']:.1f}% | {r['roe']:.1f}% | {r['ldr']:.0f}% |")
L += ["", "## 5. Reasonableness against history (observed history, estimated forecast)", "",
      f"- ROE history (year-end equity): FY2022 {H('FY2022', 'profit_after_tax') / H('FY2022', 'total_equity') * 100:.1f}% (a loss year), FY2023 {H('FY2023', 'profit_after_tax') / H('FY2023', 'total_equity') * 100:.1f}%, FY2024 {H('FY2024', 'profit_after_tax') / H('FY2024', 'total_equity') * 100:.1f}%, FY2025 {H('FY2025', 'profit_after_tax') / H('FY2025', 'total_equity') * 100:.1f}% (year-end equity). Base forecast ROE is in the table above.",
      "- FY2025 profit after tax was 1,762.4m with an impairment charge of only 3.3m; 9M-2026 impairment is 198.4m. The forecast carries a cost of risk, so FY2026E profit is lower than FY2025.",
      "- Loan-to-deposit ratio was 54.4% at 30 Sep 2026 (net loans / customer deposits).", "",
      "## 6. Known limits", "",
      "- The shared macro rate paths (policy, bills, bonds) drive securities yields; deposit pricing uses a single ratio to the policy rate. There is no deposit beta, no maturity ladder and no FX translation (the statements do not give a net FX position).",
      "- Securities are a plug (liquid assets); if loan growth exceeds deposit growth the plug falls, and a negative plug would fail check 1.",
      "- Borrowings (5,754.5m at 30 Sep 2026, up from 4,077.6m at FY2025) are held flat; terms were not read.",
      "- Trading assets (3,637m) are held flat inside other assets; the history is a codex transcription the owner could not re-read (sources.md).",
      "- 1,115m of dividends was paid in 9M-2026; later dividends use a payout on prior-year profit with caps.",
      "- The CAR figures are proxies; the regulatory ratio, Tier 1 and NPL are not forecast.", ""]
with open(os.path.join(HERE, "checks.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print(f"forecast rows: {len(out)} | forecast failures: {fails} | haircut {HAIRCUT:+.2f} | COF {COF:.3f} | opcash {OPCASH:.4f}")
for sc in ("base", "downside", "upside"):
    for y in ("FY2026E", "FY2030E"):
        r = all_res[sc][y]
        print(sc, y, f"PAT {r['pat']:.0f} equity {r['te']:.0f} CAR {r['car_proxy']:.1f} ROE {r['roe']:.1f} LDR {r['ldr']:.0f} secs {r['secs']:.0f} II {r['ii']:.0f} IE {r['ie']:.0f} div {r['div']:.0f}")
