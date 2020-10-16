'''
courtyard_frame.py
analysis to determine whether there is a dark border around the photo, which would likely indicate
that the photo was taken inside a courtyard or through an alleyway
'''

import numpy as np
import cv2

from app.models import Photo

MODEL = Photo

def analyze(photo: Photo):
    """
    Determines if an image is a courtyard photo by identifying a dark frame around outer boundary
    of photo. Returns boolean.
    """
    image = photo.get_image_data()

    # Convert image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalize image pixels to range from 0 to 1
    normalized_grayscale_image = grayscale_image / np.max(grayscale_image)

    # Setting up variables
    counter = 0
    failed = []
    borders_passed = []
    percent_failed = 0.20
    border_percentage = 0.05 #top and bottom 0.5% of photo
    length = len(normalized_grayscale_image[0])
    width = len(normalized_grayscale_image)
    border_num = int(border_percentage * min(length, width)) #number of pixels we want to check
    if border_num < 1:
        border_num = 1

    # Using half of highest pixel as threshold
    max_pixel = 0
    for row in normalized_grayscale_image:
        for pixel in row:
            if pixel > max_pixel:
                max_pixel = pixel
    DARK_THRESHOLD = max_pixel * 0.5

    # Evaluating the top border of photo by comparing each pixel to DARK_THRESHOLD
    # and seeing if at least 80% pass the threshold
    failed = top_bottom_single_border(normalized_grayscale_image[0:border_num-1], DARK_THRESHOLD)
    if len(failed) > percent_failed * border_num * length:
        borders_passed.append(False)
    else:
        borders_passed.append(True)
    del(failed[0:len(failed)])

    # Evaluating the bottom border of photo by comparing each pixel to DARK_THRESHOLD
    # and seeing if at least 80% pass the threshold
    failed = top_bottom_single_border(normalized_grayscale_image[::-1][0:border_num - 1], DARK_THRESHOLD)
    if len(failed) > percent_failed * border_num * length:
        borders_passed.append(False)
    else:
        borders_passed.append(True)
    del(failed[0:len(failed)])

    # Evaluating the left border of photo by comparing each pixel to DARK_THRESHOLD
    # and seeing if at least 80% pass the threshold
    for row in normalized_grayscale_image[1:len(normalized_grayscale_image)-2]:
        for pixel in range(border_num):
            if row[pixel] > DARK_THRESHOLD:
                failed.append(row[pixel])
            counter += 1
    if len(failed) > percent_failed * border_num * (width-2):
        borders_passed.append(False)
    else:
        borders_passed.append(True)
    del(failed[0:len(failed)])

    # Evaluating the right border of photo by comparing each pixel to DARK_THRESHOLD
    # and seeing if at least 80% pass the threshold
    for row in normalized_grayscale_image[1:len(normalized_grayscale_image) - 2]:
        for pixel in range(border_num):
            if row[::-1][pixel] > DARK_THRESHOLD:
                failed.append(row[pixel])
            counter += 1
    if len(failed) > percent_failed * border_num * (width-2):
        borders_passed.append(False)
    else:
        borders_passed.append(True)

    # Determining how many borders passed the test
    # Returns True if three or more borders pass
    true_counter = 0
    for border_passed in borders_passed:
        if border_passed:
            true_counter += 1
    if true_counter >= 3:
        return True
    else:
        return False

def top_bottom_single_border(border, threshold):
    '''
    Compares each pixel of the given border to the threshold. Returns a list of failed pixels.
    '''
    failed = []
    for row in border:
        for pixel in row:
            if pixel > threshold:
                failed.append(pixel)
    return failed
