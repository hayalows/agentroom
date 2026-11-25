// Standalone proposed policy; not imported by the live supervisor.
// Synthetic tests; not approval of any bank or scope record.
export function classifyConditional({task,scope,reviewers,registered,coverage,readme,decisionHash,now}) {
  const result=(stage,acceptance="not-accepted",extra={})=>({stage,acceptance,...extra});
  const label="conditional: 9M-2026 unavailable";
  const hex=s=>typeof s==="string"&&/^[a-f0-9]{64}$/.test(s);
  if(task.slug!=="prudential-bank")return result("not-applicable","not-applicable");
  if(!coverage||!Array.isArray(coverage.actualPeriods)||!Array.isArray(coverage.nonblankMissingRows))return result("coverage-unverified");
  if(coverage.actualPeriods.includes("9M-2026"))return result("scope-lapsed-rebuild-and-review");
  if(coverage.nonblankMissingRows.length)return result("missing-period-has-numbers");
  if(!["FY2021","FY2022","FY2023","FY2024","FY2025"].every(p=>coverage.actualPeriods.includes(p)))return result("annual-coverage-incomplete");
  if(!scope||scope.schema!==1||scope.slug!==task.slug||scope.approvedBy!=="claude"||!registered.includes(scope.approvedBy)||scope.label!==label||scope.missingPeriod!=="9M-2026"||scope.anchor!=="FY2025"||!hex(decisionHash)||scope.decisionSha256!==decisionHash||!Number.isFinite(Date.parse(scope.approvedAt))||!Number.isFinite(Date.parse(now))||Date.parse(scope.approvedAt)>Date.parse(now))return result("scope-unapproved-or-invalid");
  if(task.gate?.status!=="core-checks-pass")return result("core-checks-need-fix");
  if(!hex(task.gate.fingerprint)||!hex(task.gate.macroFingerprint)||scope.packageFingerprint!==task.gate.fingerprint||scope.macroFingerprint!==task.gate.macroFingerprint)return result("scope-stale");
  if(!readme.includes(label)||!scope.conditions?.fy2025AuditedAnchor||!scope.conditions?.fy2026Estimated||!scope.conditions?.recapitalizationSensitivity||!scope.conditions?.separateOutputLabels)return result("scope-conditions-missing");
  if(!Array.isArray(scope.excludedReviewers)||!task.owner||!task.worker||!["needs-review","done"].includes(task.status))return result("owner-or-scope-invalid");
  const forbidden=new Set([task.owner,task.worker,...(task.priorStewards||[]),...scope.excludedReviewers]);
  const eligible=reviewers.filter(r=>registered.includes(r.reviewer)&&!forbidden.has(r.reviewer));
  if(eligible.some(r=>["CHANGES","BLOCK"].includes(r.verdict)))return result("unresolved-blocker");
  const pass=eligible.filter(r=>r.verdict==="CONDITIONAL-PASS"&&r.packageFingerprint===scope.packageFingerprint&&r.macroFingerprint===scope.macroFingerprint&&r.scopeDecisionSha256===decisionHash&&r.scopeLabel===label&&hex(r.reviewSha256));
  const distinct=[...new Map(pass.map(r=>[r.reviewer,r])).values()];
  if(distinct.length<2)return result("conditional-two-reviews-required");
  const evidence=distinct.map(r=>({reviewer:r.reviewer,reviewSha256:r.reviewSha256}));
  if(task.status!=="done")return result("conditional-owner-close-required","not-accepted",{evidence,label});
  return result("conditional-accepted","conditional-accepted",{evidence,label});
}
function selfTest(){
 const p="a".repeat(64),m="b".repeat(64),h="c".repeat(64),label="conditional: 9M-2026 unavailable";
 const make=()=>({task:{slug:"prudential-bank",owner:"papa-kojo-agent",worker:"papa-kojo-agent",status:"done",gate:{status:"core-checks-pass",fingerprint:p,macroFingerprint:m}},scope:{schema:1,slug:"prudential-bank",approvedBy:"claude",approvedAt:"2026-11-25T18:00:00Z",label,missingPeriod:"9M-2026",anchor:"FY2025",decisionSha256:h,packageFingerprint:p,macroFingerprint:m,excludedReviewers:["codex"],conditions:{fy2025AuditedAnchor:true,fy2026Estimated:true,recapitalizationSensitivity:true,separateOutputLabels:true}},reviewers:["chatgpt-support","claude-helper-1"].map((reviewer,i)=>({reviewer,verdict:"CONDITIONAL-PASS",packageFingerprint:p,macroFingerprint:m,scopeDecisionSha256:h,scopeLabel:label,reviewSha256:String(i+1).repeat(64)})),registered:["claude","papa-kojo-agent","codex","chatgpt-support","claude-helper-1"],coverage:{actualPeriods:["FY2021","FY2022","FY2023","FY2024","FY2025"],nonblankMissingRows:[]},readme:label,decisionHash:h,now:"2026-11-25T18:30:00Z"});
 const cases=[
 ["valid",x=>{},"conditional-accepted"],["owner close pending",x=>x.task.status="needs-review","conditional-owner-close-required"],["only one review",x=>x.reviewers.pop(),"conditional-two-reviews-required"],["duplicate reviewer",x=>x.reviewers[1].reviewer=x.reviewers[0].reviewer,"conditional-two-reviews-required"],["owner review",x=>x.reviewers[1].reviewer=x.task.owner,"conditional-two-reviews-required"],["source contributor",x=>x.reviewers[1].reviewer="codex","conditional-two-reviews-required"],["unregistered reviewer",x=>x.reviewers[1].reviewer="unknown","conditional-two-reviews-required"],["wrong package",x=>x.reviewers[1].packageFingerprint="d".repeat(64),"conditional-two-reviews-required"],["wrong macro",x=>x.reviewers[1].macroFingerprint="d".repeat(64),"conditional-two-reviews-required"],["wrong decision hash",x=>x.reviewers[1].scopeDecisionSha256="d".repeat(64),"conditional-two-reviews-required"],["ordinary PASS",x=>x.reviewers[1].verdict="PASS","conditional-two-reviews-required"],["legacy qualified PASS",x=>x.reviewers[1].verdict="PASS-with-limitation","conditional-two-reviews-required"],["old unresolved BLOCK",x=>x.reviewers.push({...x.reviewers[0],reviewer:"claude",verdict:"BLOCK"}),"unresolved-blocker"],["no scope",x=>x.scope=null,"scope-unapproved-or-invalid"],["future approval",x=>x.scope.approvedAt="2026-11-26T00:00:00Z","scope-unapproved-or-invalid"],["wrong authority",x=>x.scope.approvedBy="codex","scope-unapproved-or-invalid"],["scope stale",x=>x.task.gate.fingerprint="e".repeat(64),"scope-stale"],["arithmetic failed",x=>x.task.gate.status="core-checks-need-fix","core-checks-need-fix"],["missing README label",x=>x.readme="ordinary model","scope-conditions-missing"],["missing output segregation",x=>x.scope.conditions.separateOutputLabels=false,"scope-conditions-missing"],["interim recovered",x=>x.coverage.actualPeriods.push("9M-2026"),"scope-lapsed-rebuild-and-review"],["fabricated interim numeric",x=>x.coverage.nonblankMissingRows.push("total_assets"),"missing-period-has-numbers"],["annual missing",x=>x.coverage.actualPeriods.shift(),"annual-coverage-incomplete"],["wrong bank",x=>x.task.slug="umb","not-applicable"],["wrong decision bytes",x=>x.decisionHash="e".repeat(64),"scope-unapproved-or-invalid"],["unverified coverage",x=>x.coverage=null,"coverage-unverified"]];
 const results=cases.map(([name,mutate,want])=>{const x=make();mutate(x);const out=classifyConditional(x);if(out.stage!==want||out.acceptance==="accepted")throw Error(name+": "+JSON.stringify(out));return {name,stage:out.stage}});
 const fixture=[{acceptance:"accepted"},{acceptance:"conditional-accepted"},{acceptance:"not-accepted"}];
 if(fixture.filter(t=>t.acceptance==="accepted").length!==1)throw Error("ordinary isolation");
 return results;
}
console.log(JSON.stringify({pass:selfTest().length,results:selfTest()},null,2));
