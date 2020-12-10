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
    foreground_percentage,
    whitespace_percentage,
    find_vanishing_point,
    portrait_detection,
    stdev,
    detail_fft2,
    local_variance,
    mean_detail,
    yolo_model
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

    def add_photo(self, photo_name_or_path):
        """
        Creates a Photo object and adds it to self.photo_dict given
        the name of the photo or path relative to settings.TEST_PHOTOS_DIR
        """
        if Photo.objects.exists():
            photo_number = Photo.objects.last().number + 1
        else:
            photo_number = 0

        photo = Photo(number=photo_number, map_square=self.map_square)

        if isinstance(photo_name_or_path, str):
            photo.front_local_path = os.path.join(settings.TEST_PHOTOS_DIR,
                                                  f'{photo_name_or_path}.jpg')
        elif isinstance(photo_name_or_path, Path):
            photo.front_local_path = Path(settings.TEST_PHOTOS_DIR, photo_name_or_path)

        photo.save()

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

    def test_portrait_detection_true(self):
        photo = self.add_photo('test_portrait_detection_true')
        result = portrait_detection.analyze(photo)
        self.assertEqual(True, result)

    def test_portrait_detection_false(self):
        photo = self.add_photo('test_portrait_detection_false')
        result = portrait_detection.analyze(photo)
        self.assertEqual(False, result)

    def test_foreground_percentage(self):
        """
        Test the foreground percentage function on an image with a black square in the center
        surrounded by all white pixels
        """
        photo = self.add_photo('4%_black')
        result = (foreground_percentage.analyze(photo))["percent"]
        # Result is not exact (range of values)
        # Needs more testing
        self.assertTrue(2 <= result <= 6)

    def test_foreground_percentage_real_image(self):
        """
        Test the foreground percentage function on a real competition photo.
        """
        photo = self.add_photo('foreground_801_4')
        result = (foreground_percentage.analyze(photo))["percent"]

        # Result is not exact (range of values)
        # Needs more testing
        self.assertTrue(60 <= result <= 64)

    def test_foreground_percentage_from_file(self):
        """
        Test the foreground percentage function on a real competition photo.
        The photo is read from file so that we can test performance differences between
        the django model and the real image.
        :return:
        """
        file_path = Path(settings.TEST_PHOTOS_DIR, 'foreground_801_4.jpg')

        result = (foreground_percentage.analyze_from_file(file_path))["percent"]
        # Result is not exact (range of values)
        # Needs more testing
        self.assertTrue(60 <= result <= 64)

    def test_courtyard_frame(self):
        """
        Testing a variety of images to see if they are correctly
        identified as having a dark frame, meaning they are likely
        images of a courtyard
        """
        photo_00 = self.add_photo(Path('courtyard_frame', 'test1.jpg'))
        photo_01 = self.add_photo(Path('courtyard_frame', 'test2.jpg'))
        photo_02 = self.add_photo(Path('courtyard_frame', 'test3.jpg'))
        photo_03 = self.add_photo(Path('courtyard_frame', 'test3_copy.jpg'))
        photo_04 = self.add_photo(Path('courtyard_frame', 'test4.jpg'))

        result00 = courtyard_frame.analyze(photo_00)
        self.assertEqual(False, result00)
        result01 = courtyard_frame.analyze(photo_01)
        self.assertEqual(True, result01)
        result02 = courtyard_frame.analyze(photo_02)
        self.assertEqual(True, result02)
        result03 = courtyard_frame.analyze(photo_03)
        self.assertEqual(True, result03)
        result04 = courtyard_frame.analyze(photo_04)
        self.assertEqual(True, result04)

    def test_find_windows(self):
        """
        Testing a variety of images to see if they are correctly
        identified as having windows or not
        """
        photo_square = self.add_photo(Path('window_photos', 'find_windows_test_photo.jpg'))
        photo_black = self.add_photo(Path('window_photos', 'fully_black_image.jpg'))
        photo_white = self.add_photo(Path('window_photos', 'fully_white_image.jpg'))
        photo_windows = self.add_photo(Path('window_photos', 'gray_building_with_windows.jpg'))
        photo_perspective_building = self.add_photo(Path('window_photos', 'ms_240_10_cleaned.jpg'))
        photo_tall_crane = self.add_photo(Path('window_photos', 'tall_crane.jpg'))
        photo_far_building = self.add_photo(Path('window_photos', 'far_window_buildings.jpg'))
        photo_front_desk = self.add_photo(Path('window_photos', 'indoor_front_desk.jpg'))

        self.assertEqual(True, find_windows.analyze(photo_square))
        self.assertEqual(False, find_windows.analyze(photo_black))
        self.assertEqual(False, find_windows.analyze(photo_white))
        self.assertEqual(True, find_windows.analyze(photo_windows))
        self.assertEqual(True, find_windows.analyze(photo_perspective_building))
        self.assertEqual(False, find_windows.analyze(photo_front_desk))
        self.assertEqual(False, find_windows.analyze(photo_tall_crane))
        self.assertEqual(True, find_windows.analyze(photo_far_building))

    def test_gradient_analysis(self):
        photo = self.add_photo(Path('square_503', '94_binder copy.jpg'))
        result = gradient_analysis.analyze(photo)
        self.assertEqual(True, result)

    def test_combined_indoor_analysis(self):
        """
        Testing images to see if they are correctly identified as being having taken
        indoors or outdoors
        """
        photo_far_building = self.add_photo(Path('window_photos', 'far_window_buildings.jpg'))
        photo_front_desk = self.add_photo(Path('window_photos', 'indoor_front_desk.jpg'))

        front_desk_result = combined_indoor.analyze(photo_front_desk)
        self.assertEqual(True, front_desk_result)
        far_building_result = combined_indoor.analyze(photo_far_building)
        self.assertEqual(False, far_building_result)

    def test_yolo_model_object_detection(self):
        """
        Testing images for object detection tasks using the Yolo model
        :return: boolean statements from assertions
        """
        photo_with_people = self.add_photo('test_portrait_detection_true')
        photo_with_no_objects = self.add_photo('100x100-GreySquare')
        result_with_people = yolo_model.analyze(photo_with_people)
        result_with_nothing = yolo_model.analyze(photo_with_no_objects)
        self.assertIsNotNone(result_with_people)
        self.assertEqual(result_with_nothing, {})

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

    def test_find_vanishing_point(self):
        """
        Vanishing point returned should be the point that has the most intersections
        with the lines detected in a photo

        Partition on location of vanishing point: at intersection between lines, does not exist
        Partition on number of lines: 0, 1, >1
        """
        #add photo
        photo = self.add_photo('100px_100px_vanishing_point_X')
        photo2 = self.add_photo('100x100_500px-white_500px-black')
        # covers when image is x, intersecting lines in the middle, vanishing point exists
        result = find_vanishing_point.analyze(photo)['vanishing_point_coord']
        expected = (50, 50)
        distance = ((result['x'] - expected[0]) ** 2 + (result['y'] - expected[1]) ** 2) ** (1/2)
        self.assertTrue(distance < 2)

        # covers when online line is horizontal (supposed to ignore),  1 line, van point does
        # not exist
        result2 = find_vanishing_point.analyze(photo2)['vanishing_point_coord']
        self.assertEqual(None, result2)
