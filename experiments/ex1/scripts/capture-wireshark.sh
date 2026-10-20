#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/evidence/wireshark-browser.pcapng"
if [[ -e "$OUT" ]]; then echo "文件已存在，请先另存：$OUT"; exit 1; fi
# -g allows the file's group to read the output, avoiding a root-only artifact.
exec /Applications/Wireshark.app/Contents/MacOS/dumpcap -i en0 \
  -f 'host gaia.cs.umass.edu and tcp port 80' -g -a duration:120 -w "$OUT"
