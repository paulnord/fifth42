import gc
import unittest
from dataclasses import dataclass, replace
from sealed_packets import PacketSeals

@dataclass(frozen=True)
class Task:
    id: int = 0
    matrix: tuple = ((1,0),(0,1))
@dataclass(frozen=True)
class Batch:
    tasks: tuple = (Task(),)
    packet: str = 'CANONICAL\n'
    points: int = 4
@dataclass(frozen=True)
class Plan:
    bound: int = 10
    cap: int = 42
    batches: tuple = (Batch(),)
    direct_hits: tuple = ()
    tasks: int = 1
    points: int = 4
    certificate_sha256: str = 'a'*64
@dataclass(frozen=True)
class Window:
    hi: int = 10
    cap: int = 42
    spans: tuple = ((0,4),)
    group_limit: int = 4
@dataclass(frozen=True)
class Chunk:
    window: Window
    plan: Plan
    patches: tuple = ((0,'a'*64,4),)
    geometry_sha256: str = 'b'*64
    payload_bytes: int = 10

def make():
    return Chunk(Window(), Plan(batches=(Batch(tasks=(Task(),)),)))

class Tests(unittest.TestCase):
    def setUp(self):
        self.calls = 0
        def canonical(c):
            self.calls += 1
            if c.plan.batches[0].packet != 'CANONICAL\n':
                raise ValueError('bad packet')
        self.s = PacketSeals(canonical)
    def test_valid_no_repeated_canonical(self):
        c=make(); self.s.seal(c)
        for _ in range(5):self.s.validate(c)
        self.assertEqual(self.calls,1)
    def test_bad_packet_at_entry(self):
        c=make();object.__setattr__(c.plan.batches[0],'packet','WRONG')
        with self.assertRaises(ValueError):self.s.seal(c)
    def test_no_seal(self):
        with self.assertRaises(ValueError):self.s.validate(make())
    def test_copy_not_trusted(self):
        c=make();self.s.seal(c)
        with self.assertRaises(ValueError):self.s.validate(replace(c))
    def test_mutations(self):
        for target, field, value in [
            ('chunk','patches',()),('chunk','geometry_sha256','x'),
            ('chunk','payload_bytes',11),('window','hi',11),
            ('window','cap',41),('window','spans',((1,5),)),
            ('window','group_limit',8),('plan','bound',11),
            ('plan','cap',41),('plan','tasks',2),('plan','points',5),
            ('plan','direct_hits',((1,2,3),)),('plan','certificate_sha256','x'),
            ('batch','packet','WRONG'),('batch','points',5),
            ('task','matrix',((2,0),(0,1))),('task','id',5)]:
            with self.subTest(target=target,field=field):
                c=make();self.s.seal(c)
                obj={'chunk':c,'window':c.window,'plan':c.plan,
                     'batch':c.plan.batches[0],'task':c.plan.batches[0].tasks[0]}[target]
                object.__setattr__(obj,field,value)
                with self.assertRaises(ValueError):self.s.validate(c)
    def test_mutable_rejected(self):
        c=make();object.__setattr__(c.plan.batches[0].tasks[0],'matrix',[[1,0],[0,1]])
        with self.assertRaises(ValueError):self.s.seal(c)
    def test_cap_binding(self):
        c=make();object.__setattr__(c.plan,'cap',41)
        with self.assertRaises(ValueError):self.s.seal(c)
    def test_release(self):
        c=make();self.s.seal(c);self.assertEqual(len(self.s),1)
        del c;gc.collect();self.assertEqual(len(self.s),0)

if __name__=='__main__':unittest.main()
