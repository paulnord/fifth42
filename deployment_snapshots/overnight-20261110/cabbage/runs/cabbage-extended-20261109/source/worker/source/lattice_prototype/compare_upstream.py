#!/usr/bin/env python3
"""Compile/run frozen upstream CPU and GPU-row emulation; compare exact hit sets."""
import hashlib,json,pathlib,subprocess
import lattice5 as l
ROOT=pathlib.Path(__file__).resolve().parent

def canon(hits):
    return {tuple(sorted(h)) for h in hits}

def main():
    for f in json.load(open(ROOT/'vendor/SOURCES.json')):
        b=(ROOT/'vendor'/f['path']).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_blob_sha']
    for source,libs in [('search_cpu.cpp',['-lgmpxx','-lgmp']),('search_emulated.cpp',[])]:
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(ROOT/'vendor'/source),*libs,'-o',str(ROOT/'vendor'/source[:-4])],check=True)
    healy=json.load(open(ROOT/'results/healy-1000.json'))
    signed=json.load(open(ROOT/'results/signed42-1000.json'))
    assert healy['complete'] and signed['complete']
    out=[]
    for bound,target,filtered in [(100,12,'none'),(100,2951,'none'),(1000,42,'mod11'),(1000,42,'none')]:
        oracle=l.signed_reference(bound,target)
        if target==42:
            prototype=set(map(tuple,signed['signed_hits']))
        else:
            # For these positive controls all expected triples are in the published
            # near-miss band; full signed dictionary enumeration independently checks
            # there are no missing exceptions, rather than assuming a general reduction.
            prototype=set()
            for a,b,c,r in healy['hits']:
                if c<=bound and r==target: prototype.add(tuple(sorted((a,b,-c))))
                if c<=bound and r==-target: prototype.add(tuple(sorted((-a,-b,c))))
        assert prototype==oracle,(bound,target,'prototype',prototype,oracle)
        configs=[('search_cpu',[])]+[('search_emulated',['--variant',v]) for v in ['baseline','cached','pruned','highword']]
        runs=[]
        for program,extra in configs:
            cmd=[str(ROOT/'vendor'/program),'--bound',str(bound),'--target',str(target),'--filter',filtered,*extra]
            data=json.loads(subprocess.check_output(cmd,text=True))
            assert canon(data['hits'])==oracle,(cmd,data,oracle)
            data['variant']=extra[-1] if extra else 'GMP reference'
            runs.append(data)
        out.append(dict(bound=bound,target=target,filter=filtered,complete_match=True,canonical_hits=sorted(oracle),runs=runs))
    p=ROOT/'results/upstream-comparison.json';json.dump(out,open(p,'w'),indent=2)
    print('PASS: 20 upstream runs, 4 comparison cases, exact canonical hit sets agree with lattice and signed dictionary oracle.')

if __name__=='__main__': main()
