#!/bin/bash
set -euo pipefail
TASK_DIR="$(cd "$(dirname "$0")" && pwd)"
export EX2_FINAL=1
exec '/Users/yzhbradoodrrpurp/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3' "$TASK_DIR/run-real-dns.py"
