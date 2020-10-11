"""
stdev.py

Isolate local regions of an image and find the average of all standard deviations to determine
level of detail in a photo

Josh
"""

import numpy as np
import cv2

from app.models import Photo

MODEL = Photo


def analyze(photo: Photo):
    """
    Calculate the average of the standard deviation of pixels over local regions
    Std computed locally and then averaged to account for, say, black-and-white images
    """

    image = photo.get_image_data()

    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Flatten the grayscale image ndarray to help with calculations

    flat_list = grayscale_image.flatten()

    # Initialize a list that will comprise segments ot the flattened list
    local_regions = []

    # Declare and initialize boundary markers to split flatList into segments
    i = 0
    j = flat_list.size // 64
    interval = flat_list.size // 64

    while j <= flat_list.size:
        # Append segments of the flattened grayscale image array to localRegions
        local_regions.append(flat_list[i: j])
        i, j = j, j + interval

    # Compute the standard deviation of pixels for each individual segment
    for i, region in enumerate(local_regions):
        # Before the calculation and cast, each region is an ndarray
        local_regions[i] = float(np.std(region))
        # After the cast, each element in the list is a single float

    # Return the average of the standard deviations of all local regions
    # If not, return 0
    try:
        return sum(local_regions) / len(local_regions)
    except (ZeroDivisionError, TypeError):
        return 0.0
