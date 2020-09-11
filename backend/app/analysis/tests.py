"""
Tests for the main main.
"""

from django.test import TestCase

# NOTE(ra): we have to use absolute imports in this module because the Django test runner
# will resolve imports relative to the backend working directory
# If you do, e.g.,
#   from ..models import Photo
# ... you'll crash the test runner. Please don't!
from app.models import Photo, MapSquare
from app.analysis import photographer_caption_length


class AnalysisTestBase(TestCase):
    """
    Backend TestCase
    """
    def setUp(self):
        """
        Setup for all tests -- we initialize a bunch of objects we can use in our tests
        """
        super().setUp()
        self.map_square = MapSquare()
        self.map_square.save()
        self.photo_0 = Photo(number=1, map_square=self.map_square)
        self.photo_0.save()
        self.photo_1 = Photo(number=2, map_square=self.map_square)
        self.photo_1.save()

    def test_photographer_caption_length(self):
        self.photo_0.photographer_caption = '123456'
        result = photographer_caption_length.analyze(self.photo_0)
        self.assertEqual(6, result)

