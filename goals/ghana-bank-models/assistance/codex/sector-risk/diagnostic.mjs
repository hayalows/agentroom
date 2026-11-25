// Pinned, read-only scenario concentration diagnostic. This is not an acceptance gate.
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
export const pin='67ff7c9a32bc6ab7f49b9904ccbc0ce0fccb5d6e';
export const ordinary=['access-bank-ghana','bank-of-africa-ghana','calbank','consolidated-bank-ghana','ecobank-ghana','fbnbank-ghana','fidelity-bank-ghana','first-atlantic-bank','first-national-bank-ghana','gcb','gtbank-ghana','nib','republic-bank-ghana','societe-generale-ghana','stanbic-bank-ghana','standard-chartered-ghana','uba-ghana','zenith-bank-ghana'];
export const pending=['absa-ghana','adb'];
export const conditional=['omnibsic-bank','prudential-bank','umb'];
export const scenarios=['base','downside','upside'];
export const years=[2026,2027,2028,2029,2030];
export function csv(text){
 let rows=[],row=[],v='',q=false;for(let i=0;i<text.length;i++){const c=text[i];if(q){if(c==='"'&&text[i+1]==='"'){v+='"';i++}else if(c==='"')q=false;else v+=c}else if(c==='"'&&!v)q=true;else if(c===','){row.push(v);v=''}else if(c==='\n'){row.push(v.replace(/\r$/,''));rows.push(row);row=[];v=''}else v+=c;}
 if(q)throw Error('unterminated quote');if(v||row.length){row.push(v.replace(/\r$/,''));rows.push(row)}
 const head=rows.shift().map(x=>x.replace(/^\uFEFF/,''));if(new Set(head).size!==head.length)throw Error('duplicate headers');
 return rows.filter(a=>a.some(Boolean)).map(a=>{if(a.length!==head.length)throw Error('row width');return Object.fromEntries(head.map((k,i)=>[k,a[i]]))});
}
export function extract(slug,text,blob=''){
 const rows=csv(text), groups=new Map(), keys=new Set();
 for(const r of rows){
  if(r.bank!==slug||!scenarios.includes(r.scenario)||!years.map(y=>'FY'+y+'E').includes(r.period)||!['estimated','unavailable'].includes(r.status))throw Error(slug+' row metadata');
  const k=[r.scenario,r.period,r.statement,r.line_item].join('|');if(keys.has(k))throw Error(slug+' duplicate '+k);keys.add(k);
  if(r.status==='unavailable'?r.value.trim()!=='':r.value.trim()===''||!Number.isFinite(Number(r.value)))throw Error(slug+' invalid value');
  const g=r.scenario+'|'+r.period;if(!groups.has(g))groups.set(g,new Map());if(groups.get(g).has(r.line_item))throw Error(slug+' ambiguous key '+r.line_item);
  groups.get(g).set(r.line_item,r);
 }
 const data=[];
 for(const scenario of scenarios)for(const y of years){
  const period='FY'+y+'E',g=groups.get(scenario+'|'+period);if(!g)throw Error(slug+' missing '+scenario+period);
  const val=(k,required=false)=>{const r=g.get(k);if(!r||r.status==='unavailable'){if(required)throw Error(slug+' missing '+k);return null}return Number(r.value)};
  const pat=val('profit_after_tax',true),assets=val('total_assets',true),equity=val('total_equity',true),liabilities=val('total_liabilities',true);
  if(Math.abs(assets-equity-liabilities)>.0051)throw Error(slug+' balance mismatch');
  const c=val('car_pct'),x=val('x_car_proxy_pct');if(c!==null&&x!==null&&Math.abs(c-x)>.00011)throw Error(slug+' competing CAR proxies');
  const car=c??x,car_key=c!==null?'car_pct':x!==null?'x_car_proxy_pct':'unavailable';
  data.push({scenario,year:y,pat,assets,equity,car,car_key});
 }
 return {slug,blob,rows:rows.length,data};
}
export function summarize(packages){
 const expected=[...ordinary,...pending,...conditional],map=new Map(packages.map(x=>[x.slug,x]));
 if(map.size!==expected.length||!expected.every(x=>map.has(x)))throw Error('incomplete roster');
 const get=(b,s,y)=>map.get(b).data.find(x=>x.scenario===s&&x.year===y),sum=(a,k)=>a.reduce((s,x)=>s+x[k],0);
 const annual=years.map(y=>{const base=ordinary.map(b=>get(b,'base',y)),down=ordinary.map(b=>get(b,'downside',y)),up=ordinary.map(b=>get(b,'upside',y));return {year:y,base:sum(base,'pat'),down:sum(down,'pat'),up:sum(up,'pat'),delta:sum(base,'pat')-sum(down,'pat'),down_losses:down.filter(x=>x.pat<0).length,down_negative_equity:down.filter(x=>x.equity<0).length,down_car_coverage:down.filter(x=>x.car!==null).length,down_car_lt13:down.filter(x=>x.car!==null&&x.car<13).length,down_assets:sum(down,'assets'),down_lt13_assets:sum(down.filter(x=>x.car!==null&&x.car<13),'assets')}});
 const bank=ordinary.map(b=>{const a=get(b,'base',2030),d=get(b,'downside',2030),u=get(b,'upside',2030);let cum=0,loss=0,carUnder=0,carCoverage=0,firstLoss=null,firstCar=null;for(const y of years){const x=get(b,'downside',y);cum+=get(b,'base',y).pat-x.pat;if(x.pat<0){loss++;firstLoss??=y}if(x.car!==null){carCoverage++;if(x.car<13){carUnder++;firstCar??=y}}}return {bank:b,base:a.pat,down:d.pat,up:u.pat,delta:a.pat-d.pat,cumulative_delta:cum,down_car:d.car,down_equity:d.equity,down_assets:d.assets,loss_years:loss,first_loss:firstLoss,car_under_years:carUnder,car_coverage:carCoverage,first_car_under:firstCar,car_key:d.car_key}});
 bank.sort((a,b)=>b.delta-a.delta||a.bank.localeCompare(b.bank));
 const sumDelta=bank.reduce((s,x)=>s+x.delta,0),top3=bank.slice(0,3).reduce((s,x)=>s+x.delta,0);
 const nonMonotonic=[];for(const b of ordinary)for(const y of years){const a=get(b,'base',y),d=get(b,'downside',y),u=get(b,'upside',y);if(d.pat>a.pat+.001||u.pat<a.pat-.001)nonMonotonic.push({bank:b,year:y,base:a.pat,down:d.pat,up:u.pat})}
 const excluded=[...pending,...conditional].map(b=>({bank:b,group:pending.includes(b)?'pending ordinary review':'conditional source gap',base:get(b,'base',2030).pat,down:get(b,'downside',2030).pat,up:get(b,'upside',2030).pat,down_car:get(b,'downside',2030).car,down_equity:get(b,'downside',2030).equity}));
 return {pin,ordinary_count:ordinary.length,package_count:map.size,rows:packages.reduce((s,x)=>s+x.rows,0),scenario_years:packages.length*15,annual,bank,top3_share_pct:sumDelta>0?100*top3/sumDelta:null,nonMonotonic,excluded};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname.replace(/^\/(?:([A-Za-z]:))/, '$1'))){
 const files=[...ordinary,...pending,...conditional].map(slug=>{const file='goals/ghana-bank-models/banks/'+slug+'/forecast.csv';const blob=execFileSync('git',['rev-parse',pin+':'+file],{encoding:'utf8'}).trim();return extract(slug,execFileSync('git',['show',pin+':'+file],{encoding:'utf8',maxBuffer:8*1024*1024}),blob)});
 const report=summarize(files);console.log(JSON.stringify(report,null,2));
}
