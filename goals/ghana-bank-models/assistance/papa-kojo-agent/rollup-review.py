"""Independent manifest and diagnostic review against a pinned clean input.
Usage: python -I rollup-review.py REPO_ROOT OUTPUT_DIR GENERATOR_PATH
Only writes scratch copies for fault injection.
"""
import csv,json,hashlib,subprocess,sys,tempfile,shutil
from pathlib import Path
from decimal import Decimal as D
root,out,generator=map(lambda x:Path(x).resolve(),sys.argv[1:4])
goal=root/"goals/ghana-bank-models"
m=json.loads((out/"manifest.json").read_text(encoding="utf-8"))
def run(*args,**kw):
    return subprocess.run(args,cwd=root,capture_output=True,text=True,**kw)
sha=run("git","rev-parse","HEAD",check=True).stdout.strip()
assert sha==m["sourceCommit"],(sha,m["sourceCommit"])
assert not run("git","status","--porcelain",check=True).stdout.strip()
state=json.loads(run("node","scripts/supervisor.mjs","--json",check=True).stdout)
accepted={t["slug"]:t for t in state["tasks"] if t["acceptance"]=="accepted"}
excluded={t["slug"]:t for t in state["tasks"] if t["acceptance"]!="accepted"}
assert len(accepted)+len(excluded)==23
assert m["accepted"]==len(accepted) and m["excluded"]==len(excluded) and m["roster"]==23
assert {r["bank"]:r for r in m["acceptedEvidence"]}=={b:dict(bank=b,**t["completionEvidence"]) for b,t in accepted.items()}
ex=[dict(bank=b,owner=t.get("owner"),status=t.get("status"),stage=t.get("reviewStage"),packageFingerprint=t.get("gate",{}).get("fingerprint"),macroFingerprint=t.get("gate",{}).get("macroFingerprint")) for b,t in excluded.items()]
assert sorted(m["exclusions"],key=lambda r:r["bank"])==sorted(ex,key=lambda r:r["bank"])
def hash(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert hash(generator)==m["generatorSha256"]
assert hash(goal/"sector/macro-assumptions/sector-context.csv")==m["sectorContextSha256"]
for b in excluded:
    for f in ("financials.csv","forecast.csv"):
        p=goal/"banks"/b/f
        assert m["diagnosticInputs"][b][f]==(hash(p) if p.exists() else None)
def read(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
rows=read(out/"rollup.csv")
keys=[tuple(r[k] for k in ("table","period_or_scenario","item","bank")) for r in rows]
assert len(keys)==len(set(keys))==8+42+8*len(accepted)+3+45
assert set(r["bank"] for r in rows)==set(accepted)|{"ACCEPTED_ONLY"}
# Check all excluded diagnostics against exact bank inputs, not merely their counts.
expected={}
for b,t in excluded.items():
    for f,history,periods,items in [
        ("financials.csv",True,["FY2025","9M-2026"],["total_assets","customer_deposits","profit_after_tax"]),
        ("forecast.csv",False,[s+"|"+y for s in ("base","downside","upside") for y in ("FY2026E","FY2030E")],["total_assets","profit_after_tax","total_equity"])]:
        p=goal/"banks"/b/f
        src={}
        if p.exists():
            for r in read(p):
                if r["value"] and (r["status"] in ("reported","derived") if history else r["status"]!="unavailable"):
                    key=(r["period"] if history else r["scenario"]+"|"+r["period"],r["line_item"])
                    assert key not in src,key
                    src[key]=D(r["value"])
        for per in periods:
            for item in items:
                expected[b,per,item]=src.get((per,item))
diagnostics=read(out/"provisional.csv")
assert len(diagnostics)==len(expected)
seen=set()
for r in diagnostics:
    k=(r["bank"],r["period_or_scenario"],r["item"])
    assert k not in seen and k in expected,k
    seen.add(k);v=expected[k]
    assert (r["value"]=="" if v is None else r["value"]!="" and abs(D(r["value"])-v)<=D(".000501")),k
    assert r["source_commit"]==sha
    assert r["review_stage"]==excluded[k[0]]["reviewStage"]
    assert r["claim_status"]==excluded[k[0]]["status"]
    assert r["classification"]==("unaccepted historical observation" if "|" not in k[1] else "unaccepted scenario estimate")
for f,h in m["outputHashes"].items():assert hash(out/f)==h,f
print("PASS exact manifest evidence",len(accepted),"accepted,",len(excluded),"excluded;",len(keys),"unique aggregate cells;",len(seen),"diagnostic values/statuses")
# Probe the advertised freshness check using copied outputs only.
with tempfile.TemporaryDirectory() as td:
    copy=Path(td)/"outputs";shutil.copytree(out,copy)
    mf=copy/"manifest.json"
    original=json.loads(mf.read_text())
    for label,mutate in [
        ("untouched",lambda x:None),
        ("reviewer metadata tampered",lambda x:x["acceptedEvidence"][0].update(reviewer="synthetic-fault-injection")),
        ("package evidence tampered",lambda x:x["acceptedEvidence"][0].update(packageFingerprint="0"*64)),
        ("totals tampered",lambda x:x["totals"].update(total_assets={"value":0})),
        ("input fingerprint tampered",lambda x:x.update(inputFingerprint="0"*64))]:
        x=json.loads(json.dumps(original));mutate(x);mf.write_text(json.dumps(x),encoding="utf-8")
        proc=run("node",str(generator),"--input-root",str(root),"--output-dir",str(copy),"--check")
        print("CHECK",label,"exit",proc.returncode)
