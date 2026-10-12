"""Check the threshold boundary and calendar streak behavior."""
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_cards import star_badge
from build_stats import streaks


class MetricsTests(unittest.TestCase):
    def test_stars_strictly_above_five(self):
        for count in (None, 0, 5):
            self.assertEqual(star_badge(count, 0, 0, 'dark'), '')
        for theme in ('dark', 'light'):
            self.assertIn('6 GitHub stars', star_badge(6, 0, 0, theme))

    def test_today_zero_keeps_yesterdays_streak(self):
        days = [{'date': f'2026-10-{day:02}', 'contributionCount': count}
                for day, count in [(8, 2), (9, 1), (10, 0), (11, 3), (12, 0)]]
        self.assertEqual(streaks(days, date(2026, 10, 12)), (1, 2))

    def test_missing_dates_do_not_extend_streak(self):
        days = [{'date': '2026-10-10', 'contributionCount': 1},
                {'date': '2026-10-12', 'contributionCount': 1}]
        self.assertEqual(streaks(days, date(2026, 10, 12)), (1, 1))

    def test_no_activity(self):
        self.assertEqual(streaks([], date(2026, 10, 12)), (0, 0))


if __name__ == '__main__':
    unittest.main()
