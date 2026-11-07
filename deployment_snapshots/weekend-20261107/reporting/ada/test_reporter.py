"""Exercise publication against disposable Git repositories, never the search."""
import importlib.util
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


class ReporterChecks(unittest.TestCase):
    def saved_fixture(self):
        run=self.base/'fixture-run';run.mkdir()
        output=run/'shared-output';output.mkdir()
        self.module.RUN=run;self.module.RUN_ID='fixture'
        config=dict(run_id='fixture',output=str(output),initial_patch=500,parent_selected_patches=1000,
                    stop_local='2026-11-09T09:00:00-06:00',stop_epoch=1794236400,workers=16,
                    geometry_policy='adaptive',ledger_root='/example/shared',ledger_claim_sha256='c'*64,
                    coverage_sha256='d'*64)
        raw=(json.dumps(config)+'\n').encode();(run/'config.json').write_bytes(raw)
        checkpoint=dict(identity=dict(trial='fixture',source_identity='a'*64),next_patch=756,
                        patches=256,chunks=1,points=1000,hits=[],completed_bound=None)
        metrics=dict(status='running',updated_utc=datetime.now(timezone.utc).isoformat(),patches=256,
                     chunks=1,patches_per_second=256,search_seconds=1,gmp_audited_chunks=1,
                     preparation_pacing_seconds=0,independent_oracle_verified_through=0,
                     reason=None,error=None,source_identity='a'*64,run_id='fixture')
        supervisor=dict(status='running',updated_utc=metrics['updated_utc'],error=None,
                        config_sha256=hashlib.sha256(raw).hexdigest())
        for path,row in ((output/'checkpoint.json',checkpoint),(output/'status.json',metrics),
                         (run/'supervisor-report.json',supervisor),
                         (run/'gpu-validation-report.json',dict(status='passed',speedup=2.5,
                           median_patches_per_second=dict(baseline=1000,adaptive=2500)))):
            path.write_text(json.dumps(row)+'\n')
        for name in ('worker.stderr.log','service.stderr.log'):(run/name).write_text('')
        return output

    def test_adaptive_snapshot_counts_lineage_and_formats_actual_cursor(self):
        self.saved_fixture()
        service=dict(ActiveState='active',SubState='running',MainPID='1',ActiveEnterTimestamp='test time')
        with patch.object(self.module,'show',return_value=service):
            row=self.module.snapshot()
        self.assertEqual(row['combined_selected_patches'],1256)
        text=self.module.markdown(row)
        self.assertIn('1,256',text)
        self.assertIn('verified cursor **500**',text)
        self.assertIn('2.50x',text)
        self.assertIn('selected partial patch coverage',text)

    def test_snapshot_rejects_mixed_source_and_inconsistent_committed_totals(self):
        output=self.saved_fixture();path=output/'checkpoint.json';original=json.loads(path.read_text())
        for edit in (dict(identity=dict(trial='fixture',source_identity='b'*64)),dict(next_patch=757)):
            path.write_text(json.dumps(dict(original,**edit)))
            with self.assertRaises(ValueError):self.module.snapshot()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        spec = importlib.util.spec_from_file_location(
            'reporter_under_test', Path(__file__).with_name('weekend_reporter.py'))
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.module.ROOT = self.base / 'publisher'
        self.module.ROOT.mkdir()
        self.module.REMOTE = str(self.base / 'remote.git')
        self.module.BRANCH = 'test-progress'
        self.seed = self.base / 'seed'
        self.command('init', '--bare', self.module.REMOTE)
        self.command('init', '-b', self.module.BRANCH, str(self.seed))
        legacy = self.seed / self.module.LEGACY
        legacy.parent.mkdir(parents=True)
        legacy.write_text('Historical overnight report.\n')
        (self.seed / 'unrelated.txt').write_text('Preserve me.\n')
        self.seed_commit('Initial report')

    def command(self, *args, cwd=None):
        return subprocess.run(
            ['git', '-c', 'user.name=Reporter test', '-c', 'user.email=test@example.invalid', *args],
            cwd=cwd, capture_output=True, text=True, check=True, timeout=10).stdout

    def seed_commit(self, message):
        self.command('add', '.', cwd=self.seed)
        self.command('commit', '-m', message, cwd=self.seed)
        self.command('push', self.module.REMOTE, self.module.BRANCH, cwd=self.seed)

    def remote_file(self, path):
        return self.command('--git-dir', self.module.REMOTE,
                            'show', f'{self.module.BRANCH}:{path}')

    def test_publish_preserves_history_and_adds_only_one_link(self):
        files = {self.module.PUBLIC + '/STATUS.md': 'Weekend snapshot one.\n'}
        first = self.module.push_files(files, 'First snapshot')
        files[self.module.PUBLIC + '/STATUS.md'] = 'Weekend snapshot two.\n'
        second = self.module.push_files(files, 'Second snapshot')
        parent = self.command('--git-dir', self.module.REMOTE,
                              'rev-parse', second + '^').strip()
        self.assertEqual(parent, first)
        self.assertEqual(self.remote_file('unrelated.txt'), 'Preserve me.\n')
        legacy = self.remote_file(self.module.LEGACY)
        self.assertEqual(legacy.count('<!-- current-weekend-search -->'), 1)
        self.assertTrue(legacy.endswith('Historical overnight report.\n'))
        self.assertEqual(self.remote_file(self.module.PUBLIC + '/STATUS.md'),
                         'Weekend snapshot two.\n')

    def test_concurrent_remote_update_is_preserved_on_retry(self):
        original_git = self.module.git
        pushes = []

        def git_with_concurrent_update(*args, **kwargs):
            if args[0] == 'push':
                pushes.append(args)
                if len(pushes) == 1:
                    (self.seed / self.module.LEGACY).write_text('Concurrent historical correction.\n')
                    (self.seed / 'unrelated.txt').write_text('Concurrent new work.\n')
                    self.seed_commit('Concurrent writer')
            return original_git(*args, **kwargs)

        with patch.object(self.module, 'git', git_with_concurrent_update):
            self.module.push_files({self.module.PUBLIC + '/STATUS.md': 'Progress.\n'}, 'Progress')
        self.assertEqual(len(pushes), 2)
        self.assertTrue(self.remote_file(self.module.LEGACY).endswith(
            'Concurrent historical correction.\n'))
        self.assertEqual(self.remote_file('unrelated.txt'), 'Concurrent new work.\n')
        self.assertFalse(any('--force' in arg or arg.startswith('+') for args in pushes for arg in args))

    def test_failed_push_does_not_create_success_receipt(self):
        original_git = self.module.git

        def failing_git(*args, **kwargs):
            if args[0] == 'push':
                return subprocess.CompletedProcess(args, 128, '', 'simulated transport failure')
            return original_git(*args, **kwargs)

        row = {'snapshot_utc': '2026-11-07T21:00:00+00:00', 'phase': 'running',
               'checkpoint': {'next_patch': 4000000000}}
        with patch.object(self.module, 'git', failing_git), \
             patch.object(self.module, 'markdown', return_value='Disposable snapshot.\n'):
            with self.assertRaisesRegex(RuntimeError, 'transport failure'):
                self.module.publish(row)
        self.assertFalse((self.module.ROOT / 'last-push.json').exists())
        self.assertEqual(self.remote_file('unrelated.txt'), 'Preserve me.\n')

    def test_loop_publishes_final_snapshot_and_exits(self):
        ticks = [0]
        snapshots = iter([{'phase': 'running'}, {'phase': 'stopped'}, {'phase': 'stopped'}])
        clock = SimpleNamespace(time=lambda: 1794077000 + ticks[0],
                                monotonic=lambda: ticks[0],
                                sleep=lambda seconds: ticks.__setitem__(0, ticks[0] + seconds))
        published = []
        with patch('sys.argv', ['weekend_reporter.py']), \
             patch.object(self.module, 'snapshot', lambda: next(snapshots)), \
             patch.object(self.module, 'publish', lambda row: published.append(row)), \
             patch.object(self.module, 'time', clock):
            self.assertEqual(self.module.main(), 0)
        self.assertEqual([row['phase'] for row in published], ['running', 'stopped'])
        self.assertEqual(ticks[0], 60)

    def test_reporting_deadline_stops_failed_retries(self):
        clock = SimpleNamespace(time=lambda: self.module.FINAL_LIMIT + 1)
        with patch('sys.argv', ['weekend_reporter.py']), \
             patch.object(self.module, 'snapshot', side_effect=OSError('read failed')), \
             patch.object(self.module, 'time', clock):
            self.assertEqual(self.module.main(), 3)
        self.assertFalse((self.module.ROOT / 'last-push.json').exists())


if __name__ == '__main__':
    unittest.main()
