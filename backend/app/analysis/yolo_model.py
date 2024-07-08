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
import pickle
import requests

import torch

from django.conf import settings
from ..models import Photo
from .object_detection_helpers import make_detection_boxes

# Yolo weights, yolo config, and coco names file
WEIGHTS_URL = "https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5x6.pt"
WEIGHTS_FILENAME = "yolov5x6.pt"
WEIGHTS_PATH = os.path.join(settings.YOLO_DIR, WEIGHTS_FILENAME)
MODEL_PATH = os.path.join(settings.YOLO_DIR, 'model.pkl')


def load_yolo():
    """
    Loads yolo model to analyze photo.
    """
    if not os.path.exists(WEIGHTS_PATH):
        print(f"Downloading weights to backend/app/analysis/yolo_files/{WEIGHTS_FILENAME}...")
        with open(WEIGHTS_PATH, "wb+") as file:
            file.write(requests.get(WEIGHTS_URL).content)
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


def detection_iterator(yolo_output):
    for obj_data in yolo_output.xywh[0]:
        c_x, c_y, width, height, confidence, class_idx = obj_data.numpy()
        object_class = yolo_output.names[int(class_idx)]
        yield object_class, c_x, c_y, width, height, confidence


def get_analyze():
    """
    Uses yolo model to detect objects within photos
    Returns a dictionary consisting of each object
    and its frequency in the photo
    """
    yolo_model = load_yolo()
    def run(photo: Photo):
        # Get image and image dimensions
        input_image = photo.get_image_data()
        if input_image is None:
            return {
                "boxes": [],
                "labels": {},
            }
        
        output = yolo_model(input_image)
        detections = detection_iterator(output)
        return make_detection_boxes(detections)
    return run
