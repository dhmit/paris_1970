"""

vanishing_point_finder.py

analysis to find significant lines in image and filter lines to find place where most lines
intersect, which should be the vanishing point
"""

import numpy as np
import cv2

from app.models import Photo

MODEL = Photo


def analyze(photo: Photo):
    """
    Calculate the whitespace % for a given Photo
    """
    image = photo.get_image_data()
    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = auto_canny(grayscale_image)

    return edged


def auto_canny(image, sigma=0.00001):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    print("hi" + str(v))
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, 200, 250, 3)
    lines = cv2.HoughLinesP(edged, 1, np.pi / 180, 80, 30, maxLineGap=250)
    print(lines)
    # return the edged image
    return [edged, lines]
