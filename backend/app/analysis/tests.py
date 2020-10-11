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
    stdev,
    detail_fft2,
    local_variance,
    average_detail,
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
        test_photo2_path = Path(settings.TEST_PHOTOS_DIR, '128x128_black-square.jpg')
        self.photo_2.front_local_path = test_photo2_path
        self.photo_2.save()

        # BlackRect - 100 x 76 Black Rectangle (#4)
        self.black_rect = Photo(number=4, map_square=self.map_square)
        test_black_rect_path = Path(settings.TEST_PHOTOS_DIR, '100x76-BlackRectangle.jpg')
        self.black_rect.front_local_path = test_black_rect_path
        self.black_rect.save()

        # GreyRect - 100 x 76 Grey Rectangle (#5)
        self.grey_rect = Photo(number=5, map_square=self.map_square)
        test_grey_rect_path = Path(settings.TEST_PHOTOS_DIR, '100x76-GreyRectangle.jpg')
        self.grey_rect.front_local_path = test_grey_rect_path
        self.grey_rect.save()

        # WhiteRect - 100 x 76 White Rectangle (#6)
        self.white_rect = Photo(number=6, map_square=self.map_square)
        test_white_rect_path = Path(settings.TEST_PHOTOS_DIR, '100x76-WhiteRectangle.jpg')
        self.white_rect.front_local_path = test_white_rect_path
        self.white_rect.save()

        # BlackSquare - 100 x 100 Black Square (#7)
        self.black_square = Photo(number=7, map_square=self.map_square)
        test_black_square_path = Path(settings.TEST_PHOTOS_DIR, '100x100-BlackSquare.jpg')
        self.black_square.front_local_path = test_black_square_path
        self.black_square.save()

        # GreySquare - 100 x 100 Grey Square (#8)
        self.grey_square = Photo(number=8, map_square=self.map_square)
        test_grey_square_path = Path(settings.TEST_PHOTOS_DIR, '100x100-GreySquare.jpg')
        self.grey_square.front_local_path = test_grey_square_path
        self.grey_square.save()

        # WhiteSquare - 100 x 100 White Square (#9)
        self.white_square = Photo(number=9, map_square=self.map_square)
        test_white_square_path = Path(settings.TEST_PHOTOS_DIR, '100x100-WhiteSquare.jpg')
        self.white_square.front_local_path = test_white_square_path
        self.white_square.save()

    def test_photographer_caption_length(self):
        self.photo_0.photographer_caption = '123456'
        result = photographer_caption_length.analyze(self.photo_0)
        self.assertEqual(6, result)

    def test_whitespace_percentage(self):
        result = whitespace_percentage.analyze(self.photo_0)
        self.assertEqual(50, result)

    def test_stdev(self):
        """
        Test Standard Deviation analysis (stdev.py)
        """
        # Tests on BGW squares (photos #7-9)
        result = stdev.analyze(self.black_square)
        self.assertEqual(0, result)

        result = stdev.analyze(self.grey_square)
        self.assertEqual(0, result)

        result = stdev.analyze(self.white_square)
        self.assertEqual(0, result)

        # Tests on BGW rectangles (photos #4-6)
        result = stdev.analyze(self.black_rect)
        self.assertEqual(0, result)

        result = stdev.analyze(self.grey_rect)
        self.assertEqual(0, result)

        result = stdev.analyze(self.white_rect)
        self.assertEqual(0, result)

    def test_local_variance(self):
        """
        Test Local Variance analysis (local_variance.py)
        """
        # Tests on BGW squares (photos #7-9)
        result = local_variance.analyze(self.black_square)
        self.assertEqual(0, result)

        result = local_variance.analyze(self.grey_square)
        self.assertEqual(0, result)

        result = local_variance.analyze(self.white_square)
        self.assertEqual(0, result)

        # Tests on BGW rectangles (photos #4-6)
        result = local_variance.analyze(self.black_rect)
        self.assertEqual(0, result)

        result = local_variance.analyze(self.grey_rect)
        self.assertEqual(0, result)

        result = local_variance.analyze(self.white_rect)
        self.assertEqual(0, result)

    def test_detail_fft2(self):
        """
        Test Fast Fourier Transform analysis (detail_fft2.py)
        """
        # Tests on BGW squares (photos #7-9)
        result = detail_fft2.analyze(self.black_square)
        self.assertEqual(0, result)

        result = detail_fft2.analyze(self.grey_square)
        self.assertEqual(0, result)

        result = detail_fft2.analyze(self.white_square)
        self.assertEqual(0, result)

        # Tests on BGW rectangles (photos #4-6)
        result = detail_fft2.analyze(self.black_rect)
        self.assertEqual(0, result)

        result = detail_fft2.analyze(self.grey_rect)
        self.assertEqual(0, result)

        result = detail_fft2.analyze(self.white_rect)
        self.assertEqual(0, result)

    def test_average_detail(self):
        """
        Test Average Detail function (average_detail.py)
        """
        # Tests on BGW squares (photos #7-9)
        result = average_detail.analyze(self.black_square)
        self.assertEqual(0, result)

        result = average_detail.analyze(self.grey_square)
        self.assertEqual(0, result)

        result = average_detail.analyze(self.white_square)
        self.assertEqual(0, result)

        # Tests on BGW rectangles (photos #4-6)
        result = average_detail.analyze(self.black_rect)
        self.assertEqual(0, result)

        result = average_detail.analyze(self.grey_rect)
        self.assertEqual(0, result)

        result = average_detail.analyze(self.white_rect)
        self.assertEqual(0, result)
