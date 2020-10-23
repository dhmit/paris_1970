"""

mean_detail.py

Calculate arithmetic mean of results from stdev.py, local_variance.py, and detail_fft2.py to gauge
how these measures of detail compare with each other

"""

from app.models import Photo
from .detail_fft2 import analyze as detail_analyze
from .stdev import analyze as square_analyze
from .local_variance import analyze as lv_analyze

MODEL = Photo


def analyze(photo: Photo):
    """
    Calculate the mean detail for a given Photo arithmetically
    """

    detail = detail_analyze(photo)
    square = square_analyze(photo)
    local_variance = lv_analyze(photo)

    mean = (detail + square + local_variance) / 3

    return mean
