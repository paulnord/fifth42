"""Correctness, guard, crash and durable-prefix tests for buffering strategies."""
import copy,dataclasses,gc,hashlib,json,os
from pathlib import Path
import subprocess,sys,tempfile,threading,time,unittest
from unittest.mock import patch
import buffered_pipeline as b
import adapter_runtime as adapter
import audit_grouped
import coordinator_pipeline as pipeline
import runtime_initialize
import scaling_core as core
import width_coverage as coverage
ROOT=Path(__file__).resolve().parent;W=ROOT/'worker'
TRIAL='TEST_ONLY_buffering-unit'
class Serial:
    def map(self,fn,args,chunksize):return list(map(fn,args))

def cp(path):return json.loads((Path(path)/'checkpoint.json').read_bytes())
def save_refs(folder,refs):
    dest=Path(folder)/'independent-audits';dest.mkdir()
    for sequence,group in enumerate(refs,1):
        for index,reference in enumerate(group):
            (dest/f'{sequence:08d}-{index}.json').write_text(json.dumps(reference)+'\n')

class BufferingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.sched_setaffinity(0,set(range(16)));runtime_initialize.initialize(W/'source/lattice_prototype')
        cls.engine=adapter.open_session(W/'bin/scaling_gpu','gpu',time.monotonic()+180)
        cls.first=4398843264;cls.records=[];cls.references=[]
        for index in range(6):
            first=cls.first+index*256;window=pipeline.Window(100000000001,200000000000,first,first+256,8,222,42,'adaptive')
            chunk=coverage.prepare_chunk(Serial(),window,2)
            row=coverage.add_coverage(pipeline.execute_chunk(chunk,pipeline.OwnedEngine(cls.engine),trial=TRIAL,coordinator=0),chunk,2)
            refs=[]
            for batch,receipt in zip(chunk.plan.batches,row['batches']):
                done=subprocess.run([str(W/'bin/gmp_reference')],input=batch.packet,capture_output=True,text=True,check=True,timeout=20)
                reference=json.loads(done.stdout);assert adapter.normalized_counts(batch,reference)==list(map(tuple,receipt['native_counts']))
                assert adapter.normalized_hits(batch,reference)==list(map(tuple,receipt['native_hit_records']))
                refs.append(reference)
            row['independent_gmp_audited']=True;cls.records.append(row);cls.references.append(refs)
        cls.whole=coverage.Window(100000000001,200000000000,cls.first,cls.first+6*256,8,222,42,'adaptive',2)
        cls.window=pipeline.Window(100000000001,200000000000,cls.first,cls.first+256,8,222,42,'adaptive')
        cls.chunk=b.prepare_cached(Serial(),cls.window,2)
    @classmethod
    def tearDownClass(cls):cls.engine.close()
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT,prefix='unit-');self.folder=Path(self.temp.name)
        save_refs(self.folder,self.references)
    def tearDown(self):self.temp.cleanup()
    def journal(self,**kwargs):return b.BufferedJournal(self.folder,dict(trial=TRIAL),self.whole,**kwargs)
    def audit(self,state):
        result=audit_grouped.audit_suffix(self.folder,dict(checkpoint=dict(next_patch=self.first),config=dict(group_limit=2,gmp_audit_period=1)),state,'fresh',1)
        self.assertEqual(result['new_chunks'],state['chunks']);return result
    def test_single_encoding_preserves_hash_and_all_record_values(self):
        previous='0'*64
        for record in self.records:
            a,da=b.night.encode_record(previous,record);raw,db=b.encode_record_once(previous,record)
            self.assertEqual(da,db);self.assertEqual(json.loads(a),json.loads(raw));previous=db
    def test_pending_is_not_committed(self):
        j=self.journal(records=2);j.commit(self.records[0]);self.assertEqual(j.state['chunks'],0)
        self.assertFalse((self.folder/'checkpoint.json').exists());self.assertEqual(j.head['chunks'],1)
        j.commit(self.records[1]);self.assertEqual(cp(self.folder)['chunks'],2);j.close();self.audit(cp(self.folder))
    def test_graceful_close_flushes_final_partial_group(self):
        j=self.journal(records=4)
        for row in self.records[:5]:j.commit(row)
        self.assertEqual(j.state['chunks'],4);j.close();self.assertEqual(cp(self.folder)['chunks'],5);self.audit(cp(self.folder))
    def test_byte_bound_and_owner_checks(self):
        size=len(b.encode_record_once('0'*64,dict(self.records[0],sequence=1))[0]);budget=2*size+1000
        j=self.journal(records=64,max_bytes=budget)
        for row in self.records:j.commit(row)
        j.close();self.assertLessEqual(j.peak_pending_bytes,budget);self.assertEqual(cp(self.folder)['chunks'],6);self.audit(cp(self.folder))
    def test_age_threshold_flushes_on_next_accept(self):
        j=self.journal(records=64,max_age=.005);j.commit(self.records[0]);time.sleep(.01);j.commit(self.records[1])
        self.assertEqual(j.state['chunks'],2);j.close()
    def test_failed_checkpoint_preserves_old_prefix_and_poisoned_writer(self):
        j=self.journal(records=2);j.commit(self.records[0]);j.commit(self.records[1]);old=(self.folder/'checkpoint.json').read_bytes()
        j.commit(self.records[2])
        with patch.object(b.night,'atomic_json',side_effect=OSError('checkpoint failure')):
            with self.assertRaises(OSError):j.commit(self.records[3])
        self.assertEqual((self.folder/'checkpoint.json').read_bytes(),old)
        with self.assertRaises(RuntimeError):j.commit(self.records[4])
        j.close();self.audit(cp(self.folder))
        recovered=self.journal(records=2);self.assertEqual(recovered.state['chunks'],2);recovered.close();self.audit(cp(self.folder))
    def test_fsync_failure_does_not_advance_checkpoint(self):
        j=self.journal(records=2);j.commit(self.records[0]);j.commit(self.records[1]);old=(self.folder/'checkpoint.json').read_bytes();j.commit(self.records[2])
        with patch.object(b.os,'fsync',side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):j.commit(self.records[3])
        j.close();self.assertEqual((self.folder/'checkpoint.json').read_bytes(),old);self.audit(cp(self.folder))
    def test_process_crash_loses_only_uncommitted_buffer(self):
        fixture=self.folder/'fixture.json';fixture.write_text(json.dumps(self.records))
        code="""import json,os,sys;from pathlib import Path;import buffered_pipeline as b;import width_coverage as c
p=Path(sys.argv[1]);rows=json.loads((p/'fixture.json').read_bytes());w=rows[0]['window'];whole=c.Window(w['lo'],w['hi'],w['first'],w['first']+6*256,8,222,42,'adaptive',2)
j=b.BufferedJournal(p,dict(trial='TEST_ONLY_buffering-unit'),whole,records=2)
for row in rows[:3]:j.commit(row)
os._exit(0)
"""
        subprocess.run([sys.executable,'-B','-c',code,str(self.folder)],cwd=ROOT,check=True,timeout=20)
        self.assertEqual(cp(self.folder)['chunks'],2);j=self.journal();self.assertEqual(j.state['chunks'],2);j.close();self.audit(cp(self.folder))
    def test_async_queue_snapshot_and_graceful_drain(self):
        writer=b.AsyncJournal(self.folder,dict(trial=TRIAL),self.whole,records=2,queue_records=2)
        for original in self.records:
            row=copy.deepcopy(original);writer.commit(row);row['window']['first']=-1
        writer.close();self.assertEqual(writer.state['chunks'],6);self.assertLessEqual(writer.peak_queued_records,2);self.audit(cp(self.folder))
    def test_async_writer_reports_failed_record(self):
        writer=b.AsyncJournal(self.folder,dict(trial=TRIAL),self.whole,records=2)
        for row in self.records[:2]:writer.commit(row)
        bad=copy.deepcopy(self.records[2]);bad['batches'][0]['native_counts'][0]=[self.first,1,0];writer.commit(bad)
        with self.assertRaises(RuntimeError):writer.close()
        self.assertFalse(writer.thread.is_alive());self.assertEqual(cp(self.folder)['chunks'],2);self.audit(cp(self.folder))
    def test_async_idle_timer_flushes_without_more_work(self):
        writer=b.AsyncJournal(self.folder,dict(trial=TRIAL),self.whole,records=64);writer.commit(self.records[0]);until=time.monotonic()+2
        while time.monotonic()<until and writer.state['chunks']==0:time.sleep(.02)
        self.assertEqual(writer.state['chunks'],1);writer.close();self.audit(cp(self.folder))
    def test_cached_canonical_bytes_and_packets_match_baseline(self):
        baseline=coverage.prepare_chunk(Serial(),self.window,2);b.validate_cached(self.chunk);pipeline.validate_chunk(self.chunk)
        self.assertEqual(baseline.patches,self.chunk.patches);self.assertEqual(baseline.geometry_sha256,self.chunk.geometry_sha256)
        self.assertEqual(baseline.plan,self.chunk.plan)
    def test_cached_replacement_and_field_tampering_rejected(self):
        with self.assertRaises(ValueError):b.validate_cached(dataclasses.replace(self.chunk,geometry_sha256='0'*64))
        task=self.chunk.plan.batches[0].tasks[0];original=task.J
        object.__setattr__(task,'J',tuple(j+1 for j in original))
        try:
            with self.assertRaises(ValueError):b.validate_cached(self.chunk)
        finally:object.__setattr__(task,'J',original)
        b.validate_cached(self.chunk)
    def test_cached_packet_manifest_and_geometry_tampering_rejected(self):
        for name,value in [('patches',()),('geometry_sha256','0'*64)]:
            old=getattr(self.chunk,name);object.__setattr__(self.chunk,name,value)
            try:
                with self.assertRaises(ValueError):b.validate_cached(self.chunk)
            finally:object.__setattr__(self.chunk,name,old)
        plan=self.chunk.plan;old=plan.batches;bad=dataclasses.replace(old[0],packet=old[0].packet+'1\n')
        object.__setattr__(plan,'batches',(bad,)+old[1:])
        try:
            with self.assertRaises(ValueError):b.validate_cached(self.chunk)
        finally:object.__setattr__(plan,'batches',old)
    def test_cached_seals_released_with_chunk(self):
        before=b.cache_size();chunk=b.prepare_cached(Serial(),self.window,2);self.assertEqual(b.cache_size(),before+1)
        del chunk;gc.collect();self.assertEqual(b.cache_size(),before)
    def test_nonempty_gpu_gmp_candidates_preserved(self):
        window=pipeline.Window(16,31,0,2,8,222,42,'adaptive');chunk=b.prepare_cached(Serial(),window,2)
        b.validate_cached(chunk);pipeline.validate_chunk(chunk);found=set()
        for batch in chunk.plan.batches:
            raw,_=self.engine.run(batch.packet,timeout=20);gpu=core.decode_batch(batch,raw,'gpu');found.update(gpu)
            done=subprocess.run([str(W/'bin/gmp_reference')],input=batch.packet,capture_output=True,text=True,check=True,timeout=20)
            ref=json.loads(done.stdout);self.assertEqual(adapter.normalized_counts(batch,raw),adapter.normalized_counts(batch,ref));self.assertEqual(gpu,core.decode_batch(batch,ref,'emulated'))
        self.assertIn((13,16,17,12),found)
    def test_memory_only_mode_preserves_record_chain_without_claiming_durability(self):
        m=b.MemoryJournal(dict(trial=TRIAL),self.whole)
        for row in self.records:m.commit(row)
        lines=m.data.splitlines();last='0'*64
        for index,line in enumerate(lines,1):
            row=json.loads(line);digest=row.pop('sha256');self.assertEqual(row['sequence'],index);self.assertEqual(row['previous_sha256'],last)
            self.assertEqual(hashlib.sha256(audit_grouped.stable(row)).hexdigest(),digest);last=digest
        self.assertEqual(m.state['journal_sha256'],last);self.assertEqual(m.state['chunks'],6)

if __name__=='__main__':unittest.main(verbosity=2)
