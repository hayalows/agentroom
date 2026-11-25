import re,csv,os,collections
G='/home/claude/agentroom/goals/ghana-bank-models/'
md=open(G+'reports/iconka/Ghana_Banking_Sector_Research_2026-2030.md',encoding='utf-8').read()
parts=re.split(r'\*\*BANK PROFILE (\d+) / 23\*\*',md)
SLUG={'Absa Bank Ghana':'absa-ghana','Access Bank Ghana':'access-bank-ghana','Agricultural Development Bank':'adb','Bank of Africa Ghana':'bank-of-africa-ghana','CalBank':'calbank','Consolidated Bank Ghana':'consolidated-bank-ghana','Ecobank Ghana':'ecobank-ghana','First Bank Ghana (FBNBank)':'fbnbank-ghana','Fidelity Bank Ghana':'fidelity-bank-ghana','First Atlantic Bank':'first-atlantic-bank','First National Bank Ghana':'first-national-bank-ghana','GCB Bank':'gcb'}
comp={r['bank']:r for r in csv.DictReader(open(G+'sector/peer-comparison/comparison.csv'))}
res=[]
def ok(c,msg): res.append((c,msg)); 
for i in range(1,len(parts),2):
    n=int(parts[i]);body=parts[i+1]
    name=re.search(r'## (.+)',body).group(1)
    if name not in SLUG: continue
    s=SLUG[name]
    fin=list(csv.DictReader(open(G+f'banks/{s}/financials.csv')))
    fc=list(csv.DictReader(open(G+f'banks/{s}/forecast.csv')))
    cl=open(G+f'claims/{s}.md').read()
    kv=dict(re.findall(r'^(\w+): (.*)$',cl,flags=re.M))
    m=re.search(r'Evidence trail: (.+?)\. (\d+) historical rows; (\d+) forecast rows; (\d+) reported-source IDs',body)
    trail,h,f,sid=m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4))
    ok(len(fin)==h,f'{s} hist rows paper {h} actual {len(fin)}')
    ok(len(fc)==f,f'{s} fc rows paper {f} actual {len(fc)}')
    ids={r['source_id'] for r in fin if r['status']=='reported' and r['source_id']}
    ok(len(ids)==sid,f'{s} reported-source IDs paper {sid} actual {len(ids)} (reported-status rows) / all ids {len({r["source_id"] for r in fin if r["source_id"]})}')
    own=re.match(r'(\S+) \(original\)|(\S+) \(original\)',trail)
    orig=re.match(r'([\w-]+) \(original\)',trail).group(1)
    stew=re.search(r'steward ([\w-]+)',trail); stew=stew.group(1) if stew else None
    rev=re.search(r'([\w-]+) \(manifest reviewer\)',trail).group(1)
    ok(rev==comp[s]['reviewer'],f'{s} manifest reviewer paper {rev} comparison.csv {comp[s]["reviewer"]}')
    print(f'{n:2} {s:26} claimfile agent={kv.get("agent")} steward={kv.get("steward")} | paper orig={orig} steward={stew}')
    # CAR / NPL reported
    p=re.search(r'FY25: net LDR ([\d.]+)%; closing-equity ROE ([\d.]+)%; reported CAR ([\w./]+)%?; reported NPL ([\w./]+)%?',body)
    car,npl=p.group(3),p.group(4)
    c=comp[s]
    ccar=c['reported_car_2025_pct'];cnpl=c['reported_npl_2025_pct']
    ok((car=='n/a' and not ccar) or (ccar and abs(float(car)-float(ccar))<0.051),f'{s} CAR paper {car} csv {ccar}')
    ok((npl.rstrip('%')=='n/a' and not cnpl) or (cnpl and abs(float(npl.rstrip('%'))-float(cnpl))<0.051),f'{s} NPL paper {npl} csv {cnpl}')
for c,m in res:
    if not c: print('MISMATCH',m)
print('checks',len(res),'fail',sum(1 for c,_ in res if not c))
