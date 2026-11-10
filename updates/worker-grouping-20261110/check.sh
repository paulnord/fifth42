#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
sha256sum -c SHA256SUMS
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_policy
(cd controller && PYTHONDONTWRITEBYTECODE=1 python3 -B test_completion.py)
