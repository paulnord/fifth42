"""Critical continuation/deadline checks; fixtures never touch existing evidence."""
import copy
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import threading
import time
import unittest
from unittest import mock

import policy
from packed_worker import windows,run,PreparationPacer
import search_supervisor as supervisor


class PolicyTests(unittest.TestCase):
    def test_shared_claim_read_retries_transient_registry_contention(self):
        import ada_export_store
        with tempfile.TemporaryDirectory() as tmp:
            coverage=dict(status='verified_receipts',final_checkpoint=True,next_patch=500,
                          parent_checkpoint_sha256='parent',parent_journal_sha256='chain')
            path=Path(tmp)/'coverage.json';path.write_text(json.dumps(coverage))
            config=dict(coverage_file=str(path),coverage_sha256=policy.digest(path),
                        initial_patch=500,parent_checkpoint_sha256='parent',parent_journal_sha256='chain',
                        ledger_root=tmp,ledger_device=1,ledger_job='test',ledger_claim_sha256='claim',
                        range_end=1000,manifest_sha256='runtime')
            claim=dict(sha256='claim',first=500,last=1000,identity='runtime',
                       coverage=dict(sha256=config['coverage_sha256'],manifest=coverage))
            store=mock.Mock(device=1)
            store.claim.side_effect=[ada_export_store.Busy('other host reserving'),claim]
            with mock.patch.object(ada_export_store,'Store',return_value=store), \
                 mock.patch.object(policy.time,'sleep'):
                self.assertEqual(policy.validate_ledger(config),(store,claim))
            self.assertEqual(store.claim.call_count,2)

    def test_pacing_waits_and_honors_stop_without_touching_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'checkpoint.json';path.write_bytes(b'unchanged cursor')
            event=threading.Event()
            pacer=PreparationPacer(dict(stop_epoch=time.time()+60,prep_load_ceiling=2.5),Path(tmp),event)
            with mock.patch('packed_worker.os.getloadavg',side_effect=[(3.2,0,0),(2.4,0,0)]),mock.patch.object(event,'wait') as wait:
                pacer.wait();self.assertEqual(wait.call_count,1)
            event.set()
            with self.assertRaises(policy.RequestedStop):pacer.wait()
            self.assertEqual(path.read_bytes(),b'unchanged cursor')

    def test_generator_is_lazy_contiguous_and_starts_at_parent_cursor(self):
        config=dict(initial_patch=3809566592,shell_lo=100000000001,shell_hi=200000000000,width=8,bits=222,cap=42)
        stream=windows(config,11250000001)
        first=next(stream);second=next(stream)
        self.assertEqual((first.first,first.last,second.first,second.last),
                         (3809566592,3809566848,3809566848,3809567104))

    def test_absolute_deadline_and_stop_do_not_advance_any_cursor(self):
        with tempfile.TemporaryDirectory() as tmp:
            event=threading.Event()
            with mock.patch.object(policy.time,'time',return_value=100):
                self.assertEqual(policy.remaining(dict(stop_epoch=150),event,tmp,30),30)
                with self.assertRaises(policy.RequestedStop):policy.remaining(dict(stop_epoch=108),event,tmp)
                event.set()
                with self.assertRaises(policy.RequestedStop):policy.remaining(dict(stop_epoch=1000),event,tmp)
            self.assertEqual(list(Path(tmp).iterdir()),[])

    def test_parent_cursor_and_checkpoint_hash_are_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'coverage.jsonl').write_bytes(b'committed\n')
            checkpoint=dict(status='stopped',completed_bound=None,next_patch=500,journal_sha256='chain',journal_offset=10)
            (root/'checkpoint.json').write_text(json.dumps(checkpoint))
            config=dict(parent_run=str(root),parent_checkpoint_sha256=policy.digest(root/'checkpoint.json'),
                        initial_patch=500,parent_journal_sha256='chain',parent_journal_offset=10)
            policy.validate_parent(config)
            wrong=dict(config,initial_patch=499)
            with self.assertRaises(RuntimeError):policy.validate_parent(wrong)
            with (root/'coverage.jsonl').open('ab') as stream:stream.write(b'new suffix')
            with self.assertRaises(RuntimeError):policy.validate_parent(config)

    def test_old_active_service_blocks(self):
        result=subprocess.CompletedProcess([],0,'LoadState=loaded\nActiveState=active\nSubState=running\nMainPID=123\n','')
        with mock.patch.object(supervisor.subprocess,'run',return_value=result):
            with self.assertRaises(RuntimeError):supervisor.service_and_process_checks({})

    def test_existing_checkpoint_is_never_reused_or_recovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint=Path(tmp)/'checkpoint.json';checkpoint.write_bytes(b'preserved existing checkpoint')
            with self.assertRaises(FileExistsError):run(dict(output=tmp))
            self.assertEqual(checkpoint.read_bytes(),b'preserved existing checkpoint')
            self.assertEqual([p.name for p in Path(tmp).iterdir()],['checkpoint.json'])

    def test_other_gpu_group_blocks(self):
        result=subprocess.CompletedProcess([],0,'123\n','')
        child=mock.Mock(pid=400)
        with mock.patch.object(supervisor.subprocess,'run',return_value=result),mock.patch.object(supervisor.os,'getpgid',return_value=401):
            with self.assertRaises(RuntimeError):supervisor.gpu_process_checks(child)

    def test_owned_process_group_is_stopped(self):
        child=subprocess.Popen([os.sys.executable,'-c','import time; time.sleep(30)'],start_new_session=True)
        try:
            supervisor.stop_owned(child,grace=.25)
            self.assertIsNotNone(child.poll())
        finally:
            if child.poll() is None:
                os.killpg(child.pid,signal.SIGKILL);child.wait()

    def test_deadline_cannot_be_extended_or_mislabeled(self):
        root=Path(__file__).resolve().parent
        original=json.loads((root/'config.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'config.json'
            extended=dict(original,stop_epoch=original['stop_epoch']+1)
            path.write_text(json.dumps(extended))
            with self.assertRaisesRegex(RuntimeError,'deadline'):policy.load_config(path)
            mislabeled=dict(original,stop_epoch=original['stop_epoch']-1)
            path.write_text(json.dumps(mislabeled))
            with self.assertRaisesRegex(RuntimeError,'Local and absolute'):policy.load_config(path)


if __name__=='__main__':unittest.main(verbosity=2)
