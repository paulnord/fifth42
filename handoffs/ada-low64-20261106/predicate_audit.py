#!/usr/bin/env python3
"""Independent Python bigint check of the NEW proposed kernel's low64 helper."""
import argparse, hashlib, json, random, subprocess, sys
from pathlib import Path

CPP='''#include "kernel.hpp"
#include <iostream>
int main(){S64 a,b,c; std::uint64_t cap;
while(std::cin>>a>>b>>c>>cap){
 const auto u=fifth_low64(static_cast<std::uint64_t>(a))
             +fifth_low64(static_cast<std::uint64_t>(b))
             -fifth_low64(static_cast<std::uint64_t>(c));
 std::cout<<u<<' '<<residual_low64_passes(a,b,c,cap)<<'\\n';
}}
'''

def main():
    if sys.flags.optimize:raise SystemExit('Do not use Python -O')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=False);work=a.work.resolve()
    source=out/'predicate.cpp';source.write_text(CPP);binary=out/'predicate'
    cmd=['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',
         '-I',str(work/'low64/src'),str(source),'-o',str(binary)]
    compile_=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
    (out/'compile.stderr').write_text(compile_.stderr);compile_.check_returncode()
    rng=random.Random(20261106);M=1<<64;maximum=(1<<63)-1
    values=[0,1,-1,2,-2,8192,16384,2**32-1,2**32,2**32+1,200000000000,-200000000000]
    caps=[0,1,12,42,2951,maximum]
    cases=[(x,y,z,c) for x in values for y in values for z in values for c in caps]
    cases += [(rng.randint(1,200000000000),rng.randint(1,200000000000),
               rng.randint(1,200000000000),rng.choice(caps+[rng.randrange(maximum+1)])) for _ in range(50000)]
    data=''.join('%d %d %d %d\n'%row for row in cases)
    run=subprocess.run([str(binary)],input=data,capture_output=True,text=True,timeout=30);run.check_returncode()
    rows=run.stdout.splitlines();assert len(rows)==len(cases)
    for (x,y,z,c),line in zip(cases,rows):
        r=x**5+y**5-z**5;word,pred=map(int,line.split());assert word==r%M
        expected=(word<=c or word>=M-c) if c else word==0
        assert bool(pred)==expected
        if abs(r)<=c:assert pred
    summary=dict(status='passed',cases=len(cases),seed=20261106,ubsan=True,cuda_executed=False,
        scope='New candidate helper against Python integers; exact engine parity is in the separate probe',
        source_sha256=hashlib.sha256((work/'low64/src/kernel.hpp').read_bytes()).hexdigest(),
        command=cmd,stderr=run.stderr)
    (out/'report.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
