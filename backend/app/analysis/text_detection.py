"""
text_ocr.py
extracts text from image
"""
import cv2
import pytesseract
from ..models import Photo

from django.conf import settings

MODEL = Photo

WIDTH = 50
HEIGHT = 50


def analyze(photo: Photo):
    """
    Function that returns text from an image
    """
    image = photo.get_image_data()
    # Convert image to grayscale
    photo = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # apply threshold
    ret, thresh = cv2.threshold(photo, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    # rectangle-shaped kernel with size WIDTH and HEIGHT

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (WIDTH, HEIGHT))
    # apply dilation
    dilation = cv2.dilate(thresh, kernel, iterations=1)
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    photo2 = photo.copy()
    # A text file is created and flushed
    # file = open("recognized.txt", "w+")
    # file.write("")
    # file.close()

    # Loop through contours to crop rectangles
    # that will be passed to pytesseract for text extraction
    text = ""
    config = f"-l fra --oem 1 --psm 7 --tessdata-dir {settings.TESSDATA_DIR}"
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        # draw rectangle
        rect = cv2.rectangle(photo2, (x, y), (x + width, y + height), (0, 255, 0), 2)
        # crop block
        block = photo2[y:y+height, x:x+width]
        cv2.imshow("test", block)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # Apply OCR
        text += pytesseract.image_to_string(block, config=config) + "\n"
        print("TEXT\n===========", text)

    return text
