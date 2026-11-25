#!/usr/bin/env python3
"""Historical checks for banks/stanbic-bank-ghana (bank-only, GHS millions).

Recomputes the balances, bridges and reported-vs-derived ratios from financials.csv
and writes banks/stanbic-bank-ghana/checks_history.md. Run: python checks_history.py
"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
H = list(csv.DictReader(open(os.path.join(HERE, "financials.csv"), encoding="utf-8")))
TOL = 0.003
PERIODS = []
for r in H:
    if r["period"] not in PERIODS:
        PERIODS.append(r["period"])


def hv(p, k):
    for r in H:
        if r["period"] == p and r["line_item"] == k:
            v = r["value"]
            return None if v == "" else float(v)
    return None


fails = []
lines = []
lines.append("# Stanbic Bank Ghana Ltd historical checks")
lines.append("")
lines.append("Recomputed from the committed `financials.csv`. GHS millions; ratios in percent; tolerance %.3f. "
             "NA = input unavailable, not zero." % TOL)
lines.append("")
lines.append("## Balance and income bridges")
lines.append("")
lines.append("| Period | Assets-L-E | Asset components | Liab components | Equity components | NII | Operating income | PAT | Net loans |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
for p in PERIODS:
    ta, tl, te = hv(p, "total_assets"), hv(p, "total_liabilities"), hv(p, "total_equity")
    r1 = None if None in (ta, tl, te) else ta - tl - te
    cash = hv(p, "cash_and_bog_balances")
    comps = [hv(p, x) for x in ["due_from_banks", "x_trading_assets", "x_pledged_assets",
                                "investment_securities", "loans_and_advances_net",
                                "property_equipment_intangibles", "other_assets"]]
    comps = [0.0 if c is None else c for c in comps]
    r2 = None if (ta is None or cash is None) else ta - cash - sum(comps)
    liabs = [hv(p, x) for x in ["customer_deposits", "due_to_banks", "borrowings", "other_liabilities"]]
    liabs = [0.0 if c is None else c for c in liabs]
    r3 = None if tl is None else tl - sum(liabs)
    eqs = [hv(p, x) for x in ["stated_capital", "retained_earnings", "reserves_other"]]
    eqs = [0.0 if c is None else c for c in eqs]
    r4 = None if te is None else te - sum(eqs)
    nii, ii, ie = hv(p, "net_interest_income"), hv(p, "interest_income"), hv(p, "interest_expense")
    r5 = None if None in (nii, ii, ie) else nii - ii + ie
    toi, fci, fce, nt, ooi = (hv(p, x) for x in ["total_operating_income", "fee_commission_income",
                                "fee_commission_expense", "net_trading_income", "other_operating_income"])
    r6 = None if None in (toi, nii, fci, fce, nt, ooi) else toi - nii - fci + fce - nt - ooi
    pat, pbt, tax = hv(p, "profit_after_tax"), hv(p, "profit_before_tax"), hv(p, "income_tax")
    r7 = None if None in (pat, pbt, tax) else pat - pbt + tax
    ind, dirt = hv(p, "x_indirect_tax"), hv(p, "x_direct_tax")
    r7b = None if None in (tax, ind, dirt) else tax - ind - dirt
    loann, loang, allow = hv(p, "loans_and_advances_net"), hv(p, "loans_and_advances_gross"), hv(p, "loan_loss_allowance")
    iis = hv(p, "x_interest_in_suspense") or 0.0
    r8 = None if None in (loann, loang, allow) else loann - (loang - allow - iis)
    for lab, res in [("assets-l-e", r1), ("asset comps", r2), ("liab comps", r3), ("equity comps", r4),
                     ("nii", r5), ("op income", r6), ("pat", r7), ("tax split", r7b), ("net loans", r8)]:
        if res is not None and abs(res) > TOL:
            fails.append((p, lab, res))
    f = lambda x: "NA" if x is None else "%.3f" % x
    lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        p, f(r1), f(r2), f(r3), f(r4), f(r5), f(r6), f(r7), f(r8)))
lines.append("")

# Source / schema checks
dupes = len(H) - len({(r["bank"], r["period"], r["statement"], r["line_item"]) for r in H})
miss = [r for r in H if r["status"] == "reported" and (r["source_id"] == "" or r["page"] == "")]
badun = [r for r in H if r["status"] == "unavailable" and r["value"] != ""]
lines.append("## Source and schema checks")
lines.append("")
lines.append("- Historical rows: %d; duplicate keys: %d; reported rows missing source/page: %d; unavailable rows with a value: %d."
             % (len(H), dupes, len(miss), len(badun)))
lines.append("- Spot-checks against the audited pages: FY2025 total assets 36,708,145k = %.3f; FY2025 PAT 1,608,667k = %.3f; "
             "FY2024 total assets 32,590,921k = %.3f; 9M-2026 total assets 43,243,634k = %.3f."
             % (hv("FY2025", "total_assets"), hv("FY2025", "profit_after_tax"),
                hv("FY2024", "total_assets"), hv("9M-2026", "total_assets")))
lines.append("")

lines.append("## Reported vs derived ratios (%)")
lines.append("")
lines.append("| Period | Reported CAR | Reported CET1 | Reported NPL | Derived LDR | Derived cost/income | Derived ROE | Derived ROA |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for p in PERIODS:
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
    lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (p, g(car), g(t1), g(npl), g(ldr), g(ci), g(roe), g(roa)))
lines.append("")
lines.append("Reported CAR/CET1 come from each year's unaudited/audited summary quantitative disclosures; the capital-adequacy "
             "note agrees (FY2022 12.3%, FY2023 19.6%, FY2024 19.0%, FY2025 23.2%). ROE/ROA and cost/income here use year-end "
             "or single-period figures, so they differ slightly from any average-balance ratios. LDR uses gross loans over "
             "customer deposits. `income_tax` is the sum of the reported indirect and direct tax.")
lines.append("")

lines.append("## Result")
lines.append("")
if fails:
    for p, lab, res in fails:
        lines.append("- FAIL %s %s residual %.6f" % (p, lab, res))
else:
    lines.append("- **PASS** - all bridge residuals within tolerance.")
lines.append("")

with open(os.path.join(HERE, "checks_history.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("FAILURES=%d" % len(fails))
for p, lab, res in fails:
    print("  FAIL", p, lab, res)
sys.exit(1 if fails else 0)
