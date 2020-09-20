"""

standard_deviation.py

analysis to calculate the standard deviation of pixels in the photo
"""

import numpy as np
import cv2

from app.models import Photo

MODEL = Photo

WHITESPACE_THRESHOLD = .6


def analyze(photo: Photo):
    """
    Calculate the standard deviation of pixels in the image
    """
    image = photo.get_image_data()

    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    standard_deviation = np.std(grayscale_image)

    return standard_deviation
