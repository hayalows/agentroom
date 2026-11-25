import {readState,peerReviewsFor,hash} from './room-state.mjs';
import {gateBank} from './bank-gate.mjs';

export const MAX_ACTIVE=6;
export const MAX_SUBMITTED=6;
export const MAX_OPEN=6;
const submitted=t=>['needs-review','done','changes-requested'].includes(t.status);
const blocker=v=>['CHANGES','BLOCK'].includes(v);

// All acceptance states are computed, not claims written by the monitor.
export function assessBank(t,reviews,registered,context={}){
  if(!t.owner||!submitted(t)||!t.gate){t.acceptance='not-submitted';t.reviewStage=t.status;return t;}
  const peers=peerReviewsFor(reviews,t).filter(r=>registered.has(r.reviewer));
  t.peerReviews=peers.map(r=>({
    file:r.file,reviewer:r.reviewer,verdict:r.verdict,rounds:r.rounds,
    bound:!!t.gate.fingerprint&&!!t.gate.macroFingerprint&&r.packageFingerprint===t.gate.fingerprint&&r.macroFingerprint===t.gate.macroFingerprint,
    reviewHash:hash(r.text)
  }));
  // A paused reviewer is not silently erased. A resolution is a version-bound
  // record backed by TWO distinct independent current PASS reviews, plus the
  // exact prior blocking review hash and explicit finding-by-finding evidence.
  const paused=context.availability?.paused||{},record=context.reviewResolutions?.[t.slug];
  const resolved=[];
  if(record?.schema===1&&record.packageFingerprint===t.gate.fingerprint&&record.macroFingerprint===t.gate.macroFingerprint&&Array.isArray(record.resolutions)){
    for(const x of record.resolutions){
      const b=t.peerReviews.find(r=>r.file===x.blockedReviewFile&&r.reviewHash===x.blockedReviewHash&&blocker(r.verdict));
      const p=t.peerReviews.find(r=>r.file===x.primaryReviewFile&&r.reviewHash===x.primaryReviewHash&&r.verdict==='PASS'&&r.bound);
      const v=t.peerReviews.find(r=>r.file===x.verificationReviewFile&&r.reviewHash===x.verificationReviewHash&&r.verdict==='PASS'&&r.bound);
      const date=Date.parse(x.resolvedAt),since=Date.parse(paused[b?.reviewer]?.since);
      const resumed=context.events?.some(e=>e.agent===b?.reviewer&&/^RESUME\b/i.test(e.text)&&Date.parse(e.at)>since&&Date.parse(e.at)<=date);
      const evidence=Array.isArray(x.findings)&&x.findings.length>0&&x.findings.every(f=>typeof f.finding==='string'&&f.finding.trim()&&typeof f.evidence==='string'&&f.evidence.trim());
      // Both PASS sections must explicitly attest to the prior review hash.
      const pt=peers.find(r=>r.file===p?.file)?.section||'',vt=peers.find(r=>r.file===v?.file)?.section||'';
      const ack='Resolved review SHA-256: '+x.blockedReviewHash;
      if(b&&p&&v&&p.reviewer!==v.reviewer&&p.reviewer!==b.reviewer&&v.reviewer!==b.reviewer&&Number.isFinite(date)&&Number.isFinite(since)&&date>=since&&date<=Date.parse(context.generatedAt)&&!resumed&&evidence&&pt.split(/\r?\n/).includes(ack)&&vt.split(/\r?\n/).includes(ack))resolved.push(b.file);
    }
  }
  t.resolvedReviews=[...new Set(resolved)];
  const blocking=t.peerReviews.filter(r=>blocker(r.verdict)&&!t.resolvedReviews.includes(r.file));
  const pass=t.peerReviews.find(r=>r.verdict==='PASS'&&r.bound);
  t.repairRequested=blocking.length>0;
  t.resubmitted=t.status==='needs-review'&&!!t.gate.fingerprint&&t.claim?.review_revision===t.gate.fingerprint&&t.claim?.review_macro===t.gate.macroFingerprint;
  t.acceptance='not-accepted';
  if(t.gate.status!=='core-checks-pass'){t.reviewStage='core-checks-need-fix';return t;}
  if(blocking.length){
    t.reviewStage=blocking.some(r=>r.rounds>=3&&!context.agents?.find(a=>a.id===r.reviewer)?.paused)?'lead-resolution-required':t.resubmitted?'re-review-required':'repairs-required';
    return t;
  }
  if(!pass){
    t.reviewStage=t.peerReviews.some(r=>r.verdict==='PASS')?'current-version-review-required':'peer-review-required';
    return t;
  }
  t.completionEvidence={owner:t.owner,reviewer:pass.reviewer,reviewFile:pass.file,reviewSha256:pass.reviewHash,packageFingerprint:t.gate.fingerprint,macroFingerprint:t.gate.macroFingerprint,resolvedReviews:t.resolvedReviews};
  if(t.status!=='done'){t.reviewStage='owner-close-required';return t;}
  t.reviewStage='accepted';
  t.acceptance='accepted';
  return t;
}
export function prioritize(s){
  const all=[...s.tasks,...s.shared];
  const isBank=t=>s.tasks.includes(t);
  const active=t=>t.owner&&!['released','done'].includes(t.status)&&(t.status!=='needs-review'||(isBank(t)&&['repairs-required','core-checks-need-fix'].includes(t.reviewStage))||(!isBank(t)&&t.repairRequested));
  const waiting=t=>t.owner&&t.status==='needs-review'&&!active(t);
  const now=Date.parse(s.generatedAt);
  // A recently posted review-start is advisory; a subsequent verdict/check-in or age expires it.
  const inReview=new Map();
  const pausedIds=new Set(s.agents.filter(a=>a.paused).map(a=>a.id));
  for(const e of s.events){
    const m=/^REVIEW-START\s+([a-z0-9-]+)\b/i.exec(e.text);
    if(m&&!pausedIds.has(e.agent)&&now-Date.parse(e.at)<20*60000)inReview.set(m[1],{reviewer:e.agent,at:e.at});
    const end=/^REVIEW\s+([a-z0-9-]+)\b/i.exec(e.text);
    if(end&&inReview.get(end[1])?.reviewer===e.agent)inReview.delete(end[1]);
  }
  for(const a of s.agents){
    const own=all.filter(t=>t.worker===a.id);
    a.activeClaims=own.filter(active).length;
    a.awaitingReview=own.filter(waiting).length;
    a.open=a.activeClaims;
    a.accepted=s.tasks.filter(t=>t.owner===a.id&&t.acceptance==='accepted').length;
    a.totalOpen=own.filter(t=>!['done','released'].includes(t.status)).length;
  }
  const reviewable=t=>isBank(t)?['peer-review-required','current-version-review-required','re-review-required'].includes(t.reviewStage):t.status==='needs-review'&&!t.repairRequested;
  const canReview=(a,t)=>!a.paused&&t.owner&&t.owner!==a.id&&t.worker!==a.id&&!(t.priorStewards||[]).includes(a.id)&&reviewable(t)&&(!inReview.has(t.slug)||inReview.get(t.slug).reviewer===a.id)&&(
    isBank(t)?(t.reviewStage!=='re-review-required'||(t.peerReviews.some(r=>r.reviewer===a.id&&blocker(r.verdict))||t.peerReviews.some(r=>blocker(r.verdict)&&pausedIds.has(r.reviewer)&&!t.resolvedReviews?.includes(r.file))&&!t.peerReviews.some(r=>r.reviewer===a.id&&r.bound&&r.verdict==='PASS'))):!t.reviewSummary.some(r=>r.reviewer===a.id&&r.verdict==='PASS'));
  const unclaimed=all.filter(t=>['unclaimed','released'].includes(t.status)&&(!['sector-rollup','peer-comparison','qa-sweep'].includes(t.slug)||s.tasks.every(b=>b.acceptance==='accepted')));
  for(const a of s.agents){
    const own=all.filter(t=>t.worker===a.id),old=s.actionable[a.id],help=old.help;
    const repair=own.filter(t=>isBank(t)?['repairs-required','core-checks-need-fix'].includes(t.reviewStage):t.repairRequested||['changes-requested','blocked'].includes(t.status)).map(t=>t.slug);
    const close=own.filter(t=>t.reviewStage==='owner-close-required').map(t=>t.slug);
    const review=all.filter(t=>canReview(a,t)).sort((x,y)=>Number(y.reviewStage==='re-review-required')-Number(x.reviewStage==='re-review-required')||x.slug.localeCompare(y.slug)).map(t=>t.slug);
    const lead=a.id==='claude'?s.tasks.filter(t=>t.reviewStage==='lead-resolution-required').map(t=>t.slug):[];
    const ongoing=own.filter(t=>t.status==='in-progress').map(t=>t.slug);
    const slots=a.totalOpen<MAX_OPEN&&a.activeClaims<MAX_ACTIVE&&a.awaitingReview<MAX_SUBMITTED;
    // Never suggest a fresh claim when there is an existing closure, repair or useful review.
    const handoff=slots&&!a.paused?all.filter(t=>t.handoffAvailable&&t.owner!==a.id).map(t=>t.slug):[];
    const claim=slots&&!a.paused&&!repair.length&&!close.length&&!lead.length&&!help.verify.length?unclaimed.map(t=>t.slug):[];
    const next=a.paused?'paused-no-dispatch':help.verify.length?'verify-assistance':close.length?'close-reviewed-claim':repair.length?'repair':lead.length?'resolve-review-dispute':help.assist.length?'assist-peer':review.length?'review':ongoing.length?'continue':handoff.length?'accept-handoff':claim.length?'claim':'wait-or-report-blocker';
    s.actionable[a.id]={...old,repair:a.paused?[]:repair,close:a.paused?[]:close,leadResolution:a.paused?[]:lead,review,continue:a.paused?[]:ongoing,claim,handoff,next,activeClaims:a.activeClaims,awaitingReview:a.awaitingReview,activeLimit:MAX_ACTIVE,submissionLimit:MAX_SUBMITTED,totalOpenLimit:MAX_OPEN};
  }
  return s;
}
export async function evaluateRoom(root,goal,now=Date.now()){
  const s=readState(root,goal,now),registered=new Set(s.agents.map(a=>a.id));
  for(const t of s.tasks){
    if(submitted(t))t.gate=await gateBank(root,goal,t);
    assessBank(t,s.reviews,registered,s);
  }
  prioritize(s);
  s.goalReadyForLead=s.goalClaimComplete&&s.tasks.every(t=>t.acceptance==='accepted');
  s.goalComplete=s.goalReadyForLead; // ready for final sector-level lead sign-off, not a claim of financial correctness.
  return s;
}
