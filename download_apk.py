#!/usr/bin/env python3
"""Download APK from GitHub release chunks and reassemble."""
import os, sys, json, requests, zipfile

REPO = os.environ.get('GITHUB_REPOSITORY', 'rexban18/jaiho91-mod')
TOKEN = os.environ.get('GITHUB_TOKEN', '')
headers = {'Accept': 'application/vnd.github.v3+json'}
if TOKEN:
    headers['Authorization'] = f'token {TOKEN}'

if '--verify' in sys.argv:
    with zipfile.ZipFile('original.apk') as z:
        names = z.namelist()
        print(f'Entries: {len(names)}')
        assert 'AndroidManifest.xml' in names
        assert 'classes.dex' in names
    print('Valid APK!')
    sys.exit(0)

rel = requests.get(f'https://api.github.com/repos/{REPO}/releases/tags/v1', headers=headers).json()
assets = rel.get('assets', [])

apk = [a for a in assets if a['name'].endswith('.apk') and a['size'] > 1000000]
if apk:
    url = apk[0]['url']
    data = requests.get(url, headers={**headers, 'Accept': 'application/octet-stream'}).content
    with open('original.apk', 'wb') as f:
        f.write(data)
    print(f'Downloaded full APK: {len(data)} bytes')
    sys.exit(0)

chunks = sorted([a for a in assets if a['name'].startswith('apk_part_')], key=lambda x: x['name'])
if not chunks:
    print('ERROR: No APK or chunks found!')
    sys.exit(1)

with open('original.apk', 'wb') as out:
    for c in chunks:
        data = requests.get(c['url'], headers={**headers, 'Accept': 'application/octet-stream'}).content
        out.write(data)
        print(f'  {c["name"]}: {len(data)} bytes')

size = os.path.getsize('original.apk')
print(f'Reassembled: {size} bytes')

with zipfile.ZipFile('original.apk') as z:
    assert 'AndroidManifest.xml' in z.namelist()
print('Valid APK!')
