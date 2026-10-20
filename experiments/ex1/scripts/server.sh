#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
case "${1:-status}" in
start|stop|restart|graceful) /usr/sbin/httpd -f "$ROOT/apache/httpd.conf" -k "$1" ;;
check) /usr/sbin/httpd -t -f "$ROOT/apache/httpd.conf" ;;
status) /usr/sbin/lsof -nP -iTCP:8080 -sTCP:LISTEN ;;
*) echo 'Usage: server.sh start|stop|restart|graceful|check|status'; exit 2 ;;
esac
