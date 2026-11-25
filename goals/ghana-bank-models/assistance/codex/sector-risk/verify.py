"""Independent Decimal verification of pinned scenario-risk diagnostic.
Run from repo root: python -I goals/ghana-bank-models/assistance/codex/sector-risk/verify.py.
No model code or supervisor executed; original source blobs are read with git show.
"""
import csv
import io
import json
import subprocess
from decimal import Decimal as D
from pathlib import Path

HERE=Path(__file__).resolve().parent
root=HERE.parents[4]
# root = repository, assistance/codex/sector-risk is four levels below goals
if not (root/'ACTIVE_GOAL').exists():
    root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
report=json.loads((HERE/'diagnostic-results.json').read_text(encoding='utf-8'))
pin=report['pin']
ordinary=[b['bank'] for b in report['bank']]
excluded=[b['bank'] for b in report['excluded']]
assert len(ordinary)==18 and len(excluded)==5 and len(set(ordinary+excluded))==23
assert set(excluded)=={'absa-ghana','adb','omnibsic-bank','prudential-bank','umb'}
extracted={}
for i in (1,2,3):
    for b in json.loads((HERE/f'extract-{i}.json').read_text(encoding='utf-8')):
        assert b['slug'] not in extracted
        extracted[b['slug']]=b
assert set(extracted)==set(ordinary+excluded)
checks=0
maxerr=D('0')
def check(actual,expected,tol=D('0.00000001')):
    global checks,maxerr
    checks+=1
    if actual is None or expected is None:
        assert actual is None and expected is None,(actual,expected)
        return
    err=abs(D(str(actual))-D(str(expected)))
    maxerr=max(err,maxerr)
    assert err<=tol,(actual,expected,err)
def git(*args):
    return subprocess.check_output(['git','-C',str(root),*args])
data={}
count=0
for slug in ordinary+excluded:
    path=f'goals/ghana-bank-models/banks/{slug}/forecast.csv'
    blob=git('rev-parse',pin+':'+path).decode().strip()
    assert extracted[slug]['blob']==blob,(slug,'blob mismatch')
    raw=git('show',pin+':'+path).decode('utf-8-sig')
    rows=list(csv.DictReader(io.StringIO(raw,newline='')))
    check(len(rows),extracted[slug]['rows'])
    count+=len(rows)
    groups={}
    for row in rows:
        assert row['bank']==slug and row['status'] in ('estimated','unavailable')
        if row['status']=='unavailable':
            assert not row['value'].strip()
            value=None
        else:
            assert row['value'].strip()
            value=D(row['value'])
            assert value.is_finite()
        key=(row['scenario'],row['period'])
        group=groups.setdefault(key,{})
        assert row['line_item'] not in group
        group[row['line_item']]=value
    assert len(groups)==15
    for entry in extracted[slug]['data']:
        key=(entry['scenario'],f"FY{entry['year']}E")
        r=groups[key]
        car=r.get('car_pct')
        if car is None:car=r.get('x_car_proxy_pct')
        vals={'pat':r['profit_after_tax'],'assets':r['total_assets'],'equity':r['total_equity'],'car':car}
        for k,v in vals.items():check(entry[k],v)
        check(r['total_assets'],r['total_liabilities']+r['total_equity'],D('.0051'))
        data[(slug,entry['scenario'],entry['year'])]=vals
check(count,report['rows'])
check(len(data),report['scenario_years'])
for a in report['annual']:
    y=a['year']
    b=[data[(slug,'base',y)] for slug in ordinary]
    d=[data[(slug,'downside',y)] for slug in ordinary]
    u=[data[(slug,'upside',y)] for slug in ordinary]
    sums=lambda rows,key:sum(x[key] for x in rows)
    for label,rows in [('base',b),('down',d),('up',u)]:check(a[label],sums(rows,'pat'))
    check(a['delta'],sums(b,'pat')-sums(d,'pat'))
    check(a['down_losses'],sum(x['pat']<0 for x in d))
    check(a['down_negative_equity'],sum(x['equity']<0 for x in d))
    check(a['down_car_coverage'],sum(x['car'] is not None for x in d))
    under=[x for x in d if x['car'] is not None and x['car']<13]
    check(a['down_car_lt13'],len(under))
    check(a['down_assets'],sums(d,'assets'))
    check(a['down_lt13_assets'],sums(under,'assets'))
diffs=[]
for b in report['bank']:
    slug=b['bank']
    annual=[data[(slug,'downside',y)] for y in range(2026,2031)]
    base,down,up=(data[(slug,s,2030)] for s in ('base','downside','upside'))
    for k,x in [('base',base),('down',down),('up',up)]:check(b[k],x['pat'])
    delta=base['pat']-down['pat'];diffs.append(delta)
    check(b['delta'],delta)
    check(b['cumulative_delta'],sum(data[(slug,'base',y)]['pat']-data[(slug,'downside',y)]['pat'] for y in range(2026,2031)))
    check(b['down_car'],down['car']);check(b['down_equity'],down['equity']);check(b['down_assets'],down['assets'])
    check(b['loss_years'],sum(x['pat']<0 for x in annual))
    check(b['car_coverage'],sum(x['car'] is not None for x in annual))
    check(b['car_under_years'],sum(x['car'] is not None and x['car']<13 for x in annual))
    check(b['first_loss'],next((2026+i for i,x in enumerate(annual) if x['pat']<0),None))
    check(b['first_car_under'],next((2026+i for i,x in enumerate(annual) if x['car'] is not None and x['car']<13),None))
assert diffs==sorted(diffs,reverse=True)
check(report['top3_share_pct'],100*sum(diffs[:3])/sum(diffs))
inversions={(slug,y) for slug in ordinary for y in range(2026,2031) if data[(slug,'downside',y)]['pat']>data[(slug,'base',y)]['pat']+D('.001') or data[(slug,'upside',y)]['pat']<data[(slug,'base',y)]['pat']-D('.001')}
assert inversions=={(x['bank'],x['year']) for x in report['nonMonotonic']}
for e in report['excluded']:
    for s,k in [('base','base'),('downside','down'),('upside','up')]:check(e[k],data[(e['bank'],s,2030)]['pat'])
    check(e['down_car'],data[(e['bank'],'downside',2030)]['car'])
    check(e['down_equity'],data[(e['bank'],'downside',2030)]['equity'])
print(json.dumps({'pin':pin,'checks':checks,'max_error':str(maxerr),'source_rows':count,'groups':len(data),'inversions':len(inversions),'result':'PASS'},indent=2))
