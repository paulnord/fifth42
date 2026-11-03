#!/usr/bin/env python3
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from reference import reference, verify
from run import MAX_BOUND, atomic_json, coverage, estimate, fingerprint, validate_result, x_count

GPU = False
GPU_REASON = ''
REPORT = {'cpu_status': 'pending', 'gpu_status': 'pending'}
GPU_COMPARISONS = 0


def engine(bound, target=42, filter_name='mod11', backend='cpu', start=None, stop=None, capacity=None):
    global GPU_COMPARISONS
    cmd = [str(ROOT / f'bin/search_{backend}'), '--bound', str(bound), '--target', str(target),
           '--filter', filter_name]
    for flag, value in [('--row-start', start), ('--row-stop', stop), ('--capacity', capacity)]:
        if value is not None:
            cmd.extend([flag, str(value)])
    p = subprocess.run(cmd, text=True, capture_output=True, timeout=15)
    if p.returncode:
        raise RuntimeError(p.stderr)
    if backend == 'gpu':
        GPU_COMPARISONS += 1
    return json.loads(p.stdout)


def canonical(result):
    return {verify(h, result['bound'], result['target']) for h in result['hits']}


def unpack(limbs):
    u = limbs[0] + (limbs[1] << 64)
    return u - (1 << 128) if u >> 127 else u


def wrap(n):
    n %= 1 << 128
    return n - (1 << 128) if n >> 127 else n


