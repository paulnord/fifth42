import dataclasses,hashlib,json,os,sys,time,unittest
from pathlib import Path
from unittest.mock import patch
import buffered_pipeline as b
import wire_pipeline as wire
import runtime_initialize,coordinator_pipeline as pipeline,width_coverage as coverage
import adapter_runtime as adapter
import scaling_core as core
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
class Serial:
    def map(self,fn,args,chunksize):return list(map(fn,args))
class WireSerial:
    def map(self,fn,args,chunksize):
        with patch.object(core,'task_digest',wire.capture_digest):return list(map(fn,args))
class WireTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.sched_setaffinity(0,set(range(16)));runtime_initialize.initialize(W/'source/lattice_prototype')
        cls.window=pipeline.Window(100000000001,200000000000,4398843264,4398843521,8,222,42,'adaptive')
        cls.original=coverage.prepare_chunk(Serial(),cls.window,2);cls.wired=wire.prepare_cached(WireSerial(),cls.window,2)
    def test_roundtrip_preserves_every_exact_task_and_certificate(self):
        a,c=self.original,self.wired;self.assertEqual(a.plan,c.plan);self.assertEqual(a.patches,c.patches)
        self.assertEqual(a.geometry_sha256,c.geometry_sha256);self.assertEqual(a.window,c.window)
        b.validate_cached(c);pipeline.validate_chunk(c)
    def test_corrupted_payload_or_token_rejected(self):
        task=self.wired.plan.batches[0].tasks[0];payload=b.packing_opt.task_payload(task);token=hashlib.sha256(payload).hexdigest()
        self.assertEqual(wire.decode(payload,token),task)
        with self.assertRaises(ValueError):wire.decode(payload+b' ',token)
        with self.assertRaises(ValueError):wire.decode(payload,'0'*64)
    def test_duplicate_unknown_and_noninteger_fields_rejected(self):
        task=self.wired.plan.batches[0].tasks[0];payload=b.packing_opt.task_payload(task)
        for suffix in (b',"id":1}',b',"extra":1}'):
            raw=payload[:-1]+suffix
            with self.assertRaises(ValueError):wire.decode(raw,hashlib.sha256(raw).hexdigest())
        data=json.loads(payload)
        for value in (True,1.0,float('nan')):
            data['id']=value;raw=json.dumps(data).encode()
            with self.assertRaises(ValueError):wire.decode(raw,hashlib.sha256(raw).hexdigest())
    def test_task_mutation_after_transport_rejected(self):
        task=self.wired.plan.batches[0].tasks[0];old=task.points;object.__setattr__(task,'points',old+1)
        try:
            with self.assertRaises(ValueError):b.validate_cached(self.wired)
        finally:object.__setattr__(task,'points',old)
    def test_guarded_wider_patch_recurses_without_losing_cells(self):
        original=pipeline.prepare_certified
        calls=[]
        def guard(spec):
            calls.append(spec[0])
            if len(calls)==1:raise pipeline.GuardedPatch('forced wide guard')
            return original(spec)
        args=(100000000001,200000000000,4398843264,4398843268,222,42,'adaptive')
        with patch.object(core,'task_digest',wire.capture_digest),patch.object(pipeline,'prepare_certified',side_effect=guard):rows=wire.prepare_segment(args)
        self.assertEqual([(row[3],row[4]) for row in rows],[(4398843264,4398843266),(4398843266,4398843268)])
        for payload,token,*_ in rows:wire.decode(payload,token)
    def test_nonempty_actual_gpu_gmp_candidates_preserved(self):
        chunk=wire.prepare_cached(WireSerial(),pipeline.Window(16,31,0,2,8,222,42,'adaptive'),2)
        b.validate_cached(chunk);pipeline.validate_chunk(chunk);session=adapter.open_session(W/'bin/scaling_gpu','gpu',time.monotonic()+30)
        import subprocess
        found=set()
        try:
            for batch in chunk.plan.batches:
                raw,_=session.run(batch.packet,timeout=20);found.update(core.decode_batch(batch,raw,'gpu'))
                done=subprocess.run([str(W/'bin/gmp_reference')],input=batch.packet,text=True,capture_output=True,check=True,timeout=20);ref=json.loads(done.stdout)
                self.assertEqual(adapter.normalized_counts(batch,raw),adapter.normalized_counts(batch,ref));self.assertEqual(adapter.normalized_hits(batch,raw),adapter.normalized_hits(batch,ref))
            self.assertIn((13,16,17,12),found)
        finally:session.close()
if __name__=='__main__':unittest.main(verbosity=2)
