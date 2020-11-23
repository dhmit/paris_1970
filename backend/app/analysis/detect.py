import torchvision
import numpy
import torch
import argparse
import cv2
from .detect_utils import *
from PIL import Image


# construct the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='path to input image/video')
parser.add_argument('-m', '--min-size', dest='min_size', default=800,
                    help='minimum input size for the FasterRCNN network')
args = vars(parser.parse_args())

# download or load the model from disk
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True,
                                                    min_size=args['min_size'])

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

image = Image.open(args['input'])
model.eval().to(device)
boxes, classes, labels = detect_utils.predict(image, model, device, 0.8)
image = detect_utils.draw_boxes(boxes, classes, labels, image)
cv2.imshow('Image', image)
save_name = f"{args['input'].split('/')[-1].split('.')[0]}_{args['min_size']}"
cv2.imwrite(f"outputs/{save_name}.jpg", image)
cv2.waitKey(0)