class SearchTests(unittest.TestCase):
    def test_mod11_proof(self):
        self.assertEqual({pow(n, 5, 11) for n in range(11)}, {0, 1, 10})
        possible = [(a,b,c) for a in (-1,0,1) for b in (-1,0,1) for c in (-1,0,1)
                    if (a+b+c-42) % 11 == 0]
        self.assertEqual(set(possible), {(-1,-1,0), (-1,0,-1), (0,-1,-1)})
        self.assertEqual([n for n in range(11) if pow(n,5,11) == 10], [2,6,7,8,10])
        for b in range(60):
            self.assertEqual(x_count(b, 'mod11'), sum(pow(n,5,11) == 10 for n in range(-b,b+1)))

    def compare(self, b, target, filter_name):
        expected = {tuple(h) for h in reference(b, target)}
        cpu = engine(b, target, filter_name)
        self.assertEqual(canonical(cpu), expected, (b,target,filter_name))
        self.assertEqual(len(cpu['hits']), len({tuple(h) for h in cpu['hits']}))
        if GPU:
            gpu = engine(b, target, filter_name, 'gpu')
            self.assertEqual(gpu['hits'], cpu['hits'], (b,target,filter_name))
            self.assertEqual(gpu['steps'], cpu['steps'])
        return cpu

    def test_target42_small_bounds(self):
        for b in (0,1,2,5,10,11,12,22,23,32,50,100,200):
            with self.subTest(bound=b):
                filtered = self.compare(b, 42, 'mod11')
                unfiltered = self.compare(b, 42, 'none')
                self.assertEqual(canonical(filtered), canonical(unfiltered))

    def test_positive_controls_and_endpoints(self):
        # Includes zeros, both bound endpoints, repeated a=b, negative target,
        # and all three original positions of the unique multiple of eleven.
        cases = [(0,0,'none'), (1,-2,'mod11'), (2,31,'mod11'), (6,7808,'mod11'),
                 (11,11**5+2**5-1,'mod11'), (11,-11**5+2**5-1,'mod11'),
                 (23,(-23)**5+2**5+22**5,'mod11'),
                 (3,0,'none'), (5,3,'none'), (5,-3,'none')]
        for b,target,f in cases:
            with self.subTest(bound=b,target=target):
                r = self.compare(b,target,f)
                if target not in (3,-3):
                    self.assertTrue(r['hits'])
        self.assertIn([-1,-1,0], engine(1,-2)['hits'])

    def test_generated_targets(self):
        rng = random.Random(42)
        for _ in range(15):
            b = rng.randrange(3,20)
            a,c,z = (rng.randint(-b,b) for _ in range(3))
            target = a**5+c**5+z**5
            f = 'mod11' if target%11 == 9 else 'none'
            self.compare(b,target,f)
        self.compare(7, -(1<<63), 'none')
        self.compare(7, (1<<63)-1, 'none')

    def test_over_64_bits_with_known_hits(self):
        b = 6209
        self.assertLess(6208**5, 1<<63)
        self.assertGreater(b**5, 1<<63)
        for target in (0, 6208**5-6209**5):
            cpu = engine(b,target,'none',start=b,stop=b+1)
            self.assertTrue(cpu['hits'])
            canonical(cpu)
            if target:
                self.assertIn([-6209,6208,0],cpu['hits'])
            if GPU:
                gpu = engine(b,target,'none','gpu',start=b,stop=b+1)
                self.assertEqual(gpu['hits'],cpu['hits'])
                self.assertEqual(gpu['steps'],cpu['steps'])

    def test_arithmetic_against_python(self):
        p = subprocess.run([str(ROOT/'bin/arithmetic_cpu')], text=True, capture_output=True, check=True, timeout=10)
        count = 0
        for line in p.stdout.splitlines():
            aa,bb,ss,nn,lt,eq = line.split()
            a,b,s,n = [unpack(json.loads(v)) for v in (aa,bb,ss,nn)]
            self.assertEqual(s,wrap(a+b))
            self.assertEqual(n,wrap(-a))
            self.assertEqual(int(lt),int(a<b))
            self.assertEqual(int(eq),int(a==b))
            count += 1
        REPORT['host_limb_cases_checked_with_python'] = count
        p = subprocess.run([str(ROOT/'bin/arithmetic_cpu_sanitize'), '--powers'], text=True, capture_output=True, check=True)
        endpoints = []
        for line in p.stdout.splitlines():
            n,value = line.split()
            self.assertEqual(int(n)**5,unpack(json.loads(value)))
            endpoints.append(int(n))
        self.assertEqual((min(endpoints),max(endpoints)),(-MAX_BOUND,MAX_BOUND))
        self.assertLess(3*MAX_BOUND**5+(1<<63),1<<127)

    def test_enlarged_bound_native_extremes(self):
        p = subprocess.run([str(ROOT/'bin/arithmetic_cpu_sanitize'),'--native-extremes'],
                           text=True,capture_output=True,timeout=10)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(p.stderr,'')
        cases = 0
        for line in p.stdout.splitlines():
            aa,bb,zz,tt,pair,goal,total = line.split()
            a,b,z,target = map(int,(aa,bb,zz,tt))
            self.assertEqual(unpack(json.loads(pair)),a**5+b**5)
            self.assertEqual(unpack(json.loads(goal)),target-z**5)
            self.assertEqual(unpack(json.loads(total)),a**5+b**5+z**5)
            cases += 1
        self.assertEqual(cases,375)
        REPORT['native_extreme_cases_checked_with_python_and_ubsan'] = cases

    def test_rejects_unsafe_input_and_truncation(self):
        cases = [['--bound','-1'], ['--bound',str(MAX_BOUND+1)], ['--bound','5','--target','0'],
                 ['--bound','5','--row-start','-1'], ['--bound','5','--row-stop','999'],
                 ['--bound','5x'], ['--bound','5','--target',str(1<<63)],
                 ['--bound','3','--target','0','--filter','none','--capacity','1']]
        for args in cases:
            for backend in (['cpu','gpu'] if GPU else ['cpu']):
                p = subprocess.run([str(ROOT/f'bin/search_{backend}'), *args], text=True, capture_output=True)
                self.assertNotEqual(p.returncode,0,args)
                self.assertEqual(p.stdout,'',args)

    def test_empty_and_partitioned_rows(self):
        for b,target,f in [(2,31,'mod11'),(11,161082,'mod11'),(4,0,'none')]:
            whole = engine(b,target,f)
            parts = [engine(b,target,f,start=i,stop=i+1) for i in range(whole['total_rows'])]
            self.assertEqual([h for p in parts for h in p['hits']],whole['hits'])
            self.assertEqual(sum(p['steps'] for p in parts),whole['steps'])
            empty = engine(b,target,f,start=0,stop=0)
            self.assertEqual(empty['steps'],0)
            if GPU:
                gpu = engine(b,target,f,'gpu',start=0,stop=0)
                self.assertEqual(gpu['hits'],[])
                self.assertEqual(gpu['steps'],0)

    def test_cpu_undefined_behavior_sanitizer(self):
        commands = [ ['--bound','100','--target','42'],
                     ['--bound','6209','--target','0','--filter','none','--row-start','6209','--row-stop','6210'],
                     ['--bound','5','--target',str(-(1<<63)),'--filter','none'] ]
        for args in commands:
            p = subprocess.run([str(ROOT/'bin/search_cpu_sanitize'),*args], text=True,capture_output=True,timeout=10)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(p.stderr,'')
            canonical(json.loads(p.stdout))

    def test_runner_resume_and_records(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'run'
            def cli(*args):
                return subprocess.run([sys.executable,str(ROOT/'run.py'),*args], text=True,capture_output=True,timeout=10)
            first = cli('new','--run',str(path),'--bound','11','--target','161082',
                        '--chunk-rows','1','--max-chunks','1')
            self.assertEqual(first.returncode,0,first.stderr)
            state = json.loads((path/'state.json').read_text())
            self.assertEqual(coverage(state),1)
            # Simulated uncommitted orphan file must not count as coverage.
            (path/'.checkpoint-orphan').write_text('{broken')
            p = cli('resume','--run',str(path))
            self.assertEqual(p.returncode,0,p.stderr)
            state = json.loads((path/'state.json').read_text())
            self.assertEqual(coverage(state),state['total_rows'])
            self.assertEqual([h for c in state['chunks'] for h in c['hits']],engine(11,161082)['hits'])
            p = cli('resume','--run',str(path))
            self.assertEqual(p.returncode,0,p.stderr)
            broken = json.loads(json.dumps(state))
            broken['chunks'][1]['row_start'] = 0
            with self.assertRaises(ValueError): coverage(broken)
            broken = json.loads(json.dumps(state))
            broken['fingerprint']['bin/search_cpu'] = 'wrong'
            atomic_json(path/'state.json',broken)
            p = cli('resume','--run',str(path))
            self.assertNotEqual(p.returncode,0)
            self.assertIn('changed',p.stderr)

    def test_runner_budget_and_approval_guards(self):
        with tempfile.TemporaryDirectory() as td:
            for extra in (['--bound','100001'],['--bound','10','--max-seconds','31']):
                p = subprocess.run([sys.executable,str(ROOT/'run.py'),'new','--run',str(Path(td)/'run'),*extra],
                                   text=True,capture_output=True)
                self.assertNotEqual(p.returncode,0)
                self.assertFalse((Path(td)/'run').exists())
            path = Path(td)/'budget'
            p = subprocess.run([sys.executable,str(ROOT/'run.py'),'new','--run',str(path),
                                '--bound','100000','--chunk-rows','18183','--max-seconds','0.1'],
                               text=True,capture_output=True,timeout=3)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads((path/'state.json').read_text())['next_row'],0)

    def test_false_candidate_is_rejected(self):
        config = {'backend':'cpu','bound':2,'target':31,'filter':'mod11'}
        r = engine(2,31)
        validate_result(r,config,0,1)
        r['hits'] = [[2,2,0]]
        with self.assertRaises(ValueError): validate_result(r,config,0,1)
        with self.assertRaises(ValueError): verify([1,2,3],3,42)

    def test_runner_termination_preserves_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'termination'
            p = subprocess.Popen([sys.executable,str(ROOT/'run.py'),'new','--run',str(path),
                                  '--bound','100000','--chunk-rows','18183','--max-seconds','10'],
                                 stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            try:
                deadline = time.monotonic()+3
                while not (path/'state.json').exists() and time.monotonic() < deadline:
                    time.sleep(0.005)
                self.assertTrue((path/'state.json').exists())
                # Allow the child to start; SIGTERM must kill it without committing its chunk.
                time.sleep(0.03)
                p.send_signal(signal.SIGTERM)
                out,err = p.communicate(timeout=3)
                self.assertEqual(p.returncode,0,err)
                state = json.loads((path/'state.json').read_text())
                self.assertEqual(coverage(state),0)
            finally:
                if p.poll() is None:
                    p.kill()
                    p.communicate()


if __name__ == '__main__':
    smoke = (subprocess.CompletedProcess([],1,'','CPU-only validation requested') if '--cpu-only' in sys.argv else
             subprocess.run([str(ROOT/'bin/cuda_smoke')],text=True,capture_output=True,timeout=15))
    REPORT['gpu_smoke_stdout'] = smoke.stdout.strip()
    REPORT['gpu_smoke_stderr'] = smoke.stderr.strip()
    if smoke.returncode == 0:
        GPU = True
        p = subprocess.run([str(ROOT/'bin/search_gpu'),'--self-test'],text=True,capture_output=True,timeout=15)
        if p.returncode:
            raise SystemExit('GPU arithmetic self-test failed: '+p.stderr)
        REPORT['gpu_arithmetic_test'] = json.loads(p.stdout)
    else:
        # Failure remains visible. This is not a passing GPU test.
        GPU_REASON = smoke.stderr.strip() or f'smoke exited {smoke.returncode}'
        print('GPU TESTS BLOCKED: '+GPU_REASON,flush=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SearchTests)
    start = time.monotonic()
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    REPORT.update(cpu_status='passed' if result.wasSuccessful() else 'failed',
                  gpu_status=('passed' if result.wasSuccessful() else 'failed') if GPU else 'blocked',
                  gpu_blocker=GPU_REASON,tests_run=result.testsRun,seconds=time.monotonic()-start,
                  gpu_search_comparisons=GPU_COMPARISONS,
                  cpu_fingerprint=fingerprint('cpu'),gpu_fingerprint=fingerprint('gpu'))
    atomic_json(ROOT/'runs/validation.json',REPORT)
    sys.exit(0 if result.wasSuccessful() and (GPU or '--require-gpu' not in sys.argv) else 1)
