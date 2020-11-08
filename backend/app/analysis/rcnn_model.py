"""

rcnn_model.py -
analysis that aggregates other obj detection methods
takes in the name of the obj we're looking for (for example, words, heads, pedestrians, stop signs)
returns the number of that specific obj for each photo in the database

links:
- https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
- https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/

"""
import os
import numpy

import cv2

from ..models import Photo

from gluoncv import model_zoo, data
from django.conf import settings

MODEL = Photo
CONFIDENCE = 0.5
THRESHOLD = 0.3
CLASS_NAMES = os.path.join(settings.YOLO_DIR, 'coco.names')


def analyze(photo: Photo):
    # net, labels, colors, output_layers = load_yolo()
    with open(CLASS_NAMES, "r") as f:
        labels = [line.strip() for line in f.readlines()]
    # Get image and image dimensions
    # input_image = photo.get_image_data()
    # image = cv2.resize(image, (216, 216))
    # height, width, channels = image.shape
    # input_image = image.reshape(1, height, width, channels)  # cv2.resize(image, (416, 416))

    net = model_zoo.get_model('mask_rcnn_resnet50_v1b_coco', pretrained=True)
    photo_path = photo.cleaned_local_path if photo.cleaned_local_path else photo.front_local_path
    x, orig_img = data.transforms.presets.rcnn.load_test(photo_path)

    class_ids, confidences, boxes, masks = [xx[0].asnumpy() for xx in net(x)]
    # breakpoint()

    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    # indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD)
    # breakpoint()

    # if len(indexes) == 0:
    #     return {}
    #
    # print(indexes)

    # Get quantity of detected objects in the image based on indexes
    result = {}
    # Loop over the indexes we are keeping
    class_ids = class_ids.flatten().astype('int8')
    # breakpoint()
    for i in range(len(class_ids)):
        object_class = labels[class_ids[i]]
        if confidences[i] > CONFIDENCE:
            if object_class in result:
                result[object_class] += 1
            else:
                result[object_class] = 1
    return result
