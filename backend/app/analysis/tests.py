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
    find_vanishing_point,
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

        # Following photos for find_vanishing_point
        # Team Tangled TODO: import in photo with vanishing point lines
        self.photo_2 = Photo(number=3, map_square=self.map_square)
        test_photo_path_2 = Path(settings.TEST_PHOTOS_DIR, '100px_100px_vanishing_point_X.jpg')
        self.photo_2.front_local_path = test_photo_path_2
        self.photo_2.save()

        self.photo_3 = Photo(number=4, map_square=self.map_square)
        test_photo_path_3 = Path(settings.TEST_PHOTOS_DIR, 'bpimg.jpg')
        self.photo_3.front_local_path = test_photo_path_3
        self.photo_3.save()

    def test_photographer_caption_length(self):
        self.photo_0.photographer_caption = '123456'
        result = photographer_caption_length.analyze(self.photo_0)
        self.assertEqual(6, result)

    def test_whitespace_percentage(self):
        result = whitespace_percentage.analyze(self.photo_0)
        self.assertEqual(50, result)

    def test_find_vanishing_point(self):
        # covers when image is x, intersecting lines in the middle
        result = find_vanishing_point.analyze(self.photo_2)
        self.assertEqual((50, 50), result)

        # covers when online line is horizontal (supposed to ignore)
        result2 = find_vanishing_point.analyze(self.photo_0)
        self.assertEqual((0, 0), result2)
