"""
text_ocr.py - analysis to get the words from an image.
"""
from PIL import ImageEnhance, Image
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import cv2
from django.conf import settings

from ..models import Photo


# Code Source:
# https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/

# pylint: disable-msg=too-many-locals
def decode_predictions(scores, geometry, min_confidence):
    """
    Using scores (probabilities) and the geometrical data to derive
    potential bounding box coordinates that surround text

    :param scores: A list of probabilities
    :param geometry: coordinates
    :param min_confidence: the minimum confidence that you need for a piece of text to be considered
    :return: a tuple of the bounding boxes and associated confidences
    """
    # Grab the number of rows and columns from the scores volume, then initialize
    # our set of bounding box rectangles and corresponding confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # loop over the number of rows
    for y_coords in range(0, numRows):
        scores_data = scores[0, 0, y_coords]
        x_data0 = geometry[0, 0, y_coords]
        x_data1 = geometry[0, 1, y_coords]
        x_data2 = geometry[0, 2, y_coords]
        x_data3 = geometry[0, 3, y_coords]
        angles_data = geometry[0, 4, y_coords]
        # loop over the number of columns
        for x_coords in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scores_data[x_coords] < min_confidence:
                continue
            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x_coords * 4.0, y_coords * 4.0)
            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = angles_data[x_coords]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height
            # of the bounding box
            height = x_data0[x_coords] + x_data2[x_coords]
            width = x_data1[x_coords] + x_data3[x_coords]
            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            end_x = int(offsetX + (cos * x_data1[x_coords]) + (sin * x_data2[x_coords]))
            end_y = int(offsetY - (sin * x_data1[x_coords]) + (cos * x_data2[x_coords]))
            start_x = int(end_x - width)
            start_y = int(end_y - height)
            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((start_x, start_y, end_x, end_y))
            confidences.append(scores_data[x_coords])
    return rects, confidences


def sharpening(image, factor):
    """
    Sharpen an image

    :param image: The image to sharpen
    :param factor: an integer representing how much you want to sharpen the image
    :return: the sharpened image
    """
    image = Image.fromarray(image)
    enhancer = ImageEnhance.Sharpness(image)
    sharpened = enhancer.enhance(factor)
    return sharpened


def get_boxes_from_image(photo, height, width):
    """
    Gets the boxes that might contain text in a photo
    :param photo: the photo to get the boxes from
    :return: the boxes that might contain text in a photo
    """
    # path to input EAST text detector
    east = settings.TEXT_DETECTION_PATH.as_posix()

    # minimum probability required to inspect a region
    min_confidence = 0.5

    # define the two output layer names for the EAST detector model that
    # we are interested in -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east)

    # construct a blob from the image.
    # 123.68, 116.78, 103.94 are the average values of ImageNet training set
    blob = cv2.dnn.blobFromImage(photo, 1.0, (height, width),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    # perform a forward pass of the model to obtain the two output layer sets
    (scores, geometry) = net.forward(layerNames)
    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry, min_confidence)
    return non_max_suppression(np.array(rects), probs=confidences)


# pylint: disable-msg=too-many-locals
def analyze(photo: Photo):
    """
    Analysis function that returns the string that represents the words in the image

    NOTE: In order for this to work, you need to install Tesseract 4.0 into your computer.
    For Mac: brew install tesseract
    For Ubuntu: sudo apt-get install tesseract-ocr
    For Windows: https://github.com/tesseract-ocr/tesseract/wiki#windows
    """
    # amount of padding to add to each border of ROI
    padding = 0.15

    # nearest multiples of 32 for resized width and height
    width = 320
    height = 320

    # load the input image and grab the image dimensions
    image = photo.get_image_data()

    sharpened = sharpening(image, 2)
    orig = sharpened.copy()
    orig = np.array(orig)

    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    ratio_width = origW / float(newW)
    ratio_height = origH / float(newH)
    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (height, width) = image.shape[:2]

    boxes = get_boxes_from_image(image, height, width)

    # initialize the list of results
    results = []

    # loop over the bounding boxes
    for (start_x, start_y, end_x, end_y) in boxes:
        # scale the bounding box coordinates based on the respective ratios
        start_x = int(start_x * ratio_width)
        start_y = int(start_y * ratio_height)
        end_x = int(end_x * ratio_width)
        end_y = int(end_y * ratio_height)
        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        delta_x = int((end_x - start_x) * padding)
        delta_y = int((end_y - start_y) * padding)
        # apply padding to each side of the bounding box, respectively
        start_x = max(0, start_x - delta_x)
        start_y = max(0, start_y - delta_y)
        end_x = min(origW, end_x + (delta_x * 2))
        end_y = min(origH, end_y + (delta_y * 2))
        # extract the actual padded ROI
        roi = orig[start_y:end_y, start_x:end_x]
        # tesseract's CLI doesn't understand Windows-style paths with backslashes,
        # so we explicitly pass the posix-style path
        config = f"-l fra --oem 1 --psm 6 --tessdata-dir {settings.TESSDATA_DIR.as_posix()}"
        text = pytesseract.image_to_string(roi, config=config)
        # add the bounding box coordinates and OCR'd text to the list of results
        results.append(((start_x, start_y, end_x, end_y), text))

    # sort the results bounding box coordinates from top to bottom
    results = sorted(results, key=lambda r: r[0][1])

    # set to true if we want to draw a text box in the image
    display = False
    # loop over the results
    for ((startX, startY, endX, endY), text) in results:
        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV, then draw the text and a bounding box surrounding
        # the text region of the input image
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        # display the text OCR'd by Tesseract
        # print("OCR TEXT")
        # print("========")
        # print(text)
        if display:
            output = orig.copy()
            cv2.rectangle(output, (startX, startY), (endX, endY),
                          (0, 0, 255), 2)
            cv2.putText(output, text, (startX, startY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            # show the output image
            cv2.imshow("Text Detection", output)
            cv2.waitKey(0)

    return ' '.join([result[1].strip() for result in results])
