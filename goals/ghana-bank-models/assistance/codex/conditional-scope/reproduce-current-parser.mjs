// Run in a pinned checkout BEFORE integration. This is a reproduction of the current defect,
// not the desired future behavior. Do not run as an ordinary approval.
import assert from 'node:assert/strict';
import {reviewDecision} from '../../../../../scripts/room-state.mjs';
import {assessBank} from '../../../../../scripts/completion.mjs';
const packageFingerprint='a'.repeat(64),macroFingerprint='b'.repeat(64);
const base='Package SHA-256 fingerprint: '+packageFingerprint+'\nMacro SHA-256 fingerprint: '+macroFingerprint+'\nScope: conditional: 9M-2026 unavailable\n';
for (const verdict of ['PASS-with-limitation','PASS']) {
 const review='Verdict: '+verdict+'\n'+base;
 const parsed=reviewDecision(review);
 const task={slug:'prudential-bank',owner:'papa-kojo-agent',worker:'papa-kojo-agent',status:'done',claim:{},gate:{status:'core-checks-pass',fingerprint:packageFingerprint,macroFingerprint},priorStewards:[]};
 const reviews=[{file:'claude-helper-1-of-papa-kojo-agent-prudential-bank.md',text:review}];
 const current=assessBank(task,reviews,new Set(['papa-kojo-agent','claude-helper-1']),{generatedAt:'2026-11-25T18:30:00Z'});
 console.log(JSON.stringify({inputVerdict:verdict,parsed:parsed.verdict,acceptance:current.acceptance,reviewStage:current.reviewStage}));
 // A passing assertion reproduces the defect. After repair, invert the expectation
 // and add cases requiring two current conditional reviews with an approved scope record.
 assert.equal(parsed.verdict,'PASS');
 assert.equal(current.acceptance,'accepted');
}
console.log('Current defect reproduced on two synthetic inputs. No live task or review changed.');
