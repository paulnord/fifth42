"""Produce a reviewable launch record after validation and explicit schedule selection."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent
WORKER = ROOT / 'worker'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    cfg = json.loads((WORKER / 'config.json').read_bytes())
    runtime = json.loads((ROOT / 'runtime-validation.json').read_bytes())
    gpu = json.loads((ROOT / 'gpu-validation.json').read_bytes())
    units = json.loads((ROOT / 'unit-validation.json').read_bytes())
    assert all(x['status'] == 'passed' for x in (runtime, gpu, units))
    assert runtime['manifest_sha256'] == cfg['manifest_sha256'] == sha(WORKER / 'release-manifest.json')
    assert not Path(cfg['output']).exists() and cfg['stop_epoch'] > time.time() + 120
    assert json.loads((ROOT / 'configuration-state.json').read_bytes())['status'] == 'production_configured'
    report = dict(status='ready', prepared_utc=datetime.now(timezone.utc).isoformat(),
                  manifest_sha256=cfg['manifest_sha256'], config_sha256=sha(WORKER / 'config.json'),
                  initial_patch=cfg['initial_patch'], stop_local=cfg['stop_local'],
                  root_reuse_enabled=True, original_reservation_inherited=True,
                  parent_checkpoint_sha256=cfg['parent_checkpoint_sha256'],
                  parent_audit_sha256=cfg['parent_audit_sha256'],
                  runtime_validation_sha256=sha(ROOT / 'runtime-validation.json'),
                  gpu_validation_sha256=sha(ROOT / 'gpu-validation.json'),
                  unit_validation_sha256=sha(ROOT / 'unit-validation.json'),
                  automatic_resume=False, production_started=False)
    (WORKER / 'preparation-report.json').write_text(json.dumps(report, indent=2) + '\n')
    (ROOT / 'READY.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
