"""

count_photos.py - analysis to count all of the photos in the DB

"""
from ..models import Photo

MODEL = Photo


def analyze(photo: Photo):
    """
    Analysis function that returns the length of the photographer caption for a Photo object
    """
    return len(photo.photographer_caption)
