import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import calibrate
import run

class CalibrationTests(unittest.TestCase):
    def result(self,start,stop):
        bound=10000000
        return {'arithmetic_bits':192,'backend':'gpu','bound':bound,'target':42,'filter':'mod11',
                'row_start':start,'row_stop':stop,'total_rows':run.rows(bound,'mod11'),
                'x_count':run.x_count(bound,'mod11'),'steps':0,'search_seconds':1,'setup_seconds':.1,'hits':[]}

    def exercise(self,timeout=False,stale=False):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'runs').mkdir()
            partial={'arithmetic_bits':192,'bound':10000000,'fingerprint':{'test':'old' if stale else 'current'},
                     'complete':False,'samples':[{'region':'negative_edge','wall_seconds':18,'result':self.result(0,65536)},
                     {'region':'middle','wall_seconds':5,'result':self.result(876322,941858)}]}
            path=root/'runs/calibration.json';path.write_text(json.dumps(partial))
            calls=[]
            def execute(command,budget):
                start=int(command[command.index('--row-start')+1]);stop=int(command[command.index('--row-stop')+1])
                calls.append((start,stop))
                if timeout:raise subprocess.TimeoutExpired(command,budget)
                return self.result(start,stop)
            with patch.object(calibrate,'ROOT',root),patch.object(calibrate,'ensure_idle'),patch.object(run,'gpu_gate'), \
                 patch.object(run,'fingerprint',return_value={'test':'current'}),patch.object(run,'execute_engine',side_effect=execute), \
                 contextlib.redirect_stdout(io.StringIO()):
                if timeout:
                    with self.assertRaises(SystemExit) as error:calibrate.main()
                    self.assertEqual(error.exception.code,2)
                else:calibrate.main()
            return calls,json.loads(path.read_text())

    def test_resumes_only_the_missing_sample(self):
        calls,r=self.exercise()
        self.assertEqual(calls,[(1752645,1818181)])
        self.assertTrue(r['complete']);self.assertEqual(r['reused_samples'],2)
        self.assertEqual(r['samples'][0]['wall_seconds'],18)
        self.assertEqual(len(r['samples']),3)

    def test_interruption_keeps_saved_samples(self):
        calls,r=self.exercise(timeout=True)
        self.assertEqual(len(calls),1);self.assertFalse(r['complete'])
        self.assertEqual(len(r['samples']),2)

    def test_changed_fingerprint_restarts_calibration(self):
        calls,r=self.exercise(stale=True)
        self.assertEqual(len(calls),3);self.assertTrue(r['complete'])
        self.assertEqual(r['reused_samples'],0)

if __name__=='__main__':unittest.main()
