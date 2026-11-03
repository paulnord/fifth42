#!/usr/bin/env python3
"""CPU emulation is independently checked; GPU passes must be explicit."""
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from reference import reference,verify
from run import atomic_json,fingerprint

VARIANTS=('baseline','cached','pruned','highword')
GPU=False
REPORT={'cpu_emulation_status':'pending','gpu_status':'pending','gpu_comparisons':0}

def invoke(binary,b,target=42,filter_name='mod11',variant=None,start=None,stop=None):
    args=[str(ROOT/'bin'/binary),'--bound',str(b),'--target',str(target),'--filter',filter_name]
    if variant:args.extend(['--variant',variant])
    for key,value in (('--row-start',start),('--row-stop',stop)):
        if value is not None:args.extend([key,str(value)])
    p=subprocess.run(args,text=True,capture_output=True,timeout=15,
                     env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
    if p.returncode:raise RuntimeError(p.stderr)
    r=json.loads(p.stdout)
    for h in r['hits']:verify(h,b,target)
    return r

def canonical(r):return {tuple(sorted(h)) for h in r['hits']}
def unpack(v):
    u=v[0]+(v[1]<<64)
    return u-(1<<128) if u>>127 else u
def wrap(n):return (n+(1<<127))%(1<<128)-(1<<127)

class OptimizedTests(unittest.TestCase):
    def check(self,b,target=42,f='mod11',start=None,stop=None,oracle=True):
        native=invoke('reference_cpu',b,target,f,start=start,stop=stop)
        if oracle and b<=200 and start is None:
            self.assertEqual(canonical(native),{tuple(h) for h in reference(b,target)})
        results={}
        for variant in VARIANTS:
            r=invoke('search_emulated',b,target,f,variant,start,stop)
            self.assertEqual(r['backend'],'emulated')
            self.assertEqual(r['hits'],native['hits'],(b,target,f,variant,start,stop))
            self.assertLessEqual(r['steps'],native['steps'])
            if variant in ('baseline','cached'):self.assertEqual(r['steps'],native['steps'])
            results[variant]=r
            if GPU:
                g=invoke('search_gpu',b,target,f,variant,start,stop)
                self.assertEqual(g['hits'],r['hits'])
                self.assertEqual(g['steps'],r['steps'])
                REPORT['gpu_comparisons']+=1
        self.assertEqual(results['pruned']['steps'],results['highword']['steps'])
        return results

    def test_reference_cases_all_variants(self):
        for b in (0,1,2,5,10,11,23,50,100,200):self.check(b)
        for b,t,f in ((0,0,'none'),(1,-2,'mod11'),(2,31,'mod11'),(6,7808,'mod11'),
                      (11,161082,'mod11'),(11,-161020,'mod11'),(23,(-23)**5+2**5+22**5,'mod11'),
                      (7,-(1<<63),'none'),(7,(1<<63)-1,'none'),(4,0,'none'),(4,3,'none')):
            self.check(b,t,f)

    def test_random_targets(self):
        rng=random.Random(51542)
        for _ in range(35):
            b=rng.randrange(1,30)
            v=[rng.randint(-b,b) for _ in range(3)]
            t=sum(n**5 for n in v)
            self.check(b,t,'mod11' if t%11==9 else 'none')

    def test_every_row_and_empty_slice(self):
        for b,t,f in ((11,161082,'mod11'),(5,0,'none')):
            for row in range(2*(b//11)+1 if f=='mod11' else 2*b+1):
                self.check(b,t,f,row,row+1)
            self.check(b,t,f,0,0)

    def test_over_64_bit_powers(self):
        for t in (0,6208**5-6209**5):
            r=self.check(6209,t,'none',6209,6210,False)
            self.assertTrue(r['highword']['hits'])

    def test_pruning_reduces_steps(self):
        b=1000
        r=self.check(b,42,'mod11',0,1,False)
        self.assertLess(r['pruned']['steps'],r['baseline']['steps'])
        REPORT['example_pruning_steps']={v:r[v]['steps'] for v in VARIANTS}

    def test_high_word_compare_against_python(self):
        p=subprocess.run([str(ROOT/'bin/compare_high')],text=True,capture_output=True,check=True,timeout=10)
        count=0
        for line in p.stdout.splitlines():
            aa,bb,gg,cc=line.split()
            a,b,g=[unpack(json.loads(n)) for n in (aa,bb,gg)]
            s=wrap(a+b)
            self.assertEqual(int(cc),-1 if s<g else 1 if s>g else 0)
            count+=1
        REPORT['high_word_cases_checked_with_python']=count

    def test_sanitizers(self):
        for v in VARIANTS:
            for b,t,f,start,stop in ((23,42,'mod11',None,None),
                                    (11,161082,'mod11',None,None),
                                    (6209,6208**5-6209**5,'none',6209,6210)):
                r=invoke('search_emulated_sanitize',b,t,f,v,start,stop)
                native=invoke('reference_cpu',b,t,f,start=start,stop=stop)
                self.assertEqual(r['hits'],native['hits'])

    def test_buffer_overflow_fails(self):
        for v in VARIANTS:
            p=subprocess.run([str(ROOT/'bin/search_emulated'),'--bound','3','--filter','none',
                              '--target','0','--variant',v,'--capacity','1'],text=True,capture_output=True)
            self.assertNotEqual(p.returncode,0)
            self.assertEqual(p.stdout,'')
            if GPU:
                p=subprocess.run([str(ROOT/'bin/search_gpu'),'--bound','3','--filter','none',
                                  '--target','0','--variant',v,'--capacity','1'],text=True,capture_output=True)
                self.assertNotEqual(p.returncode,0)
                self.assertEqual(p.stdout,'')

if __name__=='__main__':
    smoke=(subprocess.CompletedProcess([],1,'','CPU-only validation requested') if '--cpu-only' in sys.argv else
           subprocess.run([str(ROOT/'bin/cuda_smoke')],capture_output=True,text=True,timeout=15))
    if smoke.returncode==0:
        GPU=True
        p=subprocess.run([str(ROOT/'bin/search_gpu'),'--self-test'],capture_output=True,text=True,timeout=15)
        if p.returncode:raise SystemExit('GPU self-test failed: '+p.stderr)
        REPORT['gpu_arithmetic_test']=json.loads(p.stdout)
    else:
        REPORT['gpu_blocker']=smoke.stderr.strip()
        print('GPU tests blocked; CPU emulation does not count as GPU validation.',flush=True)
    start=time.monotonic()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(OptimizedTests))
    REPORT.update(cpu_emulation_status='passed' if result.wasSuccessful() else 'failed',
                  gpu_status=('passed' if result.wasSuccessful() else 'failed') if GPU else 'blocked',
                  tests_run=result.testsRun,seconds=time.monotonic()-start,gpu_fingerprint=fingerprint('gpu'))
    atomic_json(ROOT/'runs/optimized-validation.json',REPORT)
    sys.exit(0 if result.wasSuccessful() and (GPU or '--require-gpu' not in sys.argv) else 1)
