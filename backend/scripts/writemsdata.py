import os
import sys

newpath = os.getcwd().replace("scripts", "app")
newpath2 = newpath[:-4]
#sys.path.insert(0, newpath)
sys.path.insert(0, newpath2)
#print(sys.path)

from app.models import MapSquare
from app.serializers import MapSquareSerializerWithoutPhotos
from rest_framework.response import Response

import json

def write_map_square_data():
    map_square_obj = MapSquare.objects.all().values()
    print(map_square_obj)
    map_square_data = list(map_square_obj)
    #ms_data_serialized = MapSquareSerializerWithoutPhotos(map_square_obj, many=True)
    #map_square_data = Response(ms_data_serialized.data)

    with open(r"scripts/mapsquaredata.json", "w") as file:
        json.dump(map_square_obj, file)


write_map_square_data()
print("write_map_square_data has finished running.")
