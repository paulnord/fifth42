from dataclasses import replace
import hashlib
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import coordinator_packing as candidate
import packing_opt
import scaling_core as core


class OnePassPacking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.initialize(Path(os.environ.get('SCALING_LATTICE_SOURCE',ROOT.parent/'lattice_prototype')))

    def inputs(self):
        specs,direct=core.specs(100,2951,8)
        tasks=[core.prepare_task(s) for s in specs]
        tokens=[core.certify_task(t) for t in tasks]
        return specs,direct,tasks,tokens

    def test_exact_plan_packets_geometry_and_payload_bytes_match(self):
        args=self.inputs()
        with patch.object(core,'MAX_TASKS',3):
            expected=packing_opt.assemble(100,2951,*args)
            plan,geometry,size=candidate.assemble_with_geometry(100,2951,*args)
        self.assertEqual(expected,plan)
        payload=b''.join(packing_opt.task_payload(t)+b'\n' for t in args[2])
        self.assertEqual(geometry,hashlib.sha256(payload).hexdigest())
        self.assertEqual(size,len(payload)+sum(len(b.packet.encode()) for b in plan.batches))
        self.assertGreater(len(plan.batches),1)
        self.assertTrue(plan.direct_hits)

    def test_all_original_assembly_guards_remain(self):
        specs,direct,tasks,tokens=self.inputs()
        for function in (packing_opt.assemble,candidate.assemble_with_geometry):
            for changed in ((specs,direct,tasks[:-1],tokens[:-1]),
                            (specs,direct,tasks,['0'*64]*len(tokens)),
                            (specs,direct,[replace(tasks[0],points=tasks[0].points+1)]+tasks[1:],tokens),
                            (specs,direct,tasks,tokens[:-1])):
                with self.assertRaises(ValueError):function(100,2951,*changed)
            with patch.object(core,'MAX_TOTAL_POINTS',1):
                with self.assertRaises(ValueError):function(100,2951,specs,direct,tasks,tokens)
            with patch.object(core,'MAX_POINTS',1):
                with self.assertRaises(ValueError):function(100,2951,specs,direct,tasks,tokens)


if __name__=='__main__':unittest.main()
