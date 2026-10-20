#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $EUID -ne 0 ]]; then
  echo "请在终端运行：sudo /bin/bash \"$0\""
  exit 1
fi
OUT="$ROOT/evidence/browser-http.pcap"
if [[ -e "$OUT" ]]; then
  echo "抓包文件已存在，请先另存，避免覆盖：$OUT"
  exit 1
fi
# Only the assigned public HTTP server; no unrelated host traffic is recorded.
/usr/sbin/tcpdump -i pktap,all -s 0 -U -w "$OUT" 'host gaia.cs.umass.edu and tcp port 80' &
CAP_PID=$!
finish() {
  kill -INT "$CAP_PID" 2>/dev/null || true
  wait "$CAP_PID" 2>/dev/null || true
  if [[ -n "${SUDO_UID:-}" ]]; then chown "$SUDO_UID:${SUDO_GID}" "$OUT"; fi
}
trap finish EXIT
trap 'exit 130' INT TERM
echo "正在抓取指定实验站点的 HTTP 流量，最长 10 分钟。请回复 Codex：抓包已启动。"
echo "实验访问结束后可按 Ctrl+C 提前保存。"
for ((i=0; i<600; i++)); do
  kill -0 "$CAP_PID" 2>/dev/null || exit 1
  sleep 1
done
