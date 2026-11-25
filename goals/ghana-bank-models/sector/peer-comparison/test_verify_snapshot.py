"""Synthetic regression fixture for verify_snapshot.py. Run with python."""
import tempfile, pathlib, subprocess, csv, json, importlib.util
p=pathlib.Path(__file__).with_name('verify_snapshot.py');spec=importlib.util.spec_from_file_location('verify_peer',p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def wr(p,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def read(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
with tempfile.TemporaryDirectory() as tmp:
 t=pathlib.Path(tmp);r=t/'root';r.mkdir();g=r/'goals/ghana-bank-models';roll=t/'roll';peer=t/'peer';roll.mkdir();peer.mkdir()
 names=['alpha','beta','prudential','umb'];write(g/'ROSTER.md','| slug | name |\n| --- | --- |\n'+''.join(f'| {x} | {x} |\n' for x in names));write(g/'sector/macro-assumptions/macro.csv','shared macro\n');macro=v.text_hash(g/'sector/macro-assumptions/macro.csv');write(g/'review-resolutions/prudential.md','Scope: conditional (9M unavailable)\n');write(g/'review-resolutions/umb.md','Scope: conditional (FY2025 unavailable)\n')
 rows=[];cond=[];evidence=[];exclusions=[];markers={};totals={x:{} for x in ['total_assets','customer_deposits','profit_after_tax']}
 for idx,b in enumerate(names):
  d=g/'banks'/b
  h=[];fc=[]
  oldeq=-5 if b=='alpha' else 5
  for per,dat in [('FY2024',{'total_assets':100,'total_equity':oldeq}),('FY2025',{'total_assets':200,'total_equity':15,'customer_deposits':100,'profit_after_tax':10,'car_pct':20,'npl_pct':4,'loans_and_advances_gross':30})]:
   for k,x in dat.items():h.append({'bank':b,'period':per,'line_item':k,'value':str(x),'status':'estimated' if b=='umb' and per=='FY2025' else 'reported'})
  for sc,x in [('base',11),('downside',-2),('upside',20)]:
   for k,n in [('profit_after_tax',x),('x_car_proxy_pct',17)]:fc.append({'bank':b,'period':'FY2030E','scenario':sc,'line_item':k,'value':str(n),'status':'estimated'})
  wr(d/'financials.csv',h);wr(d/'forecast.csv',fc)
  for n in ['README.md','sources.md','assumptions.json','checks.md','model.py']:write(d/n,'fixture\n')
  ph=v.package_hash(d);common={'bank':b,'assets_2025_m':'200.000' if b!='umb' else '', 'customer_deposits_2025_m':'100.000' if b!='umb' else '', 'pat_2025_m':'10.000' if b!='umb' else '', 'pat_base_2030_m':'11.000','pat_downside_2030_m':'-2.000','pat_upside_2030_m':'20.000','car_base_2030_proxy_pct':'17.0000','car_downside_2030_proxy_pct':'17.0000','car_upside_2030_proxy_pct':'17.0000','package_sha256':ph,'macro_sha256':macro,'source_commit':''}
  if b in names[:2]:
   review=f'reviewer-of-owner-{b}.md';write(g/'reviews'/review,'Verdict: PASS\n');evidence.append({'bank':b,'owner':'owner','reviewer':'reviewer','reviewFile':review,'reviewSha256':v.text_hash(g/'reviews'/review),'packageFingerprint':ph,'macroFingerprint':macro})
   for k,x in [('total_assets',200),('customer_deposits',100),('profit_after_tax',10)]:totals[k][b]=x
   rows.append({**common,'reviewer':'reviewer','reported_car_2025_pct':'20.0000','reported_npl_2025_pct':'4.0000','roa_2025_pct':'6.6667','equity_open_2025_m':str(oldeq),'equity_close_2025_m':'15','roe_2025_pct':'' if b=='alpha' else '100.0000','roe_2025_status':'n/m: nonpositive opening or closing equity' if b=='alpha' else 'caution: equity changed by more than 2x','roe_closing_equity_2025_pct':'66.6667','gross_ldr_2025_pct':'30.0000'})
  else:
   m=v.scope_marker(g/'review-resolutions'/(b+'.md'));markers[b]=m;exclusions.append({'bank':b,'conditional':m['label'],'status':'needs-review','stage':'pending','packageFingerprint':ph,'macroFingerprint':macro});cond.append({**common,'scope':m['label'],'scope_marker_sha256':m['sha256'],'claim_status':'needs-review','review_stage':'pending'})
 subprocess.run(['git','init','-q',str(r)],check=True);subprocess.run(['git','-C',str(r),'add','.'],check=True);subprocess.run(['git','-C',str(r),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture'],check=True);sha=subprocess.check_output(['git','-C',str(r),'rev-parse','HEAD'],text=True).strip()
 for row in rows+cond:row['source_commit']=sha
 wr(peer/'comparison.csv',rows);wr(peer/'conditional-comparison.csv',cond)
 agg=[{'table':'history_total','period_or_scenario':'FY2025','item':k,'bank':'ACCEPTED_ONLY','value':str(sum(val.values())),'n_banks_reporting':'2','n_banks_eligible':'2','reporting_banks':'alpha;beta','source_commit':sha,'input_fingerprint':'fixture'} for k,val in totals.items()];wr(roll/'rollup.csv',agg)
 m={'schema':3,'sourceCommit':sha,'inputFingerprint':'fixture','acceptedEvidence':evidence,'exclusions':exclusions,'accepted':2,'excluded':2,'roster':4,'conditional':2,'conditionalMarkers':markers,'totals':{k:{'n':len(val),'banks':list(val),'value':sum(val.values())} for k,val in totals.items()},'outputHashes':{'rollup.csv':v.digest(roll/'rollup.csv')}}
 write(roll/'manifest.json',json.dumps(m));print('VALID',v.verify(r,roll,peer));tests=1
 def attack(path,change):
  global tests
  orig=path.read_bytes()
  try:
   change(path)
   try:v.verify(r,roll,peer)
   except (ValueError,KeyError,FileNotFoundError) as e: print('REJECTED',e);tests+=1
   else:raise AssertionError('accepted corruption')
  finally:path.write_bytes(orig)
 def alter_csv(p,key,value,idx=0): rr=read(p);rr[idx][key]=value;wr(p,rr)
 def alter_m(p,fn):j=json.loads(p.read_text());fn(j);write(p,json.dumps(j))
 attack(peer/'comparison.csv',lambda p:alter_csv(p,'roe_2025_pct','44.0000'))
 attack(peer/'comparison.csv',lambda p:alter_csv(p,'roe_2025_status','comparable',1))
 attack(peer/'comparison.csv',lambda p:alter_csv(p,'reviewer','fake'))
 attack(peer/'comparison.csv',lambda p:alter_csv(p,'bank','umb'))
 attack(peer/'comparison.csv',lambda p:alter_csv(p,'source_commit','fake'))
 attack(peer/'conditional-comparison.csv',lambda p:alter_csv(p,'assets_2025_m','999.000',1))
 attack(peer/'conditional-comparison.csv',lambda p:alter_csv(p,'scope_marker_sha256','fake'))
 attack(peer/'conditional-comparison.csv',lambda p:wr(p,read(p)[:1]))
 attack(roll/'manifest.json',lambda p:alter_m(p,lambda j:j['acceptedEvidence'][0].update(reviewSha256='bad')))
 attack(roll/'manifest.json',lambda p:alter_m(p,lambda j:j['totals']['total_assets'].update(value=0)))
 attack(roll/'rollup.csv',lambda p:alter_csv(p,'value','0'))
 print('PASS',tests,'integration checks')
