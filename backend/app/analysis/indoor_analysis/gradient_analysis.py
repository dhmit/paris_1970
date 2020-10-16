"""
gradient_analysis.py - analysis to determine if significant vertical brightness gradient exists
in image

:return: boolean, True if a gradient was found, False otherwise
"""

import cv2 as cv
import numpy as np
from statistics import mean

from app.models import Photo

MODEL = Photo

WHITESPACE_THRESHOLD = .6

def analyze(photo: Photo):
    """
    Determine if image has vertical gradient. Find regression equation to represent vertical
    brightness gradient and return True if correlation coeffcient is greater than 0.85.
    """
    # Convert image to grayscale
    image = photo.get_image_data()
    grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    height = len(grayscale_image)
    width = len(grayscale_image[0])

    # Normalize pixel values in image
    normalized_grayscale_image = grayscale_image / np.max(grayscale_image)

    # Divide image into ten horizontal sections and calculate brightness of each by finding
    # number of pixels with values greater than WHITESPACE_THRESHOLD
    sectioned_pixels = []
    for i in range(10):
        section = normalized_grayscale_image[i * (height//10) : (i+1) * (height//10)]
        sectioned_pixels.append((section > WHITESPACE_THRESHOLD).sum())

    x_vals = [i * (height//10) for i in range(10)]
    xs = np.array(x_vals, dtype=np.float64)
    ys = np.array(sectioned_pixels, dtype=np.float64)

    # Find line of best fit and its r-squared value with brightness value from top to bottom of
    # picture
    m, b = best_fit_line(xs, ys)
    regression_line = [(m * x) + b for x in xs]
    r_squared = find_r_squared(ys, regression_line)

    # Return if there is a high correlation coefficient. Indicates that substantial and
    # consistent gradient is present.
    return r_squared > 0.85

def best_fit_line(xs, ys):
    """
    Parameters:
        xs (list): list of x-values where ith value corresponds to ith coordinate
        ys (list): list of y-values where ith value corresponds to ith coordinate

    Return:
        m (int): slope of line of best fit
        b (int): y-intercept of line of best fit
    """
    m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
         ((mean(xs) ** 2) - mean(xs ** 2)))
    b = mean(ys) - m * mean(xs)
    return m, b

def find_r_squared(ys_orig, ys_line):
    """
    Parameters:
        ys_orig (list): list of y-values of original datapoints where ith value corresponds to ith
        coordinate
        ys_line (list): list of y-values from line of best fit where ith value corresponds to ith
        coordinate

    Returns value of correlation coefficient.
    """
    def find_squared_error(ys_orig, ys_line):
        return sum((ys_line - ys_orig) * (ys_line - ys_orig))

    y_mean_line = [mean(ys_orig) for y in ys_orig]
    squared_error_regr = find_squared_error(ys_orig, ys_line)
    squared_error_y_mean = find_squared_error(ys_orig, y_mean_line)
    return 1 - (squared_error_regr / squared_error_y_mean)
