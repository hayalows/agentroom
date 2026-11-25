import fs from 'node:fs';
import path from 'node:path';
import {hash,read,slugOK} from './room-state.mjs';
import {runEvidenceWorkflow} from './vendor/evidence-workflow.mjs';
export function csv(s){
  const records=[];let row=[],v='',quoted=false;
  for(let i=0;i<s.length;i++){const c=s[i];if(quoted){if(c==='"'&&s[i+1]==='"'){v+='"';i++;}else if(c==='"')quoted=false;else v+=c;}
    else if(c==='"'&&v==='')quoted=true;else if(c===','){row.push(v);v='';}else if(c==='\n'){row.push(v.replace(/\r$/,''));records.push(row);row=[];v='';}else v+=c;}
  if(quoted)throw Error('unterminated CSV quote');
  if(row.length||v){row.push(v.replace(/\r$/,''));records.push(row);}
  const head=records.shift()||[];if(!head.length||new Set(head).size!==head.length)throw Error('missing/duplicate columns');
  return records.filter(r=>r.some(Boolean)).map(r=>{if(r.length!==head.length)throw Error('CSV row width mismatch');return Object.fromEntries(head.map((k,i)=>[k,r[i]]));});
}
const required=['README.md','sources.md','financials.csv','assumptions.json','forecast.csv','checks.md'];
const numeric=r=>r&&String(r.value).trim()!==''&&Number.isFinite(Number(r.value));
export async function gateBank(root,goal,task){
  if(!slugOK(goal)||!slugOK(task.slug))throw Error('invalid path');
  const dir=path.join(root,'goals',goal,'banks',task.slug);
  const files=required.map(f=>({name:f,text:read(path.join(dir,f))}));
  const code=['model.py','model.mjs','model.js','assumptions.md'].find(f=>read(path.join(dir,f)));
  if(code)files.push({name:code,text:read(path.join(dir,code))});
  const fingerprint=hash(JSON.stringify(files.map(f=>[f.name,hash(f.text)])));
  const ref='banks/'+task.slug+'/';
  const byName=Object.fromEntries(files.map(f=>[f.name,f.text]));
  const observations={};
  const result=(ok,detail,where)=>({score:ok?100:0,evidence:[{ref:ref+where,detail}]});
  observations.package=result(required.every(f=>byName[f])&&!!code,'Missing: '+[...required.filter(f=>!byName[f]),...(!code?['reproducible implementation/formulas']:[])].join(', '),'');
  if(!byName['financials.csv']||!byName['forecast.csv'])return {fingerprint,status:'incomplete',checks:observations,review:'not assessed'};
  try{
    const hist=csv(byName['financials.csv']), fc=csv(byName['forecast.csv']);
    const groups=new Map(),keys=new Set();let duplicates=0,bad=0;
    for(const [kind,rows] of [['history',hist],['forecast',fc]])for(const r of rows){
      const k=[kind,r.scenario||'',r.period,r.statement,r.line_item].join('|');if(keys.has(k))duplicates++;keys.add(k);
      if(r.bank!==task.slug||!r.period||!r.line_item||!r.statement||!['reported','derived','estimated','unavailable'].includes(r.status)||(r.status==='unavailable'?String(r.value).trim()!=='':!numeric(r))||(r.status==='reported'&&(!r.source_id||!r.page))||(kind==='forecast'&&!['estimated','unavailable'].includes(r.status)))bad++;
      const g=[kind,r.scenario||'',r.period].join('|');if(!groups.has(g))groups.set(g,new Map());groups.get(g).set(r.line_item,r);
    }
    const historyYears=new Set(hist.map(r=>r.period).filter(p=>/^FY\d{4}$/.test(p)));
    const expected=['base','downside','upside'].flatMap(s=>[2026,2027,2028,2029,2030].map(y=>s+'|FY'+y+'E'));
    const actual=new Set(fc.map(r=>r.scenario+'|'+r.period));
    observations.schema=result(bad===0&&duplicates===0&&historyYears.size===5&&expected.every(k=>actual.has(k))&&actual.size===15,'Rows '+hist.length+'/'+fc.length+'; bad '+bad+'; duplicate '+duplicates+'; annual periods '+historyYears.size+'; scenario-years '+actual.size,'financials.csv & forecast.csv');
    let checked=0,failed=0,missing=0;const failures=[];
    for(const [k,m] of groups){
      for(const [total,a,b,sign] of [['total_assets','total_liabilities','total_equity',1],['net_interest_income','interest_income','interest_expense',-1],['profit_after_tax','profit_before_tax','income_tax',-1]]){
        const vals=[m.get(total),m.get(a),m.get(b)];if(!vals.every(numeric)){missing++;failures.push(k+' '+total+' missing');continue;}
        const delta=Number(vals[0].value)-Number(vals[1].value)-sign*Number(vals[2].value);checked++;
        if(Math.abs(delta)>.005){failed++;failures.push(k+' '+total+' residual '+delta);}
      }
    }
    observations.arithmetic=result(checked>0&&failed===0&&missing===0,'Computed '+checked+' core bridges; failed '+failed+'; missing '+missing+'; '+failures.slice(0,8).join('; '),'financials.csv & forecast.csv');
    const macro=read(path.join(root,'goals',goal,'sector','macro-assumptions','macro.csv'));
    let a;try{a=JSON.parse(byName['assumptions.json']);}catch{}
    const linked=!!macro&&!!a&&/macro\.csv/.test(JSON.stringify(a))&&files.some(f=>f.name===code&&/macro\.csv|macro_file/.test(f.text));
    observations.macro=result(linked,'Shared macro file exists and is referenced by assumptions and implementation (link only; replay not verified).','assumptions.json');
  }catch(e){observations.schema=result(false,String(e.message),'financials.csv & forecast.csv');}
  const criteria=['package','schema','arithmetic','macro'];
  const rubric=criteria.map(id=>({id,weight:25,method:'deterministic',min:100,required:true,source:id}));
  const verifiers=Object.fromEntries(criteria.filter(id=>observations[id]).map(id=>[id,{method:'deterministic',independent:true,check:()=>observations[id]}]));
  const run=await runEvidenceWorkflow({runId:goal+'/'+task.slug+'/'+fingerprint,input:{fingerprint},worker:async input=>input,rubric,verifiers,threshold:100,maxRepairs:0});
  return {fingerprint,macroFingerprint:hash(read(path.join(root,'goals',goal,'sector','macro-assumptions','macro.csv'))),status:run.status==='completed'?'core-checks-pass':run.status,checks:observations,coverage:run.best?.review?.coverage??null,review:'Independent source checks, full reconciliation, reproducibility and regulatory review still required; no automatic acceptance.'};
}
