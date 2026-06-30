#!/usr/bin/env python3
"""Download APK from GitHub release chunks and reassemble."""
import os, sys, json, requests, zipfile

REPO = os.environ.get('GITHUB_REPOSITORY', 'rexban18/jaiho91-mod')
TOKEN = os.environ.get('GITHUB_TOKEN', '')

headers = {'Accept': 'application/vnd.github.v3+json'}
if TOKEN:
    headers['Authorization'] = f'token {TOKEN}'

rel_url = f'https://api.github.com/repos/{REPO}/releases/tags/v1'
rel = requests.get(rel_url, headers=headers).json()
assets = rel.get('assets', [])

# Try full APK first
apk = [a for a in assets if a['name'].endswith('.apk') and a['size'] > 1000000]
if apk:
    url = apk[0]['url']
    data = requests.get(url, headers={**headers, 'Accept': 'application/octet-stream'}).content
    with open('original.apk', 'wb') as f:
        f.write(data)
    print(f'Downloaded full APK: {len(data)} bytes')
    sys.exit(0)

# Fallback: reassemble from chunks
chunks = sorted([a for a in assets if a['name'].startswith('apk_part_')], key=lambda x: x['name'])
if not chunks:
    print('ERROR: No APK or chunks found in release!')
    sys.exit(1)

with open('original.apk', 'wb') as out:
    for c in chunks:
        data = requests.get(c['url'], headers={**headers, 'Accept': 'application/octet-stream'}).content
        out.write(data)
        print(f'  {c["name"]}: {len(data)} bytes')

size = os.path.getsize('original.apk')
print(f'Reassembled: {size} bytes')

# Verify it's a valid zip/APK
with zipfile.ZipFile('original.apk') as z:
    assert 'AndroidManifest.xml' in z.namelist()
print('Valid APK!')
