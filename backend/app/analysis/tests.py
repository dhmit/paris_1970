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

    def add_photo(self, photo_name):
        """
        Creates a photo object and adds it to self.photo_dict given the name of the photo
        """
        if photo_name not in self.photo_dict.keys():
            # Creates Photo object
            photo = Photo(number=len(self.photo_dict.keys()), map_square=self.map_square)
            photo.front_local_path = os.path.join(settings.TEST_PHOTOS_DIR, f'{photo_name}.jpg')
            photo.save()

            # Splits path string to make Photo name
            self.photo_dict[photo_name] = photo

    def test_photographer_caption_length(self):
        """
        Test Photographer Caption Length analysis (photographer_caption_length.py)
        """
        expected_values = {'100x100_500px-white_500px-black': 6}
        for image in expected_values:
            self.add_photo(image)
            self.photo_dict[image].photographer_caption = '123456'
            result = photographer_caption_length.analyze(self.photo_dict[image])
            print(f'Caption Length performed on {image}. Result: {result}')
            self.assertEqual(expected_values[image], result)

    def test_whitespace_percentage(self):
        """
        Test Whitespace Percentage analysis (whitespace_percentage.py)
        """
        expected_values = {'100x100_500px-white_500px-black': 50}
        for image in expected_values:
            self.add_photo(image)
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
                           '100x76-CheckeredRectangle_1': 126, '100x76-CheckeredRectangle_2': 126,
                           '100x76-HalfRectangle_1': 1, '100x76-HalfRectangle_2': 126,
                           '100x76-HalfRectangle_3': 1, '100x76-HalfRectangle_4': 126,
                           '100x100-CheckeredSquare_1': 125, '100x100-CheckeredSquare_2': 125,
                           '100x100-HalfSquare_1': 0, '100x100-HalfSquare_2': 125,
                           '100x100_500px-white_500px-black': 0,
                           '100x100-HalfSquare_4': 125}

        for image in expected_values:
            self.add_photo(image)
            result = stdev.analyze(self.photo_dict[image])
            print(f'StDev performed on {image}. Result: {result}')
            self.assertEqual(expected_values[image], int(result))

    def test_local_variance(self):
        """
        Test Local Variance analysis (local_variance.py)
        """
        expected_values = {'100x76-BlackRectangle': 0, '100x76-GreyRectangle': 0,
                           '100x76-WhiteRectangle': 0, '100x100-BlackSquare': 0,
                           '100x100-GreySquare': 0, '100x100-WhiteSquare': 0,
                           '100x76-CheckeredRectangle_1': 3087,
                           '100x76-CheckeredRectangle_2': 3087,
                           '100x76-HalfRectangle_1': 1717, '100x76-HalfRectangle_2': 1305,
                           '100x76-HalfRectangle_3': 1717, '100x76-HalfRectangle_4': 1305,
                           '100x100-CheckeredSquare_1': 2660, '100x100-CheckeredSquare_2': 2660,
                           '100x100-HalfSquare_1': 1305, '100x100-HalfSquare_2': 1305,
                           '100x100_500px-white_500px-black': 1300,
                           '100x100-HalfSquare_4': 1305}

        for image in expected_values:
            self.add_photo(image)
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
                           '100x76-CheckeredRectangle_1': 5, '100x76-CheckeredRectangle_2': 5,
                           '100x76-HalfRectangle_1': 0, '100x76-HalfRectangle_2': 0,
                           '100x76-HalfRectangle_3': 0, '100x76-HalfRectangle_4': 0,
                           '100x100-CheckeredSquare_1': 6, '100x100-CheckeredSquare_2': 6,
                           '100x100-HalfSquare_1': 0, '100x100-HalfSquare_2': 0,
                           '100x100_500px-white_500px-black': 0,
                           '100x100-HalfSquare_4': 0}

        for image in expected_values:
            self.add_photo(image)
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
            self.add_photo(image)
            result = average_detail.analyze(self.photo_dict[image])
            print(f'Average Detail performed on {image}. Result: {result}')
            self.assertEqual(expected_values[image], int(result))
