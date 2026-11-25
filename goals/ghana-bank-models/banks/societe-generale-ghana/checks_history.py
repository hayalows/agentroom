#!/usr/bin/env python3
"""Independent arithmetic checks on banks/societe-generale-ghana/financials.csv.

Recomputes every identity the model spec requires, from the CSV alone.
Writes the pass/fail table to checks_history.md and prints a summary.
"""
import csv, os

D = os.path.dirname(os.path.abspath(__file__))
BANK = "societe-generale-ghana"

def load():
    with open(os.path.join(D, "financials.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))

rows = load()
PERIODS = []
for r in rows:
    if r["period"] not in PERIODS:
        PERIODS.append(r["period"])

def val(period, statement, item):
    for r in rows:
        if r["period"] == period and r["statement"] == statement and r["line_item"] == item:
            return None if r["value"] == "" else float(r["value"])
    raise KeyError((period, statement, item))

fails = []
report = []

def check(label, lhs, rhs, tol=0.001):
    diff = abs(lhs - rhs) if (lhs is not None and rhs is not None) else None
    if diff is None:
        report.append((label, "n/a", "input unavailable"))
        return
    ok = diff <= tol
    report.append((label, "PASS" if ok else "FAIL", f"{lhs:.6f} vs {rhs:.6f} diff {diff:.6f}"))
    if not ok:
        fails.append(label)

for p in PERIODS:
    # income identities
    check(f"{p} NII = II - IE", val(p,"income_statement","net_interest_income"),
          val(p,"income_statement","interest_income") - val(p,"income_statement","interest_expense"))
    check(f"{p} PAT = PBT - tax", val(p,"income_statement","profit_after_tax"),
          val(p,"income_statement","profit_before_tax") - val(p,"income_statement","income_tax"))
    # balance sheet identities
    check(f"{p} BS balances", val(p,"balance_sheet","total_assets"),
          val(p,"balance_sheet","total_liabilities") + val(p,"balance_sheet","total_equity"))
    # net loans bridge
    gross = val(p,"balance_sheet","loans_and_advances_gross")
    allow = val(p,"balance_sheet","loan_loss_allowance")
    net = val(p,"balance_sheet","loans_and_advances_net")
    if gross is not None and allow is not None:
        # SG summary prints net = gross - amortised cost adj - interest in suspense - allowance
        amort = val(p,"balance_sheet","x_amortised_cost_adjustment")
        iis = val(p,"balance_sheet","x_interest_in_suspense")
        rhs = gross - (amort or 0) - (iis or 0) - allow
        check(f"{p} net loans = gross - adj - IIS - allowance", net, rhs)
    # asset subtotal
    ts = sum(v for v in [val(p,"balance_sheet","cash_and_bog_balances"),
                          val(p,"balance_sheet","x_trading_assets") if any(r["period"]==p and r["line_item"]=="x_trading_assets" and r["value"]!="" for r in rows) else 0,
                          ] if v is not None)
    # subtotal of defined asset lines
    asset_lines = ["cash_and_bog_balances","x_trading_assets","x_derivative_assets",
                   "investment_securities","loans_and_advances_net","x_equity_investments",
                   "other_assets","property_equipment_intangibles"]
    asum = 0.0
    avail = True
    for a in asset_lines:
        v = val(p,"balance_sheet",a)
        if v is None:
            # derivative/trading unavailable rows count 0
            avail=True
            continue
        asum += v
    check(f"{p} asset lines sum to total_assets", asum, val(p,"balance_sheet","total_assets"), tol=0.01)

    # equity subtotal
    eqs = sum(v for v in [val(p,"balance_sheet","stated_capital"),
                          val(p,"balance_sheet","retained_earnings"),
                          val(p,"balance_sheet","reserves_other")] if v is not None)
    check(f"{p} equity components sum", eqs, val(p,"balance_sheet","total_equity"), tol=0.01)

# report
lines = [f"# History checks: {BANK}", "",
         "Recomputed from `financials.csv` alone by `checks_history.py`.", "",
         "| check | result | numbers |", "| --- | --- | --- |"]
for label, res, nums in report:
    lines.append(f"| {label} | {res} | {nums} |")
lines += ["", f"**{len(fails)} failures** of {len(report)} checks."]
open(os.path.join(D,"checks_history.md"),"w",encoding="utf-8").write("\n".join(lines)+"\n")
print("\n".join(f"{l}: {r} [{n}]" for l,r,n in report))
print(f"FAILURES={len(fails)}")
