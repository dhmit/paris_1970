"""
text_ocr.py - analysis to get the words from an image.
"""
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2

from django.conf import settings

from ..models import Photo

MODEL = Photo

def analyze(photo: Photo):
    """
    Analysis function that returns the string that represents the words in the image

    NOTE: In order for this to work, you need to install Tesseract 4.0 into your computer.
    For Mac: brew install tesseract
    For Ubuntu: sudo apt-get install tesseract-ocr
    For Windows: https://github.com/tesseract-ocr/tesseract/wiki#windows
    """
    img = photo.get_image_data()

    # These are configurations for tesseract
    # We are using 'fra' for french. You can also use 'eng' for english
    # --oem selects the OCR Engine Mode, where 1 is the neural nets LSTM engines only mode
    # --psm is the page segmentation mode. We are using 7, which treats image as a single text line
    # --tessdata-dir is where we give the trained data for tesseract.
    #
    # More information can be found at
    # https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
    # under the section: "Understanding OpenCV OCR and Tesseract text recognition"

    config = f"-l fra --oem 1 --psm 7 --tessdata-dir {settings.TESSDATA_DIR}"
    text = pytesseract.image_to_string(img, config=config)
    return text.strip()
