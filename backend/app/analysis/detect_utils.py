import torch
import torchvision
import torchvision.transforms as transforms
import cv2
import numpy as np
# from coco_names import COCO_INSTANCE_CATEGORY_NAMES as coco_names
from app.models import Photo
MODEL = Photo

from PIL import Image


# construct the argument parser
'''parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='path to input image/video')
parser.add_argument('-m', '--min-size', dest='min_size', default=800,
                    help='minimum input size for the FasterRCNN network')
args = vars(parser.parse_args())'''

coco_names = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# this will help us create a different color for each class
COLORS = np.random.uniform(0, 255, size=(len(coco_names), 3))

# define the torchvision image transforms
transform = transforms.Compose([
    transforms.ToTensor(),
])


def predict(photo:Photo, model, device, detection_threshold=0):
    image = photo.get_image_data()
    image_dimensions = image.shape[:2]
    input_image = image
    # transform the image to tensor
    image = transform(image).to(device)
    image = image.unsqueeze(0)  # add a batch dimension
    outputs = model(image)  # get the predictions on the image
    # print the results individually
    # print(f"BOXES: {outputs[0]['boxes']}")
    all_labels = outputs[0]['labels']
    print(f"LABELS: {outputs[0]['labels']}")
    print(f"SCORES: {outputs[0]['scores']}")
    # get all the predicted class names
    pred_classes = [coco_names[i] for i in all_labels.cpu().numpy()]
    pred_classes_dict = {}
    for i in range(len(pred_classes)):
        if outputs[0]['scores'][i] > 0.5:
            pred_classes_dict[pred_classes[i]] = pred_classes_dict.get(pred_classes[i], 0)+1
    print('predicted classes dict: ', pred_classes_dict)
    # get score for all the predicted objects
    pred_scores = outputs[0]['scores'].detach().cpu().numpy()
    # get all the predicted bounding boxes
    pred_bboxes = outputs[0]['boxes'].detach().cpu().numpy()
    # get boxes above the threshold score
    boxes = pred_bboxes[pred_scores >= detection_threshold].astype(np.int32)
    # return boxes, pred_classes, outputs[0]['labels']
    return pred_classes_dict


def analyze(photo: Photo):
    try:
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True,
                                                                 min_size=600)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.eval().to(device)
        classes_dict = predict(photo, model, device, detection_threshold = 0.3)
        print('Running faster rcnn model on object detection')
        return classes_dict
    except Exception as err:
        print(err)


# might not need it for this project but just in case
def draw_boxes(boxes, classes, labels, image):
    # read the image with OpenCV
    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
    for i, box in enumerate(boxes):
        color = COLORS[labels[i]]
        cv2.rectangle(
            image,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[3])),
            color, 2
        )
        cv2.putText(image, classes[i], (int(box[0]), int(box[1]-5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2,
                    lineType=cv2.LINE_AA)
    return image


