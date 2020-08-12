"""

count_photos.py - analysis to count all of the photos in the DB

"""
import unittest
from ..models import Photo


model_field = 'photographer_caption_length'


def analysis() -> dict:
    result = {}
    for photo in Photo.objects.all():
        result[photo.id] = len(photo.photographer_caption)
    return result


class TestSampleAnalysis(unittest.TestCase):
    """
    Test cases to make sure things are running properly
    """
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()  # run the tests
