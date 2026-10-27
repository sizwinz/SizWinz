import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_profile_extras import setup_panel


class SetupPanelTests(unittest.TestCase):
    def test_setup_has_compact_bottom_padding(self):
        for theme in ('dark', 'light'):
            root = ET.fromstring(setup_panel(theme))
            height = float(root.get('viewBox').split()[3])
            artwork = root.find('{http://www.w3.org/2000/svg}rect')
            bottom = float(artwork.get('y')) + float(artwork.get('height'))
            self.assertLessEqual(height - 12 - bottom, 16)

    def test_setup_has_no_visible_device_labels(self):
        for theme in ('dark', 'light'):
            root = ET.fromstring(setup_panel(theme))
            labels = [e.text for e in root.iter('{http://www.w3.org/2000/svg}text')]
            self.assertEqual(labels, ['MY SETUP'])
