"""
gradient_analy_valuesis.py - analy_valuesis to determine if significant vertical brightness
gradient
exists
in image

:return: boolean, True if a gradient was found, False otherwise
"""
from statistics import mean
import cv2 as cv
import numpy as np
from app.models import Photo

WHITESPACE_THRESHOLD = .6

def analyze(photo: Photo):
    """
    Determine if image has vertical gradient. Find regression equation to represent vertical
    brightness gradient and return True if correlation coeffcient is greater than 0.85.
    """
    # Convert image to gray_valuescale
    image = photo.get_image_data()
    gray_valuescale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    height = len(gray_valuescale_image)

    # Normalize pixel values in image
    normalized_gray_valuescale_image = gray_valuescale_image / np.max(gray_valuescale_image)

    # Divide image into ten horizontal sections and calculate brightness of each by finding
    # number of pixels with values greater than WHITESPACE_THRESHOLD
    sectioned_pixels = []
    for i in range(10):
        section = normalized_gray_valuescale_image[i * (height//10) : (i+1) * (height//10)]
        sectioned_pixels.append((section > WHITESPACE_THRESHOLD).sum())

    x_vals = [i * (height//10) for i in range(10)]
    x_values = np.array(x_vals, dtype=np.float64)
    y_values = np.array(sectioned_pixels, dtype=np.float64)

    # Find line of best fit and its r-squared value with brightness value from top to bottom of
    # picture
    slope, y_intercept = best_fit_line(x_values, y_values)
    regression_line = [(slope * x) + y_intercept for x in x_values]
    r_squared = find_r_squared(y_values, regression_line)

    # Return if there is a high correlation coefficient. Indicates that substantial and
    # consistent gradient is present.
    return r_squared > 0.85


def best_fit_line(x_values, y_values):
    """
    Parameters:
        x_values (list): list of x-values where ith value corresponds to ith coordinate
        y_values (list): list of y-values where ith value corresponds to ith coordinate

    Return:
        slope (int): slope of line of best fit
        b (int): y-intercept of line of best fit
    """
    slope = (((mean(x_values) * mean(y_values)) - mean(x_values * y_values)) /
         ((mean(x_values) ** 2) - mean(x_values ** 2)))
    y_intercept = mean(y_values) - slope * mean(x_values)
    return slope, y_intercept


def find_r_squared(y_values_orig, y_values_line):
    """
    Parameters:
        y_values_orig (list): list of y-values of original datapoints where ith value corresponds
        to ith
        coordinate
        y_values_line (list): list of y-values from line of best fit where ith value corresponds
        to ith
        coordinate

    Returns value of correlation coefficient.
    """
    def find_squared_error(y_values_orig, y_values_line):
        return sum((y_values_line - y_values_orig) * (y_values_line - y_values_orig))

    y_mean_line = [mean(y_values_orig) for y in y_values_orig]
    squared_error_regr = find_squared_error(y_values_orig, y_values_line)
    squared_error_y_mean = find_squared_error(y_values_orig, y_mean_line)
    return 1 - (squared_error_regr / squared_error_y_mean)
