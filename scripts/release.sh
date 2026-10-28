#!/usr/bin/env bash
# Rebuilds site/ from source/ and runs the release gate.
#   scripts/release.sh          build + all checks
# Publishing happens by pushing to main: Netlify deploys the site/ folder as it is (no build on Netlify).
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 -c "import jinja2" 2>/dev/null || pip install --quiet --break-system-packages jinja2 markupsafe
cd "$ROOT/source"
python3 build.py
rm -rf "$ROOT/site"
cp -a "$ROOT/source/build/dist" "$ROOT/site"
rm -rf "$ROOT/source/build"
cd "$ROOT"
bash tests/run_all.sh
