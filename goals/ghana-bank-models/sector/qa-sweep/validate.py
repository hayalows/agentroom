#!/usr/bin/env python3
"""QA sweep for goals/ghana-bank-models. Standard library only.

Run from anywhere:  python validate.py          writes report.md and report.json next to this file.

For every folder in banks/ it checks the MODEL-SPEC rules, with three result levels:
  FAIL  = breaks a rule of MODEL-SPEC (fix before the bank can count)
  WARN  = suspicious, an owner should look (does not block)
  info  = facts for the roll-up
It does NOT check numbers against filings. Only a reviewer who opens the source can do that.
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOAL = os.path.abspath(os.path.join(HERE, "..", ".."))
BANKS = os.path.join(GOAL, "banks")
CLAIMS = os.path.join(GOAL, "claims")
MACRO = os.path.join(GOAL, "sector", "macro-assumptions", "macro.csv")

COLS = ["bank", "period", "statement", "line_item", "value", "unit", "source_id", "page", "status", "notes"]
STATEMENTS = {"income_statement", "balance_sheet", "ratios"}
STATUSES = {"reported", "derived", "estimated", "unavailable"}
KEYS = {
    "income_statement": "interest_income interest_expense net_interest_income fee_commission_income fee_commission_expense net_trading_income other_operating_income total_operating_income staff_costs depreciation_amortisation other_operating_expenses impairment_charge profit_before_tax income_tax profit_after_tax".split(),
    "balance_sheet": "cash_and_bog_balances due_from_banks investment_securities loans_and_advances_gross loan_loss_allowance loans_and_advances_net property_equipment_intangibles other_assets total_assets customer_deposits due_to_banks borrowings other_liabilities total_liabilities stated_capital retained_earnings reserves_other total_equity".split(),
    "ratios": "car_pct tier1_pct npl_pct ldr_pct cost_to_income_pct roe_pct roa_pct".split(),
}
ALLOWED = {k for v in KEYS.values() for k in v}
SCEN = ["base", "downside", "upside"]
FYE = [f"FY{y}E" for y in range(2026, 2031)]
SECTOR_ASSETS_DEC25 = 446900.0  # GHS m, BoG Summary Nov 2026, banking sector total assets Dec 2025

def num(x):
    try:
        return float(x)
    except Exception:
        return None

def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        rows = list(rd)
        return rows, list(rd.fieldnames or [])

def claim_status(slug):
    p = os.path.join(CLAIMS, slug + ".md")
    if not os.path.exists(p):
        return "", ""
    owner = status = ""
    for line in open(p, encoding="utf-8-sig"):
        m = re.match(r"^(agent|status):\s*(.*)$", line.strip())
        if m and m.group(1) == "agent" and not owner:
            owner = m.group(2)
        if m and m.group(1) == "status":
            status = m.group(2)
    return owner, status

def check_bank(slug):
    d = os.path.join(BANKS, slug)
    res = {"slug": slug, "fail": [], "warn": [], "info": {}}
    F, W, I = res["fail"], res["warn"], res["info"]
    owner, status = claim_status(slug)
    I["owner"], I["claim_status"] = owner, status
    files = set(os.listdir(d))
    for need in ["README.md", "sources.md", "financials.csv", "forecast.csv", "checks.md"]:
        if need not in files:
            F.append(f"missing file {need}")
    if not any(f in files for f in ["assumptions.json", "assumptions.md"]):
        F.append("missing assumptions.json or assumptions.md")
    if not any(f in files for f in ["model.py", "model.mjs", "model.js", "assumptions.md"]):
        F.append("no reproducible model (model.py / model.mjs) or written formulas")
    if "financials.csv" not in files:
        return res
    try:
        rows, header = read_csv(os.path.join(d, "financials.csv"))
    except Exception as e:
        F.append(f"financials.csv unreadable: {e}")
        return res
    if header != COLS:
        F.append(f"financials.csv columns are {header}, expected {COLS}")
    I["history_rows"] = len(rows)
    seen = set()
    V, S = {}, {}
    for r in rows:
        k = (r["period"], r["line_item"])
        if k in seen:
            F.append(f"duplicate row {k}")
        seen.add(k)
        if r["bank"] != slug:
            F.append(f"row bank '{r['bank']}' != folder '{slug}' ({k})")
        if r["statement"] not in STATEMENTS:
            F.append(f"bad statement '{r['statement']}' ({k})")
        if r["status"] not in STATUSES:
            F.append(f"bad status '{r['status']}' ({k})")
        li = r["line_item"]
        if li not in ALLOWED and not li.startswith("x_"):
            F.append(f"line_item '{li}' is not in the spec and not an x_ item")
        if r["status"] == "unavailable":
            if r["value"].strip() != "":
                F.append(f"unavailable row has a value {k}")
        else:
            if num(r["value"]) is None:
                F.append(f"non-numeric value {k}")
            else:
                V[k] = float(r["value"])
        if r["status"] == "reported" and (not r["source_id"].strip() or not r["page"].strip()):
            F.append(f"reported row without source_id/page {k}")
        if r["status"] == "derived" and len(r["notes"].strip()) < 10:
            F.append(f"derived row without a formula in notes {k}")
        S[k] = r["status"]
        if not li.startswith("x_") and r["unit"] not in ("GHS millions", "percent", "%", ""):
            W.append(f"unit '{r['unit']}' on {k}")
    periods = sorted({r["period"] for r in rows})
    fy = [p for p in periods if re.fullmatch(r"FY\d{4}", p)]
    I["periods"] = periods
    if len(fy) < 5:
        F.append(f"only {len(fy)} full fiscal years in history (spec asks for 5)")
    if "9M-2026" not in periods and "H1-2026" not in periods:
        W.append("no 2026 interim period in history (9M-2026 expected)")
    g = lambda p, i: V.get((p, i))
    # period completeness: income lines need a balance sheet and vice versa
    for p in periods:
        has_is = any(k[0] == p and k[1] in KEYS["income_statement"] and k in V for k in V)
        has_bs = g(p, "total_assets") is not None
        if has_is and not has_bs:
            F.append(f"{p}: has income statement rows but no balance sheet (the gate needs both)")
        if has_bs and not has_is:
            F.append(f"{p}: has balance sheet rows but no income statement")
    # identities
    bad = 0
    for p in periods:
        ta, tl, te = g(p, "total_assets"), g(p, "total_liabilities"), g(p, "total_equity")
        if None not in (ta, tl, te) and abs(ta - tl - te) > 0.0051:
            F.append(f"{p}: assets {ta:.3f} != liabilities + equity {tl + te:.3f}")
            bad += 1
        nii, ii, ie = g(p, "net_interest_income"), g(p, "interest_income"), g(p, "interest_expense")
        if None not in (nii, ii, ie) and abs(nii - (ii - ie)) > 0.0051:
            F.append(f"{p}: NII {nii:.3f} != interest income - expense {ii - ie:.3f}")
            bad += 1
        pat, pbt, tax = g(p, "profit_after_tax"), g(p, "profit_before_tax"), g(p, "income_tax")
        if None not in (pat, pbt, tax) and abs(pat - (pbt - tax)) > 0.0051:
            F.append(f"{p}: PAT {pat:.3f} != PBT - tax {pbt - tax:.3f}")
            bad += 1
        comps = [g(p, k) for k in ["cash_and_bog_balances", "due_from_banks", "investment_securities", "loans_and_advances_net", "property_equipment_intangibles", "other_assets"]]
        got = [c for c in comps if c is not None]
        if ta is not None and len(got) >= 5 and abs(sum(got) - ta) > 0.0051:
            W.append(f"{p}: asset lines sum {sum(got):.3f} vs total assets {ta:.3f} (due_from_banks may be inside another line; say so in notes)")
        ln, lg, la = g(p, "loans_and_advances_net"), g(p, "loans_and_advances_gross"), g(p, "loan_loss_allowance")
        if None not in (ln, lg, la):
            gap = lg - la - ln
            sus = sum(v for (pp, ii), v in V.items() if pp == p and re.fullmatch(r"x_.*(suspense|adjustment).*", ii))
            if abs(gap) > 0.0051 and abs(gap - sus) > 0.0051:
                msg = f"{p}: gross loans {lg:.3f} - allowance {la:.3f} - net loans {ln:.3f} leaves {gap:.3f}" + (f", of which x_ suspense/adjustment rows explain {sus:.3f}, leaving {gap - sus:.3f} unexplained" if sus else " and no x_ suspense/adjustment row explains it")
                F.append(msg)
    I["identity_failures"] = bad
    # sign convention: costs positive
    for item in ["interest_expense", "staff_costs", "fee_commission_expense", "depreciation_amortisation", "other_operating_expenses"]:
        neg = [p for p in fy if g(p, item) is not None and g(p, item) < 0]
        if neg:
            F.append(f"{item} is negative in {neg} (spec: costs are stored positive)")
    # right-of-use convention
    for r in rows:
        if r["line_item"] == "other_assets" and re.search(r"right[- ]of[- ]use|\bROU\b", r["notes"], re.I) and "property_equipment" not in r["notes"]:
            W.append(f"{r['period']}: right-of-use assets appear to be inside other_assets (spec: property_equipment_intangibles)")
            break
    # size sanity
    ta25 = g("FY2025", "total_assets")
    I["total_assets_fy2025"] = ta25
    if ta25 is not None and not (500 <= ta25 <= 150000):
        W.append(f"FY2025 total assets {ta25:.0f} GHS m looks outside the plausible range for a Ghanaian bank")
    # forecast
    if "forecast.csv" in files:
        try:
            frows, fh = read_csv(os.path.join(d, "forecast.csv"))
        except Exception as e:
            F.append(f"forecast.csv unreadable: {e}")
            return res
        for need in ["bank", "scenario", "period", "line_item", "value", "unit", "status"]:
            if need not in fh:
                F.append(f"forecast.csv lacks column {need}")
        if not F or all("forecast.csv" not in x for x in F):
            fv, keys = {}, set()
            for r in frows:
                k = (r.get("scenario"), r.get("period"), r.get("line_item"))
                if k in keys:
                    F.append(f"duplicate forecast row {k}")
                    break
                keys.add(k)
                v = num(r.get("value"))
                if v is not None:
                    fv[k] = v
                if r.get("status") not in ("estimated", "unavailable"):
                    badstat = locals().get("badstat", 0) + 1
                li = r.get("line_item", "")
                if li and li not in ALLOWED and not li.startswith("x_"):
                    F.append(f"forecast line_item '{li}' is not in the spec and not an x_ item")
                    break
            if locals().get("badstat"):
                W.append(f"{badstat} forecast rows have a status other than estimated/unavailable (spec: estimated)")
            have = {(k[0], k[1]) for k in fv}
            miss = [f"{s}|{y}" for s in SCEN for y in FYE if (s, y) not in have]
            if miss:
                F.append(f"forecast missing scenario-years: {miss[:5]}{'...' if len(miss) > 5 else ''}")
            I["forecast_rows"] = len(frows)
            bad_bs = []
            for s in SCEN:
                for y in FYE:
                    ta, tl, te = fv.get((s, y, "total_assets")), fv.get((s, y, "total_liabilities")), fv.get((s, y, "total_equity"))
                    if None not in (ta, tl, te) and abs(ta - tl - te) > 0.01:
                        bad_bs.append(f"{s} {y} off by {ta - tl - te:.3f}")
                    nii, ii, ie = fv.get((s, y, "net_interest_income")), fv.get((s, y, "interest_income")), fv.get((s, y, "interest_expense"))
                    if None not in (nii, ii, ie) and abs(nii - (ii - ie)) > 0.01:
                        bad_bs.append(f"{s} {y} NII off")
                    fpat, fpbt, ftax = fv.get((s, y, "profit_after_tax")), fv.get((s, y, "profit_before_tax")), fv.get((s, y, "income_tax"))
                    if None not in (fpat, fpbt, ftax) and abs(fpat - (fpbt - ftax)) > 0.01:
                        bad_bs.append(f"{s} {y} PAT != PBT - tax ({fpat:.3f} vs {fpbt - ftax:.3f})")
                    al = [fv.get((s, y, k)) for k in ["cash_and_bog_balances", "due_from_banks", "investment_securities", "loans_and_advances_net", "property_equipment_intangibles", "other_assets"]]
                    got = [x for x in al if x is not None]
                    if ta is not None and len(got) >= 5 and abs(sum(got) - ta) > 0.01:
                        bad_bs.append(f"{s} {y} asset lines sum {sum(got):.3f} != total assets {ta:.3f}")
            if bad_bs:
                F.append(f"forecast identities fail: {bad_bs[:4]}")
            # anchor test: FY2026E vs 9M-2026 x 12/9 (informational, WARN when far)
            for item in ["interest_income", "interest_expense", "profit_after_tax"]:
                a9, f26 = g("9M-2026", item), fv.get(("base", "FY2026E", item))
                if a9 and f26 and abs(a9) > 1:
                    gap = (f26 / (a9 * 12 / 9) - 1) * 100
                    I[f"anchor_gap_{item}_pct"] = round(gap, 1)
                    if abs(gap) > 25:
                        W.append(f"base FY2026E {item} is {gap:+.0f}% away from 9M-2026 annualised (interest lines that are far off can hide offsetting errors)")
            ta26, ta30 = fv.get(("base", "FY2026E", "total_assets")), fv.get(("base", "FY2030E", "total_assets"))
            if ta26 and ta30:
                cagr = ((ta30 / ta26) ** (1 / 4) - 1) * 100
                I["base_asset_cagr_26_30_pct"] = round(cagr, 1)
                if cagr > 30 or cagr < -5:
                    W.append(f"base total assets grow {cagr:.0f}% a year FY2026E-FY2030E, check the growth drivers")
    # macro link
    a = ""
    for f in ("assumptions.json", "assumptions.md"):
        if f in files:
            a += open(os.path.join(d, f), encoding="utf-8-sig").read()
    code = ""
    for f in ("model.py", "model.mjs", "model.js"):
        if f in files:
            code += open(os.path.join(d, f), encoding="utf-8-sig").read()
    if not re.search(r"macro\.csv|macro_file", a + code):
        F.append("no reference to macro.csv / macro_file in assumptions or model (the core gate requires it)")
    return res

def main():
    slugs = sorted(x for x in os.listdir(BANKS) if os.path.isdir(os.path.join(BANKS, x)) and not x.startswith("__"))
    results = [check_bank(s) for s in slugs]
    for r in results:
        r["assessed"] = r["info"].get("claim_status") in ("needs-review", "done")
        if not r["assessed"]:
            r["wip"] = r["fail"] + r["warn"]
            r["fail"], r["warn"] = [], []
    out = ["# QA sweep report", "", f"Generated by `sector/qa-sweep/validate.py` over {len(results)} bank folders. Banks still marked `in-progress` are listed as work in progress and are not counted: only `needs-review` and `done` banks are assessed. This checks structure, arithmetic and conventions. **It does not compare numbers with filings.**", "",
           "| Bank | Owner | Claim status | FAIL | WARN | History rows | Forecast rows | FY2025 assets (GHS m) |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in results:
        I = r["info"]
        out.append(f"| {r['slug']} | {I.get('owner','')} | {I.get('claim_status','')} | {len(r['fail']) if r['assessed'] else 'WIP'} | {len(r['warn']) if r['assessed'] else 'WIP'} | {I.get('history_rows','')} | {I.get('forecast_rows','')} | {'' if I.get('total_assets_fy2025') is None else format(I['total_assets_fy2025'], ',.0f')} |")
    total_f = sum(len(r["fail"]) for r in results)
    out += ["", f"**Total FAIL: {total_f}.** Total WARN: {sum(len(r['warn']) for r in results)}.", ""]
    wip = [r for r in results if not r["assessed"] and r.get("wip")]
    if wip:
        out += ["## Work in progress (informational, not counted)", ""]
        for r in wip:
            out.append(f"- **{r['slug']}** ({r['info'].get('owner','')}): {len(r['wip'])} open items, first: {r['wip'][0]}")
        out.append("")
    for r in results:
        if r["fail"] or r["warn"]:
            out += [f"## {r['slug']}", ""]
            out += [f"- **FAIL** {x}" for x in r["fail"][:25]] + [f"- WARN {x}" for x in r["warn"][:25]]
            more = len(r["fail"]) - 25
            if more > 0:
                out.append(f"- ... {more} more FAIL")
            out.append("")
    with open(os.path.join(HERE, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    with open(os.path.join(HERE, "report.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
    print(f"{len(results)} banks | FAIL {total_f} | WARN {sum(len(r['warn']) for r in results)}")
    for r in results:
        print(f"  {r['slug']:28s} FAIL {len(r['fail']):3d}  WARN {len(r['warn']):3d}  [{r['info'].get('claim_status','')}{'' if r['assessed'] else ', not assessed'}]")

if __name__ == "__main__":
    main()
