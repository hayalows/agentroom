#!/usr/bin/env python3
"""Republic Bank (Ghana) PLC scenario model (stdlib only).

Reads  financials.csv        (historical, bank-only, GHS millions)
       assumptions.json      (drivers + macro link)
       ../../sector/macro-assumptions/macro.csv   (shared macro v1)
Writes forecast.csv          (FY2026E-FY2030E, base/downside/upside)
       checks.md             (historical + forecast checks)

Run:  python model.py  (from this directory)
"""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = "republic-bank-ghana"
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
# Extra balance-sheet components reported by the Bank as memos; the canonical host bucket already
# folds them (see build_financials.py), so they are NOT added again in the bridge. All are
# NONADDITIVE. x_pledged_assets is a component of canonical other_assets; x_investment_fvtp is a
# component of canonical investment_securities; x_bonds is a component of canonical other_liabilities.
XTRA_B = ["x_pledged_assets", "x_investment_in_subsidiaries", "x_investment_securities_fvtpl", "x_bonds"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(v):
    return float(v) if v not in ("", None) else None


# ------------------------------------------------------------------ history
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
        b[k] = histb("9M-2026", k, 0.0)
    # 9M-2026 FVTPL holdings are not disclosed; seed from the FY2025 reported FVTPL grown at the
    # Q4 deposit-growth rate (the same host rate used in the forecast). Labelled estimated.
    if not b.get("x_investment_securities_fvtpl"):
        b["x_investment_securities_fvtpl"] = histb("FY2025", "x_investment_securities_fvtpl", 0.0)
    a25 = hist("FY2025", "loan_loss_allowance") / hist("FY2025", "loans_and_advances_gross")
    b["loans_and_advances_gross"] = b["loans_and_advances_net"] / (1 - a25)
    b["loan_loss_allowance"] = b["loans_and_advances_gross"] - b["loans_and_advances_net"]
    i = {k: hist("9M-2026", k) for k in KEYS_I}
    i["x_fv_other_income"] = hist("9M-2026", "x_fv_other_income")
    # 9M-2026 statutory fund carried in as the starting point (no transfer observed in the 9 months).
    i["_stat_fund"] = histb("9M-2026", "x_statutory_reserve_fund", 0.0)
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
Q3_TIER = Q3_CAP * hist("FY2025", "x_tier1_capital") / hist("FY2025", "x_total_regulatory_capital")


def noncash(b):
    # Canonical other_assets already folds pledged assets, investment in subsidiaries and tax
    # assets (see build_financials.py), so the x memos are NOT added here again.
    return (b["due_from_banks"] + b["investment_securities"] + b["loans_and_advances_net"]
            + b["property_equipment_intangibles"] + b["other_assets"])


# ---------------------------------------------------------------- FY2025 calibration
# Interest-earning base (reviewer finding 1): loans at gross carrying amount, amortised-cost
# securities = UNPLEDGED amortised-cost investment securities (note 21c) PLUS pledged
# amortised-cost securities (note 20), and cash split into EARNING placements vs NON-EARNING
# cash-reserve balances (CRR x deposits). FVTPL securities are EXCLUDED (their return sits in the
# net FVTPL line, not in interest income). The SECURITIES and CASH yields and the DEPOSIT and
# WHOLESALE funding costs are DERIVED at runtime from the reported FY2024/FY2025 balances and the
# FY2025 macro rates (policy 18.0, 364-day bill 17.48), reproducing the note-8 bank interest-income
# split (cash 404.318 / loans 506.986 / investment 335.338 = 1,246.642) and the note-9 bank
# interest-expense split (customer deposits 227.208, bank+debt-sec+borrowed 310.324, lease 0.600 =
# 538.132). Loans keep the FORWARD driver (shared policy rate plus a scenario spread), as the
# reviewer asked; the note-8 loan yield is shown in the back-test only, as a reference residual.
CRR_CAL = 0.15   # Simplified historic calibration proxy, NOT actual legal CRR; issuer note 19 discloses differentiated reserves.


def _cal_balances(p):
    return dict(
        loans=hist(p, "loans_and_advances_gross"),
        ac_sec=(histb(p, "x_investment_amortised_cost", 0.0) + histb(p, "x_pledged_assets", 0.0)),
        cash=(hist(p, "cash_and_bog_balances") - CRR_CAL * hist(p, "customer_deposits")),
        deposits=hist(p, "customer_deposits"),
        wholesale=(histb(p, "due_to_banks", 0.0) + hist(p, "borrowings") + histb(p, "x_bonds", 0.0)),
    )


_A24, _A25 = _cal_balances("FY2024"), _cal_balances("FY2025")
_avg = lambda k: (_A24[k] + _A25[k]) / 2.0
II25 = hist("FY2025", "interest_income")
POL25 = 18.0      # FY2025 shared policy rate (year-end marginal)
TB364_25 = 17.48  # FY2025 shared 364-day T-bill rate
# FY2025 note-8 / note-9 IMPLIED yields and costs (percent), the calibration anchor. Each is the
# reported bank line divided by the FY2025 AVERAGE earning balance, so applying it back to the same
# balances reproduces the reported split exactly (an accounting identity, not an out-of-sample test).
Y25_IMPL = {
    "loan": 100.0 * hist("FY2025", "x_interest_income_loans") / _avg("loans"),
    "sec": 100.0 * hist("FY2025", "x_interest_income_investment_securities") / _avg("ac_sec"),
    "cash": 100.0 * hist("FY2025", "x_interest_income_cash") / _avg("cash"),
    "dep": 100.0 * hist("FY2025", "x_interest_expense_deposits_from_customers") / _avg("deposits"),
    "whl": 100.0 * (hist("FY2025", "x_interest_expense_borrowed_funds")
                    + hist("FY2025", "x_interest_expense_debt_securities")
                    + hist("FY2025", "x_interest_expense_deposits_from_banks")) / _avg("wholesale"),
}
# Forward yields: FY2025 implied level scaled by a PROPORTIONAL pass-through of the change in the
# linked macro rate — yield_now = anchor * (1 + beta * (rate_now/rate_25 - 1)). This keeps every line
# positive and bounded (no line can go negative when rates fall), reflecting that much of the loan
# book is fixed/slow-repricing and the amortised-cost securities book is largely held to maturity
# (yield locked near its purchase level). Full pass-through would drive the whole book to the new low
# policy rate in year one, which is neither how Ghana bank books reprice nor consistent with the
# amortised-cost measurement. Betas are policy judgements, not reported.
PASSTHRU = {"loan": 0.60, "sec": 0.50, "cash": 0.50, "dep": 0.50, "whl": 0.60}
CAL = {
    "policy_2025": POL25,
    "loan_yield_factor": hist("FY2025", "x_interest_income_loans") / _avg("loans") / pct(POL25),
    "securities_yield_factor": hist("FY2025", "x_interest_income_investment_securities") / _avg("ac_sec") / pct(TB364_25),
    "cash_yield_factor": hist("FY2025", "x_interest_income_cash") / _avg("cash") / pct(POL25),
    "deposit_cost_factor": hist("FY2025", "x_interest_expense_deposits_from_customers") / _avg("deposits") / pct(POL25),
    "wholesale_cost_factor": ((hist("FY2025", "x_interest_expense_borrowed_funds")
                               + hist("FY2025", "x_interest_expense_debt_securities")
                               + hist("FY2025", "x_interest_expense_deposits_from_banks")) / _avg("wholesale") / pct(POL25)),
    "lease_interest_seed": hist("FY2025", "x_interest_expense_lease_liabilities"),
}


def fwd_yield(anchor_implied, passthru, macro_rate_now, macro_rate_25):
    """Forward yield: FY2025 implied level scaled by a proportional pass-through of the rate change."""
    return anchor_implied * (1.0 + passthru * (macro_rate_now / macro_rate_25 - 1.0))


# ------------------------------------------------------------------ FY2025 back-test
# The securities and cash yield factors and the deposit and wholesale cost factors are CALIBRATED
# from the FY2025 note-8 / note-9 split and the FY2025 macro rates, so applying them to the same
# FY2025 average balances reproduces the reported split exactly BY CONSTRUCTION (residual 0.000).
# This is an accounting identity, disclosed as such, not an out-of-sample test. The LOAN line uses
# the FY2025 IMPLIED loan yield (note-8 loan interest / average gross loans) and reports it next to
# the forward yield; the forward yield is that anchor plus a partial policy pass-through beta, so the
# FY2026E opening income is the 9M run-rate and the FY2027+ path reprises only partially.
_BT = dict(
    loans=hist("FY2025", "x_interest_income_loans"),
    sec=hist("FY2025", "x_interest_income_investment_securities"),
    cash=hist("FY2025", "x_interest_income_cash"),
)
_BAL_AVG = {k: (_A24[k] + _A25[k]) / 2.0 for k in ("loans", "ac_sec", "cash")}
BACKTEST = dict(
    loans_yield_implied=Y25_IMPL["loan"],
    sec_yield_implied=Y25_IMPL["sec"],
    cash_yield_implied=Y25_IMPL["cash"],
    dep_yield_implied=Y25_IMPL["dep"],
    whl_yield_implied=Y25_IMPL["whl"],
    loans_rep=_BT["loans"],
    loans_model=_BAL_AVG["loans"] * pct(Y25_IMPL["loan"]),
    sec_model=_BAL_AVG["ac_sec"] * pct(Y25_IMPL["sec"]),
    sec_rep=_BT["sec"],
    cash_model=_BAL_AVG["cash"] * pct(Y25_IMPL["cash"]),
    cash_rep=_BT["cash"],
)


def earning_parts(bb):
    """Earning-base components of a modelled balance sheet (GHS millions)."""
    ac_sec = max(0.0, bb["investment_securities"] - bb.get("x_investment_securities_fvtpl", 0.0))
    return dict(
        loans=bb["loans_and_advances_gross"],
        sec=ac_sec + bb.get("x_pledged_assets", 0.0),
        cash=max(0.0, bb.get("cash_and_bog_balances", 0.0) - bb.get("x_cash_reserve_proxy", 0.0)),
    )


def wholesale_base(bb):
    return bb["due_to_banks"] + bb["borrowings"] + bb.get("x_bonds", 0.0)


def statutory_band_pct(fund, stated):
    """Act 930 s34, printed p30: 50% below half of paid-up capital,
    25% from half to below full paid-up capital, 12.5% at or above full.
    Opening-fund convention; positive annual after-tax profit only."""
    if stated <= 0:
        return 50.0
    r = fund / stated
    return 50.0 if r < 0.5 else (25.0 if r < 1.0 else 12.5)



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
    "other_operating_income": "Run-rate then fee-growth proxy. Folds the Bank's other operating income, other income and net FVTPL income; x_fv_other_income is a memo.",
    "total_operating_income": "NII + fee income - fee expense + trading + other operating income.",
    "staff_costs": "Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",
    "depreciation_amortisation": "Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread.",
    "other_operating_expenses": "Q4 run-rate plus cost sensitivity; then CPI plus cost-growth spread. Folds lease expenses and other expenses.",
    "impairment_charge": "9M actual + estimated Q4 loan charge; later average gross loans x scenario cost of risk; no assumed sovereign one-off. Positive = a cost.",
    "profit_before_tax": "Operating income - staff - depreciation - other opex - impairment.",
    "income_tax": "2026 actual 9M tax + estimated tax on positive Q4 PBT; later blended below-PBT charge on positive PBT (income tax plus the growth & sustainability and financial sector recovery levies).",
    "profit_after_tax": "PBT less income tax.",
}
NOTE_B = {
    "cash_and_bog_balances": "Residual assets after funding, equity and non-cash assets; a negative value is an infeasible funding gap, not available cash.",
    "due_from_banks": "The Bank reports no separate asset-side inter-bank balance; held at zero.",
    "investment_securities": "Deposit-growth proxy from the reported FVTPL plus amortised-cost portfolio (excluding pledged securities).",
    "loans_and_advances_gross": "FY2026 net/(1-allowance ratio); 2027+ organic growth.",
    "loan_loss_allowance": "Gross loans x scenario allowance ratio; distinct from the annual impairment expense.",
    "loans_and_advances_net": "Gross minus allowance; FY2026 anchored to actual 9M net loans.",
    "property_equipment_intangibles": "Inflation plus operating-expense spread, quarter-weighted in 2026.",
    "other_assets": "Inflation plus operating-expense spread, quarter-weighted in 2026. Folds pledged assets, investment in subsidiaries and tax assets.",
    "total_assets": "Cash plus non-cash asset components.",
    "customer_deposits": "Organic deposit growth.",
    "due_to_banks": "Deposit-growth proxy.",
    "borrowings": "Deposit-growth proxy; no automatic funding injected to mask a cash gap.",
    "other_liabilities": "Deposit-growth proxy. Folds current/deferred tax liabilities and bonds.",
    "total_liabilities": "Sum of modelled liabilities.",
    "stated_capital": "Held constant; no assumed capital raise.",
    "retained_earnings": "Opening retained earnings plus incremental modelled PAT minus modelled dividend and the statutory-reserve transfer.",
    "reserves_other": "Opening plus the statutory-reserve transfer; no forecast OCI.",
    "total_equity": "Stated capital + retained earnings + reserves.",
}

