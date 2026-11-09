"""A real completed test replica supplies a terminal relay view; tampering fails."""
import copy,json,tempfile,unittest
from pathlib import Path
import peer_reporting_relay as relay
ROOT=Path(__file__).resolve().parent
class RelayTests(unittest.TestCase):
    def binding(self,folder):
        cfg=relay.read(ROOT/'runtime/finite/configuration.json')
        replica=relay.server_path(cfg['replica_output']);cp=relay.read(replica/'checkpoint.json')
        row=dict(run_id=cfg['run_id'],phase='running',worker_metrics=dict(patches_per_second=0,error=None,gmp_audited_chunks=0),checkpoint=cp)
        relay.atomic(folder/'status.json',row)
        return dict(config=cfg,view=str(folder),spec=dict(source_identity=cp['identity']['source_identity']))
    def test_real_final_replica_becomes_terminal_without_changing_coverage(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            b=self.binding(Path(d));before=relay.read(relay.server_path(b['config']['replica_output'])/'checkpoint.json')
            relay.finalize_view(b);after=relay.read(Path(d)/'status.json')
            self.assertEqual(after['phase'],'stopped');self.assertEqual(after['checkpoint'],before)
            self.assertEqual(after['local_next_patch'],before['next_patch']);self.assertEqual(after['service']['ActiveState'],'inactive')
    def test_wrong_source_identity_is_rejected_before_view_replacement(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            b=self.binding(Path(d));raw=(Path(d)/'status.json').read_bytes();b['spec']['source_identity']='0'*64
            with self.assertRaises(RuntimeError):relay.finalize_view(b)
            self.assertEqual((Path(d)/'status.json').read_bytes(),raw)
if __name__=='__main__':unittest.main(verbosity=2)
