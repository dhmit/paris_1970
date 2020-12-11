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
    pop_density_detection,
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
        self.photo_0.cleaned_local_path = test_photo_path
        self.photo_0.save()

        self.photo_1 = Photo(number=2, map_square=self.map_square)
        self.photo_1.save()

    def test_photographer_caption_length(self):
        self.photo_0.photographer_caption = '123456'
        result = photographer_caption_length.analyze(self.photo_0)
        self.assertEqual(6, result)

    def test_whitespace_percentage(self):
        result = whitespace_percentage.analyze(self.photo_0)
        self.assertEqual(50, result)

    def test_pop_density_detection(self):
        """
        Tests for pop_density_detection analysis
        """
        photo_three_people = Photo(number=3, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'pop_density_detection_test_3_people.jpg')
        photo_three_people.cleaned_local_path = test_photo_path
        photo_three_people.save()

        # this photo we know has 3 people
        result = pop_density_detection.analyze(photo_three_people)
        self.assertEqual(3, result)

        # this is the half black half white square with no people
        result = pop_density_detection.analyze(self.photo_0)
        self.assertEqual(0, result)
