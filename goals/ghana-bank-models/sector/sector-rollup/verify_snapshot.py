import csv,json,math,hashlib,sys
from pathlib import Path
from decimal import Decimal as D
root,out=map(Path,sys.argv[1:3])
goal=root/'goals/ghana-bank-models'
m=json.loads((out/'manifest.json').read_text())
accepted={e['bank'] for e in m['acceptedEvidence']}
excluded={e['bank'] for e in m['exclusions']}
assert len(accepted)+len(excluded)==23 and not accepted & excluded
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
hist={};fc={}
for b in accepted:
    for r in read(goal/'banks'/b/'financials.csv'):
        if r['status'] in ('reported','derived') and r['value']!='':hist[b,r['period'],r['line_item']]=D(r['value'])
    for r in read(goal/'banks'/b/'forecast.csv'):
        if r['status']!='unavailable' and r['value']!='':fc[b,r['scenario'],r['period'],r['line_item']]=D(r['value'])
def h(b,p,i):
    if i=='operating_income_pre_impairment':
        vs=[hist.get((b,p,k)) for k in ('net_interest_income','fee_commission_income','fee_commission_expense','net_trading_income','other_operating_income')]
        return None if None in vs else vs[0]+vs[1]-vs[2]+vs[3]+vs[4]
    return hist.get((b,p,i))
def aggregate(values):
    a={k:v for k,v in values.items() if v is not None}
    return (sum(a.values()) if a else None,set(a))
def ratio(bs,p,i):
    v={}
    for b in bs:
        if i=='net_ldr':n,d=h(b,p,'loans_and_advances_net'),h(b,p,'customer_deposits')
        elif i=='closing_equity_roe':n,d=h(b,p,'profit_after_tax'),h(b,p,'total_equity')
        else:
            a=[h(b,p,k) for k in ('staff_costs','depreciation_amortisation','other_operating_expenses')]
            n,d=(None if None in a else sum(a)),h(b,p,'operating_income_pre_impairment')
        if n is not None and d is not None and d>0:v[b]=(n,d)
    return (100*sum(n for n,d in v.values())/sum(d for n,d in v.values()) if v else None,set(v))
ctx={r['indicator']:r for r in read(goal/'sector/macro-assumptions/sector-context.csv')}
ncheck=0;maxerr=D(0)
for r in read(out/'rollup.csv'):
    t,p,i,b=r['table'],r['period_or_scenario'],r['item'],r['bank']
    bs=accepted if b=='ACCEPTED_ONLY' else {b}
    assert bs<=accepted and r['source_commit']==m['sourceCommit'] and r['input_fingerprint']==m['inputFingerprint']
    if t=='forecast_total':
        sc,year=p.split('|')
        value,seen=aggregate({b:fc.get((b,sc,year,i)) for b in bs})
    elif t=='paired_ratio' or i in ('net_ldr','closing_equity_roe','cost_to_income'):value,seen=ratio(bs,p,i)
    else:
        value,seen=aggregate({b:h(b,p,i) for b in bs})
        if t=='coverage_ratio' and value is not None:
            k='total_deposits' if i=='customer_deposits' else 'total_assets'
            value=value/D(1000)/D(ctx[k]['2025-12' if p=='FY2025' else '2026-09'])*100
    assert seen==set(filter(None,r['reporting_banks'].split(';'))) and len(seen)==int(r['n_banks_reporting']),r
    assert int(r['n_banks_eligible'])==len(accepted),r
    if value is None:assert r['value']=='',r
    else:
        err=abs(D(r['value'])-value);maxerr=max(maxerr,err)
        assert err<=(D('.000051') if r['unit']=='percent' else D('.000501')),(r,err)
    ncheck+=1
pr=read(out/'provisional.csv');assert set(r['bank'] for r in pr)==excluded and len(pr)==len(excluded)*24
for f,sha in m['outputHashes'].items():assert hashlib.sha256((out/f).read_bytes()).hexdigest()==sha
assert len({e['packageFingerprint'] for e in m['acceptedEvidence']})==len(accepted)
print('INDEPENDENT PASS',ncheck,'output cells,',len(pr),'separate diagnostics, max rounding error',maxerr)
print('EXCLUDED',','.join(sorted(excluded)))
print('ACCEPTED',len(accepted),'of',len(accepted|excluded))
