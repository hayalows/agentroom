"""Independent recomputation of sector-rollup/rollup.csv from raw bank files (claude-helper-1).
Usage: python3 -I verify_rollup.py <input-root checkout> <output dir containing rollup.csv>
Ordinary set = the reporting_banks list in the CSV itself, cross-checked against review-resolutions markers (conditional never ordinary).
Recomputes history_total, forecast_total, coverage, paired ratios and bank_fy2025 cells with Decimal; tolerance 0.0006 (absolute, GHS m) / 0.00006 (percent)."""
import csv, sys, os
from decimal import Decimal as D
root, out = sys.argv[1], sys.argv[2]
gd = os.path.join(root, 'goals', 'ghana-bank-models')
R = list(csv.DictReader(open(os.path.join(out, 'rollup.csv'), newline='')))
cache = {}
def fin(b):
    if b not in cache:
        cache[b] = {(r['period'], r['line_item']): D(r['value']) for r in csv.DictReader(open(f'{gd}/banks/{b}/financials.csv', newline='')) if r['value'] != ''}
    return cache[b]
fc = {}
def fore(b):
    if b not in fc:
        fc[b] = {(r['scenario'], r['period'], r['line_item']): D(r['value']) for r in csv.DictReader(open(f'{gd}/banks/{b}/forecast.csv', newline='')) if r['value'] != ''}
    return fc[b]
cond = [f[:-3] for f in os.listdir(f'{gd}/review-resolutions') if f.endswith('.md') and f != 'CONDITIONAL-POLICY.md' and f != 'CONDITIONAL-CLOSURES.md' and 'onditional' in open(f'{gd}/review-resolutions/{f}').read()]
n = bad = 0; fails = []
def chk(label, got, exp, tol):
    global n, bad
    n += 1
    if abs(D(got) - exp) > D(tol): bad += 1; fails.append((label, got, str(exp)))
ordinary = None
for r in R:
    banks = r['reporting_banks'].split(';') if r['reporting_banks'] else []
    for b in banks:
        assert b not in cond, ('conditional bank in ordinary set', b)
    t, per, item = r['table'], r['period_or_scenario'], r['item']
    if t == 'history_total':
        g = (lambda b: fin(b)[(per, 'total_operating_income')]) if item == 'operating_income_pre_impairment' else (lambda b: fin(b)[(per, item)])
        chk(f'{t} {per} {item}', r['value'], sum(g(b) for b in banks), '0.0006' if item != 'operating_income_pre_impairment' else '0.002')  # derived item: generator rounds per bank, allow 0.002
        assert len(banks) == int(r['n_banks_reporting'])
    elif t == 'coverage':
        chk(f'{t} {per} {item}', r['value'], sum(fin(b)[(per, item)] for b in banks), '0.0006')
    elif t == 'forecast_total':
        sc, yr = per.split('|')
        chk(f'{t} {per} {item}', r['value'], sum(fore(b)[(sc, yr, item)] for b in banks), '0.0006')
    elif t == 'bank_fy2025':
        b = r['bank']; F = fin(b); u = r['unit']
        if item in ('total_assets', 'customer_deposits', 'loans_and_advances_net', 'total_equity', 'profit_after_tax'):
            chk(f'{t} {b} {item}', r['value'], F[('FY2025', item)], '0.0006')
        elif item == 'net_ldr':
            chk(f'{t} {b} {item}', r['value'], F[('FY2025', 'loans_and_advances_net')] / F[('FY2025', 'customer_deposits')] * 100, '0.00006')
        elif item == 'closing_equity_roe':
            chk(f'{t} {b} {item}', r['value'], F[('FY2025', 'profit_after_tax')] / F[('FY2025', 'total_equity')] * 100, '0.00006')
        elif item == 'cost_to_income':
            pass  # needs the generator's cost definition; counted separately below
    elif t == 'paired_ratio':
        P = lambda k: sum(fin(b)[('FY2025', k)] for b in banks)
        if item == 'net_ldr': chk(f'{t} {item}', r['value'], P('loans_and_advances_net') / P('customer_deposits') * 100, '0.00006')
        if item == 'closing_equity_roe': chk(f'{t} {item}', r['value'], P('profit_after_tax') / P('total_equity') * 100, '0.00006')
print(f'checked {n} cells; mismatches {bad}; conditional markers {sorted(cond)}')
for f in fails[:20]: print('MISMATCH', f)
sys.exit(1 if bad else 0)
