import csv,re
from decimal import Decimal as D, ROUND_HALF_UP
S='sector/'
md=open('reports/iconka/Ghana_Banking_Sector_Research_2026-2030.md').read().split('\n')
RU=list(csv.DictReader(open(S+'sector-rollup/rollup.csv')))
MA=list(csv.DictReader(open(S+'macro-assumptions/macro.csv')))
SC={r['indicator']:r for r in csv.DictReader(open(S+'macro-assumptions/sector-context.csv'))}
def tables(a,b):
    out=[];cur=None
    for i in range(a,b):
        l=md[i]
        if l.startswith('|'):
            cells=[c.strip() for c in l.strip('|').split('|')]
            if set(''.join(cells))<=set('- '): continue
            if cur is None: cur=[i+1,[]]; out.append(cur)
            cur[1].append(cells)
        else: cur=None
    return out
def r2(x,p=2): return str(D(x).quantize(D(10)**-p,rounding=ROUND_HALF_UP))
n=bad=half=0; fails=[]
def chk(label,shown,exact,p=2):
    global n,bad,half
    n+=1
    s=str(shown)
    e=D(exact).quantize(D(10)**-p,rounding=ROUND_HALF_UP)
    if D(s)!=e:
        # accept python-style round-half-even or tiny float edge: within 0.5 unit of last place
        if abs(D(s)-D(exact))<=D(10)**-p*D('0.5000001'): half+=1
        else: bad+=1; fails.append((label,s,str(exact)))
hist={}
for r in RU:
    if r['table']=='history_total': hist[(r['period_or_scenario'],r['item'])]=D(r['value'])/1000
fore={}
for r in RU:
    if r['table']=='forecast_total': fore[(r['period_or_scenario'],r['item'])]=D(r['value'])/1000
T=tables(51,182)
# history table
ht=T[0][1]; per=['FY2021','FY2022','FY2023','FY2024','FY2025','9M-2026']
mp={'Assets':'total_assets','Deposits':'customer_deposits','Net loans':'loans_and_advances_net','Equity':'total_equity','PAT':'profit_after_tax','Net interest income':'net_interest_income'}
for row in ht[1:]:
    for j,p in enumerate(per): chk(f'hist {row[0]} {p}',row[j+1],hist[(p,mp[row[0]])])
# chart data PAT
ct=T[1][1]
for j,p in enumerate(per[:5]): chk(f'chart PAT {p}',ct[1][j+1],hist[(p,'profit_after_tax')],3)
# macro tables (macro.csv)
M={(r['scenario'],int(re.sub(r'\D','',r['year'])[:4]),r['driver']):D(r['value']) for r in MA if r['value'] not in ('','unavailable')}
names={'Policy rate (%)':'policy_rate_pct','91-day Treasury bill yield (%)':'tbill_91d_pct','CPI inflation (%)':'inflation_cpi_pct','Real GDP growth (%)':'gdp_growth_pct','End-year GHS per USD':'ghs_per_usd_end'}
for start,t in T:
    h=t[0][0]
    if h in names:
        for row in t[1:]:
            sc=row[0].lower()
            for j,y in enumerate(range(2026,2031)): chk(f'macro {h} {sc} {y}',row[j+1],M[(sc,y,names[h])])
# BoG table
bog=[t for s,t in T if t[0][0]=='BoG indicator'][0]
cols={'Dec 2025':'2025-12','Apr 2026':'2026-04','Sep 2026':'2026-09','Oct 2026':'2026-10'}
im={'Assets (GHS bn)':'total_assets','Deposits (GHS bn)':'total_deposits','Gross advances (GHS bn)':'total_advances','CAR (%)':'capital_adequacy_ratio','NPL (%)':'npl_ratio','NIM (%)':'net_interest_margin','ROE after tax (%)':'return_on_equity_after_tax','Average lending rate (%)':'average_lending_rate','Private credit growth YoY (%)':'private_sector_credit_growth_yoy','Operational cost / gross income (%)':'operational_cost_to_gross_income'}
for row in bog[1:]:
    for j,h in enumerate(bog[0][1:]):
        v=D(SC[im[row[0]]][cols[h]]); p=2 if 'lending' in row[0] else 1
        chk(f'BoG {row[0]} {h}',row[j+1],v,p)
