"""
Tests for the main main.
"""

from django.test import TestCase

from app.models import Photo, MapSquare


class AnalysisTestBase(TestCase):
    """
    Backend TestCase
    """
    def setUp(self):
        super().setUp()
        map_square = MapSquare()
        map_square.save()
        photo_0 = Photo(number=1, map_square=map_square)
        photo_0.save()
        photo_1 = Photo(number=2, map_square=map_square)
        photo_1.save()

    def test_sample(self):
        """
        Remove me once we have real tests here.
        """
        num_photos = Photo.objects.all().count()
        self.assertEqual(num_photos, 2)


class TestCalcWhitespace(AnalysisTestBase):
    """
    Tests calc_whitespace
    """

    def test_analysis(self):
        """
        TODO: write me!
        """
        pass
