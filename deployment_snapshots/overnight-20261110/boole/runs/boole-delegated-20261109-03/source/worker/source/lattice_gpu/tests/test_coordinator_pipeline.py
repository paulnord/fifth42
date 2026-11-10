import copy
from dataclasses import replace
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import coordinator_pipeline as p
import scaling_core as core
from engine_session import EngineSession
import overnight_search as night

SOURCE = Path(os.environ.get('SCALING_LATTICE_SOURCE', ROOT.parent/'lattice_prototype'))


class SerialPool:
    def map(self, function, items, chunksize):
        return list(map(function, items))


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.initialize(SOURCE)

    def chunk(self):
        return p.prepare_chunk(SerialPool(), p.Window(64,100,0,8,cap=2951), 'fused')

    def execute(self, chunk):
        with EngineSession([str(ROOT/'bin/scaling_cpu'), '--threads', '2'], 'emulated', time.monotonic()+20) as engine:
            return p.execute_chunk(chunk,p.OwnedEngine(engine),trial='test',coordinator=0)

    def test_fused_matches_baseline_every_task_packet_geometry_certificate(self):
        window=p.Window(64,100,0,8,cap=2951)
        base=p.prepare_chunk(SerialPool(),window,'baseline')
        fused=p.prepare_chunk(SerialPool(),window,'fused')
        packed=p.prepare_chunk(SerialPool(),window,'packed')
        for field in ('window','plan','patches','geometry_sha256','payload_bytes'):
            self.assertEqual(getattr(base,field),getattr(fused,field))
            self.assertEqual(getattr(base,field),getattr(packed,field))
        p.validate_chunk(fused)

    def test_nonempty_oracle_matches_complete_selected_shell(self):
        chunk=self.chunk()
        result=self.execute(chunk)
        expected=core.lattice().direct_positive(64,100,lambda _:2951,lambda r,c:abs(r)<=2951)
        self.assertIn((42,71,72,2951),expected)
        self.assertEqual(set(map(tuple,result['hits'])),expected)
        self.assertTrue(result['complete'])

    def test_guarded_patch_fails_before_counting_coverage(self):
        spec=self.chunk().window.specifications()[0]
        with patch.object(night,'native_safe',return_value=False):
            with self.assertRaises(p.GuardedPatch):p.prepare_certified(spec)

    def test_partition_union_and_global_audits_ignore_coordinator_split(self):
        window=p.Window(4096,8191,3,400)
        pieces=p.partition(window,2)
        p.verify_partition(window,pieces)
        self.assertEqual(tuple(i for w in pieces for i in p.audited_patch_ids(w,64)),p.audited_patch_ids(window,64))
        for wrong in (pieces[::-1],(pieces[0],pieces[0]),pieces[:1],(replace(pieces[0],bits=64),pieces[1])):
            with self.assertRaises(ValueError):p.verify_partition(window,wrong)

    def test_truncated_plan_or_tampered_packet_rejected_before_engine(self):
        chunk=self.chunk()
        for bad in (replace(chunk,plan=replace(chunk.plan,batches=())),
                    replace(chunk,plan=replace(chunk.plan,batches=(replace(chunk.plan.batches[0],packet='wrong'),))),
                    replace(chunk,patches=chunk.patches[:-1])):
            with self.assertRaises(ValueError):p.validate_chunk(bad)

    def test_malformed_count_types_and_incomplete_outputs_rejected(self):
        chunk=self.chunk();batch=chunk.plan.batches[0]
        response=dict(backend='emulated',box_complete=True,points_visited=batch.points,
            counts=[dict(id=i,expected=t.points,visited=t.points) for i,t in enumerate(batch.tasks)],hits=[])
        p.validate_response_types(response)
        for change in (dict(points_visited=float(batch.points)),dict(points_visited=True),dict(counts=None),dict(hits=[dict(task=0,linear=0,a=True,b=1,c=2)])):
            with self.assertRaises(ValueError):p.validate_response_types(dict(response,**change))
        class Incomplete:
            backend='emulated'
            def run(self,*args,**kwargs):return dict(response,box_complete=False),0
        with self.assertRaises(ValueError):p.execute_chunk(chunk,Incomplete(),trial='test',coordinator=0)

    def test_stale_native_reply_rejected_by_persistent_session(self):
        code = "import json,sys; print(json.dumps(dict(ready=True,backend='emulated',persistent=True)),flush=True); head=sys.stdin.readline().split(); sys.stdin.read(int(head[2])); print(json.dumps(dict(request_id=0)),flush=True)"
        with EngineSession([sys.executable,'-u','-c',code],'emulated',time.monotonic()+10) as session:
            with self.assertRaisesRegex(RuntimeError,'stale or mismatched'):
                session.run('LATTICE_GPU_V1 0 42 0\n')

    def test_engine_owner_rejects_other_thread(self):
        class Session:
            backend='emulated'
            def run(self,*args,**kwargs):raise AssertionError('must not reach session')
        errors=[];engine=p.OwnedEngine(Session())
        def call():
            try:engine.run('packet')
            except RuntimeError as e:errors.append(e)
        thread=threading.Thread(target=call);thread.start();thread.join()
        self.assertEqual(len(errors),1)

    def test_journal_resume_replays_uncommitted_suffix_without_advancing(self):
        chunk=self.chunk();record=self.execute(chunk);identity=dict(trial='test',source_identity='frozen')
        with tempfile.TemporaryDirectory() as folder:
            with p.TrialJournal(folder,identity,chunk.window) as journal:
                with patch.object(night,'atomic_json',side_effect=OSError('injected checkpoint failure')):
                    with self.assertRaises(OSError):journal.commit(record)
                self.assertEqual(journal.state['next_patch'],chunk.window.first)
                with self.assertRaises(RuntimeError):journal.commit(record)
            with p.TrialJournal(folder,identity,chunk.window) as recovered:
                self.assertEqual(recovered.state['next_patch'],chunk.window.first)
                recovered.commit(record)
            with p.TrialJournal(folder,identity,chunk.window) as recovered:
                self.assertEqual(recovered.state['next_patch'],chunk.window.last)
                self.assertIsNone(recovered.state['completed_bound'])
                with self.assertRaises(ValueError):recovered.commit(record)
            self.assertEqual(len(list(Path(folder).glob('uncommitted-*.jsonl'))),1)

    def test_reopen_reconciles_checkpoint_replaced_before_fsync_failure(self):
        chunk=self.chunk();record=self.execute(chunk);identity=dict(trial='test',source_identity='frozen')
        atomic=night.atomic_json
        def uncertain(path,data):
            atomic(path,data)
            raise OSError('simulated failure after replace')
        with tempfile.TemporaryDirectory() as folder:
            with p.TrialJournal(folder,identity,chunk.window) as journal:
                with patch.object(night,'atomic_json',side_effect=uncertain):
                    with self.assertRaises(OSError):journal.commit(record)
            with p.TrialJournal(folder,identity,chunk.window) as recovered:
                self.assertEqual(recovered.state['next_patch'],chunk.window.last)
                with self.assertRaises(ValueError):recovered.commit(record)

    def test_closed_journal_cannot_bypass_a_new_writer_lock(self):
        chunk=self.chunk();record=self.execute(chunk);identity=dict(trial='test',source_identity='frozen')
        with tempfile.TemporaryDirectory() as folder:
            old=p.TrialJournal(folder,identity,chunk.window)
            old.close()
            with p.TrialJournal(folder,identity,chunk.window):
                with self.assertRaises(RuntimeError):old.commit(record)

    def test_journal_rejects_stale_gap_manifest_changed_source_and_other_writer(self):
        chunk=self.chunk();record=self.execute(chunk);identity=dict(trial='test',source_identity='frozen')
        with tempfile.TemporaryDirectory() as folder:
            with p.TrialJournal(folder,identity,chunk.window) as journal:
                with self.assertRaises(BlockingIOError):p.TrialJournal(folder,identity,chunk.window)
                for edit in ('gap','incomplete','duplicate','bad_hash','stale_trial','missing_batch','float_id'):
                    bad=copy.deepcopy(record)
                    if edit=='gap':bad['window']['first']+=1
                    elif edit=='incomplete':bad['complete']=False
                    elif edit=='duplicate':bad['patches']=bad['patches'][:-1]+bad['patches'][:1]
                    elif edit=='bad_hash':bad['patches']=((0,'x'*64,bad['patches'][0][2]),)+bad['patches'][1:]
                    elif edit=='stale_trial':bad['batches'][0]['identity']['trial']='old'
                    elif edit=='missing_batch':bad['batches']=[]
                    elif edit=='float_id':bad['patches']=((0.,*bad['patches'][0][1:]),)+bad['patches'][1:]
                    with self.assertRaises(ValueError,msg=edit):journal.commit(bad)
                journal.commit(record)
            with self.assertRaises(ValueError):p.TrialJournal(folder,dict(identity,source_identity='changed'),chunk.window)


if __name__=='__main__':unittest.main()
