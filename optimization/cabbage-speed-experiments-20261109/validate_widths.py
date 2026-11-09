import json,time
from fractions import Fraction
from validate import oracle,reference,response,norm
import host_probe as h
r=h.ROOT;core=h.core;h.initialize(h.SOURCE,(),'combined');rows=[];expected={x for x in oracle(34,384) if x[2]>=16 and Fraction(3,4)*x[2]<=x[0]<=Fraction(4,5)*x[2]}
assert expected
with h.open_session(r/'bin/scaling_gpu','gpu',time.monotonic()+180) as session:
 for count in [1,2,4,8,16]:
    specs=[];tasks=[];tokens=[]
    for i in range(count):
        left=Fraction(3,4)+Fraction(i,20*count);right=Fraction(3,4)+Fraction(i+1,20*count)
        spec=(i,16,34,left.as_integer_ratio(),right.as_integer_ratio(),384,48)
        task=core.prepare_task(spec);token=core.certify_task(task);specs.append(spec);tasks.append(task);tokens.append(token)
    plan=h.packing_opt.assemble(34,384,specs,(),tasks,tokens);hits=set()
    for batch in plan.batches:
        x=response(session,batch.packet);g=reference(batch.packet);assert norm(x)==norm(g)
        hits|=core.decode_batch(batch,x,'gpu')
    assert hits==expected,(count,hits,expected)
    rows.append(dict(partitions=count,points=plan.points,hits=sorted(hits),complete_exact_region=True,independent_gmp=True))
(r/'results/width-validation.json').write_text(json.dumps(dict(status='passed',rows=rows),indent=2)+'\n')
print('All five nested partitions preserve nonempty exact hits',flush=True)
