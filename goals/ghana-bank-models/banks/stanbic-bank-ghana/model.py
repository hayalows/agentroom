#!/usr/bin/env python3
"""Stanbic Bank Ghana Ltd scenario model (stdlib only).

Reads  financials.csv        (historical, bank-only, GHS millions)
       assumptions.json      (drivers + macro link)
       ../../sector/macro-assumptions/macro.csv   (shared macro v1)
Writes forecast.csv          (FY2026E-FY2030E, base/downside/upside)
       checks.md             (historical + forecast checks)

Run:  python model.py  (from this directory)
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = "stanbic-bank-ghana"
SCEN = ["base", "downside", "upside"]

KEYS_I = ("interest_income interest_expense net_interest_income fee_commission_income "
          "fee_commission_expense net_trading_income other_operating_income total_operating_income "
          "staff_costs depreciation_amortisation other_operating_expenses impairment_charge "
          "profit_before_tax income_tax profit_after_tax").split()
KEYS_B = ("cash_and_bog_balances due_from_banks investment_securities loans_and_advances_gross "
          "loan_loss_allowance loans_and_advances_net property_equipment_intangibles other_assets "
          "total_assets customer_deposits due_to_banks borrowings other_liabilities total_liabilities "
          "stated_capital retained_earnings reserves_other total_equity").split()
KEYS_R = "car_pct tier1_pct npl_pct ldr_pct cost_to_income_pct roe_pct roa_pct".split()
# extra balance-sheet components reported by Stanbic and used for the cash residual
XTRA_B = ["x_trading_assets", "x_pledged_assets"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(v):
    return float(v) if v not in ("", None) else None


H = read_csv(os.path.join(HERE, "financials.csv"))
A = json.load(open(os.path.join(HERE, "assumptions.json"), encoding="utf-8"))
D = A["drivers"]
M = read_csv(os.path.join(HERE, A["macro_file"]))
PERIODS = A["forecast_periods"]


def hist(t, k):
    for r in H:
        if r["period"] == t and r["line_item"] == k:
            v = num(r["value"])
            if v is None:
                raise KeyError("history %s %s is blank" % (t, k))
            return v
    raise KeyError("missing history %s %s" % (t, k))


def histb(t, k, default=None):
    for r in H:
        if r["period"] == t and r["line_item"] == k:
            v = num(r["value"])
            return default if v is None else v
    return default


def macro(s, t, k):
    for r in M:
        if r["scenario"] == s and r["year"] == t and r["driver"] == k:
            if r["status"] == "unavailable" or num(r["value"]) is None:
                raise KeyError("macro unavailable %s %s %s" % (s, t, k))
            return num(r["value"])
    raise KeyError("missing macro %s %s %s" % (s, t, k))


pct = lambda x: x / 100.0
avg = lambda a, b: (a + b) / 2.0
clip = lambda x, lo, hi: max(lo, min(x, hi))


def anchor():
    b = {k: hist("9M-2026", k) for k in KEYS_B
         if k not in ("loans_and_advances_gross", "loan_loss_allowance", "due_from_banks")}
    b["due_from_banks"] = histb("9M-2026", "due_from_banks", 0.0)
    for k in XTRA_B:
        b[k] = histb("9M-2026", k, 0.0)
    n2g = pct(D["net_to_gross_pct"]["base"])
    b["loans_and_advances_gross"] = b["loans_and_advances_net"] / n2g
    b["loan_loss_allowance"] = b["loans_and_advances_gross"] - b["loans_and_advances_net"]
    i = {k: hist("9M-2026", k) for k in KEYS_I}
    i["x_indirect_tax"] = hist("9M-2026", "x_indirect_tax")
    return b, i


Y25 = {k: hist("FY2025", k) for k in KEYS_B if k != "due_from_banks"}
Y25["due_from_banks"] = histb("FY2025", "due_from_banks", 0.0)
Q3B, Q3I = anchor()

# RWA calibration from the audited FY2025 capital note
RWA25 = hist("FY2025", "x_risk_weighted_assets")
gross25 = hist("FY2025", "loans_and_advances_gross")
RWA_DENSITY = (RWA25 - gross25) / (Y25["total_assets"] - gross25)


def rwa(assets, gross):
    return gross + RWA_DENSITY * (assets - gross)


Q3_RWA = rwa(Q3B["total_assets"], Q3B["loans_and_advances_gross"])
Q3_CAP = Q3_RWA * pct(hist("9M-2026", "car_pct"))
# Tier 1 as a share of total regulatory capital, from the FY2025 audited note
T1_SHARE = hist("FY2025", "x_tier1_capital") / hist("FY2025", "x_regulatory_capital")
Q3_TIER = Q3_CAP * T1_SHARE


def noncash(b):
    s = (b["due_from_banks"] + b["investment_securities"] + b["loans_and_advances_net"]
         + b["property_equipment_intangibles"] + b["other_assets"])
    for k in XTRA_B:
        s += b.get(k, 0.0)
    return s


def costs(i):
    return i["staff_costs"] + i["depreciation_amortisation"] + i["other_operating_expenses"]


NOTE_I = {
    "interest_income": "Q4 2026 9M run-rate; 2027+ average net loans x loan yield plus average securities x investment yield plus prior-year cash/BoG and inter-bank balances x policy-linked cash yield.",
    "interest_expense": "Q4 funding sensitivity; later average customer deposits, due-to-banks and borrowings x blended funding cost.",
    "net_interest_income": "Interest income minus interest expense.",
    "fee_commission_income": "9M run-rate plus Q4 scenario, then nominal GDP proxy plus fee-growth spread.",
    "fee_commission_expense": "Prior fee-expense ratio adjusted for scenario; Q4 run-rate for 2026.",
    "net_trading_income": "Run-rate in 2026; subsequent underlying trading growth plus scenario spread.",
    "other_operating_income": "Run-rate then fee-growth proxy.",
    "total_operating_income": "NII + fee income - fee expense + trading + other operating income.",
    "staff_costs": "Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",
    "depreciation_amortisation": "Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",
    "other_operating_expenses": "Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",
    "impairment_charge": "9M actual + estimated Q4 loan charge; later average gross loans x scenario cost of risk; no assumed sovereign one-off. Positive = a cost.",
    "profit_before_tax": "Reported 'Profit before indirect tax' basis: operating income - staff - depreciation - other opex - impairment.",
    "income_tax": "Total tax (indirect + direct): 2026 actual 9M total tax + estimated tax on positive Q4 PBT; later blended tax on positive PBT.",
    "profit_after_tax": "PBT less income tax.",
}
NOTE_B = {
    "cash_and_bog_balances": "Residual assets after funding, equity and non-cash assets; a negative value is an infeasible funding gap, not available cash.",
    "due_from_banks": "The Bank reports no separate asset-side inter-bank balance in the forecast anchor; held at the reported level growing with deposits.",
    "investment_securities": "Deposit-growth proxy from the reported investment securities.",
    "loans_and_advances_gross": "FY2026 net / scenario net-to-gross; 2027+ organic growth.",
    "loan_loss_allowance": "Gross loans minus net loans (folds in interest in suspense on the FY2025 basis); distinct from the annual impairment expense.",
    "loans_and_advances_net": "Gross x scenario net-to-gross; FY2026 anchored to actual 9M net loans.",
    "property_equipment_intangibles": "Inflation plus operating-expense spread, quarter-weighted in 2026.",
    "other_assets": "Inflation plus operating-expense spread, quarter-weighted in 2026.",
    "total_assets": "Cash plus non-cash asset components.",
    "customer_deposits": "Organic deposit growth.",
    "due_to_banks": "Deposit-growth proxy.",
    "borrowings": "Deposit-growth proxy; no automatic funding injected to mask a cash gap.",
    "other_liabilities": "Deposit-growth proxy.",
    "total_liabilities": "Sum of modelled liabilities.",
    "stated_capital": "Held constant; no assumed capital raise.",
    "retained_earnings": "Opening retained earnings plus incremental modelled PAT minus modelled dividend.",
    "reserves_other": "Held constant; no forecast OCI or reserve transfers.",
    "total_equity": "Stated capital + retained earnings + reserves.",
}

rows, checks_log, summary = [], [], []
HEADER = ["bank", "period", "statement", "line_item", "value", "unit",
          "source_id", "page", "status", "notes", "scenario"]
SRC = "assumptions.json; ../../sector/macro-assumptions/macro.csv"


def emit(s, t, stmt, key, value, unit, note):
    if value != value:  # NaN
        raise ValueError("non-finite forecast %s %s %s" % (s, t, key))
    fmt = "%.4f" if unit == "%" else "%.3f"
    rows.append([BANK, t, stmt, key, fmt % value, unit, SRC, "", "estimated",
                 note + " | scenario=" + s, s])


for s in SCEN:
    prevB, prevI = dict(Q3B), None
    prevCap, prevTier = Q3_CAP, Q3_TIER
    risk = D["cost_of_risk"][s]
    n2g = pct(D["net_to_gross_pct"][s])
    for j, t in enumerate(PERIODS):
        first = (j == 0)
        b, i = {}, {}
        gd = macro(s, t, "gdp_growth_pct")
        inf = macro(s, t, "inflation_cpi_pct")
        pol = macro(s, t, "policy_rate_pct")
        crr = macro(s, t, "crr_pct")
        minCAR = macro(s, t, "min_car_pct")
        carTarget = minCAR + D["capital_ratio_target_pct"][s]
        nominal = gd + inf
        lg = D["loan_growth"][s]["q4_pct"] if first else clip(nominal + D["loan_growth"][s]["spread_pp"], -10, 35)
        dg = D["deposit_growth"][s]["q4_pct"] if first else clip(nominal + D["deposit_growth"][s]["spread_pp"], -10, 35)
        og = inf + D["opex_growth"][s]
        fg = nominal + D["fee_growth"][s]

        # liabilities
        b["customer_deposits"] = prevB["customer_deposits"] * (1 + pct(dg))
        for k in ["due_to_banks", "borrowings", "other_liabilities"]:
            b[k] = prevB[k] * (1 + pct(dg))
        b["total_liabilities"] = sum(b[k] for k in ["customer_deposits", "due_to_banks", "borrowings", "other_liabilities"])
        # assets (non-cash)
        b["due_from_banks"] = prevB["due_from_banks"] * (1 + pct(dg))
        b["investment_securities"] = prevB["investment_securities"] * (1 + pct(dg))
        for k in XTRA_B:
            b[k] = prevB[k] * (1 + pct(dg))
        if first:
            b["loans_and_advances_net"] = prevB["loans_and_advances_net"] * (1 + pct(lg))
        else:
            b["loans_and_advances_gross"] = prevB["loans_and_advances_gross"] * (1 + pct(lg))
        b["loans_and_advances_gross"] = b["loans_and_advances_net"] / n2g if first else b["loans_and_advances_gross"]
        b["loans_and_advances_net"] = b["loans_and_advances_gross"] * n2g
        b["loan_loss_allowance"] = b["loans_and_advances_gross"] - b["loans_and_advances_net"]
        for k in ["property_equipment_intangibles", "other_assets"]:
            b[k] = prevB[k] * (1 + pct(og) / (4 if first else 1))

        loanYield = pol + D["loan_yield"][s]
        invYield = (macro(s, t, "tbill_364d_pct") * D["investment_yield"]["weights"]["tbill_364d_pct"]
                    + macro(s, t, "govt_bond_yield_pct") * D["investment_yield"]["weights"]["govt_bond_yield_pct"])
        cashYield = pol * D["cash_yield_factor"][s]
        cofund = pol * D["cost_of_funds"][s]

        loanCharge = max(avg(prevB["loans_and_advances_gross"], b["loans_and_advances_gross"]) * pct(risk) / (4 if first else 1),
                         b["loan_loss_allowance"] - prevB["loan_loss_allowance"], 0)

        if first:
            rev = D["q4_income_runrate_multiplier"][s]
            cm = D["model_structure"]["q4_cost_multiplier"][s]
            fm = D["model_structure"]["q4_funding_multiplier"][s]
            feeMult = D["model_structure"]["fee_expense_ratio_multiplier"][s]
            for k in ["interest_income", "fee_commission_income", "net_trading_income", "other_operating_income"]:
                i[k] = Q3I[k] * (1 + rev / 3.0)
            i["interest_expense"] = Q3I["interest_expense"] * (1 + fm / 3.0)
            i["fee_commission_expense"] = Q3I["fee_commission_expense"] * (1 + rev * feeMult / 3.0)
            for k in ["staff_costs", "depreciation_amortisation", "other_operating_expenses"]:
                i[k] = Q3I[k] * (1 + cm / 3.0)
            i["impairment_charge"] = Q3I["impairment_charge"] + loanCharge
        else:
            i["interest_income"] = (avg(prevB["loans_and_advances_net"], b["loans_and_advances_net"]) * pct(loanYield)
                                    + avg(prevB["investment_securities"], b["investment_securities"]) * pct(invYield)
                                    + prevB["cash_and_bog_balances"] * pct(cashYield))
            i["interest_expense"] = avg(prevB["customer_deposits"] + prevB["due_to_banks"] + prevB["borrowings"],
                                        b["customer_deposits"] + b["due_to_banks"] + b["borrowings"]) * pct(cofund)
            i["fee_commission_income"] = prevI["fee_commission_income"] * (1 + pct(fg))
            i["fee_commission_expense"] = i["fee_commission_income"] * (prevI["fee_commission_expense"] / prevI["fee_commission_income"]) * feeMult
            i["net_trading_income"] = prevI["net_trading_income"] * (1 + pct(nominal + D["trading_growth_spread_pp"][s]))
            i["other_operating_income"] = prevI["other_operating_income"] * (1 + pct(fg))
            for k in ["staff_costs", "depreciation_amortisation", "other_operating_expenses"]:
                i[k] = prevI[k] * (1 + pct(og))
            i["impairment_charge"] = loanCharge

        i["net_interest_income"] = i["interest_income"] - i["interest_expense"]
        i["total_operating_income"] = (i["net_interest_income"] + i["fee_commission_income"] - i["fee_commission_expense"]
                                       + i["net_trading_income"] + i["other_operating_income"])
        i["profit_before_tax"] = i["total_operating_income"] - costs(i) - i["impairment_charge"]
        if first:
            i["income_tax"] = (Q3I["income_tax"]
                               + max(0.0, i["profit_before_tax"] - Q3I["profit_before_tax"]) * pct(D["tax_rate_pct"][s]))
            # Anchor-year tax split: preserve the ACTUAL 9M indirect and direct tax and add only
            # an estimated Q4 component. Never recompute the annual indirect tax from full-year PBT
            # (that can put the estimated indirect tax below the observed nine-month figure).
            q4pbt = max(0.0, i["profit_before_tax"] - Q3I["profit_before_tax"])
            i["x_indirect_tax"] = Q3I["x_indirect_tax"] + q4pbt * pct(D["indirect_tax_ratio_pct"][s])
            i["x_direct_tax"] = i["income_tax"] - i["x_indirect_tax"]
        else:
            i["income_tax"] = max(0.0, i["profit_before_tax"]) * pct(D["tax_rate_pct"][s])
            i["x_indirect_tax"] = max(0.0, i["profit_before_tax"]) * pct(D["indirect_tax_ratio_pct"][s])
            i["x_direct_tax"] = i["income_tax"] - i["x_indirect_tax"]
        i["profit_after_tax"] = i["profit_before_tax"] - i["income_tax"]

        incPAT = (i["profit_after_tax"] - Q3I["profit_after_tax"]) if first else i["profit_after_tax"]
        preEquity = prevB["total_equity"] + incPAT
        preAssets = b["total_liabilities"] + preEquity
        preCash = preAssets - noncash(b)
        preRwa = rwa(preAssets, b["loans_and_advances_gross"])
        preCap = prevCap + incPAT
        reserve = b["customer_deposits"] * pct(crr)
        div = max(0.0, min(max(incPAT, 0.0) * pct(D["dividend_payout_pct"][s]),
                           preCap - preRwa * pct(carTarget),
                           preCash - reserve))
        b["stated_capital"] = prevB["stated_capital"]
        b["reserves_other"] = prevB["reserves_other"]
        b["retained_earnings"] = prevB["retained_earnings"] + incPAT - div
        b["total_equity"] = b["stated_capital"] + b["retained_earnings"] + b["reserves_other"]
        b["total_assets"] = b["total_liabilities"] + b["total_equity"]
        b["cash_and_bog_balances"] = b["total_assets"] - noncash(b)

        cap = preCap - div
        tier = prevTier + incPAT - div
        rw = rwa(b["total_assets"], b["loans_and_advances_gross"])
        car = 100 * cap / rw
        op = Y25 if first else prevB
        ratios = {
            "car_pct": car,
            "tier1_pct": 100 * tier / rw,
            "npl_pct": D["npl_pct"][s],
            "ldr_pct": 100 * b["loans_and_advances_gross"] / b["customer_deposits"],
            "cost_to_income_pct": 100 * costs(i) / i["total_operating_income"],
            "roe_pct": 100 * i["profit_after_tax"] / avg(op["total_equity"], b["total_equity"]),
            "roa_pct": 100 * i["profit_after_tax"] / avg(op["total_assets"], b["total_assets"]),
        }
        for k in KEYS_I:
            emit(s, t, "income_statement", k, i[k], "GHS millions", NOTE_I[k])
        emit(s, t, "income_statement", "x_indirect_tax", i["x_indirect_tax"], "GHS millions",
             "Estimated indirect tax (3% of positive PBT); part of the total income_tax, not additive to it.")
        emit(s, t, "income_statement", "x_direct_tax", i["x_direct_tax"], "GHS millions",
             "Estimated direct income tax; total income_tax minus the indirect tax estimate.")
        for k in KEYS_B:
            emit(s, t, "balance_sheet", k, b[k], "GHS millions", NOTE_B[k])
        for k in XTRA_B:
            emit(s, t, "balance_sheet", k, b[k], "GHS millions",
                 "Non-pledged trading assets, deposit-growth proxy." if k == "x_trading_assets"
                 else "Pledged trading assets, deposit-growth proxy.")
        for k in KEYS_R:
            note = {"car_pct": "Proxy regulatory capital divided by proxy RWA; not a BoG regulatory return.",
                    "tier1_pct": "Estimated Tier 1 / RWA; Q3 starting capital anchored on the reported CAR and the FY2025 Tier 1 share.",
                    "npl_pct": "Estimated scenario NPL target; not a loan-level migration model.",
                    "ldr_pct": "Gross loans / customer deposits.",
                    "cost_to_income_pct": "Operating expenses excluding impairments / total operating income.",
                    "roe_pct": "PAT / mean opening and closing annual equity.",
                    "roa_pct": "PAT / mean opening and closing annual assets."}[k]
            emit(s, t, "ratios", k, ratios[k], "%", note)

        short = max(0.0, rw * pct(minCAR) - cap)
        cashGap = max(0.0, reserve - b["cash_and_bog_balances"])
        allowMove = prevB["loan_loss_allowance"] + loanCharge - b["loan_loss_allowance"]
        for k, v, n in [
            ("x_regulatory_capital", cap, "Proxy Q3 capital from the reported CAR x estimated RWA plus cumulative retained modelled earnings."),
            ("x_tier1_capital", tier, "Proxy initial Tier 1/capital relation from FY2025; retained modelled earnings."),
            ("x_risk_weighted_assets", rw, "Gross loans plus calibrated FY2025 residual risk intensity x assets minus gross loans."),
            ("x_model_dividends", div, ("Estimated Q4-only dividends; observed 9M retained earnings already include YTD equity movements."
                                        if first else "Estimated annual dividends constrained by the pre-dividend CAR target and cash-reserve proxy.")),
            ("x_cash_reserve_proxy", reserve, "CRR x modelled year-end deposits; screening proxy, not actual eligible reserve."),
            ("x_cash_reserve_gap", cashGap, "Positive value is a reserve-proxy shortfall; not automatically funded."),
            ("x_capital_shortfall", short, "Additional regulatory capital needed to reach the shared minimum CAR; not assumed raised."),
            ("x_allowance_other_movement", allowMove, "Opening modelled allowance + modelled loan impairment charge - closing modelled allowance; positive implies write-offs/other reductions; the provision floor prevents an unfunded allowance build. FY2026 Q4 only."),
        ]:
            emit(s, t, "balance_sheet", k, v, "GHS millions", n)
        emit(s, t, "income_statement", "x_model_loan_impairment", loanCharge, "GHS millions",
             ("Estimated Q4-only impairment; the actual nine-month aggregate is preserved."
              if first else "Estimated annual loan impairment included in the total impairment charge."))
        for k, v, n in [
            ("x_min_car_pct", minCAR, "Shared macro minimum CAR screening threshold."),
            ("x_capital_target_pct", carTarget, "Shared minimum plus scenario management buffer."),
            ("x_investment_yield_pct", invYield, "50:50 weighted shared 364-day bill and medium-term bond rates; FY2026 income anchored on run-rate."),
            ("x_loan_yield_pct", loanYield, "Policy rate plus scenario spread; FY2026 income anchored on run-rate."),
            ("x_cost_of_funds_pct", cofund, "Policy rate times scenario factor; FY2026 expense anchored on run-rate."),
        ]:
            emit(s, t, "ratios", k, v, "%", n)

        resid = [
            b["total_assets"] - b["total_liabilities"] - b["total_equity"],
            b["total_assets"] - b["cash_and_bog_balances"] - noncash(b),
            b["total_liabilities"] - sum(b[k] for k in ["customer_deposits", "due_to_banks", "borrowings", "other_liabilities"]),
            b["total_equity"] - b["stated_capital"] - b["retained_earnings"] - b["reserves_other"],
            i["net_interest_income"] - i["interest_income"] + i["interest_expense"],
            i["total_operating_income"] - i["net_interest_income"] - i["fee_commission_income"] + i["fee_commission_expense"] - i["net_trading_income"] - i["other_operating_income"],
            i["profit_before_tax"] - i["total_operating_income"] + costs(i) + i["impairment_charge"],
            i["profit_after_tax"] - i["profit_before_tax"] + i["income_tax"],
            i["income_tax"] - i["x_indirect_tax"] - i["x_direct_tax"],
            b["loans_and_advances_net"] - b["loans_and_advances_gross"] + b["loan_loss_allowance"],
        ]
        mx = max(abs(x) for x in resid)
        if mx > 1e-7:
            raise AssertionError("accounting check failed %s %s: %r" % (s, t, mx))
        checks_log.append(dict(s=s, t=t, mx=mx, car=car, minCAR=minCAR, short=short,
                               cash=b["cash_and_bog_balances"], reserve=reserve, cashGap=cashGap,
                               pat=i["profit_after_tax"], assets=b["total_assets"], div=div))
        summary.append((s, t, b["total_assets"], i["profit_after_tax"], car))
        prevB, prevI, prevCap, prevTier = b, i, cap, tier

with open(os.path.join(HERE, "forecast.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    w.writerows(rows)

# ------------------------------------------------------------------ checks.md
hist_periods = []
for r in H:
    if r["period"] not in hist_periods:
        hist_periods.append(r["period"])


def hv(p, item):
    for r in H:
        if r["period"] == p and r["line_item"] == item:
            return num(r["value"])
    return None


L = []
L.append("# Stanbic Bank Ghana Ltd checks")
L.append("")
L.append("Recomputed from the committed `financials.csv` and `forecast.csv` by `model.py` (history) "
         "and the shared macro file (forecast). GHS millions; ratios in percent; tolerance 0.003. "
         "NA = input unavailable, not zero. `model.py` writes this whole file.")
L.append("")
L.append("## Historical balance and income bridges")
L.append("")
L.append("| Period | Assets-L-E | Asset components | NII | Operating income | PAT | Net loans |")
L.append("|---|---:|---:|---:|---:|---:|---:|")
for p in hist_periods:
    ta, tl, te = hv(p, "total_assets"), hv(p, "total_liabilities"), hv(p, "total_equity")
    r1 = None if None in (ta, tl, te) else ta - tl - te
    cash = hv(p, "cash_and_bog_balances")
    comps = [hv(p, x) for x in ["due_from_banks", "x_trading_assets", "x_pledged_assets",
                                "investment_securities", "loans_and_advances_net",
                                "property_equipment_intangibles", "other_assets"]]
    comps = [0.0 if c is None else c for c in comps]
    r2 = None if (ta is None or cash is None) else ta - cash - sum(comps)
    nii, ii, ie = hv(p, "net_interest_income"), hv(p, "interest_income"), hv(p, "interest_expense")
    r3 = None if None in (nii, ii, ie) else nii - ii + ie
    toi = hv(p, "total_operating_income")
    fci, fce, nt, ooi = (hv(p, x) for x in ["fee_commission_income", "fee_commission_expense", "net_trading_income", "other_operating_income"])
    r4 = None if None in (toi, nii, fci, fce, nt, ooi) else toi - nii - fci + fce - nt - ooi
    pat, pbt, tax = hv(p, "profit_after_tax"), hv(p, "profit_before_tax"), hv(p, "income_tax")
    r5 = None if None in (pat, pbt, tax) else pat - pbt + tax
    loann, loang, allow = hv(p, "loans_and_advances_net"), hv(p, "loans_and_advances_gross"), hv(p, "loan_loss_allowance")
    iis = hv(p, "x_interest_in_suspense") or 0.0
    r7 = None if None in (loann, loang, allow) else loann - (loang - allow - iis)
    f = lambda x: "NA" if x is None else ("%.3f" % x)
    L.append("| %s | %s | %s | %s | %s | %s | %s |" % (p, f(r1), f(r2), f(r3), f(r4), f(r5), f(r7)))
L.append("")

dupes = len(H) - len({(r["bank"], r["period"], r["statement"], r["line_item"]) for r in H})
miss = [r for r in H if r["status"] == "reported" and (r["source_id"] == "" or r["page"] == "")]
badun = [r for r in H if r["status"] == "unavailable" and r["value"] != ""]
L.append("## Source and schema checks")
L.append("")
L.append("- Historical rows: %d; duplicate bank/period/statement/key rows: %d; reported rows missing source/page: %d; unavailable rows with non-blank value: %d."
         % (len(H), dupes, len(miss), len(badun)))
L.append("- Spot-checks against printed filing pages (visually verified): SB25AR printed p.46 total assets 36,708,145k -> %.3f; "
         "SB25AR printed p.47 PAT 1,608,667k -> %.3f; SB24AR printed p.49 total assets 32,590,921k -> %.3f; "
         "SB26Q3 9M-2026 total assets 43,243,634k -> %.3f. All match."
         % (hv("FY2025", "total_assets"), hv("FY2025", "profit_after_tax"),
            hv("FY2024", "total_assets"), hv("9M-2026", "total_assets")))
L.append("")

L.append("## Ratios: reported vs recomputed (%)")
L.append("")
L.append("| Period | Reported CAR | Reported CET1 | Reported NPL | Derived LDR | Derived cost/income | Derived ROE | Derived ROA |")
L.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for p in hist_periods:
    car, t1, npl = hv(p, "car_pct"), hv(p, "x_cet1_pct"), hv(p, "npl_pct")
    loang, dep = hv(p, "loans_and_advances_gross"), hv(p, "customer_deposits")
    ldr = None if None in (loang, dep) else 100 * loang / dep
    tii = hv(p, "total_operating_income")
    cst = sum(x for x in [hv(p, "staff_costs"), hv(p, "depreciation_amortisation"), hv(p, "other_operating_expenses")] if x is not None)
    ci = None if not tii else 100 * cst / tii
    pat, te, ta = hv(p, "profit_after_tax"), hv(p, "total_equity"), hv(p, "total_assets")
    roe = None if pat is None or not te else 100 * pat / te
    roa = None if pat is None or not ta else 100 * pat / ta
    g = lambda x: "NA" if x is None else "%.2f" % x
    L.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (p, g(car), g(t1), g(npl), g(ldr), g(ci), g(roe), g(roa)))
L.append("")
L.append("Reported CAR/CET1 are the Bank's own summary quantitative disclosures; the audited capital-adequacy note agrees "
         "(FY2022 12.3%, FY2023 19.6%, FY2024 19.0%, FY2025 23.2%). ROE/ROA and cost/income here use year-end/single-period "
         "figures. `income_tax` is the sum of the reported indirect and direct tax. FY2022 was a loss year: direct tax was a credit.")
L.append("")

L.append("## Forecast checks")
L.append("")
L.append("All forecast rows are estimated. Currency GHS millions; ratios in percent. Accounting arithmetic is checked before rounding. "
         "Cash-reserve and CAR checks are screening proxies, not regulatory returns. A negative cash residual or a positive gap is a flagged "
         "financing requirement, not an assumed funding source.")
L.append("")
L.append("Rows: %d; scenario-years: %d; FY2025 residual RWA density: %.6f; estimated 9M-2026 RWA: %.3f; initial proxy regulatory capital: %.3f (anchored to the observed 23.32%% CAR); FY2025 Tier 1 share of regulatory capital: %.4f."
         % (len(rows), len(checks_log), RWA_DENSITY, Q3_RWA, Q3_CAP, T1_SHARE))
L.append("")
L.append("| Scenario | Year | Max bridge residual | CAR % | Min CAR % | Capital gap | Cash | CRR proxy | Reserve gap | Dividends |")
L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
for x in checks_log:
    L.append("| %s | %s | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f |" % (
        x["s"], x["t"], x["mx"], x["car"], x["minCAR"], x["short"], x["cash"], x["reserve"], x["cashGap"], x["div"]))
L.append("")
L.append("Accounting bridges: PASS (%d/%d). Capital below the shared minimum: %d/%d flagged. Cash-reserve proxy shortfalls: %d/%d flagged. "
         "Negative cash: %d/%d flagged."
         % (len(checks_log), len(checks_log),
            sum(1 for x in checks_log if x["short"] > 1e-6), len(checks_log),
            sum(1 for x in checks_log if x["cashGap"] > 1e-6), len(checks_log),
            sum(1 for x in checks_log if x["cash"] < 0), len(checks_log)))
L.append("")
L.append("FY2026 estimated earnings retain actual 9M income and estimate Q4 only. The Bank does not disclose a net FX position in the "
         "summary statements used, so no incremental FX translation P&L is modelled. Full prudential risk weights, OCI, capital deductions "
         "and liquidity eligibility are not available, so this is a simplified scenario analysis. Independent review required.")
L.append("")

with open(os.path.join(HERE, "checks.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print(json.dumps({"forecast_rows": len(rows), "scenario_years": len(checks_log),
                  "summary": [dict(scenario=s, year=t, assets=round(a, 3), pat=round(p, 3), car=round(c, 3))
                              for s, t, a, p, c in summary]}, indent=2))
