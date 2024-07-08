import torch


def make_detection_boxes(detections):
    classes = {}
    boxes = []
    with torch.no_grad():
        # Loop over the detections
        for object_class, c_x, c_y, width, height, confidence in detections:

            # Get coordinates of top left corner of the object
            x = int(round(c_x - (width / 2)))
            y = int(round(c_y - (height / 2)))

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
            "labels": classes
        }
