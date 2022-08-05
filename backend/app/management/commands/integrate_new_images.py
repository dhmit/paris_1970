"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

import sys
import pickle
import os
import json

from importlib import import_module
from typing import Callable

from django.conf import settings
from django.core.management.base import BaseCommand

from app.common import print_header
from app.models import Photo, MapSquare
from scripts import rename_photos


class Command(BaseCommand):
    """
    Custom django-admin command used to integrate new images
    """
    help = 'Integrate new images'

    def add_arguments(self, parser):
        parser.add_argument('source_dir', action='store', type=str)
        parser.add_argument('map_square')

    def handle(self, *args, **options):
        source_dir = options.get('source_dir')
        map_square = options.get('map_square')
        map_square_dir = os.path.join(settings.LOCAL_PHOTOS_LOCATION, map_square)
        try:
            os.mkdir(map_square_dir)
        except:
            pass

        rename_photos.rename(source_dir, map_square_dir)

        ### WARNING: CLEARING ALL MAP SQUARE PHOTOS!!! ###
        map_square_instance = MapSquare.objects.get(number=int(map_square))
        map_square_instance.photo_set.all().delete()

        for img_src in os.listdir(map_square_dir):
            photo_num = int(img_src.split("_")[0])
            try:
                Photo.objects.create(number=photo_num,
                                 map_square=map_square_instance)
            except:
                # here because each image has a slide and photo with same number
                pass
