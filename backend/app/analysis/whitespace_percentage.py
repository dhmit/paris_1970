"""

calc_whitespace.py

analysis to calculate ratio of pixels above a certain threshold value to the size of the image
"""

import numpy as np
import cv2

from app.models import Photo


WHITESPACE_THRESHOLD = .6


def analyze(photo: Photo):
    """
    Calculate the whitespace % for a given Photo
    """
    image = photo.get_image_data()

    if image is None:
        return -1

    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalize image pixels to range from 0 to 1
    # Normalized values are used instead of absolute pixel values to account for
    # differences in brightness (across all photos) that may cause white areas in
    # some photos, like a piece of paper, to appear dark.
    normalized_grayscale_image = grayscale_image / np.max(grayscale_image)

    # Count number of pixels that have a value greater than the WHITESPACE_THRESHOLD
    # n.b. this threshold was arbitrarily chosen
    # (uses numpy broadcasting and creates an array of boolean values (0 and 1))
    number_of_pixels = (normalized_grayscale_image > WHITESPACE_THRESHOLD).sum()

    # Percentage of pixels above the threshold to the total number of pixels in the photo
    # (Prevent larger images from being ranked as being composed mostly of whitespace,
    # just because they are larger)
    whitespace_percentage = number_of_pixels / grayscale_image.size * 100

    return whitespace_percentage
