"""Exercise real CUDA executable host parser; invalid inputs must fail before GPU use."""
import argparse,json,struct,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('binary');p.add_argument('output');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
def packet(n,d,b):return struct.pack('<II',1,b)+n.to_bytes(256,'little')+d.to_bytes(256,'little')
good=packet(1,2,88)
cases={'overwidth':packet(1,(1<<2000)+1,222),'outside-unit':packet(2,1,88),'den-zero':packet(1,0,88),'bits-zero':packet(1,2,0),'bits-large':packet(1,2,223),'truncated':good[:-1],'trailing':good+b'x','count-zero':struct.pack('<I',0)}
rows=[]
for name,data in cases.items():
 src=out/(name+'.bin');dest=out/(name+'.out');src.write_bytes(data)
 if dest.exists():raise SystemExit('Use a fresh guard output directory')
 r=subprocess.run([str(Path(a.binary).resolve()),str(src),str(dest),'1'],capture_output=True,text=True)
 assert r.returncode!=0 and not dest.exists(),name
 assert 'cudaSetDevice' not in r.stderr,'reached GPU before rejecting invalid input'
 rows.append(dict(case=name,returncode=r.returncode,stderr=r.stderr))
(out/'RESULTS.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS:',len(rows),'host rejection cases')
