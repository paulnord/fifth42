"""Exercise the actual proposed scaling_core.py patch, with exact stdlib LLL.
The dependency facade changes only reduction backend availability, not geometry.
"""
import dataclasses,importlib.util,json,subprocess,sys,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'reference'))
import lattice5 as L
from validate_cube import direct

def module(filename,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/filename)
    result=importlib.util.module_from_spec(spec);sys.modules[name]=result;spec.loader.exec_module(result)
    facade=types.SimpleNamespace(**vars(L))
    facade.reduce_basis=lambda basis,backend:L.lll(basis)
    result._ENGINE=('isolated-stdlib-test',facade)
    return result

class ActualCorePatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=module('scaling_core.original.py','original_core_fixture')
        cls.new=module('scaling_core.cube.py','cube_core_fixture')
    def test_full_pipeline_and_oracle(self):
        expected=direct(100,'constant',2951)
        all_results=[]
        for core in (self.old,self.new):
            specs,small=core.specs(100,2951,8)
            tasks=[core.prepare_task(s) for s in specs]
            tokens=[core.certify_task(t) for t in tasks]
            plan=core.assemble(100,2951,specs,small,tasks,tokens)
            hits=set(plan.direct_hits)
            for batch in plan.batches:
                raw=subprocess.check_output([str(ROOT/'bin/emulated-ubsan')],input=batch.packet,text=True)
                hits|=core.decode_batch(batch,json.loads(raw),'emulated')
            self.assertEqual(hits,expected)
            all_results.append(plan.points)
        self.assertLess(all_results[1],all_results[0])
    def test_certificate_tampering(self):
        core=self.new;specs,_=core.specs(100,42,8);task=core.prepare_task(specs[-1])
        core.certify_task(task)
        for changed in (dataclasses.replace(task,J=(task.J[0]+1,*task.J[1:])),
                        dataclasses.replace(task,points=task.points+1),
                        dataclasses.replace(task,bits=task.bits+1)):
            with self.assertRaises(ValueError):core.certify_task(changed)
        with self.assertRaises(ValueError):core.checked_tasks([specs[-1]],[])
        with self.assertRaises(ValueError):core.assemble(100,42,[specs[-1]],[],[task],['0'*64])
    def test_identity_cube_equality_boundary(self):
        identity=[[L.Q(i==j) for j in range(3)] for i in range(3)]
        self.assertEqual(self.old.coefficient_bounds(identity),(2,2,2))
        self.assertEqual(self.new.coefficient_bounds(identity),(1,1,1))
if __name__=='__main__':unittest.main(verbosity=2)
