"""

calc_variance.py

analysis to calculate blurriness of pixels using Laplacian operator from openCV

Lydia + Jackie
"""

import numpy as np
import cv2

from app.models import Photo

MODEL = Photo

def analyze(photo: Photo):
    """
    Calculate the blurriness for a given Photo
    """
    image = photo.get_image_data()

    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Laplacian operator to give a "blurriness" metric
    # Returns this number of a photo in a single floating point number
    local_variance = cv2.Laplacian(grayscale_image, cv2.CV_64F).var()

    # print(local_variance)

    return local_variance
