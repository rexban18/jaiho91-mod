#!/bin/bash
set -e

echo "=== Step 1: Download APK ==="
python3 download_apk.py

echo "=== Step 2: Verify APK ==="
python3 download_apk.py --verify

echo "=== Step 3: Build MOD ==="
python3 build.py original.apk \
  --package "$1" \
  --name "$2" \
  -o mod.apk

echo "=== Done ==="
ls -lh mod*.apk
