"""

pop_density_detection.py - analysis to count the number of people in the photos in the DB

"""

import numpy as np
import imutils
from imutils.object_detection import non_max_suppression
import cv2
from ..models import Photo




MODEL = Photo

def analyze(photo: Photo):
    """
    Analysis function that returns the length of the photographer caption for a Photo object
    """

    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # load the image and resize it to (1) reduce detection time
    # and (2) improve detection accuracy
    image = photo.get_image_data()
    image = imutils.resize(image, width=min(400, image.shape[1]))
    orig = image.copy()

    # detect people in the image, try adjusting parameters before creating new one
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # draw the final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    #cv2.imwrite(f'test_pop_density_detection_{photo.id}.jpg', image)

    num_people = len(pick)
    return num_people

