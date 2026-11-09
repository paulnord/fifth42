import json,subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent;rows=[]
for variant in ['roots','inverse','combined','serializer','warm','native']:
    p=subprocess.run([sys.executable,str(r/'validate.py'),variant],capture_output=True,text=True,timeout=240)
    row=dict(variant=variant,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr);rows.append(row)
    (r/'validation-suite.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(variant,p.returncode,p.stdout.strip(),p.stderr[-1500:],flush=True)
    if p.returncode:raise RuntimeError(variant+' failed')
