"""

photographer_dist.py -
analysis that calculates the distance between a photo's map square and its photographer's
home address

"""
import os
import json
from math import sin, cos, sqrt, atan2, radians

from django.conf import settings
from ..models import Photo

DATA_PATH = os.path.join(settings.BACKEND_DATA_DIR, "photographer_locations.json")


def lat_lon_distance(coord1, coord2):
    """
    Returns the distance in kilometers between two (latitude, longitude) coordinates.
    Calculated using the haversine formula
    """
    # Approximate radius of earth in km
    earth_radius = 6373.0

    lat1, lon1, lat2, lon2 = [radians(d) for d in coord1 + coord2]
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Intermediate calculation variables
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = earth_radius * c
    return distance


def analyze(photo: Photo):
    with open(DATA_PATH, 'r', encoding="utf-8") as file:
        photographer_locations = json.load(file)
    photographer = photo.photographer
    if not (photographer and photographer_locations.get(str(photographer.number))):
        return -1
    photo_coords = tuple([float(c) for c in photo.map_square.coordinates.split(', ')])
    location = photographer_locations.get(str(photographer.number))
    photographer_coords = (float(location['lat']), float(location['lon']))
    return lat_lon_distance(photo_coords, photographer_coords)
