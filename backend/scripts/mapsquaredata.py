import json
import os
import sys

newpath = os.getcwd().replace("scripts", "app")
newpath2 = newpath[:-4]
#sys.path.insert(0, newpath)
sys.path.insert(0, newpath2)
print(sys.path)

from django.conf import settings
settings.configure()

import django
django.setup()

from config import settings as setts

from app.models import MapSquare


def get_map_square_data():
    """
    Python script for generating JSON file of map square data

    :return: ???
    """

    return(MapSquare.objects.all())

print(get_map_square_data())
