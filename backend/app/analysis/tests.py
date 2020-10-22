"""
Tests for the main main.
"""

from pathlib import Path
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
    mean_detail,
)
from app.analysis.indoor_analysis import (
    combined_indoor,
    courtyard_frame,
    find_windows,
    gradient_analysis
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
        self.photo_number_counter = 0

        self.photo_0 = Photo(number=0, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, '100x100_500px-white_500px-black.jpg')
        self.photo_0.front_local_path = test_photo_path
        self.photo_0.save()
        self.photo_number_counter += 1

        self.photo_00 = Photo(number=1, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'courtyard_frame', 'test1.jpg')
        self.photo_00.front_local_path = test_photo_path
        self.photo_00.save()
        self.photo_number_counter += 1

        self.photo_01 = Photo(number=2, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'courtyard_frame', 'test2.jpg')
        self.photo_01.front_local_path = test_photo_path
        self.photo_01.save()
        self.photo_number_counter += 1

        self.photo_02 = Photo(number=3, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'courtyard_frame', 'test3.jpg')
        self.photo_02.front_local_path = test_photo_path
        self.photo_02.save()
        self.photo_number_counter += 1

        self.photo_03 = Photo(number=4, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'courtyard_frame', 'test3_copy.jpg')
        self.photo_03.front_local_path = test_photo_path
        self.photo_03.save()
        self.photo_number_counter += 1

        self.photo_04 = Photo(number=5, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'courtyard_frame', 'test4.jpg')
        self.photo_04.front_local_path = test_photo_path
        self.photo_04.save()
        self.photo_number_counter += 1

        self.photo_square = Photo(number=7, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'window_photos',
                               'find_windows_test_photo.jpg')
        self.photo_square.front_local_path = test_photo_path
        self.photo_square.save()
        self.photo_number_counter += 1

        self.photo_black = Photo(number=9, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'window_photos', 'fully_black_image.jpg')
        self.photo_black.front_local_path = test_photo_path
        self.photo_black.save()
        self.photo_number_counter += 1

        self.photo_white = Photo(number=10, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'window_photos', 'fully_white_image.jpg')
        self.photo_white.front_local_path = test_photo_path
        self.photo_white.save()
        self.photo_number_counter += 1

        self.photo_windows = Photo(number=11, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'window_photos',
                               'gray_building_with_windows.jpg')
        self.photo_windows.front_local_path = test_photo_path
        self.photo_windows.save()
        self.photo_number_counter += 1

        self.photo_perspective_building = Photo(number=12, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'window_photos', 'ms_240_10_cleaned.jpg')
        self.photo_perspective_building.front_local_path = test_photo_path
        self.photo_perspective_building.save()
        self.photo_number_counter += 1

        self.photo_front_desk = Photo(number=13, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'window_photos', 'indoor_front_desk.jpg')
        self.photo_front_desk.front_local_path = test_photo_path
        self.photo_front_desk.save()
        self.photo_number_counter += 1

        self.photo_tall_crane = Photo(number=14, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'window_photos', 'tall_crane.jpg')
        self.photo_tall_crane.front_local_path = test_photo_path
        self.photo_tall_crane.save()
        self.photo_number_counter += 1

        self.photo_far_building = Photo(number=15, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'window_photos',
                               'far_window_buildings.jpg')
        self.photo_far_building.front_local_path = test_photo_path
        self.photo_far_building.save()
        self.photo_number_counter += 1

        self.photo_2 = Photo(number=16, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, '29_binder copy.jpg')
        self.photo_2.front_local_path = test_photo_path
        self.photo_2.save()
        self.photo_number_counter += 1

        self.photo_3 = Photo(number=17, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, '94_binder copy.jpg')
        self.photo_3.front_local_path = test_photo_path
        self.photo_3.save()
        self.photo_number_counter += 1

        self.photo_4 = Photo(number=18, map_square=self.map_square)
        test_photo_path = Path(settings.TEST_PHOTOS_DIR, 'square_503', '94_binder copy.jpg')
        self.photo_4.front_local_path = test_photo_path
        self.photo_4.save()
        self.photo_number_counter += 1

    def add_photo(self, photo_name):
        """
        Creates a photo object and adds it to self.photo_dict given the name of the photo
        """
        # Creates Photo object
        photo = Photo(number=self.photo_number_counter, map_square=self.map_square)
        photo.front_local_path = os.path.join(settings.TEST_PHOTOS_DIR, f'{photo_name}.jpg')
        photo.save()
        self.photo_number_counter += 1

        return photo

    def test_photographer_caption_length(self):
        """
        Test Photographer Caption Length analysis (photographer_caption_length.py)
        """
        photo = self.add_photo('100x100_500px-white_500px-black')
        photo.photographer_caption = '123456'
        result = photographer_caption_length.analyze(photo)
        print(f'Caption Length performed on 100x100_500px-white_500px-black. Result: {result}')
        self.assertEqual(6, result)

    def test_whitespace_percentage(self):
        """
        Test Whitespace Percentage analysis (whitespace_percentage.py)
        """
        photo = self.add_photo('100x100_500px-white_500px-black')
        result = whitespace_percentage.analyze(photo)
        print(f'Whitespace Percentage performed on \
            100x100_500px-white_500px-black. Result:'f' {result}')
        self.assertEqual(50, result)

    def test_courtyard_frame(self):
        """
        Testing a variety of images to see if they are correctly
        identified as having a dark frame, meaning they are likely
        images of a courtyard
        """
        result00 = courtyard_frame.analyze(self.photo_00)
        self.assertEqual(False, result00)
        result01 = courtyard_frame.analyze(self.photo_01)
        self.assertEqual(True, result01)
        result02 = courtyard_frame.analyze(self.photo_02)
        self.assertEqual(True, result02)
        result03 = courtyard_frame.analyze(self.photo_03)
        self.assertEqual(True, result03)
        result04 = courtyard_frame.analyze(self.photo_04)
        self.assertEqual(True, result04)

    def test_find_windows(self):
        """
        Testing a variety of images to see if they are correctly
        identified as having windows or not
        """
        square_result = find_windows.analyze(self.photo_square)
        black_result = find_windows.analyze(self.photo_black)
        white_result = find_windows.analyze(self.photo_white)
        many_windows = find_windows.analyze(self.photo_windows)
        building_perspective_view = find_windows.analyze(self.photo_perspective_building)
        front_desk = find_windows.analyze(self.photo_front_desk)
        tall_crane = find_windows.analyze(self.photo_tall_crane)
        far_building = find_windows.analyze(self.photo_far_building)

        self.assertEqual(True, square_result)
        self.assertEqual(False, black_result)
        self.assertEqual(False, white_result)
        self.assertEqual(True, many_windows)
        self.assertEqual(True, building_perspective_view)
        self.assertEqual(False, front_desk)
        self.assertEqual(False, tall_crane)
        self.assertEqual(True, far_building)

    def test_gradient_analysis(self):
        result = gradient_analysis.analyze(self.photo_4)
        self.assertEqual(True, result)

    def test_combined_indoor_analysis(self):
        """
        Testing images to see if they are correctly identified as being having taken
        indoors or outdoors
        """
        front_desk_result = combined_indoor.analyze(self.photo_front_desk)
        self.assertEqual(True, front_desk_result)
        far_building_result = combined_indoor.analyze(self.photo_far_building)
        self.assertEqual(False, far_building_result)

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
            result = stdev.analyze(self.add_photo(image))
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
            result = local_variance.analyze(self.add_photo(image))
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
            result = detail_fft2.analyze(self.add_photo(image))
            print(f'FFT performed on {image}. Result: {result}')
            self.assertEqual(expected_values[image], int(result))

    def test_mean_detail(self):
        """
        Test Mean Detail function (mean_detail.py)
        """
        expected_values = {'100x76-BlackRectangle': 0, '100x76-GreyRectangle': 0,
                           '100x76-WhiteRectangle': 0, '100x100-BlackSquare': 0,
                           '100x100-GreySquare': 0, '100x100-WhiteSquare': 0,
                           '100x76-CheckeredRectangle_1': 1073, '100x76-CheckeredRectangle_2': 1073}

        for image in expected_values:
            result = mean_detail.analyze(self.add_photo(image))
            print(f'Mean Detail performed on {image}. Result: {result}')
            self.assertEqual(expected_values[image], int(result))

