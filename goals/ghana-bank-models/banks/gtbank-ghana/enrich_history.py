from pathlib import Path
import csv,json,re,subprocess,sys
b=Path(__file__).resolve().parent
p=b/'financials.csv'
rows=list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
fields=list(rows[0])
idx={(r['period'],r['line_item']):r for r in rows}
def put(y,k,v,source='',page='',status='reported',note='',stmt='balance_sheet',unit='GHS millions'):
    r=idx.get((y,k))
    if r is None:
        r=dict.fromkeys(fields,'');rows.append(r);idx[y,k]=r
    r.update(bank='gtbank-ghana',period=y,statement=stmt,line_item=k,value='' if v is None else str(v),unit=unit,source_id=source,page=page,status='unavailable' if v is None else status,notes=note)
def get(y,k):
    r=idx.get((y,k));return float(r['value']) if r and r['value']!='' else None
for y,gross,ecl,bankcash,due,cash_ecl,capital,rwa,car,src,loanpage in [
('FY2021',1655.443137,7.802549,461.984480,432.182311,0,1157.700625,3004.810468,38.53,'GTB-AR22','131'),
('FY2022',2043.933443,17.588781,1506.155116,278.766264,5.645631,1151.870358,3446.876161,33.42,'GTB-AR22','131'),
('FY2023',1830.757628,40.335860,1776.427779,1329.318645,11.005965,1977.588755,4726.803408,41.84,'GTB-AR24','158'),
('FY2024',2583.143175,29.348012,3195.342016,2475.973976,11.005651,2294.374230,6199.479597,37.01,'GTB-AR24','158')]:
    put(y,'loans_and_advances_gross',gross,src,loanpage,note='Audited IFRS gross loan carrying amount.')
    put(y,'loan_loss_allowance',ecl,src,loanpage,'derived','Sum of stage 1/2 and stage 3 allowances.')
    for k,v in [('x_cash_and_bog_gross',bankcash),('x_due_from_banks_gross',due),('x_cash_impairment',cash_ecl)]:
        put(y,k,v,src,'note 15',note='Nonadditive audited component of combined cash; gross before separately shown aggregate allowance.')
    for k,v in [('x_regulatory_capital',capital),('x_tier1_capital',capital),('x_risk_weighted_assets',rwa)]:
        put(y,k,v,src,'note 3.6',note='Audited capital note; relief basis differs by period; FY21 total capital differs from Tier1 by GHS1.')
    put(y,'tier1_pct',round(100*capital/rwa,5),src,'note 3.6','derived','Tier 1 capital / RWA; not leverage ratio.','ratios','percent')
    put(y,'x_car_note_pct',car,src,'note 3.6',note='Audited note ratio, preserve separately from published summary.',stmt='ratios',unit='percent')
    assert abs(gross-ecl-get(y,'loans_and_advances_net'))<.005
    assert abs(bankcash+due-cash_ecl-get(y,'cash_and_bog_balances'))<.005
for y in sorted({r['period'] for r in rows}):
    put(y,'due_from_banks',None,note='Included in combined cash; separate net allocation unavailable, audited gross memo where available.')
    for k in ['cash_and_bog_balances','property_equipment_intangibles']:
        r=idx[y,k]
        if k=='cash_and_bog_balances':r['notes']='Combined cash and bank balances net of aggregate ECL; note15 gross components where available. Do not add memo rows.'
        else:r['notes']+=' AR22/AR24 lease note confirms ROU is already within PPE; no additional ROU added.'
    r=idx.get((y,'reserves_other'))
    if r:
        match=re.search(r'statutory reserve fund ([\d,]+)',r['notes'],re.I)
        if match:put(y,'x_statutory_reserve',int(match.group(1).replace(',',''))/1000,r['source_id'],r['page'],note='Statutory reserve included in reserves_other.')
    for k in ['loans_and_advances_gross','loan_loss_allowance']:
        if get(y,k) is None:idx[y,k]['notes']='Summary net only; full annual loan note not available for this period.'
    if get(y,'loans_and_advances_gross') is not None:
        put(y,'ldr_pct',round(100*get(y,'loans_and_advances_gross')/get(y,'customer_deposits'),5),status='derived',note='Gross loans / customer deposits.',stmt='ratios',unit='percent')
    put(y,'x_net_ldr_pct',round(100*get(y,'loans_and_advances_net')/get(y,'customer_deposits'),5),status='derived',note='Net loans / customer deposits.',stmt='ratios',unit='percent')
for y,v in [('FY2023',10.349744),('FY2024',11.984863)]:
    put(y,'x_rate_100bp_pbt_sensitivity',v,'GTB-AR24','note 3.5.1',note='Audited static +100bp PBT sensitivity, not annual forecast.',stmt='income_statement')
for y,v in [('FY2023',.747943),('FY2024',1.606045)]:
    put(y,'x_fx_5pct_strengthening_profit',v,'GTB-AR24','note 3.5.2',note='Audited static 5% cedi strengthening profit/equity sensitivity.',stmt='income_statement')
put('FY2024','x_parent_ownership_pct',98.32,'GTB-AR24','10',note='Nigeria parent shareholding at FY24.',stmt='ratios',unit='percent')
assert get('9M-2026','x_statutory_reserve')==946.091
with p.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
