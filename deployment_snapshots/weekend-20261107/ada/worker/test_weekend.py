"""Weekend allocation, unchanged non-CPU guards, disk budget and fixed stop."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import launch_weekend
import policy
import search_supervisor

ROOT=Path(__file__).resolve().parent


class WeekendTests(unittest.TestCase):
    def test_cpu_budget_preserves_competing_work_and_memory_checks(self):
        resources=mock.Mock()
        resources.blockers.return_value=['CPU load exceeds idle threshold','busy lock: other','less than 4 GiB memory available']
        with mock.patch.object(search_supervisor.os,'getloadavg',return_value=(16,0,0)):
            self.assertEqual(search_supervisor.resource_blockers(resources,[],dict(running_load_limit=20)),
                             ['busy lock: other','less than 4 GiB memory available'])
        with mock.patch.object(search_supervisor.os,'getloadavg',return_value=(20.1,0,0)):
            self.assertIn('CPU load exceeds weekend running budget',
                          search_supervisor.resource_blockers(resources,[],dict(running_load_limit=20)))

    def test_weekend_journal_can_pass_four_gib_and_stops_at_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);journal=folder/'coverage.jsonl'
            config=dict(journal_limit_bytes=96*1024**3,minimum_free_disk_bytes=4*1024**3)
            with journal.open('wb') as stream:stream.truncate(5*1024**3)
            with mock.patch.object(policy.shutil,'disk_usage',return_value=SimpleNamespace(free=100*1024**3)):
                policy.check_storage(config,folder)
                with journal.open('r+b') as stream:stream.truncate(config['journal_limit_bytes'])
                with self.assertRaisesRegex(policy.RequestedStop,'byte budget'):policy.check_storage(config,folder)
            with mock.patch.object(policy.shutil,'disk_usage',return_value=SimpleNamespace(free=3*1024**3)):
                with self.assertRaisesRegex(policy.RequestedStop,'disk reserve'):policy.check_storage(config,folder)

    def test_monday_deadline_and_timer_cleanup_margin(self):
        config=json.loads((ROOT/'config.json').read_text())
        self.assertEqual(config['stop_local'],'2026-11-09T09:00:00-06:00')
        plan=launch_weekend.commands(config,now=config['stop_epoch']-3600)
        self.assertEqual(plan['cleanup_starts_utc'],'2026-11-09 14:59:50 UTC')
        self.assertEqual(plan['runtime_max_seconds'],3590)
        self.assertIn('--property=CPUAffinity=0-15',plan['service'])
        self.assertIn('--property=Restart=no',plan['service'])
        self.assertIn('--timer-property=Persistent=no',plan['timer'])

    def test_actual_configuration_requires_sixteen_workers(self):
        original=json.loads((ROOT/'config.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'config.json'
            path.write_text(json.dumps(dict(original,workers=4)))
            with self.assertRaisesRegex(RuntimeError,'workers'):policy.load_config(path)


if __name__=='__main__':unittest.main(verbosity=2)
