"""

count_photos.py - analysis to count all of the photos in the DB

"""
import unittest
from ..models import Photo

MODEL = Photo


def analysis(photo) -> dict:
    return {'photographer_caption_length': len(photo.photographer_caption)}


class TestSampleAnalysis(unittest.TestCase):
    """
    Test cases to make sure things are running properly
    """
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()  # run the tests
