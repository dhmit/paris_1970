"""
Tests for the main main.
"""

import os
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

        self.photo_dict = {}

        for i, image in enumerate(os.scandir(settings.TEST_PHOTOS_DIR)):
            photo_number = i + 1
            if image.path.endswith('.jpg') and image.is_file():  # Ensures file is an image
                # Creates Photo object
                photo = Photo(number=photo_number, map_square=self.map_square)
                photo.front_local_path = image.path
                photo.save()

                # Splits path string to make Photo name
                photo_name = image.path.split(str(settings.TEST_PHOTOS_DIR)+'/')[1].split('.jpg')[0]
                self.photo_dict[photo_name] = photo

    def test_photographer_caption_length(self):
        expected_values = {'100x100_500px-white_500px-black': 6}
        for image in expected_values:
            if image in self.photo_dict.keys():
                self.photo_dict[image].photographer_caption = '123456'
                result = photographer_caption_length.analyze(self.photo_dict[image])
                print(f'Caption Length performed on {image}. Result: {result}')
                self.assertEqual(expected_values[image], result)

    def test_whitespace_percentage(self):
        expected_values = {'100x100_500px-white_500px-black': 50}
        for image in expected_values:
            if image in self.photo_dict.keys():
                result = whitespace_percentage.analyze(self.photo_dict[image])
                print(f'Whitespace Percentage performed on {image}. Result: {result}')
                self.assertEqual(expected_values[image], result)

    def test_stdev(self):
        """
        Test Standard Deviation analysis (stdev.py)
        """
        expected_values = {'100x76-BlackRectangle': 0, '100x76-GreyRectangle': 0,
                           '100x76-WhiteRectangle': 0, '100x100-BlackSquare': 0,
                           '100x100-GreySquare': 0, '100x100-WhiteSquare': 0,
                           '100x76-CheckeredRectangle_1': 0, '100x76-CheckeredRectangle_2': 0}

        for image in expected_values:
            if image in self.photo_dict.keys():
                result = stdev.analyze(self.photo_dict[image])
                print(f'StDev performed on {image}. Result: {result}')
                self.assertEqual(expected_values[image], result)

    def test_local_variance(self):
        """
        Test Local Variance analysis (local_variance.py)
        """
        expected_values = {'100x76-BlackRectangle': 0, '100x76-GreyRectangle': 0,
                           '100x76-WhiteRectangle': 0, '100x100-BlackSquare': 0,
                           '100x100-GreySquare': 0, '100x100-WhiteSquare': 0,
                           '100x76-CheckeredRectangle_1': 3087, '100x76-CheckeredRectangle_2': 3087}

        for image in expected_values:
            if image in self.photo_dict.keys():
                result = local_variance.analyze(self.photo_dict[image])
                print(f'Local Variance performed on {image}. Result: {result}')
                self.assertEqual(expected_values[image], int(result))

    def test_detail_fft2(self):
        """
        Test Fast Fourier Transform analysis (detail_fft2.py)
        """
        expected_values = {'100x76-BlackRectangle': 0, '100x76-GreyRectangle': 0,
                           '100x76-WhiteRectangle': 0, '100x100-BlackSquare': 0,
                           '100x100-GreySquare': 0, '100x100-WhiteSquare': 0,
                           '100x76-CheckeredRectangle_1': 5, '100x76-CheckeredRectangle_2': 5}

        for image in expected_values:
            if image in self.photo_dict.keys():
                result = detail_fft2.analyze(self.photo_dict[image])
                print(f'FFT performed on {image}. Result: {result}')
                self.assertEqual(expected_values[image], int(result))

    def test_average_detail(self):
        """
        Test Average Detail function (average_detail.py)
        """
        expected_values = {'100x76-BlackRectangle': 0, '100x76-GreyRectangle': 0,
                           '100x76-WhiteRectangle': 0, '100x100-BlackSquare': 0,
                           '100x100-GreySquare': 0, '100x100-WhiteSquare': 0,
                           '100x76-CheckeredRectangle_1': 1030, '100x76-CheckeredRectangle_2': 1030}

        for image in expected_values:
            if image in self.photo_dict.keys():
                result = average_detail.analyze(self.photo_dict[image])
                print(f'Average Detail performed on {image}. Result: {result}')
                self.assertEqual(expected_values[image], int(result))

        # Tests on BGW squares (photos #7-9)
        # result = average_detail.analyze(self.black_square)
        # self.assertEqual(0, result)
        #
        # result = average_detail.analyze(self.grey_square)
        # self.assertEqual(0, result)
        #
        # result = average_detail.analyze(self.white_square)
        # self.assertEqual(0, result)
        #
        # # Tests on BGW rectangles (photos #4-6)
        # result = average_detail.analyze(self.black_rect)
        # self.assertEqual(0, result)
        #
        # result = average_detail.analyze(self.grey_rect)
        # self.assertEqual(0, result)
        #
        # result = average_detail.analyze(self.white_rect)
        # self.assertEqual(0, result)
