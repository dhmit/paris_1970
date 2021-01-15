"""

yolo_model.py -
analysis that aggregates other obj detection methods
takes in the name of the obj we're looking for (for example, words, heads, pedestrians, stop signs)
returns the number of that specific obj for each photo in the database

links:
- https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
- https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/

"""
import os
import sys

import numpy as np
import cv2

from django.conf import settings
from ..models import Photo

MODEL = Photo
CONFIDENCE = 0.5
THRESHOLD = 0.3

# Yolo weights, yolo config, and coco names file
WEIGHTS = os.path.join(settings.YOLO_DIR, 'yolov3.weights')
CONFIG = os.path.join(settings.YOLO_DIR, 'yolov3.cfg')
CLASS_NAMES = os.path.join(settings.YOLO_DIR, 'coco.names')


def load_yolo():
    """
    Loads yolo model to analyze photo.
    """
    if not os.path.exists(WEIGHTS):
        print(
            'Please download the YLOLOv3-608 weights file at '
            'https://pjreddie.com/media/files/yolov3.weights '
            'and place it in the yolo_files directory before running this analysis.'
        )
        sys.exit(1)

    net = cv2.dnn.readNet(WEIGHTS, CONFIG)
    with open(CLASS_NAMES, "r") as file:
        classes = [line.strip() for line in file.readlines()]
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    return net, classes, colors, output_layers


def create_box(detection, image_dimensions):
    """
    Creates box around detected objects.
    """
    image_height, image_width = image_dimensions
    box = detection[0:4] * np.array([image_width, image_height, image_width, image_height])
    center_x, center_y, box_width, box_height = box.astype("int")

    # Reformat box coordinates to top-left based from center based
    x_coordinate = int(center_x - (box_width / 2))
    y_coordinate = int(center_y - (box_height / 2))

    return [x_coordinate, y_coordinate, int(box_width), int(box_height)]


def yolo_setup(input_image, net):
    """
    Generates the output layers used to extract class IDs and
    confidence values of the object detections in the input image
    """
    # Determine only the *output* layer names that we need from YOLO
    layer_names = [net.getLayerNames()[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Construct a blob from the input image
    blob = cv2.dnn.blobFromImage(input_image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform a forward pass of the YOLO object detector to get bounding boxes and their
    # associated probabilities
    return net.forward(layer_names)


def analyze(photo: Photo):
    """
    Uses yolo model to detect objects within photos
    Returns a dictionary consisting of each object
    and its frequency in the photo
    """
    # pylint: disable=too-many-locals

    yolo_model = load_yolo()
    net = yolo_model[0]
    labels = yolo_model[1]

    # Get image and image dimensions
    input_image = photo.get_image_data()
    if input_image is None:
        return {
            "boxes": [],
            "labels": [],
        }

    image_dimensions = input_image.shape[:2]
    layer_outputs = yolo_setup(input_image, net)

    boxes = []
    confidences = []
    class_ids = []

    # Loop over each of the layer outputs
    for output in layer_outputs:
        # Loop over each detection in the output
        for detection in output:
            # Extract the class ID and confidence (probability) of the current object detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # Filter out predictions with a probability less than CONFIDENCE (minimum probability)
            if confidence > CONFIDENCE:
                new_box = create_box(detection, image_dimensions)
                boxes.append(new_box)
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD)
    if indexes is None or len(indexes) == 0:
        return {}

    # Get quantity of detected objects in the image based on indexes
    classes = {}
    result = []

    # Loop over the indexes we are keeping
    for i in indexes.flatten():
        object_class = labels[class_ids[i]]
        rect_coord = boxes[i]

        if object_class in classes:
            classes[object_class] += 1
        else:
            classes[object_class] = 1

        result.append(
            {
                "label": object_class,
                "x_coord": rect_coord[0],
                "y_coord": rect_coord[1],
                "width": rect_coord[2],
                "height": rect_coord[3],
            }
        )

    return {
        "boxes": result,
        "labels": classes,
    }
