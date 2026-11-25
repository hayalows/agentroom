import copy,json,sys,tempfile,subprocess,shutil
from pathlib import Path
root,gen,out=map(Path,sys.argv[1:4])
def check(directory):
    return subprocess.run(['node',str(gen),'--input-root',str(root),'--output-dir',str(directory),'--check'],capture_output=True,text=True)
assert check(out).returncode==0
def change(m,k,v):m[k]=v
def reviewer(m):m['acceptedEvidence'][0]['reviewer']='wrong-reviewer'
def package(m):m['acceptedEvidence'][0]['packageFingerprint']='0'*64
def totals(m):m['totals']['total_assets']['value']=0
def outputs(m):m['outputHashes']['unexpected.txt']='0'*64
tests=[('reviewer',reviewer),('package',package),('total',totals),('extra-output-key',outputs),('schema',lambda m:change(m,'schema',999)),('exclusions',lambda m:change(m,'exclusions',[])),('diagnostic-inputs',lambda m:change(m,'diagnosticInputs',{})),('timestamp',lambda m:change(m,'generatedAt','invalid')),('fingerprint',lambda m:change(m,'inputFingerprint','0'*64))]
with tempfile.TemporaryDirectory(prefix='rollup-manifest-faults-') as t:
    d=Path(t)/'output'
    for label,mutate in tests:
        if d.exists():shutil.rmtree(d)
        shutil.copytree(out,d)
        p=d/'manifest.json'
        m=json.loads(p.read_text(encoding='utf-8'))
        mutate(m);p.write_text(json.dumps(m),encoding='utf-8')
        a=check(d);assert a.returncode!=0,(label,a.stdout,a.stderr)
        print('REJECTED',label)
    shutil.rmtree(d);shutil.copytree(out,d)
    with (d/'rollup.csv').open('ab') as f:f.write(b'\n')
    assert check(d).returncode!=0
print('PASS: clean checkpoint; all 9 manifest faults and modified CSV rejected')
