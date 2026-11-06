import json,collections,math
from pathlib import Path

def measure(m):
 h=collections.Counter(pow(i,5,m) for i in range(m)); ts={42%m,(-42)%m}; count=[0]*m
 for a,na in h.items():
  for b,nb in h.items():count[(a+b)%m]+=na*nb
 counts={t:sum(n*count[(c+t)%m] for c,n in h.items()) for t in ts}
 c_viable={t:sum(n for c,n in h.items() if count[(c+t)%m]>0) for t in ts}
 return {'modulus':m,'fifth_residue_count':len(h),'plus42_triples':counts[42%m],'either42_triples':sum(counts.values()),'plus42_density':counts[42%m]/m**3,'either42_density':sum(counts.values())/m**3,'c_residues_with_plus42_completion':c_viable[42%m]}

def prime(p):return p>1 and all(p%d for d in range(2,math.isqrt(p)+1))
mods=[2,3,4,5,7,8,9,11,16,25,27,32,49,64,121,125,128,243,625,961,1024,3125,3721]
mods+= [p for p in range(13,252) if prime(p)]
out=[measure(m) for m in sorted(set(mods))]
for d in out: print(d)
(p:=Path(__file__).parent/'densities.json').write_text(json.dumps(out,indent=2))
for qs in [[25,31,61],[11,25,31,61],[11,25,31,61,16],[11,25,31,61,16,9,49]]:
 # Same target across coprime moduli, two signs unless whole CRT target collisions.
 ds={d['modulus']:d for d in out}; single=math.prod(ds[m]['plus42_density'] for m in qs)
 relaxed=math.prod(ds[m]['either42_density'] for m in qs)
 print('CRT',qs,{'single':single,'coherent_either':2*single,'relaxed_either':relaxed,'relaxed/coherent':relaxed/(2*single)})
print('forbidden factor primes <=1000',[p for p in range(2,1001) if prime(p) and p%5==1 and pow(42,(p-1)//5,p)!=1 and 42%p])
