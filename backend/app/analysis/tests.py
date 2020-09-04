"""
Tests for the main main.
"""

from django.test import TestCase

from app.models import Photo


class AnalysisTestBase(TestCase):
    """
    Backend TestCase
    """
    def setUp(self):
        super().setUp()
        p_0 = Photo()
        p_0.save()
        p_1 = Photo()
        p_1.save()

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
