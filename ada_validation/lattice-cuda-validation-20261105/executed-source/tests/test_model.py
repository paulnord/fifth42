import copy,itertools,sys,unittest
from fractions import Fraction as Q
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model as m

class CertificateTests(unittest.TestCase):
    def test_outward_square_roots(self):
        for x in [Q(0),Q(1),Q(3),Q(4),Q(17,5),Q(1,10**40),Q(10**60+1)]:
            k=m.ceil_sqrt(x);self.assertGreaterEqual(k*k,x)
            if k:self.assertLess((k-1)**2,x)
    def test_coefficient_box_contains_closed_sphere(self):
        for b in [[[Q(i==j) for j in range(3)] for i in range(3)],[[Q(1),Q(1,3),Q(0)],[Q(0),Q(1),Q(1,2)],[Q(0),Q(0),Q(1)]]]:
            bounds=m.coefficient_bounds(b)
            for n in itertools.product(range(-3,4),repeat=3):
                v=[sum(n[i]*b[i][j] for i in range(3)) for j in range(3)]
                if sum(x*x for x in v)<=3:self.assertTrue(all(abs(n[i])<=bounds[i] for i in range(3)))
        self.assertEqual(m.coefficient_bounds([[Q(i==j) for j in range(3)] for i in range(3)]),[2,2,2])
    def test_integer_range_and_work_guards(self):
        t=dict(U=[[1,0,0],[0,1,0],[0,0,1]],J=[2,2,2],points=125,cmin=1,cmax=10)
        self.assertEqual(m.integer_task_checks(t),125)
        for key,value in [('U',[[m.MAX_I64,0,0],[0,1,0],[0,0,1]]),('J',[1000,1000,1000]),('cmax',m.MAX_BASE+1),('points',124)]:
            bad=copy.deepcopy(t);bad[key]=value
            with self.assertRaises(ValueError):m.integer_task_checks(bad)
    def test_patch_certificate_reconstruction(self):
        ref=m.reference();t=m.task_from_patch(10,10,Q(4,5),Q(9,10),18098,48,8,9)
        a=m.matrix_read(t['A']);b=m.matrix_read(t['B']);self.assertEqual(ref.matmul(t['U'],a),b)
        self.assertEqual(abs(ref.det3(t['U'])),1);self.assertEqual(m.coefficient_bounds(b),t['J'])
        p=m.patch_for_task(t);self.assertTrue(p.contains(9,9,10))
    def test_full_domain_preparation_limits(self):
        for args in [(1001,'constant',42,2),(100,'other',42,2),(100,'constant',-1,2),(100,'constant',42,0)]:
            with self.assertRaises(ValueError):m.expected_specs(*args)
        specs,direct=m.expected_specs(10,'constant',42,2)
        self.assertEqual(direct,[[1,1],[2,3]])
        self.assertEqual([(s[0],s[1]) for s in specs],[(4,7)]*2+[(8,10)]*4)
    def test_certificate_and_missing_device_counts_fail_closed(self):
        plan=m.make_plan(4);self.assertTrue(m.verify_plan(plan))
        bad=copy.deepcopy(plan);bad['tasks'].pop()
        with self.assertRaises(ValueError):m.verify_plan(bad)
        bad=copy.deepcopy(plan);bad['tasks'][0]['J'][0]+=1
        with self.assertRaises(ValueError):m.verify_plan(bad)
        bad=copy.deepcopy(plan);bad['tasks'][0]['U'][0][0]+=1
        with self.assertRaises(ValueError):m.verify_plan(bad)
        result=dict(backend='gpu',box_complete=True,points_visited=plan['points'],counts=[],hits=[])
        with self.assertRaises(ValueError):m.decode(plan,result,'gpu')
        result['counts']=[dict(id=t['id'],expected=t['points'],visited=t['points']) for t in plan['tasks']]
        result['hits']=[dict(task=-1,linear=0,a=1,b=1,c=2)]
        with self.assertRaises(ValueError):m.decode(plan,result,'gpu')

if __name__=='__main__':unittest.main(verbosity=2)
