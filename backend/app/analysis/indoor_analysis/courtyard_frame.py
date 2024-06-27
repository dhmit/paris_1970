'''
courtyard_frame.py
analysis to determine whether there is a dark border around the photo, which would likely indicate
that the photo was taken inside a courtyard or through an alleyway
'''

import numpy as np
import cv2

from app.models import Photo


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
    borders_passed = []
    percent_failed = 0.20
    border_percentage = 0.05 #top and bottom 0.5% of photo
    border_num = int(border_percentage * min(len(normalized_grayscale_image[0]), #length
                                             len(normalized_grayscale_image))) #width
    border_num = max(border_num, 1)

    # Using half of highest pixel as threshold
    max_pixel = 0
    for row in normalized_grayscale_image:
        for pixel in row:
            max_pixel = max(max_pixel, pixel)
    dark_threshold = max_pixel * 0.5

    # Evaluating the top border of photo by comparing each pixel to dark_threshold
    # and seeing if at least 80% pass the threshold
    failed = top_bottom_single(normalized_grayscale_image[0:border_num-1], dark_threshold)
    if len(failed) > percent_failed * border_num * len(normalized_grayscale_image[0]):
        borders_passed.append(False)
    else:
        borders_passed.append(True)
    del(failed[0:len(failed)])

    # Evaluating the bottom border of photo by comparing each pixel to dark_threshold
    # and seeing if at least 80% pass the threshold
    failed = top_bottom_single(normalized_grayscale_image[::-1][0:border_num - 1],
                                      dark_threshold)
    if len(failed) > percent_failed * border_num * len(normalized_grayscale_image[0]):
        borders_passed.append(False)
    else:
        borders_passed.append(True)
    del(failed[0:len(failed)])

    # Evaluating the left border of photo by comparing each pixel to dark_threshold
    # and seeing if at least 80% pass the threshold
    failed = left_right_single(normalized_grayscale_image[1:len(normalized_grayscale_image)-2],
                               border_num,
                               dark_threshold)
    if len(failed) > percent_failed * border_num * (len(normalized_grayscale_image)-2):
        borders_passed.append(False)
    else:
        borders_passed.append(True)
    del(failed[0:len(failed)])

    # Evaluating the right border of photo by comparing each pixel to dark_threshold
    # and seeing if at least 80% pass the threshold
    failed = left_right_single(normalized_grayscale_image[1:len(normalized_grayscale_image) - 2],
                               border_num,
                               dark_threshold,
                               True)
    if len(failed) > percent_failed * border_num * (len(normalized_grayscale_image)-2):
        borders_passed.append(False)
    else:
        borders_passed.append(True)

    # Determining how many borders passed the test
    # Returns True if three or more borders pass
    true_counter = 0
    for border_passed in borders_passed:
        if border_passed:
            true_counter += 1
    return true_counter >= 3

def top_bottom_single(border, threshold):
    '''
    Compares each pixel of the top or bottom border to the threshold. Returns a list of failed
    pixels.
    '''
    failed = []
    for row in border:
        for pixel in row:
            if pixel > threshold:
                failed.append(pixel)
    return failed

def left_right_single(photo_without_top_bottom, border_num, threshold, isRight=False):
    '''
    Compares each pixel of the left or right border to the threshold. Returns a list of failed
    pixels.
    '''
    failed = []
    for row in photo_without_top_bottom:
        if isRight:
            row = row[::-1]
        for pixel in range(border_num):
            if row[pixel] > threshold:
                failed.append(row[pixel])
    return failed
