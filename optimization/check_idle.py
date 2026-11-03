#!/usr/bin/env python3
"""Refuse an optimization GPU workload while the baseline run owns its lock."""
import fcntl
from pathlib import Path
import sys

def ensure_idle():
    lock=Path(__file__).resolve().parent.parent/'runs/gpu-B35000000/.lock'
    if not lock.exists():return
    with lock.open() as f:
        try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Baseline search is still running; do not overlap GPU validation or benchmarks.') from None

if __name__=='__main__':
    try:ensure_idle()
    except RuntimeError as e:
        print(f'ERROR: {e}',file=sys.stderr)
        sys.exit(1)
