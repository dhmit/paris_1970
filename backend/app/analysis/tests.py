"""
Tests for the main main.
"""

from pathlib import Path

from django.conf import settings
from django.test import TestCase
from matplotlib import pyplot as plt
import numpy as np
import cv2
import os
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
        # TODO: get a photo with lines that we can easily analyze/test against
        lines = find_vanishing_point.analyze(self.photo_2)

        # plt.subplot(121), plt.imshow(self.photo_2, cmap='gray')
        # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(lines, cmap='gray')
        # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        # plt.show()

        # path = os.path.abspath('100px_100px_vanishing_point_X.jpg')
        # image = cv2.imread(path)
        # print(path)

        blank_image = img_1 = np.zeros([100,100,3],dtype=np.uint8)
        image = self.photo_2.get_image_data()

        for l in lines:
            rho, theta = l[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow('image', image)
        cv2.waitKey()
        #cv2.imwrite('houghlines.jpg', image)
        #plt.subplot(122), plt.imshow(image, cmap='gray')
        # assertEquals(expected,output)
        pass
