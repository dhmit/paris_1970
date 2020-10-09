"""

average_detail.py

analysis to average out results from three standard deviation functions

"""

from app.models import Photo
from .detail import analyze as detail_analyze
from .stdev import analyze as square_analyze
from .local_variance import analyze as lv_analyze


MODEL = Photo

def analyze(photo: Photo):
    """
    Calculate the average detail for a given Photo
    """

    detail = detail_analyze(photo)
    square = square_analyze(photo)
    local_variance = lv_analyze(photo)

    average = (detail + square + local_variance) / 3

    return average
