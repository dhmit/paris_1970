import json
import os

from app.models import MapSquare

def get_map_square_data():
    """
    Python script for generating JSON file of map square data

    :return: ???
    """

    return(MapSquare.objects.all())

print(get_map_square_data())
