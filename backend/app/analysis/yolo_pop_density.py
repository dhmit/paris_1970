"""

yolo_pop_density.py -
analysis that calculates the relative density of people in a photo based on the object
bounding boxes returned by the yolo_model

"""
from app.models import Photo
from app.models import PhotoAnalysisResult

MODEL = Photo


def overlap_1d(line1, line2):
    """
    Given a two line segments, return a float representing how overlapped the two line
    segments are.
    :param line1: A list/tuple containing two numbers representing the start and end point
    of the first line.
    :param line2: A list/tuple containing two numbers representing the start and end point
    of the second line.
    :return: A float from 1 - 0 representing how overlapped the two input line segments are
    (A value of ~.5 indicates that the lines are approximately touching but not overlapped.)
    """
    min1, max1 = line1
    min2, max2 = line2
    # smallest_line_len = min(max1 - min1, max2 - min2)
    longest_line_len = max(max1 - min1, max2 - min2)
    line_overlap = (min(max1, max2) - max(min1, min2)) / longest_line_len
    if line_overlap < 0:
        line_overlap = 1 / (line_overlap ** 2 + 1)
    else:
        line_overlap += 1
    return line_overlap / 2


def overlap_2d(rect1, rect2):
    """
    Given a two rectangles, return a float representing how overlapped they are.
    :param rect1: A list/tuple of (x_position, y_position, width, height)
    :param rect2: A list/tuple of (x_position, y_position, width, height)
    :return: A float from 1 - 0 representing how overlapped the two input rectangles are
    (A value of ~.5 indicates that the lines are approximately touching but not overlapped.)
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    x_overlap = overlap_1d((x1, x1 + w1), (x2, x2 + w2))
    y_overlap = overlap_1d((y1, y1 + h1), (y2, y2 + h2))
    return x_overlap * y_overlap


def box_to_rect(box):
    """
    Given a box representing an object's location in a photo as predicted by the yolo_model,
    return a tuple representing a rectangle to be used for calculating overlap.
    :param box: dictionary with keys 'x_coord', 'y_coord', 'width', 'height'
    :return: tuple (rectangle)
    """
    return (
        box['x_coord'],
        box['y_coord'],
        box['width'],
        box['height']
    )


def object_density(object_name, yolo_dict, photo_dim=(10000, 10000)):
    """
    Given an object name, the output of the yolo_model analysis for a photo (yolo_dict),
    and the dimensions of the photo, return the density of the specified object
    in the photo.
    :param object_name: string (name of the object)
    :param yolo_dict: dictionary (output of the yolo_model for the photo)
    :param photo_dim: tuple (dimensions of the photo the object is located in)
    :return: A number representing how densely the specified object type is packed
    in an image. More overlapping objects corresponds to higher density.
    """
    yolo_boxes = yolo_dict.get("boxes", {})
    boxes = [box for box in yolo_boxes if box['label'] == object_name]

    if len(boxes) == 1:
        photo_width, photo_height = photo_dim
        rect1 = box_to_rect(boxes[0])
        rect2 = (
            boxes[0]['x_coord'] + photo_width,  # Assume that there is another object
            boxes[0]['y_coord'] + photo_height,  # outside the frame of the photo
            boxes[0]['width'],
            boxes[0]['height']
        )
        # pylint: disable=arguments-out-of-order
        return overlap_2d(rect1, rect2) + overlap_2d(rect2, rect1)

    density = 0
    for i, box_i in enumerate(boxes):
        density_i = 0
        for j, box_j in enumerate(boxes):
            if i == j:
                continue
            density_i += overlap_2d(
                box_to_rect(box_i), box_to_rect(box_j)
            )
        density += density_i / (len(boxes) - 1)

    return density


def analyze(photo: Photo):
    yolo_dict = PhotoAnalysisResult.objects.filter(
        name="yolo_model", photo=photo
    ).first().parsed_result()
    image = photo.get_image_data()
    photo_dim = image.shape[:2][::-1] if image is not None else (10000, 10000)
    return object_density("person", yolo_dict, photo_dim)
