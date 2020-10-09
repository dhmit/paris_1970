"""
text_ocr.py - analysis to get the words from an image.
"""
from PIL import ImageEnhance
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import cv2

from django.conf import settings

from ..models import Photo

MODEL = Photo


# Code Source:
# https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/

def decode_predictions(scores, geometry, min_confidence):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scores_data = scores[0, 0, y]
        x_data0 = geometry[0, 0, y]
        x_data1 = geometry[0, 1, y]
        x_data2 = geometry[0, 2, y]
        x_data3 = geometry[0, 3, y]
        angles_data = geometry[0, 4, y]
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scores_data[x] < min_confidence:
                continue
            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = angles_data[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height
            # of the bounding box
            h = x_data0[x] + x_data2[x]
            w = x_data1[x] + x_data3[x]
            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * x_data1[x]) + (sin * x_data2[x]))
            endY = int(offsetY - (sin * x_data1[x]) + (cos * x_data2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scores_data[x])
    # return a tuple of the bounding boxes and associated confidences
    return rects, confidences


def sharpening(image, factor):
    enhancer = ImageEnhance.Sharpness(image)
    sharpened = enhancer.enhance(factor)
    return sharpened


def analyze(photo: Photo):
    """
    Analysis function that returns the string that represents the words in the image

    NOTE: In order for this to work, you need to install Tesseract 4.0 into your computer.
    For Mac: brew install tesseract
    For Ubuntu: sudo apt-get install tesseract-ocr
    For Windows: https://github.com/tesseract-ocr/tesseract/wiki#windows
    """
    # path to input EAST text detector
    east = settings.TEXT_DETECTION_PATH.as_posix()

    # minimum probability required to inspect a region
    min_confidence = 0.01

    # nearest multiples of 32 for resized width and height
    width = 320
    height = 320

    # amount of padding to add to each border of ROI
    padding = 0.12

    # load the input image and grab the image dimensions
    image = photo.get_image_data()
    sharpened = sharpening(image, 2)
    orig = sharpened.copy()
    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    ratio_width = origW / float(newW)
    ratio_height = origH / float(newH)
    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested in -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east)

    # construct a blob from the image.
    # 123.68, 116.78, 103.94 are the average values of ImageNet training set
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    # perform a forward pass of the model to obtain the two output layer sets
    (scores, geometry) = net.forward(layerNames)
    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry, min_confidence)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []
    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective ratios
        startX = int(startX * ratio_width)
        startY = int(startY * ratio_height)
        endX = int(endX * ratio_width)
        endY = int(endY * ratio_height)
        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((endX - startX) * padding)
        dY = int((endY - startY) * padding)
        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(origW, endX + (dX * 2))
        endY = min(origH, endY + (dY * 2))
        # extract the actual padded ROI
        roi = orig[startY:endY, startX:endX]
        # tesseract's CLI doesn't understand Windows-style paths with backslashes,
        # so we explicitly pass the posix-style path
        config = f"-l fra --oem 1 --psm 6 --tessdata-dir {settings.TESSDATA_DIR.as_posix()}"
        text = pytesseract.image_to_string(roi, config=config)
        # add the bounding box coordinates and OCR'd text to the list of results
        results.append(((startX, startY, endX, endY), text))

    # sort the results bounding box coordinates from top to bottom
    results = sorted(results, key=lambda r: r[0][1])

    # set to true if we want to draw a text box in the image
    display = True
    # loop over the results
    for ((startX, startY, endX, endY), text) in results:
        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV, then draw the text and a bounding box surrounding
        # the text region of the input image
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        # display the text OCR'd by Tesseract
        print("OCR TEXT")
        print("========")
        print(text)
        if display:
            output = orig.copy()
            cv2.rectangle(output, (startX, startY), (endX, endY),
                          (0, 0, 255), 2)
            cv2.putText(output, text, (startX, startY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            # show the output image
            # cv2.imshow("Text Detection", output)
            # cv2.waitKey(0)

    detected_text = {result[1].strip() for result in results}
    print(detected_text)
    return detected_text
