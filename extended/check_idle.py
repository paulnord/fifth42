#!/usr/bin/env python3
import fcntl
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
def ensure_idle():
    for p in (ROOT/'runs/.gpu-job.lock',ROOT.parent/'runs/gpu-B35000000/.lock'):
        if not p.exists():continue
        with p.open() as f:
            try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:raise RuntimeError('A search is already running; do not overlap GPU work') from None
if __name__=='__main__':
    try:ensure_idle()
    except RuntimeError as e:print(f'ERROR: {e}',file=sys.stderr);sys.exit(1)
