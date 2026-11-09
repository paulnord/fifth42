"""Local-only isolated exact-root equivalence tests; no native engine needed."""
import importlib.util
import multiprocessing
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'lattice_gpu'))
import exact_root_opt as opt
import overnight_search as night
import packing_opt

SOURCE = ROOT / 'lattice_prototype'


def private_core(lattice):
    name = lattice.__name__ + '_core'
    spec = importlib.util.spec_from_file_location(name, ROOT/'lattice_gpu/scaling_core.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    module._ENGINE = (str(SOURCE), lattice)
    module.MAX_BOUND = night.MAX_BASE
    return module


def worker_probe(ignored):
    import scaling_core as core
    shared = sys.modules['_experiment_lattice_mpq']
    try:
        opt.initialize(SOURCE)
    except RuntimeError:
        rejected = True
    else:
        rejected = False
    return (core.lattice().iroot(3125), core.lattice().iroot is opt.exact_iroot,
            shared.iroot is opt.exact_iroot, rejected)


class ExactRootTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control = opt.load_private_lattice(SOURCE, optimized=False)
        cls.fast = opt.load_private_lattice(SOURCE)

    def test_boundaries_and_seeded_random_integer_inputs(self):
        rng = random.Random(20261106)
        cases = [(0, 5), (1, 5), (2, 10**100), (123, 1)]
        for degree in (1, 2, 3, 5, 7, 31, 127, 2048):
            for bits in (1, 8, 64, 256, 1024, 2048):
                for _ in range(4):
                    cases.append((rng.getrandbits(bits), degree))
                root = rng.getrandbits(max(1, bits // degree))
                power = root**degree
                if power.bit_length() <= 2049:
                    cases.extend((power + delta, degree) for delta in (-1, 0, 1) if power + delta >= 0)
        for n, k in cases:
            with self.subTest(bits=n.bit_length(), degree=k):
                value = opt.exact_iroot(n, k)
                self.assertIs(type(value), int)
                self.assertEqual(value, self.control.iroot(n, k))
                # Avoid constructing 2**(10**100) in the huge-degree edge case.
                if k <= 2048:
                    self.assertLessEqual(value**k, n)
                    self.assertGreater((value+1)**k, n)
                self.assertEqual(value, opt.exact_iroot(opt.gmpy2.mpz(n), k))

    def test_invalid_inputs_and_large_degrees(self):
        for args in ((-1,5),(1,0),(0,-1)):
            with self.assertRaises(ValueError): opt.exact_iroot(*args)
        for args in ((1.5,5),(1,2.5)):
            with self.assertRaises(TypeError): opt.exact_iroot(*args)
        self.assertEqual(opt.exact_iroot(1,10**100),1)

    def test_independence_and_refusal_to_patch_shared_module(self):
        import scaling_core
        import types
        with self.assertRaises(ValueError): opt.install_on_private_lattice(scaling_core)
        with self.assertRaises(ValueError): opt.install_on_private_lattice(types.ModuleType('fake'))
        self.assertIsNot(self.control.iroot, opt.exact_iroot)
        self.assertIs(self.fast.iroot, opt.exact_iroot)
        self.assertIsNot(self.control.root_bracket.__globals__, self.fast.root_bracket.__globals__)

    def test_spawn_initializer_does_not_mutate_shared_snapshot(self):
        context = multiprocessing.get_context('spawn')
        with context.Pool(1, initializer=opt.initialize, initargs=(SOURCE,)) as pool:
            self.assertEqual(pool.map(worker_probe, [None]), [(5, True, False, True)])

    def test_outward_rational_enclosures(self):
        for numerator, denominator in ((0,1),(1,1),(31,1),(32,1),(33,1),(42,17),(2**2048-1,2**1040+1)):
            for bits in (1,48,80):
                value = self.fast.Q(numerator,denominator)
                self.assertEqual(self.control.root_bracket(value,bits), self.fast.root_bracket(value,bits))
                lo, hi = self.fast.root_bracket(value,bits)
                self.assertLessEqual(lo**5,value)
                self.assertGreaterEqual(hi**5,value)

    def test_tasks_certificates_payloads_packets_low_and_high(self):
        baseline, fast = private_core(self.control), private_core(self.fast)
        count = 0
        for lo, hi, cap in ((64,100,2951),(4096,8191,42),(2**30,2**31-1,42),(10**11,2*10**11-1,42)):
            total = night.grid_count(lo,8)
            for start in sorted({total//4,total//2,total-1}):
                bits = 80 if lo >= 10**11 else 48
                specs = night.shell_specs(lo,hi,8,bits,start,start+1,cap)
                a, b = baseline.prepare_task(specs[0]), fast.prepare_task(specs[0])
                # Dataclasses belong to different private modules: compare values/bytes.
                self.assertEqual(vars(a),vars(b))
                self.assertEqual(baseline.certify_task(a),fast.certify_task(b))
                self.assertEqual(packing_opt.task_payload(a),packing_opt.task_payload(b))
                self.assertEqual(baseline.encode_batch([a],cap).packet.encode(),fast.encode_batch([b],cap).packet.encode())
                count += 1
        self.assertEqual(count,12)


if __name__ == '__main__':
    unittest.main()
