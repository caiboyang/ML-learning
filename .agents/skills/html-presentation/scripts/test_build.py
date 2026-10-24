import copy
import json
import tempfile
import unittest
from pathlib import Path

from build import TEMPLATE, build
from validate import validate_site


class PresentationBuildTests(unittest.TestCase):
    def setUp(self):
        self.deck = json.loads((TEMPLATE / 'deck.json').read_text())
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / 'site'

    def test_build_without_video_has_matching_pages_and_assets(self):
        build(self.deck, self.output)
        self.assertEqual(validate_site(self.output), 4)
        self.assertNotIn('视频页 V', (self.output / 'notes.html').read_text())

    def test_delete_and_reorder_keep_notes_and_thumbnails_together(self):
        self.deck['slides'] = [self.deck['slides'][2], self.deck['slides'][0]]
        build(self.deck, self.output)
        self.assertEqual(validate_site(self.output), 2)
        self.assertIn('SLIDE 01 / 2', (self.output / 'notes.html').read_text())

    def test_short_budget_is_not_the_speech_estimate(self):
        self.deck['slides'][1]['budget_seconds'] = 30
        report = build(self.deck, self.output)
        self.assertEqual(report[1]['budget_seconds'], 30)
        self.assertNotEqual(report[1]['estimate_seconds'], [30, 30])
        self.assertIn('data-budget-seconds="30"', (self.output / 'notes.html').read_text())

    def test_cues_are_not_counted_as_speech_and_say_is_escaped(self):
        self.deck['slides'][1]['notes'] = [{'cue': 'Do not read these extra words'}, {'say': 'One <two> three.'}]
        report = build(self.deck, self.output)
        self.assertEqual(report[1]['words'], 3)
        self.assertIn('One &lt;two&gt; three.', (self.output / 'notes.html').read_text())

    def test_invalid_ids_budgets_and_notes_fail_before_output(self):
        cases = [lambda d: d['slides'].append(copy.deepcopy(d['slides'][0])),
                 lambda d: d['slides'][0].update(id='top'),
                 lambda d: d['slides'][0].update(budget_seconds=-1),
                 lambda d: d['slides'][0].update(budget_seconds=float('nan')),
                 lambda d: d['slides'][0].update(notes=[{'say': 'x', 'cue': 'y'}])]
        for mutate in cases:
            with self.subTest(mutate=mutate):
                deck = copy.deepcopy(self.deck)
                mutate(deck)
                with self.assertRaises(ValueError):
                    build(deck, self.output)
                self.assertFalse(self.output.exists())

    def test_media_is_copied_and_included_in_estimate(self):
        assets = Path(self.temp.name) / 'assets'
        assets.mkdir()
        (assets / 'clip.mp4').write_bytes(b'test fixture, not real media')
        self.deck['slides'][1].update(id='video', html='<video id="demo-film" src="assets/clip.mp4"></video><p id="film-hint" hidden></p>', media_seconds=69)
        report = build(self.deck, self.output, assets)
        self.assertGreaterEqual(report[1]['estimate_seconds'][0], 69)
        self.assertEqual(validate_site(self.output), 4)
        self.assertIn('视频页 V', (self.output / 'notes.html').read_text())
        (self.output / 'assets/clip.mp4').unlink()
        with self.assertRaisesRegex(AssertionError, 'Missing local asset'):
            validate_site(self.output)

    def test_stale_thumbnail_is_detected(self):
        build(self.deck, self.output)
        path = self.output / 'index.html'
        path.write_text(path.read_text().replace('Choose one thing you can test.', 'Changed slide.'))
        with self.assertRaisesRegex(AssertionError, 'Thumbnail mismatch'):
            validate_site(self.output)


if __name__ == '__main__':
    unittest.main()
