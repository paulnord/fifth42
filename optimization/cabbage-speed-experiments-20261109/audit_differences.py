import json,random,subprocess
from pathlib import Path
r=Path(__file__).resolve().parent;rng=random.Random(20261109);cases=[]
for i in range(512):
    limits=[0,1,2**31,200000000000,2**63-1]
    values=[rng.randint(-limits[i%len(limits)],limits[i%len(limits)]) for _ in range(6)]
    cases.append((*values,rng.choice([1,32,251,2**32+1]),rng.randrange(1,80),rng.choice([0,1,42,125,2**63-1])))
text=''.join(' '.join(map(str,x))+'\n' for x in cases)
rows=[]
for binary in ['audit','audit_ubsan']:
    p=subprocess.run([str(r/'bin'/binary)],input=text,text=True,capture_output=True,check=True,timeout=20)
    got=[tuple(map(int,line.split())) for line in p.stdout.splitlines()];expected=[]
    for c,a,b,uc,ua,ub,stride,steps,cap in cases:
        for k in range(steps):
            value=(pow(a+k*stride*ua,5)+pow(b+k*stride*ub,5)-pow(c+k*stride*uc,5))%(2**64)
            expected.append((value,int((value+cap)%(2**64)<=2*cap)))
    assert got==expected,(binary,'Big-integer recurrence mismatch')
    rows.append(dict(binary=binary,cases=len(cases),steps=len(got),exact_bigint_match=True,stderr=p.stderr))
(r/'results/difference-audit.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows),flush=True)
