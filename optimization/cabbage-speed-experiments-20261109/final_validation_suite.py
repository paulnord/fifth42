import hashlib,json,subprocess,sys,time
from pathlib import Path
r=Path(__file__).resolve().parent;rows=[]
commands=[
 [sys.executable,str(r/'validate.py'),'native'],
 [sys.executable,str(r/'validate_candidate.py')],
 [sys.executable,str(r/'validate_widths.py')],
 [sys.executable,str(r/'audit_differences.py')],
 [sys.executable,'-m','unittest','discover','-s',str(r/'source/lattice_gpu/tests'),'-p','test_exact_host_opt.py','-v'],
 [sys.executable,'-m','unittest','discover','-s',str(r/'source/lattice_gpu/tests'),'-p','test_exact_root_opt.py','-v'],
 [sys.executable,'-m','unittest','discover','-s',str(r/'source/lattice_gpu/tests'),'-p','test_coordinator_pipeline.py','-v']]
for command in commands:
 p=subprocess.run(command,capture_output=True,text=True,timeout=180);row=dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr);rows.append(row)
 (r/'results/final-validation-suite.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(' '.join(command[1:]),p.returncode,p.stdout[-1000:],p.stderr[-1000:],flush=True)
 if p.returncode:raise RuntimeError('Final validation failed')
from validate import response,norm
import host_probe as h
packets=json.loads((r/'validation-packets.json').read_text());parity=[]
for name in ['scaling_gpu-rebuilt','gmp_reference-rebuilt']:
 if name.startswith('scaling'):
  with h.open_session(r/'bin'/name,'gpu',time.monotonic()+120) as session:
   for item in packets:assert norm(response(session,item['packet']))==item['expected'],(name,item['label'])
 else:
  for item in packets:
   p=subprocess.run([str(r/'bin'/name)],input=item['packet'],capture_output=True,text=True,check=True,timeout=30)
   assert norm(json.loads(p.stdout))==item['expected'],(name,item['label'])
 parity.append(dict(binary=name,packets=len(packets),exact_match=True,sha256=hashlib.sha256((r/'bin'/name).read_bytes()).hexdigest()))
(r/'results/rebuild-parity.json').write_text(json.dumps(parity,indent=2)+'\n')
print('Rebuilt baseline and GMP binaries match all packets',flush=True)
