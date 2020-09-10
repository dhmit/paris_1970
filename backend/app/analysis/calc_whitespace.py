"""

calc_whitespace.py - analysis to calculate ratio of pixels above a certain threshold value (0.6)
to the size of the image

"""

from urllib.error import HTTPError
from http.client import RemoteDisconnected
from textwrap import dedent

from skimage import io
import numpy as np
import cv2

from app.models import Photo

# from .tests import AnalysisTestBase

MODEL = Photo

def analysis(photo) -> dict:
    """
    Calculates the whitespace for all sides of a photo
    """
    photo_srcs = {
        'front_src': photo.front_src,
        'back_src': photo.back_src,
        'binder_src': photo.binder_src
    }
    results = {}
    number_of_photos = len(Photo.objects.all())
    for side in ['front', 'back', 'binder']:
        try:
            url = photo_srcs[side + '_src']

            # Get image, will raise ValueError if src url is ''
            # will raise FileNotFound error if src is just a filename rather than a url
            image = io.imread(url)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            normalized_gray_image = gray_image / np.max(gray_image)
            number_of_pixels = (normalized_gray_image > .6).sum()
            white_space_ratio = number_of_pixels / gray_image.size
            results[f'white_space_ratio_{side}'] = white_space_ratio
            print(f'Successfully calculated whitespace ratio for photo {photo.id} {side}')
        except (ValueError, FileNotFoundError):
            pass
        except (HTTPError, RemoteDisconnected) as base_exception:
            raise Exception(dedent(f'''
                *** Right now, the analysis breaks after too many http requests, so it may not
                calculate whitespace for all the photos, even the first time. If it stops
                working, you will have to wait a while before it is successfully able to make
                requests again. ***
                Successfully calculated whitespace ratio for {photo.id-1}/{number_of_photos}
                photos.
                ''')) from base_exception
    print('Successfully calculated whitespace ratio for all photos.')
    return results
