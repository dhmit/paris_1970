"""

average.py

analysis to average out results from three standard deviation functions

"""

import numpy as np
import cv2

from app.models import Photo
from .detail import analyze as detailanalyze
from .stdev_3 import analyze as squareanalyze
from .local_variance import analyze as lvanalyze


MODEL = Photo

def analyze(photo: Photo):
    """
    Calculate the average detail for a given Photo
    """

    detail = detailanalyze(photo)
    square = squareanalyze(photo)
    local_variance = lvanalyze(photo)

    average = (detail + square + local_variance) / 3

    return average