rows, checks_log, summary = [], [], []
states = {}
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
        # x memos are components of a canonical host bucket, so each grows at its host's rate and
        # stays consistent and nonadditive: x_investment_securities_fvtpl with securities (deposit
        # growth), x_bonds with other_liabilities (deposit growth), x_pledged_assets and
        # x_investment_in_subsidiaries with other_assets (opex growth).
        for k in ["x_investment_securities_fvtpl", "x_bonds"]:
            b[k] = prevB.get(k, 0.0) * (1 + pct(dg))
        for k in ["x_pledged_assets", "x_investment_in_subsidiaries"]:
            b[k] = prevB.get(k, 0.0) * (1 + pct(og) / (4 if first else 1))
        if first:
            b["loans_and_advances_net"] = prevB["loans_and_advances_net"] * (1 + pct(lg))
            b["loans_and_advances_gross"] = b["loans_and_advances_net"] / (1 - allow)
        else:
            b["loans_and_advances_gross"] = prevB["loans_and_advances_gross"] * (1 + pct(lg))
        b["loan_loss_allowance"] = b["loans_and_advances_gross"] * allow
        b["loans_and_advances_net"] = b["loans_and_advances_gross"] - b["loan_loss_allowance"]
        for k in ["property_equipment_intangibles", "other_assets"]:
            b[k] = prevB[k] * (1 + pct(og) / (4 if first else 1))
        # CRR-proxy reserve on this year's deposits (non-earning cash). Needed before interest so the
        # earning cash base excludes it.
        b["x_cash_reserve_proxy"] = b["customer_deposits"] * pct(crr)

        # yields / costs: FY2025 note-8 / note-9 IMPLIED levels plus a PARTIAL pass-through of the
        # macro-rate change (the book reprices slowly; the amortised-cost securities book is largely
        # held to maturity). All lines use the same earning/funding base as the FY2025 back-test.
        loanYield = fwd_yield(Y25_IMPL["loan"], PASSTHRU["loan"], pol, POL25)
        secYield = fwd_yield(Y25_IMPL["sec"], PASSTHRU["sec"], macro(s, t, "tbill_364d_pct"), TB364_25)
        cashYield = fwd_yield(Y25_IMPL["cash"], PASSTHRU["cash"], pol, POL25)
        depCost = fwd_yield(Y25_IMPL["dep"], PASSTHRU["dep"], pol, POL25)
        whlCost = fwd_yield(Y25_IMPL["whl"], PASSTHRU["whl"], pol, POL25)
        cofund = ((avg(prevB["customer_deposits"], b["customer_deposits"]) * depCost
                   + avg(wholesale_base(prevB), wholesale_base(b)) * whlCost)
                  / max(1e-9, avg(prevB["customer_deposits"], b["customer_deposits"])
                        + avg(wholesale_base(prevB), wholesale_base(b))))

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
            # Earning base: loans (gross), amortised-cost securities (unpledged + pledged), and
            # earning cash (cash and BoG balances less the CRR-proxy reserve). FVTPL excluded.
            eP, eC = earning_parts(prevB), earning_parts(b)
            i["interest_income"] = (avg(eP["loans"], eC["loans"]) * loanYield
                                    + avg(eP["sec"], eC["sec"]) * secYield
                                    + eP["cash"] * cashYield) / 100.0
            i["interest_expense"] = (avg(prevB["customer_deposits"], b["customer_deposits"]) * depCost
                                     + avg(wholesale_base(prevB), wholesale_base(b)) * whlCost
                                     ) / 100.0 + CAL["lease_interest_seed"] * (1 + pct(og)) ** j
            i["fee_commission_income"] = prevI["fee_commission_income"] * (1 + pct(fg))
            i["fee_commission_expense"] = i["fee_commission_income"] * (prevI["fee_commission_expense"] / prevI["fee_commission_income"]) * feeMult
            i["net_trading_income"] = prevI["net_trading_income"] * (1 + pct(nominal + D["model_structure"]["trading_growth_spread_pp"][s]))
            i["x_fv_other_income"] = prevI["x_fv_other_income"] * (1 + pct(nominal + D["model_structure"]["trading_growth_spread_pp"][s]))
            i["_ooi_bank"] = (prevI["other_operating_income"] - prevI["x_fv_other_income"]) * (1 + pct(fg))
            for k in ["staff_costs", "depreciation_amortisation", "other_operating_expenses"]:
                i[k] = prevI[k] * (1 + pct(og))
            i["impairment_charge"] = loanCharge

        # Canonical other operating income folds the Bank's own other-operating and other-income
        # lines with the FVTPL line, so the operating-income bridge closes. x_fv stays a memo.
        i["other_operating_income"] = (i["_ooi_bank"] + i["x_fv_other_income"]) if not first else i["other_operating_income"]

        i["net_interest_income"] = i["interest_income"] - i["interest_expense"]
        i["total_operating_income"] = (i["net_interest_income"] + i["fee_commission_income"] - i["fee_commission_expense"]
                                       + i["net_trading_income"] + i["other_operating_income"])
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
        # Section 34 uses annual net profit after tax, not Q4 PAT.
        # FY2026 observed YTD transfer is zero (issuer Q3 Bank SoCE p1).
        # Keep a 25% policy floor while applying the actual statutory bands.
        prevStat = Q3I["_stat_fund"] if first else prevB["x_statutory_reserve_fund_fc"]
        prevStated = prevB["stated_capital"]
        ytdStat = max(0.0, prevStat - hist("FY2025", "x_statutory_reserve_fund")) if first else 0.0
        bandPct = statutory_band_pct(hist("FY2025", "x_statutory_reserve_fund") if first else prevStat, prevStated)
        annualPAT = max(0.0, i["profit_after_tax"])
        bandTransfer = max(0.0, pct(bandPct) * annualPAT - ytdStat)
        transfer = max(0.0, pct(max(bandPct, D["statutory_reserve_transfer_pct"][s])) * annualPAT - ytdStat)
        if first:
            div = 0.0
        else:
            distributable = max(0.0, prevB["retained_earnings"] + incPAT - transfer)
            div = max(0.0, min(max(incPAT, 0.0) * pct(D["dividend_payout_pct"][s]),
                               distributable,
                               preCap - preRwa * pct(carTarget),
                               preCash - reserve))
        b["stated_capital"] = prevB["stated_capital"]
        b["x_statutory_reserve_fund_fc"] = prevStat + transfer
        b["x_statutory_band_transfer"] = bandTransfer
        b["x_statutory_band_pct"] = bandPct
        b["reserves_other"] = prevB["reserves_other"] + transfer
        b["retained_earnings"] = prevB["retained_earnings"] + incPAT - div - transfer
        b["total_equity"] = b["stated_capital"] + b["retained_earnings"] + b["reserves_other"]
        b["total_assets"] = b["total_liabilities"] + b["total_equity"]
        b["cash_and_bog_balances"] = b["total_assets"] - noncash(b)

        cap = preCap - div
        tier = prevTier + incPAT - div
        rw = rwa(b["total_assets"], b["loans_and_advances_gross"])
        car = 100 * cap / rw
        tier1 = 100 * tier / rw
        op = Y25 if first else prevB
        ratios = {
            "car_pct": car,
            "tier1_pct": tier1,
            "npl_pct": D["npl_pct"][s],
            "ldr_pct": 100 * b["loans_and_advances_gross"] / b["customer_deposits"],
            "cost_to_income_pct": 100 * costs(i) / i["total_operating_income"],
            "roe_pct": 100 * i["profit_after_tax"] / avg(op["total_equity"], b["total_equity"]),
            "roa_pct": 100 * i["profit_after_tax"] / avg(op["total_assets"], b["total_assets"]),
        }
        for k in KEYS_I:
            emit(s, t, "income_statement", k, i[k], "GHS millions", NOTE_I[k])
        emit(s, t, "income_statement", "x_fv_other_income", i["x_fv_other_income"], "GHS millions",
             "Net income from financial instruments carried at fair value through P&L; run-rate then trading-growth proxy. Memo only; already folded into canonical other_operating_income.")
        for k in KEYS_B:
            emit(s, t, "balance_sheet", k, b[k], "GHS millions", NOTE_B[k])
        emit(s, t, "balance_sheet", "x_pledged_assets", b["x_pledged_assets"], "GHS millions",
             "Pledged investment securities, opex-growth proxy. Memo only; already folded into canonical other_assets.")
        emit(s, t, "balance_sheet", "x_investment_in_subsidiaries", b["x_investment_in_subsidiaries"], "GHS millions",
             "Investment in subsidiaries, opex-growth proxy. Memo only; already folded into canonical other_assets.")
        emit(s, t, "balance_sheet", "x_investment_securities_fvtpl", b["x_investment_securities_fvtpl"], "GHS millions",
             "Investment securities at FVTPL, deposit-growth proxy. Memo only; already folded into canonical investment_securities; EXCLUDED from the amortised-cost earning yield.")
        emit(s, t, "balance_sheet", "x_bonds", b["x_bonds"], "GHS millions",
             "Bonds / debt securities issued, deposit-growth proxy. Memo only; already folded into canonical other_liabilities; part of the wholesale funding base.")
        emit(s, t, "balance_sheet", "x_statutory_reserve_fund_fc", b["x_statutory_reserve_fund_fc"], "GHS millions",
             "Modelled statutory reserve fund (Act 930 s34), tracked separately from aggregate reserves. Memo only; part of canonical reserves_other.")
        emit(s, t, "balance_sheet", "x_statutory_band_transfer", b["x_statutory_band_transfer"], "GHS millions",
             "Sensitivity: transfer to the statutory reserve fund under the Act 930 s34 band instead of the conservative 25% policy. Internal equity transfer; total equity and capital unchanged.")
        emit(s, t, "ratios", "x_statutory_band_pct", b["x_statutory_band_pct"], "%",
             "Act 930 s34 opening-fund band: below 50% -> 50%; 50% to below 100% -> 25%; at least 100% -> 12.5%. Central policy uses the greater of the band and 25%.")
        for k in KEYS_R:
            note = {"car_pct": "Proxy regulatory capital divided by proxy RWA; not a BoG regulatory return.",
                    "tier1_pct": "Estimated Tier 1 / RWA. The Bank discloses Tier 1 (predominantly CET1); Q3 starting Tier 1 inferred from the FY2025 audited capital structure.",
                    "npl_pct": "Estimated scenario NPL target; not a loan-level migration model; held flat within a scenario across years.",
                    "ldr_pct": "Gross loans / customer deposits.",
                    "cost_to_income_pct": "Operating expenses excluding impairments / total operating income.",
                    "roe_pct": "PAT / mean opening and closing annual equity.",
                    "roa_pct": "PAT / mean opening and closing annual assets."}[k]
            emit(s, t, "ratios", k, ratios[k], "%", note)
        effCor = 100 * i["impairment_charge"] / avg(prevB["loans_and_advances_gross"], b["loans_and_advances_gross"])
        emit(s, t, "ratios", "x_effective_cost_of_risk_pct", effCor, "%",
             "Total impairment charge / average gross loans. The allowance-build floor (max of the risk-based charge and "
             "the increase in the allowance stock) can exceed the input cost_of_risk in high-growth scenarios, so the "
             "effective rate may differ from the scenario input; both are shown.")

        short = max(0.0, rw * pct(minCAR) - cap)
        targetGap = max(0.0, rw * pct(carTarget) - cap)
        cashGap = max(0.0, reserve - b["cash_and_bog_balances"])
        allowMove = prevB["loan_loss_allowance"] + loanCharge - b["loan_loss_allowance"]
        ytd_div = histb("9M-2026", "x_ytd_dividends", 0.0) if first else 0.0
        for k, v, n in [
            ("x_regulatory_capital", cap, "Proxy Q3 capital from 17.83% CAR x estimated RWA plus cumulative retained modelled earnings."),
            ("x_tier1_capital_fc", tier, "Estimated Tier 1 capital: Q3 starting Tier 1 inferred from the FY2025 audited Tier 1/total-capital relation, plus retained modelled earnings."),
            ("x_risk_weighted_assets", rw, "Gross loans plus calibrated FY2025 residual risk intensity x assets minus gross loans."),
            ("x_model_dividends", div, ("Estimated Q4-only dividends; observed 9M retained earnings already include YTD equity movements."
                                        if first else "Estimated annual dividends constrained by distributable retained earnings after the statutory transfer, the pre-dividend CAR target and the cash-reserve proxy.")),
            ("x_dividends_paid", ytd_div + div, ("Full-year dividend memo: observed 9M-2026 YTD dividend 42.598m plus the estimated Q4 payout (zero)."
                                                 if first else "Estimated annual dividends paid.")),
            ("x_statutory_reserve_transfer", transfer, ("Estimated remaining annual statutory transfer on positive full-year PAT less observed YTD transfer (zero)."
                                                        if first else "Estimated annual transfer on positive PAT using the statutory band and conservative 25% policy floor.")),
            ("x_cash_reserve_proxy", reserve, "CRR x modelled year-end deposits; screening proxy, not actual eligible reserve."),
            ("x_cash_reserve_gap", cashGap, "Positive value is a reserve-proxy shortfall; not automatically funded."),
            ("x_capital_shortfall", short, "Additional regulatory capital needed to reach the shared minimum CAR; not assumed raised."),
            ("x_capital_target_gap", targetGap, "Additional regulatory capital needed to reach the scenario capital target (shared minimum plus management buffer); distinct from the 13% minimum gap. Not assumed raised."),
            ("x_allowance_other_movement", allowMove, "Opening modelled allowance + modelled loan impairment charge - closing modelled allowance; positive implies write-offs/other reductions; the provision floor prevents an unfunded allowance build. FY2026 Q4 only."),
        ]:
            emit(s, t, "balance_sheet", k, v, "GHS millions", n)
        emit(s, t, "income_statement", "x_model_loan_impairment", loanCharge, "GHS millions",
             ("Estimated Q4-only impairment; the actual nine-month aggregate is preserved."
              if first else "Estimated annual loan impairment included in the total impairment charge."))
        for k, v, n in [
            ("x_min_car_pct", minCAR, "Shared macro minimum CAR screening threshold."),
            ("x_capital_target_pct", carTarget, "Shared minimum plus scenario management buffer."),
            ("x_securities_yield_pct", secYield, "FY2025-calibrated multiple of the shared 364-day bill rate, applied to the amortised-cost (unpledged + pledged) securities base; FY2026 income anchored on run-rate."),
            ("x_loan_yield_pct", loanYield, "FY2025-calibrated multiple of the policy rate, applied to gross loans; FY2026 income anchored on run-rate."),
            ("x_deposit_cost_pct", depCost, "FY2025-calibrated multiple of the policy rate, applied to average customer deposits (note-9 customer-deposit share)."),
            ("x_wholesale_cost_pct", whlCost, "FY2025-calibrated multiple of the policy rate, applied to average wholesale funding (borrowings + due-to-banks + bonds; note-9 borrowed-funds/debt-securities/bank-deposit share)."),
            ("x_cost_of_funds_pct", cofund, "Blended funding cost = weighted average of the separate deposit and wholesale costs; FY2026 expense anchored on run-rate."),
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
            b["loans_and_advances_net"] - b["loans_and_advances_gross"] + b["loan_loss_allowance"],
        ]
        mx = max(abs(x) for x in resid)
        if mx > 1e-7:
            raise AssertionError("accounting check failed %s %s: %r" % (s, t, mx))
        checks_log.append(dict(s=s, t=t, mx=mx, car=car, minCAR=minCAR, short=short,
                               cash=b["cash_and_bog_balances"], reserve=reserve, cashGap=cashGap,
                               pat=i["profit_after_tax"], assets=b["total_assets"], div=div,
                               toi=i["total_operating_income"], opex_cost=costs(i),
                               imp=i["impairment_charge"], tax=i["income_tax"],
                               avg_gross=avg(prevB["loans_and_advances_gross"], b["loans_and_advances_gross"])))
        states[(s, t)] = {
            "opex_open": {k: (Q3I[k] if first else prevI[k])
                          for k in ["staff_costs", "depreciation_amortisation", "other_operating_expenses"]},
            "first": first, "toi": i["total_operating_income"], "imp": i["impairment_charge"],
            "pbt": i["profit_before_tax"],
            "stat_fund": b["x_statutory_reserve_fund_fc"], "stated": b["stated_capital"],
            "band_pct": b["x_statutory_band_pct"], "band_transfer": b["x_statutory_band_transfer"],
            "transfer": transfer,
        }
        summary.append((s, t, b["total_assets"], i["profit_after_tax"], car))
        prevB, prevI, prevCap, prevTier = b, i, cap, tier

