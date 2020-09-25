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
    return None

