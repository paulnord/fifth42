"""Boole's current controller selects the collector after a revision change."""
import importlib.util,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('current_relay',Path(__file__).with_name('peer_reporting_relay_r3.py'))
relay=importlib.util.module_from_spec(spec);spec.loader.exec_module(relay)
class RoutingTests(unittest.TestCase):
 def test_new_controller_share_wins_over_existing_old_collector(self):
  with patch.object(relay,'read',return_value={'collector_share':'/mnt/nfs_share/boole-preparation-publishing-20261110'}):
   self.assertEqual(relay.boole_share(),Path('/mnt/nfs_share/boole-preparation-publishing-20261110'))
 def test_legacy_controller_remains_supported(self):
  with patch.object(relay,'read',return_value={'collector_share':str(relay.DELEGATED)}):self.assertEqual(relay.boole_share(),relay.DELEGATED)
 def test_unadmitted_location_is_rejected(self):
  with patch.object(relay,'read',return_value={'collector_share':'/mnt/nfs_share/unverified-collector'}):
   with self.assertRaises(RuntimeError):relay.boole_share()
if __name__=='__main__':unittest.main(verbosity=2)
