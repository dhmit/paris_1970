"""

portrait_detection.py

analysis to calculate if there exists at least 1 face beyond the size of 200 x 200
"""

import cv2
from app.models import Photo
MODEL = Photo


def analyze(photo: Photo):
    """
    Face detection using Open CV's haar cascade.
    Param: Photo model
    Return: Boolean if there's at least one face with a minimum size of 200 by 200
    """

    # Load classifier and image. Convert image to grayscale for detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades
                                         + 'haarcascade_frontalface_default.xml')
    img = photo.get_image_data()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use cascade classifier to detect if there exists face(s) with at least given min size
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(200, 200))

    # Calculate region and area of the face(s)
    for (x_coord, y_coord, width, height) in faces:
        img = cv2.rectangle(img, (x_coord, y_coord),
                            (x_coord + width, y_coord + height),
                            (255, 0, 0), 2)

    return len(faces) > 0
