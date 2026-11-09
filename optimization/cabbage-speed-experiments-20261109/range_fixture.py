import json,time
from validate import packet,reference,response,norm
import host_probe as h
r=h.ROOT;c,a,b=24482314857,21137517920,21483066250
p=packet([1,0,0],[[c,a,b],[0,0,0],[0,0,0]],c,c,0,1)
expected=norm(reference(p));assert expected['hits']==[dict(task=0,linear=2,a=a,b=b,c=c)]
rows=[]
for binary in ['scaling_gpu','baseline','low64','rows','wheel','differences','wheel_differences']:
 with h.open_session(r/'bin'/binary,'gpu',time.monotonic()+30) as session:
  x=response(session,p);assert norm(x)==expected
  rows.append(dict(binary=binary,exact_nonempty_large_hit=True,response=x))
(r/'results/large-nonempty-fixture.json').write_text(json.dumps(dict(status='passed',rows=rows,synthetic_packet=True,production_coverage=False),indent=2)+'\n')
print('Large Healy near-miss survives all seven GPU paths',flush=True)
