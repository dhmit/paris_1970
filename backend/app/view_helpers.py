import os
import json
from django.conf import settings


def get_map_square_data():
    """
    Reading list of hand-compiled json data
    for each arrondissement
    """
    json_path = os.path.join(settings.BACKEND_DATA_DIR, 'arrondissements_map_squares.json')
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_arrondissement_geojson():
    """
    Reading list of geojson data for each arrondissement
    """
    geojson_path = os.path.join(settings.BACKEND_DATA_DIR, 'arrondissements.geojson')
    with open(geojson_path, encoding='utf-8') as f:
        data = json.load(f)
    return data
