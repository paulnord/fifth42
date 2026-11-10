#!/usr/bin/env python3
"""Portable exact geometry and shared-algorithm checks. No GPU required."""
import argparse,copy,json,random,struct,subprocess,sys,tempfile
from pathlib import Path
from fractions import Fraction as Q
from reference import *
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import lattice as baseline

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--model');args=parser.parse_args()
 rng=random.Random(1701);fields=[]
 for b in (48,80,88,176,222):
  for region in (0,3_000_000_000,7_192_000_000,10_000_000_000):
   for group in (4,8,16):
    n=region+rng.randrange(100)
    fields.append((100_000_000_000,200_000_000_000,n,n+group,12_500_000_000,42,b))
 for b in (4,8,16,32):
  for i in range(32):
   D=rng.randint(20,1000);L=rng.randint(0,D//2);R=rng.randint(L+1,D*4//5)
   fields.append((100,200,L,R,D,rng.choice((0,1,42)),b))
 # Boundary allowed packet sizes and zero-left/zero-cap.
 fields.extend(((2**40,2**40,0,1,2**40,0,222),(2**40,2**40,2**39,2**39+16,2**40,42,222)))
 packets=[];largest=0
 for f in fields:
  a=from_packet(*f);values=calculate_packet(f);cert=certify_packet(f,values)
  p=baseline.make_patch(f[0],f[1],Q(f[2],f[4]),Q(f[3],f[4]),f[5],f[6])
  assert (cert['p'],cert['q'],cert['m'],cert['eps'])==(p.p,p.q,p.m,p.eps),f
  largest=max(largest,max(v.bit_length() for v in values))
  assert max(v.bit_length() for v in values)<=validate(a)
  packets.append(values)
 # Corrupt every field, root and rational term, independently.
 rejects=0
 for f,v in zip(fields[:3],packets[:3]):
  for k in range(16):
   bad=list(v);bad[k]+=1
   try:certify_packet(f,bad)
   except (ValueError,ArithmeticError,ZeroDivisionError):rejects+=1
   else:raise AssertionError(('corruption accepted',k))
 for f in ((0,200,0,1,10,42,88),(1,200,0,1,10,42,88),(100,200,0,1,10,42,223),(100,200,0,1,2**40+1,42,88),(100,200,1,1,10,42,88)):
  try:calculate_packet(f)
  except (ValueError,OverflowError):rejects+=1
  else:raise AssertionError(('invalid packet accepted',f))
 if args.model:
  with tempfile.TemporaryDirectory(prefix='fused-model-') as d:
   ip,op=Path(d)/'input.bin',Path(d)/'output.bin'
   ip.write_bytes(struct.pack('<I',len(fields))+b''.join(struct.pack('<6QI',*f) for f in fields))
   subprocess.run([str(Path(args.model).resolve()),str(ip),str(op)],check=True)
   raw=op.read_bytes();assert len(raw)==4+len(fields)*16*512
   assert struct.unpack('<I',raw[:4])[0]==len(fields)
   for i,(f,wanted) in enumerate(zip(fields,packets)):
    got=tuple(int.from_bytes(raw[4+(i*16+j)*512:4+(i*16+j+1)*512],'little') for j in range(16))
    assert got==wanted,('shared algorithm output mismatch',i,f)
    certify_packet(f,got)
 print(json.dumps({'baseline_patch_comparisons':len(fields),'corruption_or_invalid_rejections':rejects,'largest_output_bits':largest,'shared_checked_4096bit_model':'passed' if args.model else 'not run','gpu':'not run'},indent=2))
if __name__=='__main__':main()