# forecast tables
for start,t in T:
    h=t[0][0]
    if h in ('PAT','Assets','Equity') and t[0][1]=='2026E':
        it={'PAT':'profit_after_tax','Assets':'total_assets','Equity':'total_equity'}[h]
        for row in t[1:]:
            sc=row[0].lower()
            for j,y in enumerate(range(2026,2031)): chk(f'fore {h} {sc} {y}',row[j+1],fore[(f'{sc}|FY{y}E',it)])
    if h=='Scenario':
        for row in t[1:]:
            sc=row[0].lower()
            for j,y in enumerate(range(2026,2031)): chk(f'chart fore {sc} {y}',row[j+1],fore[(f'{sc}|FY{y}E','profit_after_tax')],3)
# exec summary table
ex=tables(25,50)[0][1]
for row in ex[1:]:
    it={'Assets':'total_assets','Equity':'total_equity','PAT':'profit_after_tax'}[row[0]]
    chk(f'exec {row[0]} 2025',row[1],hist[('FY2025',it)])
    for j,(sc,y) in enumerate([('base',2026),('base',2030),('downside',2030),('upside',2030)]): chk(f'exec {row[0]} {sc}{y}',row[j+2],fore[(f'{sc}|FY{y}E',it)])
# derived statements
def pct(a,b): return (a/b-1)*100
chk('assets growth 21-25',139.2,pct(hist[('FY2025','total_assets')],hist[('FY2021','total_assets')]),1)
chk('deposit growth 21-25',160.7,pct(hist[('FY2025','customer_deposits')],hist[('FY2021','customer_deposits')]),1)
chk('PAT yoy 25',34.3,pct(hist[('FY2025','profit_after_tax')],hist[('FY2024','profit_after_tax')]),1)
chk('PAT 26 vs 25',-7.9,pct(fore[('base|FY2026E','profit_after_tax')],hist[('FY2025','profit_after_tax')]),1)
chk('PAT growth 25-30',37.4,pct(fore[('base|FY2030E','profit_after_tax')],hist[('FY2025','profit_after_tax')]),1)
chk('downside vs base 2030',-62,pct(fore[('downside|FY2030E','profit_after_tax')],fore[('base|FY2030E','profit_after_tax')]),0)
chk('upside vs base 2030',37,pct(fore[('upside|FY2030E','profit_after_tax')],fore[('base|FY2030E','profit_after_tax')]),0)
chk('Oct26 assets vs Dec25',14.8,pct(D(SC['total_assets']['2026-10']),D(SC['total_assets']['2025-12'])),1)

NAMES={'GCB Bank':'gcb','Ecobank Ghana':'ecobank-ghana','Stanbic Bank Ghana':'stanbic-bank-ghana','Absa Bank Ghana':'absa-ghana','Zenith Bank Ghana':'zenith-bank-ghana','Fidelity Bank Ghana':'fidelity-bank-ghana','Guaranty Trust Bank Ghana':'gtbank-ghana','First Atlantic Bank':'first-atlantic-bank','Access Bank Ghana':'access-bank-ghana','Agricultural Development Bank':'adb','Consolidated Bank Ghana':'consolidated-bank-ghana','Standard Chartered Bank Ghana':'standard-chartered-ghana','Republic Bank Ghana':'republic-bank-ghana','National Investment Bank':'nib','CalBank':'calbank','United Bank for Africa Ghana':'uba-ghana','Societe Generale Ghana':'societe-generale-ghana','First National Bank Ghana':'first-national-bank-ghana','First Bank Ghana (FBNBank)':'fbnbank-ghana','Bank of Africa Ghana':'bank-of-africa-ghana'}
FIN={};FC={}
for nm,b in NAMES.items():
    FIN[b]={(r['period'],r['line_item']):D(r['value']) for r in csv.DictReader(open(f'banks/{b}/financials.csv')) if r['value']!=''}
    FC[b]={(r['scenario'],r['period'],r['line_item']):D(r['value']) for r in csv.DictReader(open(f'banks/{b}/forecast.csv')) if r['value']!=''}
