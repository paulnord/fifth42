import random, subprocess, pathlib
p=pathlib.Path(__file__).parent
rng=random.Random(20261106)
M=(1<<64)-1
rows=[]
triples=[(13,16,17),(26,32,34),(2,2,4),(42,71,72),(8192,8192,16384),(1,1,2),(1,199999999999,200000000000),(199999999999,199999999999,200000000000)]
for i in range(100000):
 c=rng.randrange(2,200000000001 if i%2 else 10000)
 a,b=sorted((rng.randrange(1,c),rng.randrange(1,c)))
 triples.append((a,b,c))
for a,b,c in triples:
 r=a**5+b**5-c**5
 assert -(1<<191)<=r<(1<<191)
 rows.append(f'{a} {b} {c} {r&M} {(r>>64)&M} {(r>>128)&M} {int(abs(r)<=42)}\n')
q=subprocess.run([str(p/'audit')],input=''.join(rows),text=True,capture_output=True,check=True)
print(q.stdout,end='');(p/'audit.json').write_text(q.stdout)
