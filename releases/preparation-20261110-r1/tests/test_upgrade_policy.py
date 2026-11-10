"""CPU-only policy acceptance/rejection gates; no locks, GPU, or production I/O."""
from contextlib import ExitStack
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

UPGRADE = Path(__file__).resolve().parents[1]
CANDIDATE = UPGRADE / 'candidate/worker'
POLICY_PATH = CANDIDATE / 'cabbage_policy.py'
spec = importlib.util.spec_from_file_location('tested_upgrade_cabbage_policy', POLICY_PATH)
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)
FROZEN_CONFIG = None


class UpgradePolicyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='fifth42-upgrade-policy-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        source = FROZEN_CONFIG or CANDIDATE / 'base-config.json'
        self.config = json.loads(source.read_bytes())
        # A fresh frozen equivalent of the selected production policy. Expensive
        # lineage/output/source validation is checked separately by sealing.
        self.config.update(
            TEST_ONLY=False, run_id='cabbage-extended-policy-acceptance',
            initial_patch=1538849024, parent_selected_patches=1038849024,
            output=str(self.root / 'new-local/run'),
            replica_output=str(self.root / 'new-replica/run'),
            group_limit=8, dispatch_chunksize=2, preparation_windows=16,
            ready_queue_limit=1, preparation_backend='cpu', test_chunk_limit=None,
            stop_epoch=policy.DEADLINE,
            stop_local=policy.datetime.fromtimestamp(policy.DEADLINE, policy.timezone.utc).isoformat(),
        )

    def load(self, config=None, *, frozen=None):
        config = copy.deepcopy(self.config if config is None else config)
        base = config if frozen is None else frozen
        (self.root / 'base-config.json').write_text(json.dumps(base))
        path = self.root / 'configuration.json'
        path.write_text(json.dumps(config))
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(policy, 'ROOT', self.root))
            stack.enter_context(mock.patch.object(policy.os, 'uname', return_value=mock.Mock(nodename='cabbage')))
            stack.enter_context(mock.patch.object(policy.time, 'time', return_value=config['stop_epoch'] - 1000))
            checks = {
                name: stack.enter_context(mock.patch.object(policy, name))
                for name in ('validate_output', 'verify_sources', 'validate_parent', 'validate_ledger')
            }
            result = policy.load_config(path)
            for check in checks.values():
                check.assert_called_once_with(config)
        return result

    def reject(self, update, message=None):
        config = dict(self.config, **update)
        with self.assertRaisesRegex((RuntimeError, TypeError, ValueError), message or '.'):
            self.load(config)

    def test_selected_cpu_batch16_group8_production_policy_is_accepted(self):
        result = self.load()
        self.assertEqual((result['preparation_backend'], result['preparation_windows'],
                          result['group_limit'], result['dispatch_chunksize'],
                          result['ready_queue_limit']), ('cpu', 16, 8, 2, 1))

    def test_original_finite_test_allowed_changes_preserve_selected_policy(self):
        test = dict(self.config, TEST_ONLY=True, run_id='cabbage-extended-test-policy',
                    range_end=self.config['initial_patch'] + 256, test_chunk_limit=1,
                    stop_epoch=self.config['stop_epoch'] - 100,
                    stop_local=policy.datetime.fromtimestamp(self.config['stop_epoch'] - 100,
                                                             policy.timezone.utc).isoformat())
        result = self.load(test, frozen=self.config)
        self.assertTrue(result['TEST_ONLY'])
        self.assertEqual(result['preparation_windows'], 16)

    def test_frozen_production_config_cannot_be_overridden(self):
        changed = dict(self.config, group_limit=4)
        with self.assertRaisesRegex(RuntimeError, 'Production differs from frozen base'):
            self.load(changed, frozen=self.config)

    def test_testonly_cannot_change_preparation_or_resource_keys(self):
        for field, value in (
            ('preparation_windows', 1),
            ('ready_queue_limit', 3), ('dispatch_chunksize', 4),
            ('workers', 8), ('shell_lo', 100000000000), ('cap', 43),
        ):
            with self.subTest(field=field):
                changed = dict(self.config, TEST_ONLY=True,
                               run_id='cabbage-extended-test-policy', **{field: value})
                with self.assertRaisesRegex(RuntimeError, 'Test changed frozen'):
                    self.load(changed, frozen=self.config)

    def test_testonly_gpu_backend_override_is_finite_and_preserves_other_policy(self):
        changed = dict(self.config, TEST_ONLY=True,
                       run_id='cabbage-extended-test-policy-gpu',
                       preparation_backend='gpu', test_chunk_limit=2)
        accepted = self.load(changed, frozen=self.config)
        self.assertEqual(accepted['preparation_backend'], 'gpu')
        self.assertEqual(accepted['test_chunk_limit'], 2)
        for limit in (None, 0, 33):
            with self.subTest(limit=limit):
                invalid = dict(changed, test_chunk_limit=limit)
                with self.assertRaisesRegex(RuntimeError, '.'):
                    self.load(invalid, frozen=self.config)

    def test_all_tested_discrete_policies_are_accepted(self):
        for group in (1, 2, 4, 8, 16):
            with self.subTest(group=group):
                self.load(dict(self.config, group_limit=group))
        for windows in (1, 4, 16):
            with self.subTest(windows=windows):
                self.load(dict(self.config, preparation_windows=windows))
        for ready in (1, 2, 3):
            with self.subTest(ready=ready):
                self.load(dict(self.config, preparation_windows=1, ready_queue_limit=ready))
        for chunksize in (1, 2, 4, 8):
            with self.subTest(chunksize=chunksize):
                self.load(dict(self.config, dispatch_chunksize=chunksize))

    def test_bad_preparation_batch_and_group_bounds_are_rejected(self):
        for field, values in (
            ('preparation_windows', (0, -1, 2, 8, 17, 32)),
            ('group_limit', (0, -1, 3, 32)),
            ('dispatch_chunksize', (0, -1, 3, 16)),
            ('ready_queue_limit', (0, -1, 4, 16)),
        ):
            for value in values:
                with self.subTest(field=field, value=value):
                    self.reject({field: value})

    def test_large_preparation_batches_cannot_reserve_multiple_ready_batches(self):
        for windows in (4, 16):
            for ready in (2, 3):
                with self.subTest(windows=windows, ready=ready):
                    self.reject(dict(preparation_windows=windows, ready_queue_limit=ready),
                                'Bulk preparation queue exceeds tested memory budget')

    def test_bad_numeric_option_types_are_rejected_before_runtime(self):
        # JSON booleans and floats compare equal to ints in membership tests.
        # BulkStream requires an actual int, and range/map require integer steps.
        for field, value in (
            ('preparation_windows', 16.0), ('preparation_windows', True),
            ('group_limit', 8.0), ('group_limit', True),
            ('dispatch_chunksize', 2.0), ('dispatch_chunksize', True),
            ('ready_queue_limit', 1.0), ('ready_queue_limit', True),
        ):
            with self.subTest(field=field, value=value):
                self.reject({field: value})

    def test_invalid_preparation_backends_are_rejected(self):
        for backend in ('cuda', 'emulated', '', None, True, 0):
            with self.subTest(backend=backend):
                self.reject(dict(preparation_backend=backend), 'Unsupported preparation backend')

    def test_gpu_candidate_limits_keep_exact_quality_flag_typed(self):
        for quality in (False, True):
            with self.subTest(quality=quality):
                self.load(dict(self.config, preparation_backend='gpu',
                               preparation_gpu_capacity=128, preparation_require_lll=quality))
        for capacity in (0, 64, 129, 1024, 128.0):
            with self.subTest(capacity=capacity):
                self.reject(dict(preparation_backend='gpu', preparation_gpu_capacity=capacity),
                            'Unsupported GPU proposal policy')
        for quality in (0, 1, 'false', None):
            with self.subTest(quality=quality):
                self.reject(dict(preparation_backend='gpu', preparation_require_lll=quality),
                            'Unsupported GPU proposal policy')

    def test_memory_disk_journal_and_replication_guards_are_retained(self):
        for update in (
            dict(journal_buffer_records=9), dict(journal_buffer_bytes=16 * 1024**2),
            dict(journal_buffer_max_age_seconds=.5), dict(gpu_request_windows=2),
            dict(journal_limit_bytes=32 * 1024**3 + 1),
            dict(minimum_free_disk_bytes=16 * 1024**3 - 1),
            dict(replica_interval_seconds=61), dict(maximum_replica_lag_seconds=301),
            dict(gmp_audit_period=129), dict(automatic_resume=True),
        ):
            with self.subTest(update=update):
                self.reject(update)

    def test_existing_local_or_replica_output_prevents_reuse(self):
        for field in ('output', 'replica_output'):
            with self.subTest(field=field):
                path = self.root / (field + '-exists')
                path.mkdir()
                self.reject({field: str(path)}, 'Existing .* cannot be reused')

    def test_expired_or_changed_deadline_cannot_launch(self):
        self.reject(dict(stop_epoch=policy.DEADLINE + 1), 'Production deadline or endpoint changed')
        wrong = policy.datetime.fromtimestamp(policy.DEADLINE + 86400, policy.timezone.utc).isoformat()
        self.reject(dict(stop_local=wrong), 'Deadline changed or expired')


