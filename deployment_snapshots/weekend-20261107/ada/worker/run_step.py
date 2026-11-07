"""Run one manually selected scratch step with source hashes and continuous leases."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
HANDOFF = Path('/home/pnord/fifth42-low64-review-20261106/handoff')
PYTHON = '/home/pnord/fifth-lattice-optimizations-ada-20261105/venv/bin/python'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('name')
    p.add_argument('seconds', type=int)
    p.add_argument('command', nargs=argparse.REMAINDER)
    args = p.parse_args()
    if not args.name.replace('-', '').isalnum() or not 1 <= args.seconds <= 600:
        p.error('Invalid step name or bounded allowance')
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        p.error('Supply the explicit command')
    manifest = json.loads((ROOT/'gate-source-sha256.json').read_text())
    for name, digest in manifest.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Gate source changed: '+name)
    subprocess.run(['sha256sum', '--status', '-c', 'SHA256SUMS'], cwd=HANDOFF,
                   check=True, timeout=30)
    steps = ROOT/'steps'
    steps.mkdir(exist_ok=True)
    folder = steps/args.name
    if folder.exists():
        raise FileExistsError(folder)
    environment = dict(os.environ, PATH=str(ROOT/'toolchain/bin')+os.pathsep+os.environ['PATH'],
                       NVCC='/usr/local/cuda-13.4/bin/nvcc', CUDA_ARCH='sm_86',
                       PYTHONDONTWRITEBYTECODE='1')
    launch = dict(command=command, seconds=args.seconds, automatic_resume=False,
                  time_utc=datetime.now(timezone.utc).isoformat(), nvcc=environment['NVCC'],
                  cuda_arch=environment['CUDA_ARCH'], compiler='/usr/bin/g++-13',
                  gate_source_sha256=manifest)
    with (steps/(args.name+'-launch.json')).open('x') as stream:
        json.dump(launch, stream, indent=2)
        stream.write('\n')
    invocation = [PYTHON, '-B', str(ROOT/'ada_guard_retired_service.py'),
                  '--bundle', str(HANDOFF/'bundle'), '--retirement-record', str(ROOT/'retirement-record.json'),
                  '--seconds', str(args.seconds), '--output', str(folder), '--', *command]
    began = time.monotonic()
    result = subprocess.run(invocation, env=environment, capture_output=True, text=True)
    (steps/(args.name+'-driver.stdout.txt')).write_text(result.stdout)
    (steps/(args.name+'-driver.stderr.txt')).write_text(result.stderr)
    report_path = folder/'guard-report.json'
    report = json.loads(report_path.read_text()) if report_path.is_file() else {}
    print(json.dumps(dict(step=args.name, exit_code=result.returncode,
                          guard_status=report.get('status'), error=report.get('error'),
                          wall_seconds=time.monotonic()-began)), flush=True)
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
