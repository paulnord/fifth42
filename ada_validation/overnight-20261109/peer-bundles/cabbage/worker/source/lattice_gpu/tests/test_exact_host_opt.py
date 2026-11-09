from dataclasses import replace
import os
from pathlib import Path
import random
import time
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import exact_host_opt as candidate
import overnight_search as night
import scaling_core as core


class ExactHostArithmetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.initialize(Path(os.environ.get('SCALING_LATTICE_SOURCE',ROOT.parent/'lattice_prototype')))

    def specs(self):
        small,_=core.specs(100,2951,8)
        high=night.shell_specs(100000000001,200000000000,8,222,3751385984,3751386000)
        return small+high

    def test_inverse_matches_original_bounds_task_and_certificate(self):
        with patch.object(core,'MAX_BOUND',night.MAX_BASE),patch.object(candidate,'_MODE','inverse'):
            for spec in self.specs():
                task=core.prepare_task(spec)
                alternative=candidate.prepare_task(spec)
                self.assertEqual(task,alternative)
                self.assertEqual(core.certify_task(task),candidate.certify_task(task))

    def test_inverse_exact_check_rejects_wrong_reduced_basis_or_transform(self):
        l=core.lattice()
        spec=self.specs()[-1]
        _,lo,hi,left,right,cap,bits=spec
        patch_=l.make_patch(lo,hi,l.Q(*left),l.Q(*right),cap,bits)
        b,u=l.reduce_basis(patch_.basis(),'fpylll')
        wrong=[row[:] for row in b];wrong[0][0]+=1
        with self.assertRaises(ValueError):candidate.coefficient_bounds_from_patch(patch_,wrong,u)
        wrong_u=[row[:] for row in u];wrong_u[0]=[0,0,0]
        with self.assertRaises(ValueError):candidate.coefficient_bounds_from_patch(patch_,b,wrong_u)

    def test_inverse_supports_both_unimodular_determinant_signs(self):
        l=core.lattice();spec=self.specs()[-1]
        _,lo,hi,left,right,cap,bits=spec
        patch_=l.make_patch(lo,hi,l.Q(*left),l.Q(*right),cap,bits);a=patch_.basis()
        rng=random.Random(1942)
        for sign in (-1,1):
            for _ in range(30):
                u=[[1,0,0],[0,1,0],[0,0,sign]]
                for _ in range(8):
                    i,j=rng.sample(range(3),2);n=rng.randint(-100,100)
                    u[i]=[x+n*y for x,y in zip(u[i],u[j])]
                b=l.matmul(u,a)
                self.assertEqual(candidate.coefficient_bounds_from_patch(patch_,b,u),core.coefficient_bounds(b))

    def test_original_certificate_guards_are_retained(self):
        task=core.prepare_task(self.specs()[0])
        bads=[replace(task,J=(task.J[0]+1,*task.J[1:])),replace(task,points=task.points+1),
              replace(task,U=((0,0,0),*task.U[1:])),replace(task,cmin=0),
              replace(task,U=((2**63,0,0),*task.U[1:])),replace(task,bits=task.bits+1)]
        with patch.object(candidate,'_MODE','inverse'):
            for bad in bads:
                for function in (core.certify_task,candidate.certify_task):
                    with self.assertRaises((ValueError,ZeroDivisionError)):function(bad)

    def test_all_modes_match_nonempty_oracle_under_cpu_and_sanitizers(self):
        import exact_root_opt
        import coordinator_packing
        from engine_session import EngineSession
        from wider_patch_experiment import independent_oracle
        source=Path(os.environ.get('SCALING_LATTICE_SOURCE',ROOT.parent/'lattice_prototype'))
        for mode in candidate.MODES:
            private=exact_root_opt.load_private_lattice(source,optimized=mode in ('roots','combined'))
            with patch.object(core,'_ENGINE',(str(source),private)),patch.object(candidate,'_MODE',mode):
                for bound,cap in ((34,384),(100,2951)):
                    specs,direct=core.specs(bound,cap,8)
                    tasks=[candidate.prepare_task(spec) for spec in specs]
                    tokens=[candidate.certify_task(task) for task in tasks]
                    plan,_,_=coordinator_packing.assemble_with_geometry(bound,cap,specs,direct,tasks,tokens)
                    expected=independent_oracle(bound,cap)
                    self.assertTrue(expected)
                    for binary in ('scaling_cpu','scaling_cpu_sanitize'):
                        with EngineSession([str(ROOT/'bin'/binary),'--threads','2'],'emulated',time.monotonic()+20,
                                           dict(os.environ,ASAN_OPTIONS='detect_leaks=0')) as engine:
                            hits=set(plan.direct_hits)
                            for batch in plan.batches:
                                response,_=engine.run(batch.packet)
                                hits.update(core.decode_batch(batch,response,'emulated'))
                            self.assertEqual(hits,expected)

    def test_sampled_high_shell_patches_match_including_guard_outcomes(self):
        import exact_root_opt
        source=Path(os.environ.get('SCALING_LATTICE_SOURCE',ROOT.parent/'lattice_prototype'))
        lo=100000000001;count=night.grid_count(lo,8)
        rng=random.Random(68642)
        ids=[0,1,count//3,count//2,count-2,count-1]+rng.sample(range(count),18)
        original=core.lattice()
        specs=[night.shell_specs(lo,200000000000,8,222,i,i+1)[0] for i in ids]
        with patch.object(core,'MAX_BOUND',night.MAX_BASE):
            reference=[core.prepare_task(spec) for spec in specs]
            for mode in ('roots','inverse','combined'):
                private=exact_root_opt.load_private_lattice(source,optimized=mode in ('roots','combined'))
                with patch.object(core,'_ENGINE',(str(source),private)),patch.object(candidate,'_MODE',mode):
                    for spec,expected in zip(specs,reference):
                        task=candidate.prepare_task(spec)
                        self.assertEqual(task,expected)
                        try:token=core.certify_task(task)
                        except ValueError:
                            with self.assertRaises(ValueError):candidate.certify_task(task)
                        else:self.assertEqual(candidate.certify_task(task),token)


if __name__=='__main__':unittest.main()
