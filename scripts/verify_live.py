"""Confirm that the deployed Pages routes and versioned assets are publicly served."""
import os
import time
import urllib.request

base = os.environ['SITE_URL'].rstrip('/') + '/'
sha = os.environ.get('GITHUB_SHA', 'verify')
checks = {'': 'Good music.', 'events/': 'next night out.', 'visit/': 'Our corner.', 'assets/styles.css': '--coral:#ff7046', 'assets/site.js': 'refreshDates'}
errors = []
for path, marker in checks.items():
    url = base + path + '?verify=' + sha
    for attempt in range(12):
        try:
            request = urllib.request.Request(url, headers={'Cache-Control': 'no-cache', 'User-Agent': 'Out-n-About-Pages-Smoke-Test'})
            with urllib.request.urlopen(request, timeout=30) as response:
                status = response.status
                text = response.read().decode('utf-8')
            if status != 200 or marker not in text:
                raise ValueError(f'HTTP {status}; expected deployed content not found')
            print(f'PASS HTTP {status}: {base + path}', flush=True)
            break
        except Exception as exc:
            if attempt == 11:
                errors.append(f'{base + path}: {exc}')
            else:
                time.sleep(5)
if errors:
    raise SystemExit('\n'.join(errors))
print('Verified all three live pages and both deployed assets.', flush=True)
