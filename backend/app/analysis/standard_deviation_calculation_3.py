"""
standard_deviation_calculation.py

Isolate local regions of an image and find the average of all standard deviations to determine level of detail in a
photo
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

    #flatten the grayscale image ndarray to help with calculations
    flatList = grayscale_image.flatten()

    #initalize a list that will comprise segments ot the flattened list
    localRegions = []

    #declare and initialize boundary markers to split flatList into segments
    i = 0
    j = flatList.size//4
    interval = flatList.size//4

    while j<=flatList.size:
    #append segments of the flattened grayscale image array to localRegions
        localRegions.append(flatList[i:j])
        i, j = i+interval, j+interval

    #compute the standard deviation of pixels for each individual segment
    for pxRegion in localRegions:
        pxRegion = np.std(pxRegion)

    #return the average of the standard deviations of all local regions
    #if not, return 0
    try:
        return sum(localRegions) / len(localRegions)
    except ZeroDivisionError:
        return 0.0
