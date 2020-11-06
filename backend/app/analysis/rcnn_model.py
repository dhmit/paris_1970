"""

common_obj_aggregation.py -
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

MODEL = Photo
CONFIDENCE = 0.5
THRESHOLD = 0.3


def analyze(photo: Photo):
    # net, labels, colors, output_layers = load_yolo()

    # Get image and image dimensions
    image = photo.get_image_data()
    image = cv2.resize(image, (216, 216))
    height, width, channels = image.shape
    input_image = image.reshape(1, height, width, channels)  # cv2.resize(image, (416, 416))

    net = model_zoo.get_model('mask_rcnn_resnet50_v1b_coco', pretrained=True)
    x, orig_img = data.transforms.presets.rcnn.load_test(input_image)

    class_ids, confidences, boxes, masks = [xx[0].asnumpy() for xx in net(x)]

    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD)

    if len(indexes) == 0:
        return {}

    print(indexes)

    # Get quantity of detected objects in the image based on indexes
    result = {}
    # Loop over the indexes we are keeping
    # for i in indexes.flatten():
    #     object_class = labels[class_ids[i]]
    #     if object_class in result:
    #         result[object_class] += 1
    #     else:
    #         result[object_class] = 1
    return {}