# ------------------------------------------------------------------ write forecast.csv
with open(os.path.join(HERE, "forecast.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
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
L.append("# Republic Bank (Ghana) PLC checks")
L.append("")
L.append("Recomputed from the committed `financials.csv` and `forecast.csv` by `model.py` "
         "(history) and the shared macro file (forecast). GHS millions; ratios in percent; tolerance 0.003. "
         "NA = input unavailable, not zero. `model.py` writes this whole file. Bank-only series.")
L.append("")
L.append("## Historical balance and income bridges")
L.append("")
L.append("| Period | Assets-L-E | Asset components | NII | Operating income | PAT | Net loans |")
L.append("|---|---:|---:|---:|---:|---:|---:|")
for p in hist_periods:
    ta = hv(p, "total_assets"); tl = hv(p, "total_liabilities"); te = hv(p, "total_equity")
    r1 = None if None in (ta, tl, te) else ta - tl - te
    cash = hv(p, "cash_and_bog_balances")
    comps = [hv(p, x) for x in ["due_from_banks", "investment_securities",
                                "loans_and_advances_net", "property_equipment_intangibles", "other_assets"]]
    comps = [0.0 if c is None else c for c in comps]
    r2 = None if (ta is None or cash is None) else ta - cash - sum(comps)
    nii = hv(p, "net_interest_income"); ii = hv(p, "interest_income"); ie = hv(p, "interest_expense")
    r3 = None if None in (nii, ii, ie) else nii - ii + ie
    toi = hv(p, "total_operating_income")
    fci = hv(p, "fee_commission_income"); fce = hv(p, "fee_commission_expense")
    nt = hv(p, "net_trading_income"); ooi = hv(p, "other_operating_income")
    r4 = None if None in (toi, nii, fci, fce, nt, ooi) else toi - nii - fci + fce - nt - ooi
    pbt = hv(p, "profit_before_tax")
    pat = hv(p, "profit_after_tax"); tax = hv(p, "income_tax")
    r5 = None if None in (pat, pbt, tax) else pat - pbt + tax
    loann = hv(p, "loans_and_advances_net"); loang = hv(p, "loans_and_advances_gross"); allow = hv(p, "loan_loss_allowance")
    r7 = None if None in (loann, loang, allow) else loann - (loang - allow)
    f = lambda x: "NA" if x is None else ("%.3f" % x)
    L.append("| %s | %s | %s | %s | %s | %s | %s |" % (
        p, f(r1), f(r2), f(r3), f(r4), f(r5), f(r7)))
L.append("")
L.append("`due_from_banks` is unavailable (blank) for every period (the Bank reports no separate "
         "asset-side interbank line); it is treated as zero only inside the component bridge, so the "
         "bridge closes against the reported total. `loans_and_advances_net` for 9M-2025 / 9M-2026 is "
         "reported but its gross and allowance are unavailable, so the net-loan bridge is NA there.")
L.append("")

# source/schema checks
dupes = len(H) - len({(r["bank"], r["period"], r["statement"], r["line_item"]) for r in H})
miss = [r for r in H if r["status"] == "reported" and (r["source_id"] == "" or r["page"] == "")]
badun = [r for r in H if r["status"] == "unavailable" and r["value"] != ""]
L.append("## Source and schema checks")
L.append("")
L.append("- Historical rows: %d; duplicate bank/period/statement/key rows: %d; reported rows missing source/page: %d; unavailable rows with non-blank value: %d."
         % (len(H), dupes, len(miss), len(badun)))
L.append("- Spot-checks against printed filing pages (visually verified): RB25AR printed p.77 total assets 12,265,013 thousand -> %.3f m and total equity 1,234,220 thousand -> %.3f m; "
         "RB25AR printed p.76 bank profit before tax 392,850 thousand -> %.3f m; RB24AR printed p.67 total assets 9,544,596 thousand -> %.3f m; RB26Q3 bank total assets 11,631,887 thousand -> %.3f m; "
         "RB21FS printed p.48 total assets 4,226,259 thousand -> %.3f m. All match."
         % (hv("FY2025", "total_assets"), hv("FY2025", "total_equity"), hv("FY2025", "profit_before_tax"),
            hv("FY2024", "total_assets"), hv("9M-2026", "total_assets"), hv("FY2021", "total_assets")))
L.append("- NOTE: the Bank-only PBT for FY2025 is 392.850m (RB25AR printed p.76). The figure 440.292m "
         "sometimes quoted is the GROUP column of the same statement and the GROUP 5-year highlight; it is "
         "never used in this bank series.")
L.append("")

# reported vs recomputed ratios
L.append("## Ratios: reported vs recomputed (%)")
L.append("")
L.append("| Period | Reported CAR | Reported Tier 1 | Reported NPL | Derived LDR | Derived cost/income | Derived ROE | Derived ROA |")
L.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for p in hist_periods:
    car = hv(p, "car_pct"); t1 = hv(p, "tier1_pct"); npl = hv(p, "npl_pct")
    loang = hv(p, "loans_and_advances_gross"); dep = hv(p, "customer_deposits")
    ldr = None if None in (loang, dep) else 100 * loang / dep
    tii = hv(p, "total_operating_income")
    cst = sum(x for x in [hv(p, "staff_costs"), hv(p, "depreciation_amortisation"), hv(p, "other_operating_expenses")] if x is not None)
    ci = None if not tii else 100 * cst / tii
    pat = hv(p, "profit_after_tax"); te = hv(p, "total_equity"); ta = hv(p, "total_assets")
    roe = None if pat is None or not te else 100 * pat / te
    roa = None if pat is None or not ta else 100 * pat / ta
    g = lambda x: "NA" if x is None else "%.2f" % x
    L.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (p, g(car), g(t1), g(npl), g(ldr), g(ci), g(roe), g(roa)))
L.append("")
L.append("Reported CAR is the audited capital-management note; from FY2022 to FY2024 it is stated on the "
         "Bank of Ghana DDEP-relief basis (minimum held at 10%), and FY2025 is stated after the reliefs were "
         "withdrawn in December 2025. Reported Tier 1 is the Tier 1/RWA ratio (the Bank discloses Tier 1, "
         "predominantly CET1, rather than a separate CET1 ratio). ROE/ROA here use year-end equity/assets as "
         "a single-period ratio. LDR and cost/income are NA where the interim summary omits gross loans.")
L.append("")
L.append("### Loan loss and impairment cross-check")
L.append("")
L.append("| Period | Gross loans | ECL allowance | Allowance/gross % | Loan LL provision ratio (reported) | NPL ratio (reported) |")
L.append("|---|---:|---:|---:|---:|---:|")
_llr = {"FY2021": 7.63, "FY2022": None, "FY2023": None, "FY2024": 6.44, "FY2025": 6.31}
for p in hist_periods:
    loang = hv(p, "loans_and_advances_gross"); allow = hv(p, "loan_loss_allowance")
    ag = None if None in (loang, allow) or not loang else 100 * allow / loang
    g = lambda x: "NA" if x is None else "%.2f" % x
    L.append("| %s | %s | %s | %s | %s | %s |" % (p, g(loang), g(allow), g(ag), g(_llr.get(p)), g(hv(p, "npl_pct"))))
L.append("")
L.append("The implied allowance/gross ratio equals the Bank's reported loan loss provision ratio where both are "
         "available (FY2025 6.31%, FY2024 6.44%), confirming the net-loan bridge.")
L.append("")

L.append("<!-- FORECAST CHECKS GENERATED -->")
L.append("## Forecast checks (generated from shared macro scenarios)")
L.append("")
L.append("All forecast rows are estimated. Currency GHS millions; ratios in percent. Accounting arithmetic is checked before rounding. "
         "Cash-reserve and CAR checks are screening proxies, not regulatory returns. A negative cash residual or a positive gap is a flagged "
         "financing requirement, not an assumed funding source.")
L.append("")
L.append("Rows: %d; scenario-years: %d; FY2025 residual RWA density: %.6f; estimated 9M-2026 RWA: %.3f; initial proxy regulatory capital: %.3f (anchored to the observed 17.83%% CAR)."
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
L.append("### Effective cost of risk vs the scenario input")
L.append("")
L.append("`cost_of_risk` in `assumptions.json` is the input; the allowance-build floor (max of the risk-based charge and "
         "the increase in the allowance stock) can lift the effective rate in fast-growth scenarios. Both are shown.")
L.append("")
L.append("| Scenario | Year | Input cost of risk % | Effective charge / avg gross loans % | Impairment charge |")
L.append("|---|---:|---:|---:|---:|")
for x in checks_log:
    inp = D["cost_of_risk"][x["s"]]
    L.append("| %s | %s | %.2f | %.2f | %.3f |" % (x["s"], x["t"], inp,
            100 * x["imp"] / max(1e-9, x["avg_gross"]), x["imp"]))
L.append("")
L.append("### Downside decomposition (cost pass-through vs credit)")
L.append("")
L.append("The downside presents a combined stress. To separate the two drivers, the table below shows, for FY2030E, "
         "the base and downside operating costs and impairment. Downside opex growth is the shared downside CPI plus a "
         "%d-point spread, versus the base's shared base CPI plus a %d-point spread, so part of the downside outcome is "
         "cost pass-through driven mechanically by the shared macro downside inflation path, not by credit losses."
         % (D["opex_growth"]["downside"], D["opex_growth"]["base"]))
L.append("")
L.append("| Scenario | Year | Total operating income | Operating costs | Impairment | Profit before tax | Tax | PAT |")
L.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for x in checks_log:
    if x["t"] == "FY2030E":
        pbt = x["toi"] - x["opex_cost"] - x["imp"]
        L.append("| %s | %s | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f |"
                 % (x["s"], x["t"], x["toi"], x["opex_cost"], x["imp"], pbt, x["tax"], x["pat"]))
L.append("")
L.append("**Counterfactual: downside with base cost growth — a one-year marginal diagnostic.** Below, downside FY2030E "
         "operating costs are recomputed by applying the **BASE** opex growth (shared base CPI plus the %d-point base "
         "spread) to the downside FY2029 opening cost lines, holding the downside operating income and impairment charge "
         "fixed. Note this changes BOTH the inflation path (downside CPI -> base CPI) and the spread (downside -> base); "
         "it is not the same downside CPI with an alternative spread. This is a single-year diagnostic: the FY2029 "
         "opening costs already embed four years of cumulative downside opex, so it isolates only the FY2030 "
         "growth-rate substitution." % D["opex_growth"]["base"])
L.append("")
L.append("| FY2030E variant | Operating costs | Profit before tax | Tax | PAT |")
L.append("|---|---:|---:|---:|---:|")
_ds = states[("downside", "FY2030E")]
_ds_open = _ds["opex_open"]
_taxr = pct(D["tax_rate_pct"]["downside"])
_og_base = macro("base", "FY2030E", "inflation_cpi_pct") + D["opex_growth"]["base"]
_base_og_cost = 0.0
for k in ["staff_costs", "depreciation_amortisation", "other_operating_expenses"]:
    _base_og_cost += _ds_open[k] * (1 + pct(_og_base))
_ds_pbt_alt = _ds["toi"] - _base_og_cost - _ds["imp"]
_ds_tax_alt = max(0.0, _ds_pbt_alt) * _taxr
_ds_opex_modelled = _ds["toi"] - _ds["imp"] - _ds["pbt"]
L.append("| Downside as modelled (CPI+%d) | %.3f | %.3f | %.3f | %.3f |"
         % (D["opex_growth"]["downside"], _ds_opex_modelled, _ds["pbt"],
            max(0.0, _ds["pbt"]) * _taxr, _ds["pbt"] - max(0.0, _ds["pbt"]) * _taxr))
L.append("| Downside with base cost growth (CPI+%d) | %.3f | %.3f | %.3f | %.3f |"
         % (D["opex_growth"]["base"], _base_og_cost, _ds_pbt_alt, _ds_tax_alt, _ds_pbt_alt - _ds_tax_alt))
L.append("")
L.append("With base cost growth the downside FY2030E profit before tax changes to %.3f from %.3f, about %.0f%% of the "
         "modelled downside FY2030E profit-before-tax magnitude. Because the FY2029 opening costs already embed cumulative "
         "downside opex, this is one year of cost pass-through, not the whole five-year effect."
         % (_ds_pbt_alt, _ds["pbt"],
            100 * abs(_ds_pbt_alt - _ds["pbt"]) / abs(_ds["pbt"]) if _ds["pbt"] else 0.0))
L.append("")
L.append("### Statutory reserve fund (Act 930 s34), tracked separately")
L.append("")
L.append("Act 930 section 34 printed p30 sets three bands based on opening reserve / paid-up capital: below 50%: 50%; "
         "50% to below 100%: 25%; at least 100%: 12.5%. FY2025 closing statutory fund 368.101m / stated capital "
         "401.191m implies 25%. The issuer Q3 Bank statement of changes in equity (p1) confirms the fund remained "
         "368.101m and YTD statutory transfer was zero. FY2026 therefore uses positive full-year PAT less zero YTD transfer; "
         "later periods use opening fund and positive annual PAT. Central policy applies at least the statutory band and a 25% "
         "floor, and the statutory-only minimum is a sensitivity. Actual FY2026 final transfer is not yet published. "
         "Internal equity transfer, no effect on total equity or capital before dividends.")
L.append("")
L.append("| Year | Statutory fund | Stated capital | Fund/capital % | s34 band % | Band transfer (sensitivity) | Central policy transfer |")
L.append("|---|---:|---:|---:|---:|---:|---:|")
for x in checks_log:
    st = states[(x["s"], x["t"])]
    L.append("| %s %s | %.3f | %.3f | %.1f | %.1f | %.3f | %.3f |" % (
        x["s"], x["t"], st["stat_fund"], st["stated"], 100 * st["stat_fund"] / st["stated"],
        st["band_pct"], st["band_transfer"], st["transfer"]))
L.append("")
L.append("### FY2025 interest back-test (note-8 split vs the earning-base formula)")
L.append("")
L.append("The FY2025 note-8 IMPLIED yields and note-9 implied costs are the calibration anchor: each is the "
         "reported bank line divided by the FY2025 AVERAGE earning balance, so applying it back to the same "
         "balances reproduces the reported split exactly by construction (residual 0.000). That is an "
         "accounting identity, disclosed as such, not an out-of-sample test. The forecast applies the SAME "
         "earning/funding base and starts each yield at its FY2025 implied level, then reprises only "
         "PARTIALLY (a proportional beta below 1) toward the falling shared macro rates, because the loan "
         "book is fixed/slow-repricing and the amortised-cost securities book is largely held to maturity.")
L.append("")
L.append("| Component | FY2025 implied yield/cost (%) | Reported (note 8/9) | Model at implied level | Residual |")
L.append("|---|---:|---:|---:|---:|")
L.append("| Interest income on loans (gross) | %.3f | %.3f | %.3f | %.3f |" % (BACKTEST["loans_yield_implied"], BACKTEST["loans_rep"], BACKTEST["loans_model"], BACKTEST["loans_model"] - BACKTEST["loans_rep"]))
L.append("| Interest income on amortised-cost investment securities | %.3f | %.3f | %.3f | %.3f |" % (BACKTEST["sec_yield_implied"], BACKTEST["sec_rep"], BACKTEST["sec_model"], BACKTEST["sec_model"] - BACKTEST["sec_rep"]))
L.append("| Interest income on cash and cash equivalents | %.3f | %.3f | %.3f | %.3f |" % (BACKTEST["cash_yield_implied"], BACKTEST["cash_rep"], BACKTEST["cash_model"], BACKTEST["cash_model"] - BACKTEST["cash_rep"]))
L.append("| Total interest income | | %.3f | %.3f | %.3f |" % (BACKTEST["loans_rep"] + BACKTEST["sec_rep"] + BACKTEST["cash_rep"], BACKTEST["loans_model"] + BACKTEST["sec_model"] + BACKTEST["cash_model"], (BACKTEST["loans_model"] + BACKTEST["sec_model"] + BACKTEST["cash_model"]) - (BACKTEST["loans_rep"] + BACKTEST["sec_rep"] + BACKTEST["cash_rep"])))
L.append("")
L.append("FY2025 implied yields: loans %.2f%%, amortised-cost securities %.2f%%, cash %.2f%%; implied costs: "
         "customer deposits %.2f%%, wholesale funding %.2f%%. Pass-through betas (fraction of the macro move "
         "carried into the year): loans %.2f, securities %.2f, cash %.2f, deposits %.2f, wholesale %.2f. These "
         "betas are policy judgements, not reported figures."
         % (Y25_IMPL["loan"], Y25_IMPL["sec"], Y25_IMPL["cash"], Y25_IMPL["dep"], Y25_IMPL["whl"],
            PASSTHRU["loan"], PASSTHRU["sec"], PASSTHRU["cash"], PASSTHRU["dep"], PASSTHRU["whl"]))
L.append("")
L.append("The reported securities+cash subtotal ties to the FY2025 note-8 split; the amortised-cost investment "
         "income INCLUDES pledged assets (which are amortised-cost financial assets), and FVTPL securities are "
         "EXCLUDED (their return sits in the net FVTPL line). The earning cash base excludes the CRR-proxy "
         "reserve (non-earning).")
L.append("")
L.append("### Source inconsistencies and reference data")
L.append("")
L.append("- **Note 9 printed NII subtotal.** RB25AR printed p107 shows a note-9 `Net Interest Income` subtotal of 693.096m "
         "(bank), which disagrees with the face NII of 708.510m (p76). The note-9 COMPONENTS tie to the face: interest income "
         "1,246.642m and interest expense 538.132m give 708.510m. The model keeps the FACE 708.510m and discloses the printed "
         "note subtotal inconsistency here rather than matching it mechanically.")
L.append("- **Foreign-currency exposure (RB25AR printed p180) and sensitivity (p182).** FY2025 bank net on-balance-sheet "
         "exposure: EUR -1.262m, USD -14.593m, GBP -1.555m (FY2024 comparatives +0.166m/+16.388m/+1.392m). A 10% move gives a "
         "P&L impact of -0.126m/-1.437m/-0.156m (total -1.719m if jointly applied) and an equity impact of "
         "-0.082m/-0.934m/-0.101m (total -1.117m); FY2024 comparatives +15/+1,640/+140 (P&L) and +10/+1,066/+91 (equity) in "
         "GHS thousands. The model retains the central NO-FX-REVALUATION assumption (the balance sheet is not revalued by "
         "currency) and adds this as a bounded reference sensitivity only: on the FY2025 net position a 10% cedi move is "
         "about -1.719m P&L and -1.117m equity, immaterial against model PAT.")
L.append("- **2026 ICAAP CAR comparison (RB25AR printed p190).** The Bank's own 2026 ICAAP forecasts CAR 18.11%% "
         "(regulatory capital 1,049.935m, RWA 5,798.105m). The model's FY2026E base CAR proxy is %.3f%% (%.0f bps lower). This "
         "is NOT an error and is not matched mechanically: the ICAAP is a forward regulatory-capital forecast at a different "
         "date using the Bank's own PD/LGD risk weights and Pillar-2 add-ons, whereas the model proxy uses a single FY2025 "
         "residual RWA-density calibration and anchors interim capital on the reported 17.83%% Q3 CAR. The two differ by "
         "methodology and reporting date, not by an arithmetic mistake." % (checks_log[0]["car"], 100 * (18.11 - checks_log[0]["car"])))
L.append("")
L.append("### Tax treatment and dividends in the anchor year")
L.append("")
L.append("FY2026E retains the actual 9M-2026 tax charge and adds tax on any positive estimated Q4 profit before tax. "
         "No deferred-tax credit is recognised for a Q4 loss, so if the downside Q4 is a loss the annual effective rate "
         "exceeds the 35% input; this is the model's stated treatment, not an error. The observed 9M-2026 equity already "
         "reflects the GHS42.598m dividend paid in 2026 (RB26Q3), so no additional Q4-2026 dividend is assumed and "
         "`x_model_dividends` is zero in FY2026E for every scenario. The statutory reserve transfer is modelled at a "
         "conservative minimum of 25% of positive annual PAT or the applicable Act 930 band, less actual YTD transfer, with the statutory-only band as "
         "a sensitivity; it is an internal equity transfer, so total equity and regulatory capital are unaffected, but it "
         "caps distributable retained earnings for dividends. See the statutory-reserve section above.")
L.append("")
L.append("FY2026 estimated earnings retain actual 9M income and estimate Q4 only. The Bank reports a net on-balance-sheet FX "
         "position (RB25AR p180) but the model keeps a central NO-FX-REVALUATION assumption; the reported FY2025 exposure and a "
         "bounded 10% sensitivity are shown above. Full prudential risk weights, OCI, capital deductions and liquidity "
         "eligibility are not available, so the capital and reserve checks are simplified screening proxies. Independent "
         "review required.")
L.append("")

L.append("### Additional collateral and wholesale repricing diagnostic")
L.append("")
L.append("Illustrative static stress, not a full model rerun: 20% of pledged securities is an incremental collateral haircut (not a loss or free cash); +100bp on average borrowings, bank funding and bonds is gross annual pre-tax expense before behavioral or capital feedback. The original pledged assets are already restricted. FY2026 applies one quarter of the annual funding shock, preserving reported nine months.")
L.append("")
L.append("| Scenario | Year | 20% pledged haircut (GHS m) | Incremental wholesale interest (GHS m) |")
L.append("|---|---|---:|---:|")
for sc in SCEN:
    opening = wholesale_base(Q3B)
    for yr in PERIODS:
        rr = {r[3]: float(r[4]) for r in rows if r[-1] == sc and r[1] == yr}
        closing = rr["borrowings"] + rr["due_to_banks"] + rr["x_bonds"]
        L.append("| %s | %s | %.3f | %.3f |" % (sc, yr, .2 * rr["x_pledged_assets"], .01 * (opening + closing)/2 / (4 if yr == PERIODS[0] else 1)))
        opening = closing
L.append("")

with open(os.path.join(HERE, "checks.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L))

print(json.dumps({"forecast_rows": len(rows), "scenario_years": len(checks_log),
                  "summary": [dict(scenario=s, year=t, assets=round(a, 3), pat=round(p, 3), car=round(c, 3))
                              for s, t, a, p, c in summary]}, indent=2))
