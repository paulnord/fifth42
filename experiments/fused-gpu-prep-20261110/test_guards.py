import struct,sys,subprocess
from pathlib import Path
binary=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]);out.mkdir(exist_ok=False)
base=[100000000001,200000000000,9,45,112500000010,42,88]
bad={'empty':b'','zero':struct.pack('<I',0),'truncated':struct.pack('<I',1)}
for name,i,value in [('negative_domain',0,0),('bad_right',3,base[4]),('bad_cap',5,43),('bad_bits',6,223),('too_wide',4,2**40+1)]:
 p=base.copy();p[i]=value;bad[name]=struct.pack('<I6QI',1,*p)
bad['singular']=struct.pack('<I6QI',1,1,2,1,9,10,42,88)
bad['trailing']=struct.pack('<I6QI',1,*base)+b'x'
for name,data in bad.items():
 f=out/(name+'.bin');f.write_bytes(data);result=out/(name+'.out');p=subprocess.run([str(binary),str(f),str(result)],capture_output=True,text=True);assert p.returncode and not result.exists(),(name,p.stderr);(out/(name+'.log')).write_text(p.stderr)
print(f'{len(bad)} compiled host malformed-input checks passed')
