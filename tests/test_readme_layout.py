import re
import unittest
from pathlib import Path


class ReadmeLayoutTests(unittest.TestCase):
    def test_profile_details_are_independent_sections(self):
        readme = (Path(__file__).resolve().parents[1] / 'README.md').read_text(encoding='utf-8')
        depth = 0
        sections = []
        for match in re.finditer(r'<details>|</details>|<summary>(.*?)</summary>', readme):
            if match[0] == '<details>':
                depth += 1
            elif match[0] == '</details>':
                depth -= 1
            else:
                self.assertEqual(depth, 1, 'Each profile section should open independently')
                sections.append(match[1])
        self.assertEqual(depth, 0)
        self.assertEqual(sections, ['About me', 'Setup & current activity', 'Tech stack', 'Quotes I live by'])
