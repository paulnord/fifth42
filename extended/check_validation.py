#!/usr/bin/env python3
"""Check saved validation only; never run a GPU kernel or alter the report."""
import json
from pathlib import Path
import sys
import run
ROOT=Path(__file__).resolve().parent
def current():
    expected=run.fingerprint('gpu')
    try:
        reports=[json.loads((ROOT/'runs'/name).read_text()) for name in ('validation.json','optimized-validation.json')]
    except (OSError,ValueError):return False
    return all(r.get('gpu_status')=='passed' and r.get('gpu_fingerprint')==expected for r in reports)
if __name__=='__main__':
    try:sys.exit(0 if current() else 1)
    except OSError:sys.exit(1)
