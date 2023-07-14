"""

photographer_caption_length.py - analysis to count all of the photos in the DB
n.b. This is just a sample! Not actually useful... probably.

"""
from ..models import Photo


def analyze(photo: Photo):
    """
    Analysis function that returns the length of the photographer caption for a Photo object
    """
    return len(photo.photographer_caption)
