
"""
find_windows.py - analysis to determine if a window is present
in a given image or not

:return: boolean, True if a window was found, False otherwise
"""

import numpy as np
import cv2

from app.models import Photo

MODEL = Photo


def analyze(photo: Photo):
    """
    Determine if a given image features a window
    """
    image = photo.get_image_data()

    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find up to 200 corners in the grayscale image
    # corners is a list of 2 double lists,
    # the first double is the x-coordinate and second double is y-coordinate of
    # the pixel where a corner can be found in the image
    corners = cv2.goodFeaturesToTrack(grayscale_image, 200, .5, 10)

    # no corners found means no windows exist
    if corners is None:
        return False

    corners = np.int0(corners)
    x_set = set()
    y_set = set()

    # iterate through all corners until four corners that
    # create a perfect rectangular shape (a likely window) are found
    for i in corners:
        x, y = i.ravel()
        if x in x_set and y in y_set:
            return True  # window found
        x_set.add(x)
        y_set.add(y)

    return False
