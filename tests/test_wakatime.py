import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import refresh_wakatime
from build_wakatime import render, duration


class WakaTimeTests(unittest.TestCase):
    def test_public_badge_duration(self):
        svg = '<svg><text>wakatime</text><text>410 hrs 23 mins</text></svg>'
        self.assertEqual(refresh_wakatime.badge_seconds(svg), 410 * 3600 + 23 * 60)
        self.assertEqual(refresh_wakatime.badge_seconds('<svg><text>0 secs</text></svg>'), 0)
        with self.assertRaises(ValueError):
            refresh_wakatime.badge_seconds('<svg><text>Unavailable</text></svg>')

    def test_only_aggregate_fields_are_persisted(self):
        snapshot = refresh_wakatime.normalize({
            'total_seconds': 3600, 'total_seconds_including_other_language': 4200,
            'daily_average': 600, 'daily_average_including_other_language': 700,
            'languages': [{'name': 'Python', 'total_seconds': 3600}, {'name': 'Other', 'total_seconds': 600}],
            'projects': [{'name': 'private-project'}], 'machines': [{'name': 'private-machine'}],
            'best_day': None, 'is_up_to_date': True,
        })
        self.assertEqual(snapshot['total_seconds'], 3600)
        self.assertNotIn('private-', json.dumps(snapshot))
        self.assertEqual(set(snapshot), {'updated_at', 'range', 'total_seconds'})

    def test_incomplete_or_invalid_stats_are_rejected(self):
        for data in [{'is_up_to_date': False}, {'total_seconds': float('nan')}, {'total_seconds': -1}]:
            with self.assertRaises(ValueError):
                refresh_wakatime.normalize(data)

    def test_api_failure_preserves_last_successful_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'metrics.json'
            target.write_text('last-good', encoding='utf-8')
            error = HTTPError('https://api.wakatime.com', 503, 'Unavailable', {}, None)
            with patch.dict('os.environ', {'WAKATIME_API_KEY': '', 'WAKATIME_USERNAME': 'sizwinz'}), \
                 patch.object(refresh_wakatime, 'SNAPSHOT', target), \
                 patch.object(refresh_wakatime, 'urlopen', side_effect=error), \
                 contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    refresh_wakatime.main()
            self.assertEqual(target.read_text(encoding='utf-8'), 'last-good')

    def test_only_all_time_is_displayed(self):
        data = {'total_seconds': 0, 'range': 'all_time', 'updated_at': '2026-10-12T00:00:00Z'}
        for theme in ('dark', 'light'):
            svg = render(data, theme)
            ET.fromstring(svg)
            self.assertIn('0h 00m', svg)
            self.assertNotIn('DAILY AVERAGE', svg)
            self.assertNotIn('TOP LANGUAGE', svg)
            self.assertIn('Unavailable', render({'range': 'last_7_days'}, theme))
            ET.fromstring(render(None, theme))
        self.assertEqual(duration(3599), '1h 00m')


if __name__ == '__main__':
    unittest.main()
