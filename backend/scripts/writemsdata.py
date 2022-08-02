import os
import sys
newpath = os.getcwd().replace("scripts", "app")
newpath2 = newpath[:-4]
#sys.path.insert(0, newpath)
sys.path.insert(0, newpath2)
print(sys.path)

from django.db import models
from app.models import MapSquare

import json

def write_map_square_data():
    map_square_data = MapSquare.objects.all()

    with open("mapsquaredata.json", "w") as file:
        json.dump(map_square_data, file)

write_map_square_data()
