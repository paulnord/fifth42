import hashlib,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent/'worker'))
import durable_mirror as mirror

class MirrorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.source=self.root/'local';self.source.mkdir();self.dest=self.root/'replica'
        self.identity=dict(trial='test',source_identity='a'*64)
        self.data=b'one committed receipt\n';self.cp=dict(identity=self.identity,journal_offset=len(self.data),next_patch=256,chunks=1,journal_sha256='b'*64)
        self.write();self.m=mirror.PrefixMirror(self.source,self.dest,self.identity)
    def tearDown(self):self.m.close();self.temp.cleanup()
    def write(self):
        (self.source/'coverage.jsonl').write_bytes(self.data)
        mirror.atomic(self.source/'checkpoint.json',self.cp)
    def advance(self):
        self.data+=b'two committed receipts\n';self.cp.update(journal_offset=len(self.data),next_patch=512,chunks=2);self.write()
    def test_exact_committed_prefix_and_audits(self):
        (self.source/'coverage.jsonl').write_bytes(self.data+b'uncommitted tail')
        a=self.source/'independent-audits';a.mkdir();mirror.atomic(a/'00000001-0.json',{'ok':1});mirror.atomic(a/'00000002-0.json',{'future':1})
        r=self.m.sync();self.assertEqual((self.dest/'coverage.jsonl').read_bytes(),self.data)
        self.assertEqual(r['raw_sha256'],hashlib.sha256(self.data).hexdigest())
        self.assertTrue((self.dest/'independent-audits/00000001-0.json').exists())
        self.assertFalse((self.dest/'independent-audits/00000002-0.json').exists())
    def test_checkpoint_only_after_fsync(self):
        self.m.sync();old=(self.dest/'checkpoint.json').read_bytes();self.advance()
        with patch.object(mirror.os,'fsync',side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):self.m.sync()
        self.assertEqual((self.dest/'checkpoint.json').read_bytes(),old)
        self.m.sync();self.assertEqual(json.loads((self.dest/'checkpoint.json').read_bytes()),self.cp)
    def test_unpublished_tail_recovered(self):
        self.m.sync();self.advance()
        with (self.dest/'coverage.jsonl').open('ab') as f:f.write(self.data[self.m.offset:self.m.offset+4])
        self.m.sync();self.assertEqual((self.dest/'coverage.jsonl').read_bytes(),self.data)
    def test_wrong_tail_never_advances_checkpoint(self):
        self.m.sync();old=(self.dest/'checkpoint.json').read_bytes();self.advance()
        with (self.dest/'coverage.jsonl').open('ab') as f:f.write(b'wrong')
        with self.assertRaises(RuntimeError):self.m.sync()
        self.assertEqual((self.dest/'checkpoint.json').read_bytes(),old)
    def test_receipt_failure_after_checkpoint_can_restart(self):
        self.m.sync();self.advance();original=mirror.atomic
        def failing(path,row):
            if Path(path).name=='replica-state.json':raise OSError('receipt publication failure')
            return original(path,row)
        with patch.object(mirror,'atomic',side_effect=failing):
            with self.assertRaises(OSError):self.m.sync()
        self.m.close();self.m=mirror.PrefixMirror(self.source,self.dest,self.identity)
        r=self.m.sync();self.assertEqual(r['committed_bytes'],len(self.data))
    def test_truncated_local_prefix_rejected(self):
        self.m.sync();self.advance();(self.source/'coverage.jsonl').write_bytes(b'too short')
        with self.assertRaises(RuntimeError):self.m.sync()
        self.assertEqual(json.loads((self.dest/'checkpoint.json').read_bytes())['chunks'],1)
    def test_identity_and_regression_rejected(self):
        self.m.sync();self.cp['identity']={'trial':'alien'};self.write()
        with self.assertRaises(RuntimeError):self.m.sync()
        self.cp.update(identity=self.identity,journal_offset=1);self.write()
        with self.assertRaises(RuntimeError):self.m.sync()
    def test_second_mirror_owner_rejected(self):
        with self.assertRaises(BlockingIOError):mirror.PrefixMirror(self.source,self.dest,self.identity)
    def test_readback_corruption_does_not_publish(self):
        self.m.sync();old=(self.dest/'checkpoint.json').read_bytes();offset=len(self.data);self.advance()
        real=mirror.os.fsync
        def corrupt(fd):
            if os.readlink('/proc/self/fd/'+str(fd))==str(self.dest/'coverage.jsonl'):
                os.pwrite(fd,b'!',offset)
            return real(fd)
        with patch.object(mirror.os,'fsync',side_effect=corrupt):
            with self.assertRaises(RuntimeError):self.m.sync()
        self.assertEqual((self.dest/'checkpoint.json').read_bytes(),old)

if __name__=='__main__':unittest.main(verbosity=2)
