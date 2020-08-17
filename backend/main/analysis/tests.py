"""
Tests for the main main.
"""

from django.test import TestCase

from ..models import Photo


class AnalysisTestBase(TestCase):
    """
    Backend TestCase
    """
    def setUp(self):
        super().setUp()
        p0 = Photo()
        p0.save()
        p1 = Photo()
        p1.save()
        self.photos = Photo.objects.all()

    def test_sample(self):
        """
        Remove me once we have real tests here.
        """
        two = 2
        another_two = 2
        self.assertEqual(two + another_two, 4)
