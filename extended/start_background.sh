#!/usr/bin/env bash
# Explicit user-selected bound/time; default remains the original 70m/4h proposal.
set -euo pipefail
task_directory=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd -- "$task_directory"
mkdir -p runs
bound=70000000
hours=4
mode=launch
while [[ $# -gt 0 ]]; do
    case "$1" in
        --bound) [[ $# -ge 2 ]] || exit 2; bound=$2; shift 2 ;;
        --hours) [[ $# -ge 2 ]] || exit 2; hours=$2; shift 2 ;;
        --worker) mode=worker; shift ;;
        --dry-run) mode=dry; shift ;;
        *) printf 'Unknown option: %s\n' "$1"; exit 2 ;;
    esac
done
[[ "$bound" =~ ^[1-9][0-9]*$ && "$hours" =~ ^[1-9][0-9]*$ ]] || { printf '%s\n' 'Use positive whole-number bounds and hours.'; exit 2; }
(( bound <= 100000000 && hours <= 24 )) || exit 2
job="runs/gpu-B${bound}"
log="runs/startup-B${bound}.log"
if [[ "$mode" == dry ]]; then
    printf '%s\n' 'Reuse current GPU validation, or validate with a five-minute cap.' 'Resume only missing calibration samples with a 30-second attempt budget.'
    printf 'Then launch B=%s with a %s-hour cap in %s, subject to the calibrated budget check.\n' "$bound" "$hours" "$job"
    printf '%s\n' 'No job was started by this dry run.'
    exit 0
fi
if [[ "$mode" == worker ]]; then
    exec 9>"runs/startup-B${bound}.lock"
    flock -n 9 || { printf '%s\n' 'Another startup is already running.'; exit 1; }
    [[ ! -e "$job" ]] || { printf '%s\n' 'Job directory already exists; inspect its status.'; exit 1; }
    trap 'result=$?; printf "Startup ended: exit=%s at %s\n" "$result" "$(date -Is)"' EXIT
    printf 'Detached startup for B=%s, cap=%sh at %s\n' "$bound" "$hours" "$(date -Is)"
    if python3 check_validation.py; then
        printf '%s\n' 'Reusing passing GPU validation for these exact sources/binaries.'
    else
        timeout --signal=TERM --kill-after=10s 300s make test-gpu
    fi
    python3 calibrate.py
    python3 jobs.py start --bound "$bound" --hours "$hours" --approve --job "$job"
    exit 0
fi
[[ ! -e "$job" ]] || { printf '%s\n' 'Job directory already exists; use jobs.py status.'; exit 1; }
command -v nohup >/dev/null
command -v setsid >/dev/null
command -v flock >/dev/null
nohup setsid bash "$task_directory/start_background.sh" --worker --bound "$bound" --hours "$hours" \
    >>"$log" 2>&1 </dev/null &
printf 'Detached startup PID: %s\n' "$!"
printf 'Startup log: %s/%s\n' "$task_directory" "$log"
printf '%s\n' 'You can now close this terminal or disconnect. Ada must remain powered on and awake.'
