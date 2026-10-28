#!/usr/bin/env bash
# Release gate: serves site/ with its production headers and runs every check against it.
# Exit code 0 only when all checks pass. Nothing may be pushed to main unless this passes.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT=8766
LOG="$(mktemp -d)"
python3 -c "import playwright" 2>/dev/null || { echo "playwright for Python is missing"; exit 2; }
python3 "$ROOT/tests/serve.py" "$ROOT/site" $PORT &
SRV=$!
trap 'kill $SRV 2>/dev/null; rm -rf "$LOG"' EXIT
for i in $(seq 1 30); do curl -s -o /dev/null "http://127.0.0.1:$PORT/" && break; sleep 0.3; done
status=0
echo "== consent and conversions"
python3 "$ROOT/tests/consent_test.py" > "$LOG/consent.txt" 2>&1 || status=1
tail -20 "$LOG/consent.txt"
echo "== seo (static)"
SITE_DIR="$ROOT/site" python3 "$ROOT/tests/seo_test.py" > "$LOG/seo.txt" 2>&1 || status=1
tail -8 "$LOG/seo.txt"
echo "== security"
SITE_DIR="$ROOT/site" python3 "$ROOT/tests/security_test.py" > "$LOG/security.txt" 2>&1 || status=1
tail -20 "$LOG/security.txt"
if [ $status -eq 0 ]; then echo "ALL CHECKS PASSED"; else echo "CHECKS FAILED: do not publish"; fi
exit $status
