#!/usr/bin/env python3
"""Compare canonical modular candidates with a fresh build of the archived engine."""
import json,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from math133 import max_gap
from audit import digest,fields
def main():
    start=time.monotonic();n=hits=0;sha=digest(ROOT/'src/search.cpp');oldsha=digest(ROOT.parent/'four133-handoff/frozen/four133_4000000/search133_incremental.cpp')
    with tempfile.TemporaryDirectory() as temp:
        for B,S in ((400,42),(400,100),(400,600),(1000,42),(1000,600),(1000,1500)):
            for pattern in ('22','31'):
                if pattern=='22' and S!=42:continue
                for sign in (1,-1):
                    if pattern=='22' and sign<0:continue
                    H=max_gap(B,S,sign,pattern)
                    if not H:continue
                    for old in (0,B//2,B-1):
                        branch='22' if pattern=='22' else '31pos' if sign>0 else '31neg'
                        cmds=[[str(ROOT/'old-reference'),branch,str(B),str(old),'43','1',str(H),oldsha,str(S)],
                              [str(ROOT/'search'),pattern,str(B),str(old),'43',str(S),str(sign),'1',str(H),sha,'synthetic','1000000']]
                        outputs=[]
                        for cmd in cmds:
                            p=subprocess.run(cmd,capture_output=True,text=True,check=True)
                            outputs.append(sorted(tuple(int(fields(x)[k]) for k in ('h','a','b','c','d','distinct')) for x in p.stdout.splitlines() if x.startswith('CANDIDATE ')))
                        assert outputs[0]==outputs[1],(B,S,pattern,sign,old)
                        hits+=len(outputs[0]);n+=1
    result=dict(passed=True,configurations=n,canonical_modular_candidates=hits,source_sha256=sha,reference_source_sha256=oldsha,reference_binary_sha256=digest(ROOT/'old-reference'),seconds=time.monotonic()-start)
    (ROOT/'baseline-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
