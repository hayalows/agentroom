"""Apply the six Ecobank ROU reclassifications (source table: assistance/gemini/rou-classification/papa-kojo-agent.md)
to a COPY of banks/ecobank-ghana/financials.csv. Usage: python3 -I apply_patch.py <in_financials.csv> <out_financials.csv>
Moves ROU from other_assets to property_equipment_intangibles; asserts the table's corrected totals; adds a memo row x_right_of_use_assets."""
import csv, sys
MOVES = {  # period: (rou, correct PPE+int+ROU, correct other assets)
 'FY2021': (45.530, 657.561, 2681.191), 'FY2022': (38.670, 1312.770, 2597.921),
 'FY2023': (62.472, 1327.220, 1714.563), 'FY2024': (92.353, 1353.975, 2817.312),
 'FY2025': (90.823, 1389.626, 2654.844), '9M-2026': (73.725, 1361.731, 3518.763)}
SRC = {'FY2021':'EGH22','FY2022':'EGH22','FY2023':'EGH24','FY2024':'EGH25','FY2025':'EGH25','9M-2026':'EGH26Q3'}
rows = list(csv.DictReader(open(sys.argv[1], newline='')))
fields = list(rows[0].keys())
seen = set(); out = []
for r in rows:
    p = r['period']
    if p in MOVES and r['statement'] == 'balance_sheet' and r['line_item'] in ('property_equipment_intangibles', 'other_assets'):
        rou, ppe, oth = MOVES[p]
        v = float(r['value'])
        if r['line_item'] == 'property_equipment_intangibles':
            new = round(v + rou, 3); assert abs(new - ppe) < 0.0015, (p, new, ppe)
            r['notes'] = (r['notes'] + ' ' if r['notes'] else '') + f'Includes right-of-use assets {rou:.3f}m (moved from other_assets).'
        else:
            new = round(v - rou, 3); assert abs(new - oth) < 0.0015, (p, new, oth)
            r['notes'] = r['notes'].replace('tax assets, ROU assets, ', 'tax assets, ')
            r['notes'] = (r['notes'] + ' ' if r['notes'] else '') + f'Excludes right-of-use assets {rou:.3f}m (now in property_equipment_intangibles).'
        r['value'] = f'{new:.3f}'; seen.add((p, r['line_item']))
        r['status'] = r['status'] if r['status'] in ('reported', 'derived') else 'derived'
        if r['status'] == 'reported': r['status'] = 'derived'
    out.append(r)
    if p in MOVES and r['line_item'] == 'other_assets' and r['statement'] == 'balance_sheet':
        m = dict(r); m.update(line_item='x_right_of_use_assets', value=f'{MOVES[p][0]:.3f}', status='reported', source_id=SRC[p],
            notes='Memo, non-additive: ROU assets, already inside property_equipment_intangibles. Source: Bank column, statement of financial position.')
        out.append(m)
assert len(seen) == 12, sorted(seen)
w = csv.DictWriter(open(sys.argv[2], 'w', newline='', encoding='utf-8'), fieldnames=fields, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
w.writeheader(); w.writerows(out)
print('patched 12 rows, added 6 memo rows')
