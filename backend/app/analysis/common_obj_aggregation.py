"""

common_obj_aggregation.py -
analysis that aggregates other obj detection methods
takes in the name of the obj we're looking for (for example, words, heads, pedestrians, stop signs)
returns the number of that specific obj for each photo in the database

links:
- https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
- https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/

"""

from ..models import Photo

MODEL = Photo


def analyze(photo: Photo):
    return
