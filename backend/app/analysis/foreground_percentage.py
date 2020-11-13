"""

foreground_percentage.py

analysis to extract the foreground of an image and perform analysis on that foreground
"""

import numpy as np
from skimage import io
import cv2 as cv

from app.models import Photo

MODEL = Photo


def analyze(photo: Photo):
    """
    Returns percentage of the photo that is part of the foreground
    """
    photo_array = photo.get_image_data()
    return analyze_numpy_photo(photo_array)


def analyze_from_file(photo_path):
    """
    Reads a photo from a file and returns percentage of the photo
    that is part of the foreground
    """
    photo = io.imread(photo_path)
    return analyze_numpy_photo(photo)


def analyze_numpy_photo(photo):
    """
    Returns percentage of a numpy photo that is part of the foreground
    """
    foreground_mask = grabcut_analysis(photo)
    black_pixels = []
    for i in range(len(foreground_mask)):
        for j in range(len(foreground_mask[i])):
            if foreground_mask[i][j] == 0:
                black_pixels.append([i, j])

    print(black_pixels)
    num_foreground_pixels = np.count_nonzero(foreground_mask)
    return {
        "percent": num_foreground_pixels / foreground_mask.size * 100,
        "mask": black_pixels,
        }


def grabcut_analysis(photo):
    """
    Performs grabcut algorithm on a numpy array photo
    Returns the foreground mask
    """
    # Initialize with zeros
    mask = np.zeros(photo.shape[:2], np.uint8)
    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)

    # Set rectangle (our guess of the foreground) to be the entire photo
    rect = (1, 1, photo.shape[0], photo.shape[1])

    # Foreground extraction with GrabCut
    cv.grabCut(photo, mask, rect, background_model, foreground_model, 5, cv.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    return mask2
