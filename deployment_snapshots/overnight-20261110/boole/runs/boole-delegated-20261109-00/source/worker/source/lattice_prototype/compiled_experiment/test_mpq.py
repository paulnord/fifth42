"""Focused exactness and isolation regression tests for optional mpq experiment."""
import ast
import unittest
from fractions import Fraction
import random
import benchmark_mpq as exp
import lattice5
import modular_filters

class ExactMPQTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref,cls.rf=exp.engine('fraction')
        cls.gmp,cls.gf=exp.engine('mpq')

    def test_snapshots_match_live_behavior(self):
        class StripDocstrings(ast.NodeTransformer):
            def visit(self,node):
                node=super().visit(node)
                if isinstance(node,(ast.Module,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                    if node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):
                        node.body=node.body[1:]
                return node
        for name in ('lattice5','modular_filters'):
            live=StripDocstrings().visit(ast.parse((exp.ROOT/(name+'.py')).read_text()))
            frozen=StripDocstrings().visit(ast.parse((exp.HERE/(name+'_snapshot.py')).read_text()))
            self.assertEqual(ast.dump(live),ast.dump(frozen))

    def test_default_modules_unchanged(self):
        self.assertIs(lattice5.Q,Fraction)
        self.assertIs(modular_filters.Q,Fraction)
        self.assertIs(modular_filters.l,lattice5)

    def test_exact_outward_roots(self):
        rng=random.Random(42)
        values=[Fraction(0),Fraction(1),Fraction(1,32),Fraction((2**48-1)**5,2**240)]
        values += [Fraction(rng.randrange(1,10**30),rng.randrange(1,10**30)) for _ in range(50)]
        for x in values:
            a=self.ref.root_bracket(x)
            b=self.gmp.root_bracket(self.gmp.Q(x.numerator,x.denominator))
            self.assertEqual(exp.normalize(a),exp.normalize(b))
            self.assertLessEqual(b[0]**5,x)
            self.assertGreaterEqual(b[1]**5,x)

    def test_budget_failure_remains_failure(self):
        for l,f in [(self.ref,self.rf),(self.gmp,self.gf)]:
            for kwargs in [dict(max_nodes=0),dict(max_patches=0),dict(max_seconds=0)]:
                with self.assertRaises(l.BudgetExceeded):
                    f.signed42_filtered(100,mode='prune',backend='fpylll',**kwargs)

    def test_exact_sphere_boundary(self):
        # Standard basis has many points exactly on squared radius 3.
        outcomes=[]
        for l,f in [(self.ref,self.rf),(self.gmp,self.gf)]:
            b=[[l.Q(int(i==j)) for j in range(3)] for i in range(3)]
            stats=l.Stats()
            outcomes.append(set(l.sphere_coefficients(b,stats,l.Budget())))
        self.assertEqual(outcomes[0],outcomes[1])
        self.assertIn((1,1,1),outcomes[1])
        self.assertNotIn((2,0,0),outcomes[1])

if __name__=='__main__':
    unittest.main()
