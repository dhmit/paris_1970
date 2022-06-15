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

import torch
import pickle

from django.conf import settings
from ..models import Photo

MODEL = Photo


# Yolo weights, yolo config, and coco names file
WEIGHTS_PATH = os.path.join(settings.YOLO_DIR, 'yolov5x6.pt')
MODEL_PATH = os.path.join(settings.YOLO_DIR, 'model.pkl')


def load_yolo():
    """
    Loads yolo model to analyze photo.
    """
    if not os.path.exists(WEIGHTS_PATH):
        print(
            'Please download the YOLOv5x6 weights file at '
            'https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5x6.pt '
            'and place it in the yolo_files directory before running this analysis.'
        )
        sys.exit(1)
    try:
        # Try to load pickled model
        with open(MODEL_PATH, 'rb') as model_file:
            model = pickle.load(model_file)
    except (FileNotFoundError, ModuleNotFoundError):
        # Model loading options and their configurations can be found at
        # https://github.com/ultralytics/yolov5/blob/master/hubconf.py
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=WEIGHTS_PATH).eval()

        # Pickle model for faster subsequent load times
        with open(MODEL_PATH, 'wb+') as model_file:
            pickle.dump(model, model_file)
    return model


def analyze(photo: Photo):
    """
    Uses yolo model to detect objects within photos
    Returns a dictionary consisting of each object
    and its frequency in the photo
    """
    # pylint: disable=too-many-locals

    # Get image and image dimensions
    input_image = photo.get_image_data()
    if input_image is None:
        return {
            "boxes": [],
            "labels": [],
        }

    yolo_model = load_yolo()
    output = yolo_model(input_image)
    # Get quantity of detected objects in the image based on indexes
    classes = {}
    boxes = []

    # Loop over the indexes we are keeping
    for obj_data in output.xywh[0]:
        c_x, c_y, width, height, confidence, class_idx = obj_data.numpy()

        # Get coordinates of top left corner of the object
        x = int(round(c_x - (width / 2)))
        y = int(round(c_y - (height / 2)))

        object_class = output.names[int(class_idx)]
        classes.setdefault(object_class, 0)
        classes[object_class] += 1

        boxes.append({
            "label": object_class,
            "x_coord": x,
            "y_coord": y,
            "width": int(round(width)),
            "height": int(round(height)),
            "confidence": int(confidence * 100)
        })

    return {
        "boxes": boxes,
        "labels": classes,
    }
