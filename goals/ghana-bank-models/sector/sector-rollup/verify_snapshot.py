import csv,json,math,hashlib,sys,re
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
if m['schema']>=3:
    # Independent marker check, including a source file that says conditional without a structured label.
    markers={}
    for bank in accepted|excluded:
        marker=goal/'review-resolutions'/(bank+'.md')
        if not marker.exists():continue
        raw=marker.read_bytes()
        txt=raw.decode('utf-8')
        if not re.search(r'\bconditional\b',txt,re.I):continue
        scope=re.search(r'^Scope:\s*conditional\s*\(([^\r\n]+)\)\s*$',txt,re.I|re.M)
        label=re.search(r'["“]conditional:\s*([^"”\r\n]+)["”]',txt,re.I)
        gap=scope.group(1) if scope else label.group(1) if label else 'source gap; see scope marker'
        markers[bank]={'label':'conditional: '+gap.strip(),'sha256':hashlib.sha256(raw).hexdigest()}
    assert m['conditionalMarkers']==markers and not accepted & markers.keys()
    assert m['conditional']==len(markers) and markers.keys()<=excluded
    assert all(e['conditional']==markers.get(e['bank'],{}).get('label') for e in m['exclusions'])
    assert all(r['classification'].startswith(markers[r['bank']]['label']+'; ') if r['bank'] in markers else r['classification'].startswith('unaccepted ') for r in pr)
    seen=set()
    for r in pr:
        bank,period,item=r['bank'],r['period_or_scenario'],r['item']
        key=(bank,period,item)
        assert key not in seen and r['source_commit']==m['sourceCommit'],r
        seen.add(key)
        forecast='|' in period
        scenario,period=period.split('|') if forecast else (None,period)
        source='forecast.csv' if forecast else 'financials.csv'
        if any(e['bank']==bank and e['table']==source.removesuffix('.csv') for e in m['diagnosticErrors']):
            assert r['value']=='',r
            continue
        filename=goal/'banks'/bank/source
        source_rows=read(filename) if filename.exists() else []
        matches=[x for x in source_rows if x['period']==period and x['line_item']==item and (not forecast or x['scenario']==scenario)]
        assert len(matches)<=1,r
        value=None
        if matches:
            x=matches[0]
            allowed=(x['status']!='unavailable') if forecast else (x['status'] in ('reported','derived'))
            if allowed and x['value'].strip():
                try:
                    d=D(x['value'])
                    if d.is_finite():value=d
                except Exception:pass
        if value is None:assert r['value']=='',r
        else:assert abs(D(r['value'])-value)<=D('.000501'),r
    print('CONDITIONAL/DIAGNOSTIC PASS',len(markers),'scope markers,',len(pr),'separately verified values')

for f,sha in m['outputHashes'].items():assert hashlib.sha256((out/f).read_bytes()).hexdigest()==sha
assert len({e['packageFingerprint'] for e in m['acceptedEvidence']})==len(accepted)
print('INDEPENDENT PASS',ncheck,'output cells,',len(pr),'separate diagnostics, max rounding error',maxerr)
print('EXCLUDED',','.join(sorted(excluded)))
print('ACCEPTED',len(accepted),'of',len(accepted|excluded))
