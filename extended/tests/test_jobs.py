#!/usr/bin/env python3
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import jobs
import run

def wait_for(path,limit=5):
    deadline=time.monotonic()+limit
    while time.monotonic()<deadline:
        if path.exists():return
        time.sleep(.02)
    raise AssertionError(f'Expected output did not arrive: {path}')

class DetachedTests(unittest.TestCase):
    def test_survives_launching_parent_exit_and_hangup(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);job=root/'job';marker=root/'done'
            code="import sys,time;from pathlib import Path;time.sleep(.6);Path(sys.argv[1]).write_text('survived');print('finished',flush=True)"
            parent="import jobs,sys;from pathlib import Path;jobs.launch(Path(sys.argv[1]),[sys.executable,'-c',sys.argv[3],sys.argv[2]],5,Path(sys.argv[1])/'coverage')"
            p=subprocess.run([sys.executable,'-c',parent,str(job),str(marker),code],cwd=ROOT,capture_output=True,text=True,timeout=3)
            self.assertEqual(p.returncode,0,p.stderr)
            wait_for(job/'job.json')
            l=json.loads((job/'launcher.json').read_text())
            self.assertEqual(os.getsid(l['worker_pid']),l['worker_pid'])
            os.kill(l['worker_pid'],signal.SIGHUP)
            wait_for(marker)
            self.assertEqual(marker.read_text(),'survived')
            wait_for(job/'search.log')
            deadline=time.monotonic()+3
            while 'finished' not in (job/'search.log').read_text() and time.monotonic()<deadline:time.sleep(.02)
            self.assertIn('finished',(job/'search.log').read_text())
            deadline=time.monotonic()+3
            while time.monotonic()<deadline:
                r=json.loads((job/'job.json').read_text())
                if 'finished_utc' in r:break
                time.sleep(.02)
            self.assertIn('finished_utc',r)

    def test_time_budget_terminates_child(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);job=root/'job'
            info=jobs.launch(job,[sys.executable,'-c','import time;time.sleep(30)'],.2,root/'coverage')
            wait_for(job/'job.json')
            deadline=time.monotonic()+5
            while time.monotonic()<deadline:
                r=json.loads((job/'job.json').read_text())
                if 'finished_utc' in r:break
                time.sleep(.02)
            self.assertEqual(r['reason'],'time_budget_exhausted')
            self.assertNotEqual(r['exit_code'],0)

    def test_requires_approval_before_work(self):
        p=subprocess.run([sys.executable,str(ROOT/'jobs.py'),'start','--bound','70000000',
                          '--hours','4','--job','runs/not-approved'],text=True,capture_output=True)
        self.assertNotEqual(p.returncode,0)
        self.assertIn('approve',p.stderr)

    def test_budget_preserves_real_checkpoint(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);job=root/'job';coverage=root/'coverage'
            command=[sys.executable,str(ROOT/'run.py'),'new','--backend','cpu',
                     '--bound','100000','--chunk-rows','65536','--max-seconds','10','--run',str(coverage)]
            jobs.launch(job,command,.4,coverage)
            wait_for(job/'job.json')
            deadline=time.monotonic()+5
            while time.monotonic()<deadline:
                r=json.loads((job/'job.json').read_text())
                if 'finished_utc' in r:break
                time.sleep(.02)
            self.assertEqual(r['reason'],'time_budget_exhausted')
            self.assertEqual(r['status'],'partial')
            s=json.loads((coverage/'state.json').read_text())
            self.assertEqual(run.coverage(s),0)
            self.assertEqual(s['next_row'],0)

    def test_budget_kills_engine_in_a_separate_session(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);job=root/'job';pidfile=root/'engine'
            code="import subprocess,sys,time;from pathlib import Path;p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'],start_new_session=True);Path(sys.argv[1]).write_text(str(p.pid));time.sleep(30)"
            jobs.launch(job,[sys.executable,'-c',code,str(pidfile)],.4,root/'coverage')
            wait_for(pidfile);pid=int(pidfile.read_text());stamp=jobs.ticks(pid)
            deadline=time.monotonic()+5
            while time.monotonic()<deadline:
                if not jobs.alive(pid,stamp):break
                time.sleep(.02)
            self.assertFalse(jobs.alive(pid,stamp))

if __name__=='__main__':unittest.main()
