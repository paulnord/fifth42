import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import policy


class BulkPolicyTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(prefix='ada-bulk-policy-test-')
        self.addCleanup(tmp.cleanup);self.root=Path(tmp.name)

    def parent(self):
        journal=self.root/'coverage.jsonl';journal.write_bytes(b'committed\n')
        cp=dict(next_patch=500,journal_sha256='chain',journal_offset=10,completed_bound=None)
        (self.root/'checkpoint.json').write_text(json.dumps(cp))
        (self.root/'status.json').write_text(json.dumps(dict(status='stopped',error=None)))
        config=dict(parent_run=str(self.root),initial_patch=500,parent_journal_sha256='chain',
                    parent_journal_offset=10,parent_journal_raw_sha256=policy.digest(journal),
                    parent_checkpoint_sha256=policy.digest(self.root/'checkpoint.json'),
                    parent_status_sha256=policy.digest(self.root/'status.json'))
        audit=dict(status='passed',final_checkpoint=True,
                   captured_checkpoint_sha256=config['parent_checkpoint_sha256'],
                   committed_chain_sha256='chain',committed_raw_sha256=config['parent_journal_raw_sha256'],
                   committed_bytes=10,selected_interval=[0,500])
        path=self.root/'audit.json';path.write_text(json.dumps(audit))
        config.update(parent_audit_file=str(path),parent_audit_sha256=policy.digest(path))
        receipt=dict(status='verified',raw_sha256=config['parent_journal_raw_sha256'],
                     committed_bytes=10,captured_checkpoint_sha256=config['parent_checkpoint_sha256'])
        path=self.root/'ARCHIVE_RECEIPT.json';path.write_text(json.dumps(receipt))
        stat=journal.stat()
        config.update(parent_archive_receipt=str(path),parent_archive_receipt_sha256=policy.digest(path),
                      parent_journal_identity=[stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns])
        return config

    def test_verified_archive_and_exact_parent_cursor_are_required(self):
        config=self.parent();self.assertEqual(policy.validate_parent(config)['next_patch'],500)
        with self.assertRaisesRegex(RuntimeError,'exact selected parent cursor'):
            policy.validate_parent(dict(config,initial_patch=501))

    def test_archive_mutation_cannot_be_hidden_by_unchanged_length(self):
        config=self.parent();(self.root/'coverage.jsonl').write_bytes(b'altered!!\n')
        with self.assertRaisesRegex(RuntimeError,'inode/bytes/timestamps changed'):
            policy.validate_archive(config)

    def test_dirty_parent_suffix_blocks_handoff(self):
        config=self.parent()
        with (self.root/'coverage.jsonl').open('ab') as stream:stream.write(b'tail')
        with self.assertRaisesRegex(RuntimeError,'prefix identity/length'):
            policy.validate_parent(config)

    def test_changed_archive_receipt_blocks_handoff(self):
        config=self.parent();(self.root/'ARCHIVE_RECEIPT.json').write_text('{}')
        with self.assertRaisesRegex(RuntimeError,'receipt changed'):policy.validate_archive(config)

    def test_original_reservation_can_be_inherited_without_overlapping_claim(self):
        import ada_export_store,bulk_data_store
        coverage=dict(status='verified_receipts',final_checkpoint=True,next_patch=500,
                      parent_checkpoint_sha256='parent',parent_journal_sha256='chain')
        path=self.root/'coverage.json';path.write_text(json.dumps(coverage))
        original=dict(first=100,last=1000,identity='original-runtime',sha256='original-claim')
        origin=self.root/'origin.json';origin.write_text(json.dumps(original))
        config=dict(coverage_file=str(path),coverage_sha256=policy.digest(path),initial_patch=500,
                    parent_checkpoint_sha256='parent',parent_journal_sha256='chain',ledger_root='shared',
                    ledger_device=1,ledger_job='owned',ledger_claim_sha256='original-claim',
                    origin_claim_file=str(origin),origin_claim_file_sha256=policy.digest(origin),
                    reservation_manifest_sha256='original-runtime',reservation_initial_patch=100,
                    range_end=1000,output='bulk/run',data_device=2,manifest_sha256='new-runtime')
        store=mock.Mock(device=1);store.claim.return_value=original
        with mock.patch.object(ada_export_store,'Store',return_value=store), \
                mock.patch.object(bulk_data_store,'verify_share',return_value=2):
            self.assertEqual(policy.validate_ledger(config),(store,original))
            store.claim.return_value=dict(original,last=1001)
            with self.assertRaisesRegex(RuntimeError,'inheritance mismatch'):policy.validate_ledger(config)

    def test_stop_and_deadline_never_modify_checkpoint(self):
        path=self.root/'checkpoint.json';path.write_bytes(b'preserved')
        event=mock.Mock();event.is_set.return_value=False
        with mock.patch.object(policy.time,'time',return_value=100):
            with self.assertRaises(policy.RequestedStop):policy.remaining(dict(stop_epoch=108),event,self.root)
            event.is_set.return_value=True
            with self.assertRaises(policy.RequestedStop):policy.remaining(dict(stop_epoch=1000),event,self.root)
        self.assertEqual(path.read_bytes(),b'preserved')


if __name__=='__main__':unittest.main(verbosity=2)
