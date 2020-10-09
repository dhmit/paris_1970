"""

foreground_percentage.py

analysis to extract the foreground of an image and perform analysis on that foreground
"""

import numpy as np
import cv2 as cv

from app.models import Photo

MODEL = Photo


def analyze(photo: Photo):
    """
    Returns percentage of photo that is part of the foreground
    """
    foreground_mask = grabcut_analysis(photo)
    num_foreground_pixels = np.count_nonzero(foreground_mask)
    return num_foreground_pixels / foreground_mask.size * 100


def grabcut_analysis(photo: Photo):
    """
    Performs grabcut algorithm on the photo
    Returns the foreground mask
    """
    # Load photo
    img = photo.get_image_data()

    # Initialize with zeros
    mask = np.zeros(img.shape[:2], np.uint8)
    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)

    # Set rectangle (our guess of the foreground) to be the entire photo
    rect = (0, 0, img.shape[0], img.shape[1])

    # Foreground extraction with GrabCut
    cv.grabCut(img, mask, rect, background_model, foreground_model, 5, cv.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    return mask2
