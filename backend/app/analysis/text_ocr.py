"""
text_ocr.py - analysis to get the words from an image.
"""
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2

from ..models import Photo

MODEL = Photo


def analyze(photo: Photo):
    """
    Analysis function that returns the string that represents the words in the image
    """
    img = photo.get_image_data()

    config = "-l fra --oem 1 --psm 7"
    text = pytesseract.image_to_string(img, config=config)
    return text.strip()
    # width = int(img.shape[0] / 4)
    # height = int(img.shape[1] / 4)
    # dim = (width, height)
    # scaled = cv2.resize(img, dim)
    # cv2.imshow("test", scaled)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
