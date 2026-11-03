#!/usr/bin/env bash
# Explicit approved proposal: B=70 million, one GPU, four-hour search cap.
# Launch from the normal GPU-visible Ada terminal. No login shell is needed.
set -euo pipefail
task_directory=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd -- "$task_directory"
mkdir -p runs

if [[ "${1:-}" == --dry-run ]]; then
    printf '%s\n' \
        'Detached preparation: make test-gpu (five-minute validation cap)' \
        'Then: python3 calibrate.py (internally budgeted calibration)' \
        'Then: python3 jobs.py start --bound 70000000 --hours 4 --approve --job runs/gpu-B70000000' \
        'Any failed check stops the sequence. No job was started by this dry run.'
    exit 0
fi

if [[ "${1:-}" == --worker ]]; then
    exec 9>runs/startup-B70000000.lock
    flock -n 9 || { printf '%s\n' 'Another startup is already running.'; exit 1; }
    [[ ! -e runs/gpu-B70000000 ]] || { printf '%s\n' 'Job directory already exists; inspect its status instead of launching again.'; exit 1; }
    trap 'result=$?; printf "Startup ended: exit=%s at %s\n" "$result" "$(date -Is)"' EXIT
    printf 'Starting detached validation at %s\n' "$(date -Is)"
    timeout --signal=TERM --kill-after=10s 300s make test-gpu
    python3 calibrate.py
    python3 jobs.py start --bound 70000000 --hours 4 --approve --job runs/gpu-B70000000
    exit 0
fi

[[ $# == 0 ]] || { printf '%s\n' 'Usage: bash start_background.sh [--dry-run]'; exit 2; }
[[ ! -e runs/gpu-B70000000 ]] || { printf '%s\n' 'Job directory already exists; use jobs.py status.'; exit 1; }
command -v nohup >/dev/null
command -v setsid >/dev/null
command -v flock >/dev/null
nohup setsid bash "$task_directory/start_background.sh" --worker \
    >>runs/startup-B70000000.log 2>&1 </dev/null &
printf 'Detached startup PID: %s\n' "$!"
printf 'Startup log: %s/runs/startup-B70000000.log\n' "$task_directory"
printf '%s\n' 'You can now close this terminal or disconnect. Ada must remain powered on and awake.'
