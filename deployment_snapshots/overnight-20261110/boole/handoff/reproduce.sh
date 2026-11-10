#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
sha256sum --check SHA256SUMS
# Exact test/build commands are in HANDOFF.json. Use scratch outputs and unique TEST_ONLY revision IDs on an idle GPU.
# Never reuse archived production output directories or replace a running frozen file.
