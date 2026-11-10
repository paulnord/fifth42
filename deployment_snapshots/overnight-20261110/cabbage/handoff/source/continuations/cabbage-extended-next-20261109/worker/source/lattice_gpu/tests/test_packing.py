import ast
from dataclasses import asdict,replace
import inspect
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import scaling_core as core
import packing_opt as optimized
import scaling
SOURCE=Path(os.environ.get('SCALING_LATTICE_SOURCE','/home/pnord/fifth42-lattice-optimizations-91bb89b/lattice_prototype'))

class PackingOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):core.initialize(SOURCE)

    def tasks(self,bound=34,cap=384):
        specifications,direct=core.specs(bound,cap)
        tasks=[core.prepare_task(row) for row in specifications]
        tokens=[core.certify_task(task) for task in tasks]
        return specifications,direct,tasks,tokens

    def test_canonical_bytes_and_digests_match_for_every_task_field(self):
        _,_,tasks,_=self.tasks(100,2951)
        for task in tasks:
            expected=json.dumps(asdict(task),sort_keys=True,separators=(',',':')).encode()
            self.assertEqual(optimized.task_payload(task),expected)
            self.assertEqual(optimized.task_digest(task),core.task_digest(task))
        original=tasks[-1]
        for field,value in asdict(original).items():
            changed=replace(original,**{field:(getattr(original,field)+1 if isinstance(value,int)
                else tuple(reversed(getattr(original,field))))})
            self.assertEqual(optimized.task_digest(changed),core.task_digest(changed))

    def test_complete_plans_packets_and_certificates_are_identical(self):
        args=self.tasks()
        with patch.object(core,'MAX_TASKS',4):
            baseline=scaling.packing_assembler('baseline')(34,384,*args)
            candidate=scaling.packing_assembler('optimized')(34,384,*args)
        self.assertEqual(candidate,baseline)
        self.assertGreater(len(candidate.batches),1)
        with self.assertRaises(ValueError):scaling.packing_assembler('unknown')

    def test_tampering_missing_patches_and_exhausted_budgets_still_fail(self):
        specifications,direct,tasks,tokens=self.tasks()
        bad=tasks.copy();bad[-1]=replace(bad[-1],points=bad[-1].points+1)
        for implementation in (scaling.packing_assembler('baseline'),scaling.packing_assembler('optimized')):
            with self.assertRaises(ValueError):implementation(34,384,specifications,direct,bad,tokens)
            with self.assertRaises(ValueError):implementation(34,384,specifications,direct,tasks[:-1],tokens[:-1])
            with self.assertRaises(ValueError):implementation(34,384,specifications,direct,tasks,['0'*64]*len(tasks))
            with patch.object(core,'MAX_TOTAL_POINTS',1):
                with self.assertRaises(ValueError):implementation(34,384,specifications,direct,tasks,tokens)

    def test_assembly_algorithm_and_guards_are_unchanged(self):
        class Namespace(ast.NodeTransformer):
            def visit_Attribute(self,node):
                self.generic_visit(node)
                if isinstance(node.value,ast.Name) and node.value.id=='core':
                    return ast.copy_location(ast.Name(id=node.attr,ctx=node.ctx),node)
                return node
        baseline=ast.parse(inspect.getsource(core.assemble))
        candidate=Namespace().visit(ast.parse(inspect.getsource(optimized.assemble)))
        self.assertEqual(ast.dump(baseline),ast.dump(candidate))

if __name__=='__main__':unittest.main(verbosity=2)
