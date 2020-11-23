from pycocotools.cocoeval import COCOeval
import json
import torch
import torch.utils.model_zoo as model_zoo
import os
from PIL import Image
import cv2
from torchvision.transforms import ToTensor
import torchvision
from ..models import Photo

from django.conf import settings

MODEL = Photo
CONFIDENCE = 0.5
THRESHOLD = 0.3
WEIGHTS = os.path.join(settings.YOLO_DIR, 'resnet50-19c8e357.pth')
CLASS_NAMES = os.path.join(settings.YOLO_DIR, 'coco_resnet_50_map_0_335_state_dict(1).pt')


def analyze(photo: Photo):
    model = torchvision.models.detection.retinanet_resnet50_fpn(pretrained=True)
    model.load_state_dict(model_zoo.load_url(
        "https://download.pytorch.org/models/resnet50-19c8e357.pth", model_dir='.'), strict=False)
    evaluate_coco(photo, model, THRESHOLD)


def evaluate_coco(photo, model, threshold=0.05):
    model.eval()

    with torch.no_grad():

        # start collecting results
        results = []
        image_ids = []

        image = photo.get_image_data()
        img = Image.fromarray(image)
        img = ToTensor()(img).unsqueeze(0)  # unsqueeze to add artificial first dimension
        scores, labels, boxes = model(img.permute(2, 0, 1).float.unsqueeze(dim=0))
        scores = scores.cpu()
        labels = labels.cpu()
        boxes = boxes.cpu()



        # compute predicted labels and scores
        # for box, score, label in zip(boxes[0], scores[0], labels[0]):
        for box_id in range(boxes.shape[0]):
            score = float(scores[box_id])
            label = int(labels[box_id])
            box = boxes[box_id, :]

            # scores are sorted, so we can break
            if score < threshold:
                break

            # append detection for each positively labeled class
            image_result = {
                'image_id': photo.image_ids,
                'category_id': photo.label_to_coco_label(label),
                'score': float(score),
                'bbox': box.tolist(),
                }

            # append detection to results
            results.append(image_result)

            # append image to list of processed images
            image_ids.append(photo.image_ids)

            # print progress
            # print('{}/{}'.format(index, len(dataset)), end='\r')

        # if not len(results):
        #     return

        # write output
        # json.dump(results, open('{}_bbox_results.json'.format(dataset.set_name), 'w'), indent=4)

        # load results in COCO evaluation tool
        # coco_true = dataset.coco
        # coco_pred = coco_true.loadRes('{}_bbox_results.json'.format(dataset.set_name))
        #
        # # run COCO evaluation
        # coco_eval = COCOeval(coco_true, coco_pred, 'bbox')
        # coco_eval.params.imgIds = image_ids
        # coco_eval.evaluate()
        # coco_eval.accumulate()
        # coco_eval.summarize()


        return image_ids