def main():
    global FROZEN_CONFIG
    arguments = sys.argv[1:]
    if '--frozen-config' in arguments:
        index = arguments.index('--frozen-config')
        FROZEN_CONFIG = Path(arguments[index + 1]).resolve()
        del arguments[index:index + 2]
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(UpgradePolicyTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = dict(
        status='passed' if result.wasSuccessful() else 'failed',
        tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        policy_path=str(POLICY_PATH),
        policy_sha256=hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest(),
        seed_config=str(FROZEN_CONFIG or CANDIDATE / 'base-config.json'),
        mocked_checks=['output mount/device/path', 'source hashing', 'parent sealing', 'NFS ledger'],
        assertions='Selected frozen CPU prep16/group8/chunks2/ready1 policy plus invalid option, queue-memory, resource, provenance-immutability, deadline and output-reuse rejection.',
        no_gpu=True, no_locks=True, production_modified=False,
        detailed_failures=[dict(test=str(test), traceback=trace) for test, trace in result.failures + result.errors],
    )
    if FROZEN_CONFIG is not None:
        # Exercise the actual bytes and actual ROOT/base binding before startup,
        # in addition to the temporary-root rejection matrix above.
        actual = json.loads(FROZEN_CONFIG.read_bytes())
        actual_root = Path(actual['manifest']).parent
        actual_policy_path = actual_root / 'cabbage_policy.py'
        actual_spec = importlib.util.spec_from_file_location('actual_frozen_upgrade_policy', actual_policy_path)
        actual_policy = importlib.util.module_from_spec(actual_spec)
        actual_spec.loader.exec_module(actual_policy)
        if hashlib.sha256(actual_policy_path.read_bytes()).digest() != hashlib.sha256(POLICY_PATH.read_bytes()).digest():
            raise AssertionError('Actual frozen policy differs from the candidate policy tested above')
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(actual_policy.time, 'time', return_value=actual['stop_epoch'] - 1000))
            checks = {name: stack.enter_context(mock.patch.object(actual_policy, name)) for name in
                      ('validate_output', 'verify_sources', 'validate_parent', 'validate_ledger')}
            accepted = actual_policy.load_config(FROZEN_CONFIG)
            for check in checks.values():
                check.assert_called_once_with(actual)
        if (accepted['preparation_backend'], accepted['preparation_windows'], accepted['group_limit'],
                accepted['dispatch_chunksize'], accepted['ready_queue_limit']) != ('cpu', 16, 8, 2, 1):
            raise AssertionError('Actual frozen production policy differs from selected CPU16/group8/chunks2/ready1')
        report['actual_frozen_policy_accepted'] = True
        report['actual_frozen_config_sha256'] = hashlib.sha256(FROZEN_CONFIG.read_bytes()).hexdigest()
        report['actual_frozen_policy_path'] = str(actual_policy_path)
    (UPGRADE / 'tests/POLICY_TEST_RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
