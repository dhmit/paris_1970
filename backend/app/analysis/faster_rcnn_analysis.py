'''
faster rcnn from: https://debuggercafe.com/faster-rcnn-object-detection-with-pytorch/
'''
import torch

import torchvision
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

