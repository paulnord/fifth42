import unittest
from fractions import Fraction as Q
import reference_geometry as l
from precision_policy import geometry_bits,make_patch

class PrecisionPolicyTests(unittest.TestCase):
    def test_high_shell_current_ratio(self):
        lo,hi,n=100000000001,200000000000,11250000001
        i=3902545280
        self.assertEqual(geometry_bits(l,lo,hi,Q(9*i,10*n),Q(9*(i+1),10*n),42),96)

    def test_flat_endpoint_adapts_upward(self):
        lo,hi,n=100000000001,200000000000,11250000001
        self.assertGreaterEqual(geometry_bits(l,lo,hi,Q(0),Q(9,10*n),42),180)

    def test_original_geometry_and_roots_still_exact(self):
        for lo in [4,10**4,100000000001]:
          hi=min(2*lo-1,200000000000);n=(9*lo+79)//80
          for i in sorted(set([0,1,n//3,n//2,n-1])):
            if i>=n:continue
            left,right=Q(9*i,10*n),Q(9*(i+1),10*n)
            p,bits=make_patch(l,lo,hi,left,right,42)
            self.assertEqual(p,l.make_patch(lo,hi,left,right,42,bits))
            center=(left+right)/2;h=(right-left)/2
            qlo,qhi=l.root_bracket(1-center**5,bits)
            ml,mh=-center**4/qlo**4,-center**4/qhi**4
            actual_rounding=(qhi-qlo)/2+(mh-ml)*h/2
            lower=2*right**3*h*h+Q(42,lo**5)/5
            self.assertGreaterEqual(qlo,Q(1,2))
            if bits<max(48,5*hi.bit_length()+32):
                self.assertLessEqual(actual_rounding*(1<<16),lower)
            self.assertTrue(qlo**5<=1-center**5<=qhi**5)

    def test_original_fallback_outside_policy_ratio(self):
        self.assertEqual(geometry_bits(l,10**11,2*10**11,Q(91,100),Q(92,100),42),222)

    def test_invalid_inputs(self):
        for args in [(0,10,Q(0),Q(1,2),42),(1,10,Q(0),Q(1),42),(1,10,Q(0),Q(1,2),-1)]:
            with self.assertRaises(ValueError):geometry_bits(l,*args)
        with self.assertRaises(ValueError):geometry_bits(l,1,10,Q(0),Q(1,2),42,margin_bits=-1)

if __name__=='__main__':unittest.main()
