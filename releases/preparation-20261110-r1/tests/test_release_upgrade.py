"""Isolated freeze/rotation regressions; all runtime paths map into temp storage."""
import argparse
import ast
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

UPGRADE=Path(__file__).resolve().parents[1]
DEFAULT_RELEASE=Path('/home/pnord/scratch/cabbage-extended-upgrade-20261110/release.py')
SELECTED=dict(preparation_backend='cpu',preparation_windows=16,group_limit=8,
              dispatch_chunksize=2,ready_queue_limit=1,gpu_request_windows=1)
DEADLINE=1794438000
STOP_LOCAL='2026-11-11T17:00:00-06:00'
REPORT=[]
RELEASE_FILE=DEFAULT_RELEASE


def stable_bytes(value):
    return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_release():
    spec=importlib.util.spec_from_file_location('isolated_upgrade_release',RELEASE_FILE)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


class FreezeRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='fifth42-freeze-regression-')
        self.root=Path(self.temp.name)
        self.release=load_release()
        self.template=self.root/'template';worker=self.template/'worker';worker.mkdir(parents=True)
        actual_policy=UPGRADE/'candidate/worker/cabbage_policy.py'
        (worker/'cabbage_policy.py').write_bytes(actual_policy.read_bytes())
        (worker/'packed_worker.py').write_text('# isolated immutable runtime fixture\n')
        (worker/'source').mkdir();(worker/'source/scientific.py').write_text('BASELINE = 42\n')
        (worker/'base-config.json').write_text('{"stale":true}\n')
        (worker/'release-manifest.json').write_text('{"stale":true}\n')
        for path in worker.rglob('*'):
            if path.is_file():path.chmod(0o400)
        self.fixture=self.root/'previous';self.fixture.mkdir()
        coverage=dict(contract='exact original reservation proof',first=500000000,last=2250000000)
        coverage_raw=b'{ "contract": "exact original reservation proof", "first": 500000000, "last": 2250000000 }\n'
        coverage_file=self.fixture/'reservation-proof.json';coverage_file.write_bytes(coverage_raw)
        claim=dict(job='cabbage-extended-allocation-20261109',first=500000000,last=2250000000,
            identity='a'*64,sha256='b'*64,
            coverage=dict(sha256=sha(coverage_file),manifest=coverage))
        claim_file=self.fixture/'claim.json';claim_file.write_text(json.dumps(claim,separators=(', ',': '))+'\n\n')
        manifest=self.fixture/'release-manifest.json'
        manifest.write_bytes(stable_bytes(dict(status='sealed_baseline',files={'scientific.py':'c'*64},baseline_identity='original-tested-baseline')))
        self.previous=self.fixture/'production-config.json'
        self.old=dict(SELECTED,run_id='cabbage-extended-previous',initial_patch=1538800000,
            manifest=str(manifest),manifest_sha256=sha(manifest),
            origin_claim_file=str(claim_file),coverage_file=str(coverage_file),
            shell_lo=100000000001,shell_hi=200000000000,width=8,bits=222,cap=42,
            chunk_patches=256,geometry_policy='adaptive',workers=16,physical_cpus=list(range(16)),
            replica_interval_seconds=60,maximum_replica_lag_seconds=300,
            journal_buffer_records=8,journal_buffer_bytes=8388608,journal_buffer_max_age_seconds=.25,
            automatic_resume=False,stop_epoch=1794351600,stop_local='2026-11-10T17:00:00-06:00')
        self.previous.write_bytes(stable_bytes(self.old))
        self.archive=self.root/'sealed-archive';self.archive.mkdir()
        raw=b'{"payload":"sealed committed fixture"}\n'
        (self.archive/'coverage.jsonl').write_bytes(raw)
        self.checkpoint=dict(identity=dict(trial='sealed-parent',source_identity='d'*64),
            next_patch=1538849024,journal_sha256=hashlib.sha256(raw).hexdigest(),journal_offset=len(raw),completed_bound=None)
        (self.archive/'checkpoint.json').write_bytes(stable_bytes(self.checkpoint))
        (self.archive/'status.json').write_bytes(stable_bytes(dict(status='stopped',error=None,next_patch=self.checkpoint['next_patch'])))
        receipt=dict(status='verified',source_closed=True,source_retained=True,
            raw_sha256=hashlib.sha256(raw).hexdigest(),committed_bytes=len(raw),
            captured_checkpoint_sha256=sha(self.archive/'checkpoint.json'))
        (self.archive/'ARCHIVE_RECEIPT.json').write_bytes(stable_bytes(receipt))
        audit=dict(status='passed',final_checkpoint=True,uncommitted_trailing_bytes=0,
            committed_raw_sha256=hashlib.sha256(raw).hexdigest(),
            committed_chain_sha256=self.checkpoint['journal_sha256'],committed_bytes=len(raw),
            captured_checkpoint_sha256=sha(self.archive/'checkpoint.json'),
            selected_interval=[self.old['initial_patch'],self.checkpoint['next_patch']])
        self.seal=dict(checkpoint=self.checkpoint,archive=str(self.archive),audit=audit,receipt=receipt)
        self.original_hashes={str(path.relative_to(worker)):sha(path)
            for path in worker.rglob('*') if path.is_file()}
        self.live_prefixes=(Path('/home/pnord/fifth42-local-runs'),Path('/mnt/fifth42-storage'))
        self.path_accesses=[]

    def tearDown(self):
        self.temp.cleanup()

    def mapped_path(self,value='.'):
        path=Path(value)
        for index,prefix in enumerate(self.live_prefixes):
            if path.is_relative_to(prefix):
                mapped=self.root/f'mapped-runtime-{index}'/path.relative_to(prefix)
                self.path_accesses.append((str(path),str(mapped)))
                return mapped
        self.assertTrue(path.is_relative_to(self.root),f'Unexpected path outside isolated fixture: {path}')
        return path

    def freeze(self,run,claim=None,coverage=None):
        target=self.root/run
        with patch.object(self.release,'ROOT',self.template),patch.object(self.release,'Path',self.mapped_path):
            path=self.release.freeze(target,self.previous,self.seal,claim,coverage)
        return target,Path(path)

    def assert_frozen(self,target,path,original,initial,fresh):
        config=json.loads(path.read_bytes());worker=target/'worker'
        self.assertEqual(config,json.loads((worker/'base-config.json').read_bytes()))
        for key,value in SELECTED.items():self.assertEqual(config[key],value,key)
        self.assertEqual(config['initial_patch'],initial)
        self.assertEqual(config['range_end'],original['last'])
        self.assertEqual(config['ledger_job'],original['job'])
        self.assertEqual(config['ledger_claim_sha256'],original['sha256'])
        self.assertEqual(config['reservation_manifest_sha256'],original['identity'])
        self.assertEqual(config['reservation_initial_patch'],original['first'])
        self.assertEqual(config['parent_final_cursor'],self.checkpoint['next_patch'])
        self.assertEqual(config['parent_selected_patches'],0 if fresh else initial-original['first'])
        self.assertEqual(config['fresh_reservation'],fresh)
        self.assertEqual(config['stop_epoch'],DEADLINE)
        self.assertEqual(config['stop_local'],STOP_LOCAL)
        self.assertEqual(config['parent_identity'],self.checkpoint['identity'])
        self.assertEqual(config['parent_checkpoint_sha256'],sha(self.archive/'checkpoint.json'))
        self.assertEqual(config['parent_status_sha256'],sha(self.archive/'status.json'))
        self.assertEqual(config['parent_journal_sha256'],self.checkpoint['journal_sha256'])
        self.assertEqual(config['parent_journal_raw_sha256'],sha(self.archive/'coverage.jsonl'))
        self.assertEqual(config['parent_journal_offset'],(self.archive/'coverage.jsonl').stat().st_size)
        self.assertEqual(config['parent_archive_receipt_sha256'],sha(self.archive/'ARCHIVE_RECEIPT.json'))
        st=(self.archive/'coverage.jsonl').stat()
        self.assertEqual(config['parent_journal_identity'],[st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns])
        manifest=json.loads((worker/'release-manifest.json').read_bytes())
        self.assertEqual(manifest['predecessor_manifest_sha256'],self.old['manifest_sha256'])
        self.assertEqual(manifest['baseline_identity'],'original-tested-baseline')
        self.assertEqual(manifest['authorized_deadline'],STOP_LOCAL)
        self.assertEqual(sha(worker/'release-manifest.json'),config['manifest_sha256'])
        for name,digest in manifest['files'].items():self.assertEqual(sha(worker/name),digest,name)
        policy_constants={}
        for node in ast.parse((worker/'cabbage_policy.py').read_text()).body:
            if isinstance(node,ast.Assign):
                for name in node.targets:
                    if isinstance(name,ast.Name) and name.id in ('JOB','CLAIM','RESERVATION','FIRST','LAST','DEADLINE'):
                        policy_constants[name.id]=ast.literal_eval(node.value)
        self.assertEqual(policy_constants,dict(JOB=original['job'],CLAIM=original['sha256'],
            RESERVATION=original['identity'],FIRST=original['first'],LAST=original['last'],DEADLINE=DEADLINE))
        for file in (path,worker/'release-manifest.json',worker/'base-config.json'):
            self.assertEqual(stat.S_IMODE(file.stat().st_mode),0o400)
        self.assertTrue(Path(config['output']).is_relative_to(self.root/'mapped-runtime-0'))
        self.assertTrue(Path(config['replica_output']).is_relative_to(self.root/'mapped-runtime-1'))
        self.assertTrue(Path(config['output']).parent.is_dir())
        self.assertFalse(Path(config['output']).exists())
        self.assertTrue(Path(config['replica_output']).parent.is_dir())
        self.assertFalse(Path(config['replica_output']).exists())
        self.assertGreater(len(self.path_accesses),0)
        for name,digest in self.original_hashes.items():
            self.assertEqual(sha(self.template/'worker'/name),digest,'Template mutated')
            self.assertEqual(stat.S_IMODE((self.template/'worker'/name).stat().st_mode),0o400)
        REPORT.append(dict(test=self._testMethodName,status='passed',fresh_reservation=fresh,
            selected_settings=SELECTED,deadline=DEADLINE,initial_patch=initial,
            reservation=[original['first'],original['last']],archive_provenance_verified=True,
            immutable_template_unchanged=True,live_data_paths_remapped=True))
        return config

    def test_readonly_template_rotation_preserves_selection_and_archive(self):
        original=json.loads(Path(self.old['origin_claim_file']).read_bytes())
        target,path=self.freeze('cabbage-extended-upgrade-rotation-test')
        self.assert_frozen(target,path,original,self.checkpoint['next_patch'],False)
        for name,key in [('origin-claim.json','origin_claim_file'),('reservation-metadata.json','coverage_file')]:
            self.assertEqual((target/'worker'/name).read_bytes(),Path(self.old[key]).read_bytes())

    def test_fresh_claim_updates_job_range_and_policy_without_losing_baseline(self):
        coverage=dict(contract='fresh isolated exact reservation',first=2250000000,last=2300000000)
        claim=dict(job='cabbage-extended-allocation-20261110',first=2250000000,last=2300000000,
            identity='e'*64,sha256='f'*64,
            coverage=dict(sha256=hashlib.sha256(stable_bytes(coverage)).hexdigest(),manifest=coverage))
        target,path=self.freeze('cabbage-extended-upgrade-fresh-test',claim,coverage)
        self.assert_frozen(target,path,claim,claim['first'],True)
        self.assertEqual((target/'worker/reservation-metadata.json').read_bytes(),stable_bytes(coverage))

    def test_reused_run_directory_rejects_without_reusing_output(self):
        target,path=self.freeze('cabbage-extended-upgrade-duplicate-test')
        before=sha(path)
        with self.assertRaises(FileExistsError):
            self.freeze(target.name)
        self.assertEqual(sha(path),before)
        config=json.loads(path.read_bytes())
        self.assertFalse(Path(config['output']).exists())
        self.assertFalse(Path(config['replica_output']).exists())


def main():
    global RELEASE_FILE
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release',type=Path,default=DEFAULT_RELEASE)
    parser.add_argument('--output',type=Path,default=UPGRADE/'evidence/release-freeze-regression.json')
    args=parser.parse_args();RELEASE_FILE=args.release
    log=io.StringIO()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(FreezeRegressionTests)
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    report=dict(status='passed' if result.wasSuccessful() else 'failed',TEST_ONLY=True,
        GPU_used=False,live_data_or_ledger_modified=False,tests_run=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),results=REPORT,
        release_source=str(RELEASE_FILE),release_source_sha256=sha(RELEASE_FILE) if RELEASE_FILE.exists() else None,
        test_source_sha256=sha(Path(__file__)),unittest_log=log.getvalue())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(log.getvalue(),end='')
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':raise SystemExit(main())
