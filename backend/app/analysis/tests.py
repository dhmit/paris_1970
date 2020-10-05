"""
Tests for the main main.
"""

from pathlib import Path

from django.conf import settings
from django.test import TestCase

# NOTE(ra): we have to use absolute imports in this module because the Django test runner
# will resolve imports relative to the backend working directory
# If you do, e.g.,
#   from ..models import Photo
# ... you'll crash the test runner. Please don't!
from app.models import Photo, MapSquare
from app.analysis import (
    photographer_caption_length,
    whitespace_percentage,
    text_ocr,
)


class AnalysisTestBase(TestCase):
    """
    TestCase for testing our analysis modules
    """
    def setUp(self):
        """
        Setup for all tests -- we initialize a bunch of objects we can use in our tests
        """
        super().setUp()

        self.map_square = MapSquare()
        self.map_square.save()

        self.photo_0 = Photo(number=1, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, '100x100_500px-white_500px-black.jpg')
        self.photo_0.front_local_path = test_photo_path
        self.photo_0.save()

        self.photo_1 = Photo(number=2, map_square=self.map_square)
        self.photo_1.save()

        self.photo_2 = Photo(number=3, map_square=self.map_square)
        test_photo_path_2 = Path(settings.TEST_PHOTOS_DIR, '300x300_francais.jpg')
        self.photo_2.front_local_path = test_photo_path_2

        self.photo_3 = Photo(number=4, map_square=self.map_square)
        test_photo_path_3 = Path(settings.TEST_PHOTOS_DIR, '300x300_carre.jpg')
        self.photo_3.front_local_path = test_photo_path_3

        self.photo_4 = Photo(number=5, map_square=self.map_square)
        test_photo_path_4 = Path(settings.TEST_PHOTOS_DIR, '300x300_hello.jpg')
        self.photo_4.front_local_path = test_photo_path_4

        self.photo_5 = Photo(number=6, map_square=self.map_square)
        test_photo_path_5 = Path(settings.LOCAL_PHOTOS_DIR, '120', '42_cleaned.jpg')
        self.photo_5.front_local_path = test_photo_path_5

        self.photo_6 = Photo(number=7, map_square=self.map_square)
        test_photo_path_6 = Path(settings.TEST_PHOTOS_DIR, 'test_text.jpg')
        self.photo_6.front_local_path = test_photo_path_6

    def test_photographer_caption_length(self):
        self.photo_0.photographer_caption = '123456'
        result = photographer_caption_length.analyze(self.photo_0)
        self.assertEqual(6, result)

    def test_whitespace_percentage(self):
        result = whitespace_percentage.analyze(self.photo_0)
        self.assertEqual(50, result)

    def test_text_ocr_francais(self):
        # Tests words with the ç
        result = text_ocr.analyze(self.photo_2)
        self.assertEqual({"Français"}, result)

    def test_text_ocr_carre(self):
        # Tests words with accent mark
        result = text_ocr.analyze(self.photo_3)
        self.assertEqual({"carré"}, result)

    def test_text_ocr_hello(self):
        # Tests english word
        result = text_ocr.analyze(self.photo_4)
        self.assertEqual({"Hello"}, result)

    def test_text_ocr_real_image(self):
        result = text_ocr.analyze(self.photo_6)
        print(result)

