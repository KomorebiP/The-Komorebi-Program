"""Repository migration must preserve deep links and leave other sites alone."""
import unittest

from project_urls import canonical_project_url


class ProjectURLTests(unittest.TestCase):
    def test_legacy_reader_and_source_links_preserve_query_and_fragment(self):
        pairs = [
            ('https://komorebip.github.io/Operation-KOMOREBI/read/paper-i/index.html?view=slides#L12',
             'https://komorebip.github.io/The-Komorebi-Program/read/paper-i/index.html?view=slides#L12'),
            ('https://github.com/KomorebiP/Operation-KOMOREBI/blob/abc/docs/START_HERE.md#start',
             'https://github.com/KomorebiP/The-Komorebi-Program/blob/abc/docs/START_HERE.md#start'),
            ('https://raw.githubusercontent.com/KomorebiP/Operation-KOMOREBI/abc/input.json',
             'https://raw.githubusercontent.com/KomorebiP/The-Komorebi-Program/abc/input.json'),
            ('https://api.github.com/repos/KomorebiP/Operation-KOMOREBI/releases/1',
             'https://api.github.com/repos/KomorebiP/The-Komorebi-Program/releases/1'),
        ]
        for previous, current in pairs:
            with self.subTest(previous=previous):
                self.assertEqual(canonical_project_url(previous), current)
                self.assertEqual(canonical_project_url(current), current)

    def test_similar_repositories_other_owners_and_relative_links_are_unchanged(self):
        for url in [
            'https://github.com/Other/Operation-KOMOREBI/blob/main/x',
            'https://github.com/KomorebiP/Operation-KOMOREBI-copy/blob/main/x',
            'https://other.github.io/Operation-KOMOREBI/',
            'https://github.com.example/KomorebiP/Operation-KOMOREBI/',
            '../Operation-KOMOREBI/input.json#L2',
        ]:
            with self.subTest(url=url):
                self.assertEqual(canonical_project_url(url), url)


if __name__ == '__main__':
    unittest.main()
