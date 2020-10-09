"""


"""

import numpy as np
import cv2 as cv

from app.models import Photo

MODEL = Photo

WHITESPACE_THRESHOLD = .6


def analyze(photo: Photo):

    image = photo.get_image_data()
    print(image)
    grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    h = len(grayscale_image)
    w = len(grayscale_image[0])

    normalized_grayscale_image = grayscale_image / np.max(grayscale_image)

    top_portion = normalized_grayscale_image[:h // 10]
    bottom_portion = normalized_grayscale_image[9 * (h // 10):]
    print(top_portion)
    print(bottom_portion)

    top_pixels = (top_portion > WHITESPACE_THRESHOLD).sum()
    flagged_pixels = (top_portion < 0.4).sum()
    bottom_pixels = (bottom_portion > WHITESPACE_THRESHOLD).sum()
    top_whitespace = top_pixels / top_portion.size * 100
    bottom_whitespace = bottom_pixels / bottom_portion.size * 100
    ratio = top_whitespace / bottom_whitespace

    print('Top Portion:', top_whitespace, ' Bottom Portion:', bottom_whitespace)
    print('Flagged Pixels:', flagged_pixels)
    print('Ratio', ratio)

    return ratio > 1.1

