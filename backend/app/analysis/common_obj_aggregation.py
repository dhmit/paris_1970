"""

common_obj_aggregation.py -
analysis that aggregates other obj detection methods
takes in the name of the obj we're looking for (for example, words, heads, pedestrians, stop signs)
returns the number of that specific obj for each photo in the database

"""

from ..models import Photo

MODEL = Photo


def analyze(photo: Photo):
    return
