#!/usr/bin/env python3
"""Fetch WakaTime aggregates; keep the last good snapshot on API failures."""
import base64
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from build_wakatime import SNAPSHOT, main as build_wakatime


def number(value):
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError('Invalid duration')
    return value


def normalize(data):
    """Allowlist aggregate fields; never persist the full private API response."""
    if data.get('is_up_to_date') is False:
        raise ValueError('WakaTime stats are still being calculated')
    return {'updated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'range': 'all_time', 'total_seconds': number(data['total_seconds'])}


def badge_seconds(svg):
    """Read the public all-time badge value, rather than a weekly stats total."""
    root = ET.fromstring(svg)
    pattern = r'(?:(\d+) hrs?\s*)?(?:(\d+) mins?\s*)?(?:(\d+) secs?)?'
    for element in root.iter():
        if not element.tag.endswith('text'):
            continue
        match = re.fullmatch(pattern, (element.text or '').strip())
        if match and any(match.groups()):
            hours, minutes, seconds = (int(value or 0) for value in match.groups())
            return hours * 3600 + minutes * 60 + seconds
    raise ValueError('Public all-time badge duration unavailable')


def main():
    key = os.environ.get('WAKATIME_API_KEY', '').strip()
    username = os.environ.get('WAKATIME_USERNAME', '').strip()
    if not key and not username:
        print('WakaTime not configured; preserving the existing card.')
        build_wakatime()
        return
    user = 'current' if key else quote(username, safe='')
    headers = {'User-Agent': 'sizwinz-readme', 'Accept': 'application/json'}
    if key:
        headers['Authorization'] = 'Basic ' + base64.b64encode(key.encode()).decode()
    try:
        if key:
            request = Request(f'https://api.wakatime.com/api/v1/users/{user}/all_time_since_today', headers=headers)
            with urlopen(request, timeout=30) as response:
                if response.status != 200:
                    raise ValueError('WakaTime stats are not ready')
                snapshot = normalize(json.load(response)['data'])
        else:
            with urlopen(Request(f'https://api.wakatime.com/api/v1/users/{user}', headers=headers), timeout=30) as response:
                identifier = json.load(response)['data']['id']
            if not re.fullmatch(r'[a-fA-F0-9-]{36}', identifier):
                raise ValueError('Invalid public WakaTime user ID')
            request = Request(f'https://wakatime.com/badge/user/{identifier}.svg', headers={'User-Agent': 'sizwinz-readme'})
            with urlopen(request, timeout=30) as response:
                snapshot = normalize({'total_seconds': badge_seconds(response.read())})
        temporary = SNAPSHOT.with_suffix('.tmp')
        temporary.write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8')
        temporary.replace(SNAPSHOT)
        build_wakatime()
        print('Updated WakaTime aggregate snapshot and both themed cards.')
    except (HTTPError, URLError, ValueError, KeyError, TypeError, ET.ParseError) as error:
        # Never print response bodies, request headers or credentials.
        code = error.code if isinstance(error, HTTPError) else type(error).__name__
        print(f'WakaTime refresh failed ({code}); last good snapshot preserved.', file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
