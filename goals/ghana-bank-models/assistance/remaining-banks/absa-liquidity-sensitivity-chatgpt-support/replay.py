# Independent Absa liquidity sensitivity; no original files changed.
import tempfile,subprocess,csv,json,sys,hashlib,shutil
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
g=root/'goals/ghana-bank-models'
src=g/'assistance/remaining-banks/absa-model-draft-papa-kojo-agent'
macro=g/'sector/macro-assumptions/macro.csv'
orig=(src/'model.mjs').read_text(encoding='utf-8');a=json.loads((src/'assumptions.json').read_text())
def rd(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
q={r['line_item']:float(r['value']) for r in rd(src/'financials.csv') if r['period']=='9M-2026' and r['value'] and r['status']!='unavailable'}
reserve=3264.904;cash=q['cash_and_bog_balances'];dep=q['customer_deposits'];den=reserve/(.20*dep);share=reserve/cash
assert abs(9193.018+8.608-5936.721-reserve)<.002
patches=[
('preCash-b.customer_deposits*crr/A.liquidity.eligible_cash_share','preCash-b.customer_deposits*crr*A.liquidity.reserve_base_share/A.liquidity.eligible_cash_share'),
('let req=b.customer_deposits*crr,','let req=b.customer_deposits*crr*A.liquidity.reserve_base_share,'),
]
code=orig
for old,new in patches:
    assert code.count(old)==1,old
    code=code.replace(old,new)
# Expose multiple policy paths; retain both the all-deposit requirement stress and lower-cash stress.
rows=[];manifest=[]
for label,base,elig in [('original_full_deposit',1,a['liquidity']['eligible_cash_share']),('calibrated_base',den,share),('calibrated_20pct_cash_haircut',den,.8*share),('90pct_deposit_base',.9,share)]:
    with tempfile.TemporaryDirectory(prefix='absa-liquidity-support-') as t:
        d=Path(t); b=json.loads(json.dumps(a));b['history_file']='financials.csv';b['macro_file']='macro.csv';b['liquidity']['reserve_base_share']=base;b['liquidity']['eligible_cash_share']=elig;b['liquidity']['eligible_share_stress']=.8*elig
        shutil.copyfile(src/'financials.csv',d/'financials.csv');shutil.copyfile(macro,d/'macro.csv')
        (d/'assumptions.json').write_text(json.dumps(b,indent=2),encoding='utf-8');(d/'model.mjs').write_text(code,encoding='utf-8')
        p=subprocess.run(['node',str(d/'model.mjs')],cwd=d,capture_output=True,text=True,timeout=60)
        assert p.returncode==0,p.stderr
        rr=rd(d/'forecast.csv'); f={}
        for r in rr:
            f.setdefault((r['scenario'],r['period']),{})[r['line_item']]=float(r['value']) if r['value'] else None
        assert len(f)==15 and len(rr)==870
        if label=='original_full_deposit':
            original=rd(src/'forecast.csv')
            assert rr==original, 'baseline patch did not reproduce exact draft values'
        for (s,y),x in f.items():
            rows.append(dict(policy=label,scenario=s,period=y,deposit_base_share=base,eligible_cash_share=elig,pat_m=x['profit_after_tax'],assets_m=x['total_assets'],equity_m=x['total_equity'],car_proxy_pct=x['x_car_proxy_pct'],cash_gap_m=x['x_cash_reserve_gap'],stress_gap_m=x['x_cash_reserve_gap_stress'],additional_dividends_m=x['x_model_dividends'],full_year_dividends_m=x['x_dividends_paid']))
        manifest.append({'policy':label,'rows':len(rr),'stdout':p.stdout.strip(),'forecast_sha256':hashlib.sha256((d/'forecast.csv').read_bytes()).hexdigest(),'checks_sha256':hashlib.sha256((d/'checks.md').read_bytes()).hexdigest()})
with (out/'absa-liquidity-sensitivity.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'absa-liquidity-sensitivity-manifest.json').write_text(json.dumps({'source_draft_model_sha256':hashlib.sha256((src/'model.mjs').read_bytes()).hexdigest(),'source_draft_history_sha256':hashlib.sha256((src/'financials.csv').read_bytes()).hexdigest(),'macro_sha256':hashlib.sha256(macro.read_bytes()).hexdigest(),'implied_deposit_base_share':den,'cash_share_proxy':share,'source':'https://www.absa.com.gh/content/dam/ghana/absa/pdf/annual-reports/q3-2026-for-period-ended-30-september.pdf','variants':manifest},indent=2)+'\n',encoding='utf-8')
print('ANCHOR',den,share,'4 paths',len(rows),'scenario-year rows')
for r in rows:
    if r['period'] in ('FY2026E','FY2030E') and r['scenario']=='base':print(r)
print('FULL MODEL REPLAYS',manifest)
