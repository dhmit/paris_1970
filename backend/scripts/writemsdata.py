from django.db import models
from app.models import MapSquare

import json

def write_map_square_data():
    map_square_data = MapSquare.objects.all()

    with open("mapsquaredata.json", "w") as file:
        json.dump(map_square_data, file)

write_map_square_data()
