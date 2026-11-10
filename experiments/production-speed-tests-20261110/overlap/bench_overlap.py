#!/usr/bin/env python3
"""TEST_ONLY persistent-engine replay, exact GMP gate and alternating repeats."""
import argparse,hashlib,json,os,selectors,statistics,subprocess,time
from pathlib import Path

def canonical(row):
    if row.get('box_complete') is not True: raise ValueError('incomplete response: '+str(row))
    return dict(points=row['points_visited'],counts=sorted((x['id'],x['expected'],x['visited']) for x in row['counts']),
                hits=sorted((x['task'],x['linear'],x['a'],x['b'],x['c']) for x in row['hits']))

class Engine:
    def __init__(self,path,capacity,timeout=60):
        self.p=subprocess.Popen([str(path),'--capacity',str(capacity)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0)
        self.timeout=timeout;self.buffer=b'';self.seq=0
        try:
            assert self.read().get('ready') is True
        except BaseException:
            self.close();raise
    def read(self):
        end=time.monotonic()+self.timeout
        with selectors.DefaultSelector() as s:
            s.register(self.p.stdout,selectors.EVENT_READ)
            while b'\n' not in self.buffer:
                remaining=end-time.monotonic()
                if remaining<=0 or not s.select(remaining):raise TimeoutError('GPU response timed out')
                part=os.read(self.p.stdout.fileno(),65536)
                if not part: raise RuntimeError('engine exited: '+self.p.stderr.read().decode(errors='replace'))
                self.buffer+=part
            line,self.buffer=self.buffer.split(b'\n',1)
            return json.loads(line)
    def run(self,payload):
        self.seq+=1;start=time.perf_counter()
        data=memoryview(('RUN %d %d\n'%(self.seq,len(payload))).encode()+payload)
        while data:
            n=self.p.stdin.write(data)
            if not n:raise BrokenPipeError('engine input closed')
            data=data[n:]
        row=self.read();assert row['request_id']==self.seq
        return row,time.perf_counter()-start
    def close(self):
        if self.p.poll() is None:
            try:self.p.stdin.write(b'QUIT\n');self.p.wait(timeout=3)
            except (BrokenPipeError,subprocess.TimeoutExpired):self.p.kill();self.p.wait()
        for f in (self.p.stdin,self.p.stdout,self.p.stderr):f.close()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('baseline','candidate','gmp','packets','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--repeats',type=int,default=7);p.add_argument('--capacity',type=int,default=65536)
    a=p.parse_args();assert 3<=a.repeats<=30 and 1<=a.capacity<=1000000
    paths=sorted(a.packets.glob('*.packet'));assert paths,'no *.packet inputs'
    a.output.mkdir(parents=True,exist_ok=False)
    engines={};rows=[];references={};packets={}
    try:
        for path in paths:
            b=path.read_bytes();assert len(b)<=16*1024*1024
            ref=subprocess.run([str(a.gmp)],input=b,capture_output=True,check=True,timeout=60)
            references[path.name]=canonical(json.loads(ref.stdout));packets[path.name]=b
        for label,path in (('baseline',a.baseline),('candidate',a.candidate)):
            engines[label]=Engine(path,a.capacity)
            for name,b in packets.items():
                row,_=engines[label].run(b);assert canonical(row)==references[name],(label,name,'warmup mismatch')
        for repeat in range(a.repeats):
            order=('baseline','candidate') if repeat%2==0 else ('candidate','baseline')
            for name,b in packets.items():
                for label in order:
                    row,wall=engines[label].run(b)
                    assert canonical(row)==references[name],(label,name,'exact mismatch')
                    rows.append(dict(repeat=repeat,variant=label,packet=name,rpc_seconds=wall,response=row))
        summary={name:{label:statistics.median(x['rpc_seconds'] for x in rows if x['variant']==label and x['packet']==name) for label in engines} for name in packets}
        result=dict(status='passed',TEST_ONLY=True,production_coverage=False,scope='precomputed packet replay, NOT whole pipeline',
           packets={n:hashlib.sha256(b).hexdigest() for n,b in packets.items()},
           executables={label:hashlib.sha256(path.read_bytes()).hexdigest() for label,path in [('baseline',a.baseline),('candidate',a.candidate),('gmp',a.gmp)]},
           medians_rpc_seconds=summary,samples=rows,
           caveat='candidate kernel_seconds sums per-stream kernel event intervals; not a critical-path wall duration')
        (a.output/'results.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(summary,indent=2))
    finally:
        for engine in engines.values():engine.close()
if __name__=='__main__':main()
