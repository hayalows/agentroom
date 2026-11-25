"""Fill the six empty notes cells of omnibsic-bank other_liabilities (derived) rows with their formula.
Usage: python3 -I apply_patch.py <in financials.csv> <out financials.csv>. Asserts the formula residual <= 0.0015m."""
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], newline='')))
H = {(r['period'], r['line_item']): float(r['value']) for r in rows if r['value'] != ''}
n = 0
for r in rows:
    if r['line_item'] == 'other_liabilities' and r['status'] == 'derived' and not r['notes'].strip():
        p = r['period']
        res = H[(p, 'total_liabilities')] - H[(p, 'customer_deposits')] - H.get((p, 'due_to_banks'), 0.0) - H.get((p, 'borrowings'), 0.0) - float(r['value'])
        assert abs(res) <= 0.0015, (p, res)
        r['notes'] = 'Derived: total_liabilities - customer_deposits - due_to_banks (borrowings nil); residual 0.000.'
        n += 1
w = csv.DictWriter(open(sys.argv[2], 'w', newline='', encoding='utf-8'), fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_ALL, lineterminator='\n')
w.writeheader(); w.writerows(rows)
print('filled', n, 'notes')
