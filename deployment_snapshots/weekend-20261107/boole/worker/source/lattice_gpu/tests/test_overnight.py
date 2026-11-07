import os
from pathlib import Path
import tempfile
import unittest
import overnight_search as night
import scaling_core as core

class StreamingCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core.initialize(Path(os.environ.get('SCALING_LATTICE_SOURCE','/home/pnord/fifth42-lattice-optimizations-91bb89b/lattice_prototype')))

    def test_streaming_grid_exactly_matches_certified_baseline_and_tiles_large_shell(self):
        specs,_=core.specs(32000,42,8)
        for lo in sorted({row[1] for row in specs}):
            hi=min(2*lo-1,32000);expected=[row[1:] for row in specs if row[1]==lo]
            actual=[];count=night.grid_count(lo,8)
            for first in range(0,count,17):actual.extend(row[1:] for row in night.shell_specs(lo,hi,8,48,first,min(first+17,count)))
            self.assertEqual(actual,expected)
        lo=2**24;count=night.grid_count(lo,8)
        first=night.shell_specs(lo,2*lo-1,8,64,0,1)[0]
        last=night.shell_specs(lo,2*lo-1,8,64,count-1,count)[0]
        self.assertEqual(first[3],(0,1));self.assertEqual(last[4],(9,10))

    def test_journal_detects_tampering_and_preserves_uncommitted_suffix(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'coverage.jsonl';raw,digest=night.encode_record('0'*64,dict(sequence=1,first=0,last=10))
            path.write_bytes(raw+b'partial uncommitted write')
            state=dict(journal_offset=len(raw),journal_sha256=digest,chunks=1)
            night.verify_journal(path,state);self.assertEqual(path.read_bytes(),raw)
            self.assertEqual(len(list(Path(folder).glob('uncommitted-*.jsonl'))),1)
            path.write_bytes(raw.replace(b'"last":10',b'"last":11'))
            with self.assertRaises(RuntimeError):night.verify_journal(path,state)

    def test_resume_rejects_changed_configuration_and_gapped_shells(self):
        config=dict(width=8,backend='cuda',source_identity='abc')
        state=dict(width=8,backend='cuda',cap=42,source_identity='abc',shell_lo=32768,completed_bound=32767,next_patch=12)
        night.validate_checkpoint(state,config)
        for changes in (dict(width=4),dict(source_identity='bad'),dict(completed_bound=32000),dict(shell_lo=33000),dict(next_patch=-1)):
            with self.assertRaises(RuntimeError):night.validate_checkpoint(dict(state,**changes),config)

    def test_high_range_has_exact_arithmetic_headroom_and_no_full_box_claim(self):
        self.assertLess(3*night.MAX_BASE**5,2**191)
        config=dict(width=8,backend='cuda',source_identity='abc',start_bound=100000000001)
        state=dict(width=8,backend='cuda',cap=42,source_identity='abc',shell_lo=100000000001,
            completed_bound=None,next_patch=4000000000)
        night.validate_checkpoint(state,config)
        with self.assertRaises(RuntimeError):night.validate_checkpoint(dict(state,completed_bound=100000000000),config)

if __name__=='__main__':unittest.main()
