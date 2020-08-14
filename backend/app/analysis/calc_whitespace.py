"""

calc_whitespace.py - analysis to calculate ratio of pixels above a certain threshold value (0.6)
to the size of the image

"""
import unittest
from skimage import io
import numpy as np
import cv2
from app.models import Photo

MODEL = Photo


def analysis(photo) -> dict:
    """
    Calculates the whitespace for all sides of a photo
    """
    photo_srcs = {'front_src': photo.front_src, 'back_src': photo.back_src,
                  'binder_src': photo.binder_src}
    results = {}
    for side in ['front', 'back', 'binder']:
        try:
            url = photo_srcs[side + '_src']

            # Get image, will raise ValueError if src url is ''
            # will raise FileNotFound error if src is just a filename
            image = io.imread(url)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            normalized_gray_image = gray_image / np.max(gray_image)
            number_of_pixels = (normalized_gray_image > .6).sum()
            white_space_ratio = number_of_pixels / gray_image.size
            print(f'Successfully calculated whitespace ratio for photo {photo.id} {side}')
            results[f'white_space_ratio_{side}'] = white_space_ratio
        except (ValueError, FileNotFoundError):
            pass
    return results


class TestSampleAnalysis(unittest.TestCase):
    """
    Test cases to make sure things are running properly
    """

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()  # run the tests
