import contextlib,hashlib,io,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import validate

class PreflightTests(unittest.TestCase):
    def test_busy_guard_never_starts_a_process(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(validate,'ROOT',Path(tmp)),patch.object(validate,'blockers',return_value=['four133 active']),patch.object(sys,'argv',['validate.py']),patch.object(validate.subprocess,'Popen') as popen,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(validate.main(),3);popen.assert_not_called()
            self.assertFalse(json.loads((Path(tmp)/'preflight.json').read_text())['gpu_validation_started'])
    def test_cpu_baseline_requires_freshness_proof_and_current_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            review=Path(tmp);run=review/'validation-runs/one';run.mkdir(parents=True);scratch=review/'scratch';(scratch/'results').mkdir(parents=True)
            names={'healy-1000.json','reference-healy-1000.json','signed42-1000.json','focused-large-controls.json','upstream-comparison.json'}
            hashes={}
            for name in names:
                p=scratch/'results'/name;p.write_text('{}');hashes[name]=dict(reproduced_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
            d=dict(status='passed',source_commit='ddf28f04725b29b2f1d53b5d33c16379b0f66a20',scratch=str(scratch),regenerated_result_comparisons=hashes)
            p=run/'report.json';p.write_text(json.dumps(d))
            with patch.object(validate,'REVIEW',review):
                self.assertIsNone(validate.baseline())
                d.update(copied_outputs_removed=True,verified_fresh_outputs={name:{} for name in names});p.write_text(json.dumps(d));self.assertIsNotNone(validate.baseline())
                (scratch/'results/healy-1000.json').write_text('{"changed":true}')
                self.assertIsNone(validate.baseline())

if __name__=='__main__':unittest.main(verbosity=2)
