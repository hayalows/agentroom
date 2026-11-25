#!/usr/bin/env node
// Opt-in, bounded command adapter host. No model calls by default.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawn,spawnSync} from 'node:child_process';
import {readState,read,slugOK,hash} from './room-state.mjs';
import {validAgent} from './participants.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const args=process.argv.slice(2),arg=k=>{const i=args.indexOf(k);return i<0?null:args[i+1]};
const execute=args.includes('--execute');
const goal=arg('--goal')||read(path.join(root,'ACTIVE_GOAL')).trim();
if(!slugOK(goal))throw Error('invalid goal');
const cfgPath=arg('--config');
const cfg=cfgPath?JSON.parse(fs.readFileSync(cfgPath,'utf8')):{workers:[]};
const bounded=(v,min,max,def)=>{if(v===undefined)return def;if(!Number.isInteger(v)||v<min||v>max)throw Error('limit out of range');return v;};
const maxTurns=bounded(cfg.maxTurns,1,100,12), maxMinutes=bounded(cfg.maxMinutes,1,480,60), timeout=bounded(cfg.turnTimeoutMinutes,1,120,15), poll=bounded(cfg.pollSeconds,5,600,30), parallel=bounded(cfg.parallel,1,8,3);
const workers=cfg.workers||[];
if(!Array.isArray(workers)||new Set(workers.map(w=>w.id)).size!==workers.length)throw Error('unique workers required');
for(const w of workers)if(!validAgent(w.id)||!Array.isArray(w.argv)||!w.argv.length||w.argv.some(x=>typeof x!=='string')||w.argv.filter(x=>x==='{prompt}').length!==1||!path.isAbsolute(w.cwd||''))throw Error('worker needs ID, argv with one {prompt} argument, absolute cwd');
const prompt=(id,s)=>'Resume as '+id+' in online hayalows/agentroom, goal '+goal+'. Read latest AGENTS.md, PROTOCOL-V2.md and all goal state. Do not overwrite another agent. Suggested queue (advisory, recheck): '+JSON.stringify(s.actionable[id]||{})+'. Act on messages, repair, review, continue or claim useful work. Push a checkpoint and continue within authorized session limits. Never treat one bank as the whole goal.';
if(!execute){const s=readState(root,goal);console.log(JSON.stringify({mode:'dry-run',goal,limits:{maxTurns,maxMinutes,timeout,poll,parallel},workers:workers.map(w=>({id:w.id,prompt:prompt(w.id,s)})),actionable:s.actionable},null,2));process.exit(0);}
if(!cfgPath||cfg.authorized!==true||!workers.length)throw Error('Execution requires explicit authorized=true config and workers');
if(!cfg.stateDir||!path.isAbsolute(cfg.stateDir)||path.resolve(cfg.stateDir).startsWith(root+path.sep)||path.resolve(cfg.stateDir)===root)throw Error('stateDir must be outside the supervisor checkout');
for(const w of workers)if(path.resolve(w.cwd)===root||path.resolve(w.cwd).startsWith(root+path.sep))throw Error('worker cwd must not be supervisor checkout');
const git=(...a)=>{const r=spawnSync('git',['-C',root,...a],{encoding:'utf8',timeout:60000});if(r.status!==0)throw Error('git '+a[0]+' failed: '+String(r.stderr).slice(0,300));return r.stdout.trim();};
fs.mkdirSync(cfg.stateDir,{recursive:true});const lock=path.join(cfg.stateDir,'room.lock');
fs.writeFileSync(lock,String(process.pid),{flag:'wx'});const log=path.join(cfg.stateDir,'runs.jsonl');
let stopping=false,children=new Set();
const record=(event,data)=>fs.appendFileSync(log,JSON.stringify({at:new Date().toISOString(),goal,event,...data})+'\n');
const stop=()=>{stopping=true;for(const c of children)c.kill('SIGTERM');};
process.on('SIGINT',stop);process.on('SIGTERM',stop);
const run=(w,p,ms)=>new Promise(resolve=>{
  const started=Date.now();let timedOut=false,settled=false;
  const c=spawn(w.argv[0],w.argv.slice(1).map(a=>a==='{prompt}'?p:a),{cwd:w.cwd,shell:false,stdio:['ignore','ignore','ignore']});
  children.add(c);
  const timer=setTimeout(()=>{timedOut=true;c.kill('SIGTERM');setTimeout(()=>{if(children.has(c))c.kill('SIGKILL');},5000).unref();},ms);
  const finish=(code,error)=>{if(settled)return;settled=true;clearTimeout(timer);children.delete(c);record('turn-finished',{id:w.id,code,error,timedOut,elapsedMs:Date.now()-started});resolve({id:w.id,ok:code===0&&!timedOut&&!error});};
  c.on('error',e=>finish(null,e.code||'spawn-error'));c.on('close',code=>finish(code,null));
});
const seen=new Map(),failures=new Map(),dispatches=new Map();let turns=0,idle=0;
const deadline=Date.now()+maxMinutes*60000;
try{
  if(git('status','--porcelain'))throw Error('Use a clean dedicated supervisor checkout');
  if(git('branch','--show-current')!=='main')throw Error('Supervisor checkout must be on main');
  record('run-started',{workers:workers.map(w=>w.id),maxTurns,maxMinutes});
  while(!stopping&&turns<maxTurns&&Date.now()<deadline){
    git('pull','--ff-only','origin','main');
    const s=readState(root,goal);
    if(s.goalClaimComplete){record('goal-claims-complete',{note:'stop for independent evidence and lead confirmation'});break;}
    const signature=w=>hash(JSON.stringify({last:s.agents.find(a=>a.id===w.id)?.last,queue:s.actionable[w.id],messages:s.pending.filter(m=>m.to===w.id)}));
    const runnable=workers.filter(w=>s.actionable[w.id]&&s.actionable[w.id].next!=='wait-or-report-blocker'&&(failures.get(w.id)||0)<2&&seen.get(w.id)!==signature(w)).sort((a,b)=>(dispatches.get(a.id)||0)-(dispatches.get(b.id)||0));
    if(!runnable.length){idle++;record('idle',{note:'No fresh eligible checkpoint; do not relaunch unchanged or blocked sessions',idle});if(idle>=3)break;await new Promise(r=>setTimeout(r,Math.min(poll*1000,Math.max(0,deadline-Date.now()))));continue;}
    idle=0;
    const batch=runnable.slice(0,Math.min(parallel,maxTurns-turns));
    for(const w of batch){seen.set(w.id,signature(w));dispatches.set(w.id,(dispatches.get(w.id)||0)+1);turns++;record('turn-started',{id:w.id,turn:turns});}
    const results=await Promise.all(batch.map(w=>run(w,prompt(w.id,s),Math.min(timeout*60000,Math.max(1000,deadline-Date.now())))));
    for(const r of results)failures.set(r.id,r.ok?0:(failures.get(r.id)||0)+1);
    if(!stopping&&Date.now()<deadline&&turns<maxTurns)await new Promise(r=>setTimeout(r,Math.min(poll*1000,Math.max(0,deadline-Date.now()))));
  }
}finally{stop();record('run-stopped',{turns});fs.unlinkSync(lock);}
