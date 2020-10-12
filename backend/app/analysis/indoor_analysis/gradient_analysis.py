import cv2 as cv
import numpy as np
from statistics import mean

from app.models import Photo

MODEL = Photo

WHITESPACE_THRESHOLD = .6


def analyze(photo: Photo):

    image = photo.get_image_data()
    grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    h = len(grayscale_image)
    w = len(grayscale_image[0])

    normalized_grayscale_image = grayscale_image / np.max(grayscale_image)

    sectioned_pixels = []
    for i in range(10):
        section = normalized_grayscale_image[i * (h//10) : (i+1) * (h//10)]
        sectioned_pixels.append((section > WHITESPACE_THRESHOLD).sum())

    x_vals = [i * (h//10) for i in range(10)]
    xs = np.array(x_vals, dtype=np.float64)
    ys = np.array(sectioned_pixels, dtype=np.float64)

    def best_fit_line(xs, ys):
        m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
             ((mean(xs) ** 2) - mean(xs ** 2)))
        b = mean(ys) - m * mean(xs)
        return m, b

    def find_squared_error(ys_orig, ys_line):
        return sum((ys_line - ys_orig) * (ys_line - ys_orig))

    def find_r_squared(ys_orig, ys_line):
        y_mean_line = [mean(ys_orig) for y in ys_orig]
        squared_error_regr = find_squared_error(ys_orig, ys_line)
        squared_error_y_mean = find_squared_error(ys_orig, y_mean_line)
        return 1 - (squared_error_regr / squared_error_y_mean)

    m, b = best_fit_line(xs, ys)
    regression_line = [(m * x) + b for x in xs]
    r_squared = find_r_squared(ys, regression_line)

    return r_squared > 0.85

