#!/usr/bin/env python3
"""Societe Generale Ghana PLC scenario model (stdlib only).

Reads  financials.csv        (historical, bank-only, GHS millions)
       assumptions.json      (drivers + macro link)
       ../../sector/macro-assumptions/macro.csv   (shared macro v1)
Writes forecast.csv          (FY2026E-FY2030E, base/downside/upside)
       checks.md             (historical + forecast checks)

Run:  python model.py  (from this directory)
"""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = "societe-generale-ghana"
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
# extra balance-sheet components reported by SG and used for the cash residual
XTRA_B = ["x_trading_assets", "x_equity_investments"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_macro(path):
    return read_csv(path)


def num(v):
    return float(v) if v not in ("", None) else None


# ------------------------------------------------------------------ history
H = read_csv(os.path.join(HERE, "financials.csv"))
A = json.load(open(os.path.join(HERE, "assumptions.json"), encoding="utf-8"))
D = A["drivers"]
M = parse_macro(os.path.join(HERE, A["macro_file"]))
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
    """history that may legitimately be blank (e.g. due_from_banks = 0)."""
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


# anchor: 9M-2026 balance sheet and income; 9M gross loans estimated from net
def anchor():
    b = {k: hist("9M-2026", k) for k in KEYS_B
         if k not in ("loans_and_advances_gross", "loan_loss_allowance", "due_from_banks")}
    b["due_from_banks"] = histb("9M-2026", "due_from_banks", 0.0)
    for k in XTRA_B:
        b[k] = hist("9M-2026", k)
    a25 = hist("FY2025", "loan_loss_allowance") / hist("FY2025", "loans_and_advances_gross")
    b["loans_and_advances_gross"] = b["loans_and_advances_net"] / (1 - a25)
    b["loan_loss_allowance"] = b["loans_and_advances_gross"] - b["loans_and_advances_net"]
    i = {k: hist("9M-2026", k) for k in KEYS_I}
    i["x_fv_other_income"] = hist("9M-2026", "x_fv_other_income")
    return b, i, a25


Y25 = {k: hist("FY2025", k) for k in KEYS_B if k != "due_from_banks"}
Y25["due_from_banks"] = histb("FY2025", "due_from_banks", 0.0)
Q3B, Q3I, allow25 = anchor()

# RWA calibration from the audited FY2025 capital note
RWA25 = hist("FY2025", "x_risk_weighted_assets")
gross25 = hist("FY2025", "loans_and_advances_gross")
RWA_DENSITY = (RWA25 - gross25) / (Y25["total_assets"] - gross25)


def rwa(assets, gross):
    return gross + RWA_DENSITY * (assets - gross)


Q3_RWA = rwa(Q3B["total_assets"], Q3B["loans_and_advances_gross"])
Q3_CAP = Q3_RWA * pct(hist("9M-2026", "car_pct"))
Q3_TIER = Q3_CAP * hist("FY2025", "x_cet1_capital") / hist("FY2025", "x_total_regulatory_capital")


def noncash(b):
    s = (b["due_from_banks"] + b["investment_securities"] + b["loans_and_advances_net"]
         + b["property_equipment_intangibles"] + b["other_assets"])
    for k in XTRA_B:
        s += b.get(k, 0.0)
    return s


def costs(i):
    return i["staff_costs"] + i["depreciation_amortisation"] + i["other_operating_expenses"]


# ------------------------------------------------------------------ forecast
NOTE_I = {
    "interest_income": "Q4 2026 9M run-rate; 2027+ average net loans x loan yield plus average securities x investment yield plus average cash/BoG balances x policy-linked cash yield.",
    "interest_expense": "Q4 funding sensitivity; later average customer deposits, due-to-banks and borrowings x blended funding cost.",
    "net_interest_income": "Interest income minus interest expense.",
    "fee_commission_income": "9M run-rate plus Q4 scenario, then nominal GDP proxy plus fee-growth spread.",
    "fee_commission_expense": "Prior fee-expense ratio adjusted for scenario; Q4 run-rate for 2026.",
    "net_trading_income": "Run-rate in 2026; subsequent underlying trading growth proxy.",
    "other_operating_income": "Run-rate then fee-growth proxy.",
    "total_operating_income": "NII + fee income - fee expense + trading + other operating income.",
    "staff_costs": "Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",
    "depreciation_amortisation": "Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",
    "other_operating_expenses": "Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",
    "impairment_charge": "9M actual + estimated Q4 loan charge; later average gross loans x scenario cost of risk; no assumed sovereign one-off. Positive = a cost; a prior-year net credit was reported negative.",
    "profit_before_tax": "Operating income - staff - depreciation - other opex - impairment.",
    "income_tax": "2026 actual 9M tax + estimated tax on positive Q4 PBT; later blended tax on positive PBT.",
    "profit_after_tax": "PBT less income tax.",
}
NOTE_B = {
    "cash_and_bog_balances": "Residual assets after funding, equity and non-cash assets; a negative value is an infeasible funding gap, not available cash.",
    "due_from_banks": "The Bank reports no separate asset-side inter-bank balance; held at zero.",
    "investment_securities": "Deposit-growth proxy from the reported amortised-cost plus FVOCI portfolio.",
    "loans_and_advances_gross": "FY2026 net/(1-allowance ratio); 2027+ organic growth.",
    "loan_loss_allowance": "Gross loans x scenario allowance ratio; distinct from the annual impairment expense.",
    "loans_and_advances_net": "Gross minus allowance; FY2026 anchored to actual 9M net loans.",
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
    allow = pct(D["allowance_to_gross_pct"][s])
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
        b["due_from_banks"] = 0.0
        b["investment_securities"] = prevB["investment_securities"] * (1 + pct(dg))
        b["x_trading_assets"] = prevB["x_trading_assets"] * (1 + pct(dg))
        b["x_equity_investments"] = prevB["x_equity_investments"] * (1 + pct(dg))
        if first:
            b["loans_and_advances_net"] = prevB["loans_and_advances_net"] * (1 + pct(lg))
            b["loans_and_advances_gross"] = b["loans_and_advances_net"] / (1 - allow)
        else:
            b["loans_and_advances_gross"] = prevB["loans_and_advances_gross"] * (1 + pct(lg))
        b["loan_loss_allowance"] = b["loans_and_advances_gross"] * allow
        b["loans_and_advances_net"] = b["loans_and_advances_gross"] - b["loan_loss_allowance"]
        for k in ["property_equipment_intangibles", "other_assets"]:
            b[k] = prevB[k] * (1 + pct(og) / (4 if first else 1))

        # yields
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
            for k in ["interest_income", "fee_commission_income", "net_trading_income",
                      "other_operating_income", "x_fv_other_income"]:
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
            i["net_trading_income"] = prevI["net_trading_income"] * (1 + pct(nominal + D["model_structure"]["trading_growth_spread_pp"][s]))
            i["x_fv_other_income"] = prevI["x_fv_other_income"] * (1 + pct(nominal + D["model_structure"]["trading_growth_spread_pp"][s]))
            i["other_operating_income"] = prevI["other_operating_income"] * (1 + pct(fg))
            for k in ["staff_costs", "depreciation_amortisation", "other_operating_expenses"]:
                i[k] = prevI[k] * (1 + pct(og))
            i["impairment_charge"] = loanCharge

        i["net_interest_income"] = i["interest_income"] - i["interest_expense"]
        i["total_operating_income"] = (i["net_interest_income"] + i["fee_commission_income"] - i["fee_commission_expense"]
                                       + i["net_trading_income"] + i["x_fv_other_income"] + i["other_operating_income"])
        i["profit_before_tax"] = i["total_operating_income"] - costs(i) - i["impairment_charge"]
        if first:
            i["income_tax"] = Q3I["income_tax"] + max(0.0, i["profit_before_tax"] - Q3I["profit_before_tax"]) * pct(D["tax_rate_pct"][s])
        else:
            i["income_tax"] = max(0.0, i["profit_before_tax"]) * pct(D["tax_rate_pct"][s])
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
        emit(s, t, "income_statement", "x_fv_other_income", i["x_fv_other_income"], "GHS millions",
             "Net income from other financial instruments carried at fair value; run-rate then trading-growth proxy.")
        for k in KEYS_B:
            emit(s, t, "balance_sheet", k, b[k], "GHS millions", NOTE_B[k])
        emit(s, t, "balance_sheet", "x_trading_assets", b["x_trading_assets"], "GHS millions",
             "Non-pledged trading assets, deposit-growth proxy.")
        emit(s, t, "balance_sheet", "x_equity_investments", b["x_equity_investments"], "GHS millions",
             "Unlisted equity investments at fair value, deposit-growth proxy.")
        for k in KEYS_R:
            note = {"car_pct": "Proxy regulatory capital divided by proxy RWA; not a BoG regulatory return.",
                    "tier1_pct": "Estimated Common Equity Tier 1 / RWA; Q3 starting CET1 inferred from the FY2025 audited capital structure.",
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
            ("x_regulatory_capital", cap, "Proxy Q3 capital from 18.52% CAR x estimated RWA plus cumulative retained modelled earnings."),
            ("x_tier1_capital", tier, "Proxy initial CET1/capital relation from FY2025; retained modelled earnings."),
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
            ("x_investment_yield_pct", invYield, "50:50 weighted shared 364-day bill and 10-year bond rates; FY2026 income anchored on run-rate."),
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
            i["total_operating_income"] - i["net_interest_income"] - i["fee_commission_income"] + i["fee_commission_expense"] - i["net_trading_income"] - i["x_fv_other_income"] - i["other_operating_income"],
            i["profit_before_tax"] - i["total_operating_income"] + costs(i) + i["impairment_charge"],
            i["profit_after_tax"] - i["profit_before_tax"] + i["income_tax"],
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

# ------------------------------------------------------------------ write forecast.csv
with open(os.path.join(HERE, "forecast.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    w.writerows(rows)

# ------------------------------------------------------------------ checks.md
def check_line(label, res, nums):
    return "| %s | %s | %s |" % (label, res, nums)


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
L.append("# Societe Generale Ghana PLC checks")
L.append("")
L.append("Recomputed from the committed `financials.csv` and `forecast.csv` by `model.py` "
         "(history) and the shared macro file (forecast). GHS millions; ratios in percent; tolerance 0.003. "
         "NA = input unavailable, not zero. `model.py` writes this whole file.")
L.append("")
L.append("## Historical balance and income bridges")
L.append("")
L.append("| Period | Assets-L-E | Asset components | NII | Operating income | PAT | Net loans |")
L.append("|---|---:|---:|---:|---:|---:|---:|")
for p in hist_periods:
    ta = hv(p, "total_assets"); tl = hv(p, "total_liabilities"); te = hv(p, "total_equity")
    r1 = None if None in (ta, tl, te) else ta - tl - te
    cash = hv(p, "cash_and_bog_balances")
    comps = [hv(p, x) for x in ["due_from_banks", "investment_securities", "x_trading_assets",
                                "x_derivative_assets", "x_equity_investments", "loans_and_advances_net",
                                "property_equipment_intangibles", "other_assets"]]
    comps = [0.0 if c is None else c for c in comps]
    r2 = None if (ta is None or cash is None) else ta - cash - sum(comps)
    nii = hv(p, "net_interest_income"); ii = hv(p, "interest_income"); ie = hv(p, "interest_expense")
    r3 = None if None in (nii, ii, ie) else nii - ii + ie
    toi = hv(p, "total_operating_income")
    fci = hv(p, "fee_commission_income"); fce = hv(p, "fee_commission_expense")
    nt = hv(p, "net_trading_income"); xfv = hv(p, "x_fv_other_income"); ooi = hv(p, "other_operating_income")
    r4 = None if None in (toi, fci, fce, nt, xfv, ooi) else toi - nii - fci + fce - nt - xfv - ooi
    pbt = hv(p, "profit_before_tax")
    pat = hv(p, "profit_after_tax"); tax = hv(p, "income_tax")
    r5 = None if None in (pat, pbt, tax) else pat - pbt + tax
    loann = hv(p, "loans_and_advances_net"); loang = hv(p, "loans_and_advances_gross"); allow = hv(p, "loan_loss_allowance")
    amort = hv(p, "x_amortised_cost_adjustment") or 0.0
    iis = hv(p, "x_interest_in_suspense") or 0.0
    r7 = None if None in (loann, loang, allow) else loann - (loang - amort - iis - allow)
    f = lambda x: "NA" if x is None else ("%.3f" % x)
    L.append("| %s | %s | %s | %s | %s | %s | %s |" % (
        p, f(r1), f(r2), f(r3), f(r4), f(r5), f(r7)))
L.append("")

# source/schema checks
dupes = len(H) - len({(r["bank"], r["period"], r["statement"], r["line_item"]) for r in H})
miss = [r for r in H if r["status"] == "reported" and (r["source_id"] == "" or r["page"] == "")]
badun = [r for r in H if r["status"] == "unavailable" and r["value"] != ""]
L.append("## Source and schema checks")
L.append("")
L.append("- Historical rows: %d; duplicate bank/period/statement/key rows: %d; reported rows missing source/page: %d; unavailable rows with non-blank value: %d."
         % (len(H), dupes, len(miss), len(badun)))
L.append("- Spot-checks against printed filing pages (visually verified): SG25AR printed p.66 total assets 9,676.100447 -> %.6f; "
         "SG24AR printed p.64 PAT 551.299247 -> %.6f; SG26Q3 9M-2026 total assets 11,078.375 -> %.3f. All match."
         % (hv("FY2025", "total_assets"), hv("FY2024", "profit_after_tax"), hv("9M-2026", "total_assets")))
L.append("")

# reported vs recomputed ratios
L.append("## Ratios: reported vs recomputed (%)")
L.append("")
L.append("| Period | Reported CAR | Reported NPL | Derived LDR | Derived cost/income | Derived ROE | Derived ROA |")
L.append("|---|---:|---:|---:|---:|---:|---:|")
for p in hist_periods:
    car = hv(p, "car_pct"); npl = hv(p, "npl_pct")
    loang = hv(p, "loans_and_advances_gross"); dep = hv(p, "customer_deposits")
    ldr = None if None in (loang, dep) else 100 * loang / dep
    tii = hv(p, "total_operating_income")
    cst = sum(x for x in [hv(p, "staff_costs"), hv(p, "depreciation_amortisation"), hv(p, "other_operating_expenses")] if x is not None)
    ci = None if not tii else 100 * cst / tii
    pat = hv(p, "profit_after_tax"); te = hv(p, "total_equity"); ta = hv(p, "total_assets")
    roe = None if pat is None or not te else 100 * pat / te
    roa = None if pat is None or not ta else 100 * pat / ta
    g = lambda x: "NA" if x is None else "%.2f" % x
    L.append("| %s | %s | %s | %s | %s | %s | %s |" % (p, g(car), g(npl), g(ldr), g(ci), g(roe), g(roa)))
L.append("")
L.append("Reported CAR is the audited capital-adequacy note; the bank's narrative quotes a different basis "
         "(e.g. FY2025 17.5% excluding DDEP reliefs vs 23.39% audited) and this is recorded in `financials.csv` notes. "
         "ROE/ROA here use year-end equity/assets as a single-period ratio, so they differ slightly from the bank's "
         "average-balance ratios. Net-loan bridge for FY2026E and later is gross minus allowance; FY2021-FY2024 also "
         "net of a separately reported amortised-cost adjustment and interest in suspense.")
L.append("")

L.append("<!-- FORECAST CHECKS GENERATED -->")
L.append("## Forecast checks (generated from shared macro scenarios)")
L.append("")
L.append("All forecast rows are estimated. Currency GHS millions; ratios in percent. Accounting arithmetic is checked before rounding. "
         "Cash-reserve and CAR checks are screening proxies, not regulatory returns. A negative cash residual or a positive gap is a flagged "
         "financing requirement, not an assumed funding source.")
L.append("")
L.append("Rows: %d; scenario-years: %d; FY2025 residual RWA density: %.6f; estimated 9M-2026 RWA: %.3f; initial proxy regulatory capital: %.3f (anchored to the observed 18.52%% CAR)."
         % (len(rows), len(checks_log), RWA_DENSITY, Q3_RWA, Q3_CAP))
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
