// Accepted-only peer comparison. Run node goals/ghana-bank-models/sector/peer-comparison/compare.mjs from a clean repository checkout.
// No bank files are modified. The exact-version supervisor is the eligibility gate.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url));
const args=process.argv.slice(2), options={};
for(let i=0;i<args.length;i+=2){if(!['--input-root','--output','--report'].includes(args[i])||!args[i+1]||Object.hasOwn(options,args[i]))throw Error('Usage: compare.mjs [--input-root PATH] [--output PATH] [--report PATH]');options[args[i]]=args[i+1];}
const root=path.resolve(options['--input-root']??path.resolve(here,'../../../..'));
const goal='ghana-bank-models',dir=path.join(root,'goals',goal);
const out=path.resolve(options['--output']??path.join(here,'comparison.csv'));
const clean=()=>{const changed=execFileSync('git',['status','--porcelain','--untracked-files=all'],{cwd:root,encoding:'utf8'}).trim();if(changed)throw Error('Input checkout must be entirely clean before comparison: '+changed.slice(0,400));};
clean();
const sha=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
const {evaluateRoom}=await import(pathToFileURL(path.join(root,'scripts/completion.mjs')).href);
const {csv}=await import(pathToFileURL(path.join(root,'scripts/bank-gate.mjs')).href);
const state=await evaluateRoom(root,goal);
const num=r=>r&&r.value.trim()!==''&&r.status!=='unavailable'&&Number.isFinite(+r.value)?+r.value:null;
function values(rows,p,s){const result={};for(const r of rows.filter(r=>r.period===p&&(!s||r.scenario===s))){if(Object.hasOwn(result,r.line_item))throw Error('duplicate period/line: '+p+'/'+r.line_item);result[r.line_item]=!s&&!['reported','derived'].includes(r.status)?null:num(r)}return result;}
const ratio=(a,b)=>a!=null&&b!=null&&b>0?100*a/b:null,avg=(a,b)=>a!=null&&b!=null?(a+b)/2:null,car=x=>x.car_pct??x.x_car_proxy_pct??null;
const rows=[];
function roeFields(p,a){
 const open=p.total_equity,close=a.total_equity;
 const valid=open!=null&&close!=null&&open>0&&close>0;
 const material=valid&&(close/open>2||close/open<0.5);
 return {equity_open_2025_m:open,equity_close_2025_m:close,roe_2025_pct:valid?ratio(a.profit_after_tax,avg(open,close)):null,roe_2025_status:open==null||close==null?'unavailable':!valid?'n/m: nonpositive opening or closing equity':material?'caution: equity changed by more than 2x':'comparable',roe_closing_equity_2025_pct:ratio(a.profit_after_tax,close)};
}
for(const t of state.tasks.filter(t=>t.acceptance==='accepted')){
 const bankdir=path.join(dir,'banks',t.slug);
 const h=csv(fs.readFileSync(path.join(bankdir,'financials.csv'),'utf8')),f=csv(fs.readFileSync(path.join(bankdir,'forecast.csv'),'utf8'));
 const p=values(h,'FY2024'),a=values(h,'FY2025'),b=values(f,'FY2030E','base'),d=values(f,'FY2030E','downside'),u=values(f,'FY2030E','upside');
 rows.push({bank:t.slug,assets_2025_m:a.total_assets,customer_deposits_2025_m:a.customer_deposits,pat_2025_m:a.profit_after_tax,reported_car_2025_pct:a.car_pct,reported_npl_2025_pct:a.npl_pct,roa_2025_pct:ratio(a.profit_after_tax,avg(p.total_assets,a.total_assets)),...roeFields(p,a),gross_ldr_2025_pct:ratio(a.loans_and_advances_gross,a.customer_deposits),pat_base_2030_m:b.profit_after_tax,pat_downside_2030_m:d.profit_after_tax,pat_upside_2030_m:u.profit_after_tax,car_base_2030_proxy_pct:car(b),car_downside_2030_proxy_pct:car(d),car_upside_2030_proxy_pct:car(u),package_sha256:t.completionEvidence.packageFingerprint,macro_sha256:t.completionEvidence.macroFingerprint,reviewer:t.completionEvidence.reviewer,source_commit:sha});
}
if(!rows.length)throw Error('No accepted models; do not substitute provisional banks.');
const cols=Object.keys(rows[0]),quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
const format=(k,v)=>v==null?'':typeof v==='number'?v.toFixed(k.endsWith('_pct')?4:3):v;
const content=[cols,...rows.map(r=>cols.map(k=>format(k,r[k])))].map(r=>r.map(quote).join(',')).join('\n')+'\n';
clean();
if(execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim()!==sha)throw Error('Input commit changed during generation');
fs.writeFileSync(out,content);
if(options['--report']){
 const fmt=(v,d=3)=>v==null?'—':v.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
 const total=k=>rows.reduce((n,r)=>n+(r[k]??0),0), count=k=>rows.filter(r=>r[k]!=null).length;
 const md=['# Accepted-bank peer comparison — current pinned checkpoint','','Source commit: `'+sha+'`','',
  '**'+rows.length+' of '+state.tasks.length+' bank models accepted at this snapshot.** Excluded banks: '+state.tasks.filter(t=>t.acceptance!=='accepted').map(t=>t.slug).join(', ')+'.',
  'The earlier seven-bank comparison is superseded; its original CSV is retained as historical evidence, not current coverage. This report and comparison.csv come from the same generator invocation.','',
  '## FY2025 historical comparison (GHS millions; percent ratios)','',
  '| Bank | Assets | Deposits | PAT | Opening equity | Closing equity | Average equity ROE % | Closing equity ROE % | ROE status | ROA % | CAR % | NPL % | Gross LDR % |',
  '|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|',
  ...rows.map(r=>'| '+[r.bank,fmt(r.assets_2025_m),fmt(r.customer_deposits_2025_m),fmt(r.pat_2025_m),fmt(r.equity_open_2025_m),fmt(r.equity_close_2025_m),r.roe_2025_status.startsWith('n/m')?'n/m':fmt(r.roe_2025_pct,4),fmt(r.roe_closing_equity_2025_pct,4),r.roe_2025_status,fmt(r.roa_2025_pct,4),fmt(r.reported_car_2025_pct,4),fmt(r.reported_npl_2025_pct,4),fmt(r.gross_ldr_2025_pct,4)].join(' | ')+' |'),
  '', 'Totals: assets '+fmt(total('assets_2025_m'))+' ('+count('assets_2025_m')+' banks), deposits '+fmt(total('customer_deposits_2025_m'))+' ('+count('customer_deposits_2025_m')+' banks), PAT '+fmt(total('pat_2025_m'))+' ('+count('pat_2025_m')+' banks). Partial sector totals only.','',
  'Average-equity ROE is blank in CSV and shown n/m here when either equity endpoint is nonpositive. When positive closing equity is more than twice or less than half opening equity, the ratio is retained with a caution flag. Closing-equity ROE is PAT / positive closing book equity and is a separate comparator, not a substitute for normal average-equity ROE. ROA uses average assets; gross LDR is blank when gross loans are unavailable. Historical ratios are reported/derived rows only.','',
  '## FY2030 estimated scenarios','', '| Bank | PAT base | PAT downside | PAT upside | CAR proxy base % | CAR proxy downside % | CAR proxy upside % |','|---|---:|---:|---:|---:|---:|---:|',
  ...rows.map(r=>'| '+[r.bank,fmt(r.pat_base_2030_m),fmt(r.pat_downside_2030_m),fmt(r.pat_upside_2030_m),fmt(r.car_base_2030_proxy_pct,4),fmt(r.car_downside_2030_proxy_pct,4),fmt(r.car_upside_2030_proxy_pct,4)].join(' | ')+' |'),
  '', 'Scenario values are estimates, not actual regulatory compliance or investment recommendations. Bank-specific capital proxies differ; below-minimum and negative outcomes are retained. Scenario ordering need not be monotonic. No estimated historical rows are used, no unavailable values filled.','',
  '## Reproducibility','', 'Run the current compare.mjs against a clean LF checkout of the pinned source: `node compare.mjs --input-root PATH --output PATH/comparison.csv --report PATH/README.md`. Keep outputs outside the input checkout until both are generated. Package/macro fingerprints, reviewer and exact source commit are in the CSV. Prior independent Codex review applies to the previous snapshot; seek re-review of this label revision.',''];
 fs.writeFileSync(path.resolve(options['--report']),md.join('\n'));
}
console.log(JSON.stringify({source_commit:sha,accepted:rows.length,roster:state.tasks.length,excluded:state.tasks.filter(t=>t.acceptance!=='accepted').map(t=>({slug:t.slug,stage:t.reviewStage})),totals:Object.fromEntries(['assets_2025_m','customer_deposits_2025_m','pat_2025_m'].map(k=>[k,{total:rows.reduce((a,r)=>a+(r[k]??0),0),n:rows.filter(r=>r[k]!=null).length}]))},null,2));