T2=tables(213,327)
for start,t in T2:
    h=t[0][0]
    if h=='GHS bn, illustrative':
        base=[fore[(f'base|FY{y}E','total_assets')] for y in range(2026,2031)]
        for row,cov in ((t[2],D(next(r['value'] for r in RU if r['table']=='coverage_ratio' and r['period_or_scenario']=='FY2025' and r['item']=='total_assets'))),(t[3],D(next(r['value'] for r in RU if r['table']=='coverage_ratio' and r['period_or_scenario']=='9M-2026' and r['item']=='total_assets')))):
            for j,y in enumerate(range(2026,2031)): chk(f'scale {cov} {y}',row[j+1],base[j]/(cov/100))
        for j in range(5): chk(f'scale base row {j}',t[1][j+1],base[j])
    if h=='Bank' and t[0][1]=='Assets':
        for row in t[1:]:
            b=NAMES[row[0]];F=FIN[b]
            chk(f'size {b} assets',row[1],F[('FY2025','total_assets')]/1000)
            chk(f'size {b} deposits',row[2],F[('FY2025','customer_deposits')]/1000)
            chk(f'size {b} PAT',row[3],F[('FY2025','profit_after_tax')]/1000)
            chk(f'size {b} netLDR',row[4].rstrip('%'),F[('FY2025','loans_and_advances_net')]/F[('FY2025','customer_deposits')]*100,1)
            chk(f'size {b} ROE',row[5].rstrip('%'),F[('FY2025','profit_after_tax')]/F[('FY2025','total_equity')]*100,1)
        order=[r[0] for r in t[1:]]
        srt=sorted(NAMES,key=lambda k:-FIN[NAMES[k]][('FY2025','total_assets')])
        n+=1; bad+= (order!=srt); (fails.append(('size order',order,srt)) if order!=srt else None)
    if h=='Bank' and t[0][1]=='Base PAT':
        for row in t[1:]:
            b=NAMES[row[0]];F=FC[b]
            vals=[F[(s,'FY2030E','profit_after_tax')] for s in ('base','downside','upside')]
            for j,v in enumerate(vals): chk(f'stress {b} pat{j}',row[j+1].replace(',',''),v,1)
            for j,s in ((4,'base'),(5,'downside')):
                key=(s,'FY2030E','x_car_proxy_pct')
                if key not in F: key=(s,'FY2030E','car_pct')
                chk(f'stress {b} car {s}',row[j].rstrip('%'),F[key],1)
        dpat={NAMES[r[0]]:FC[NAMES[r[0]]][('downside','FY2030E','profit_after_tax')] for r in t[1:]}
        order=[NAMES[r[0]] for r in t[1:]]; srt=sorted(order,key=lambda b:dpat[b])
        n+=1; bad+=(order!=srt)
        if order!=srt: fails.append(('stress order',order,srt))
        n+=1; losers=sum(1 for v in dpat.values() if v<0)
        if losers!=7: bad+=1; fails.append(('loss-making downside',losers,7))
        low=[b for b in NAMES.values() if min(FC[b][('base','FY2030E',k)] for k in ['x_car_proxy_pct','car_pct'] if ('base','FY2030E',k) in FC[b])<13 or min(FC[b][('downside','FY2030E',k)] for k in ['x_car_proxy_pct','car_pct'] if ('downside','FY2030E',k) in FC[b])<13]
        print('banks with a FY2030 proxy below 13% in base or downside:',sorted(low))
    if t[0][0].startswith('Largest contributions'):
        gap={b:FC[b][('base','FY2030E','profit_after_tax')]-FC[b][('downside','FY2030E','profit_after_tax')] for b in NAMES.values()}
        net=sum(gap.values())
        for row in t[1:]:
            b=NAMES[row[0]]; chk(f'gap {b}',row[1].replace(',',''),gap[b],1); chk(f'gap share {b}',row[2].rstrip('%'),gap[b]/net*100,1)
        chk('net gap bn',12.05,net/1000,2)
tot=sum(FIN[b][('FY2025','total_assets')] for b in NAMES.values())
srt=sorted(NAMES.values(),key=lambda b:-FIN[b][('FY2025','total_assets')])
chk('top2 share',24.4,sum(FIN[b][('FY2025','total_assets')] for b in srt[:2])/tot*100,1)
chk('top4 share',41.3,sum(FIN[b][('FY2025','total_assets')] for b in srt[:4])/tot*100,1)
b30=sum(FC[b][('base','FY2030E','profit_after_tax')] for b in NAMES.values())
chk('GCB share base PAT 2030',26.9,FC['gcb'][('base','FY2030E','profit_after_tax')]/b30*100,1)
inc=b30-sum(FIN[b][('FY2025','profit_after_tax')] for b in NAMES.values())
chk('GCB share of increase',59.9,(FC['gcb'][('base','FY2030E','profit_after_tax')]-FIN['gcb'][('FY2025','profit_after_tax')])/inc*100,1)
for y,v in zip(range(2026,2031),(20.2,19.6,18.5,17.4,17.1)):
    chk(f'closing-equity return {y}',v,fore[(f'base|FY{y}E','profit_after_tax')]/fore[(f'base|FY{y}E','total_equity')]*100,1)
for b,v in (('adb',70.53),('nib',69.70),('consolidated-bank-ghana',33.42)):
    chk(f'NPL {b}',v,FIN[b][('FY2025','npl_pct')],2)

print('cells',n,'mismatches',bad,'half-way rounding cases',half)
for f in fails: print('MISMATCH',f)
