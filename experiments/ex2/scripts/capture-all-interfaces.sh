#!/bin/bash
set -euo pipefail
TASK_DIR="$(cd "$(dirname "$0")" && pwd)"
TASK_ROOT="$(cd "$TASK_DIR/.." && pwd)"
mkdir -p "$TASK_ROOT/evidence/supplement"
export EX2_SUPPLEMENT=1
exec '/Users/yzhbradoodrrpurp/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3' "$TASK_DIR/run-real-dns.py"
