#!/bin/bash
set -euo pipefail
TASK_DIR="$(cd "$(dirname "$0")" && pwd)"
exec '/Users/yzhbradoodrrpurp/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3' "$TASK_DIR/run-real-dns.py"
