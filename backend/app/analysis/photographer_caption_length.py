"""

count_photos.py - analysis to count all of the photos in the DB

"""
import unittest
from ..models import Photo

MODEL = Photo


def analyze(photo: Photo):
    return len(photo.photographer_caption)
