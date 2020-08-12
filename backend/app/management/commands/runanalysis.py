"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

import pickle
import os
import tqdm
from textwrap import dedent

from django.contrib.auth.models import User
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from app.models import Photo, MapSquare, Photographer

def count_photos():
    return Photo.objects.all().count()


class Command(BaseCommand):
    help = 'Run an analysis'

    def add_arguments(self, parser):
        parser.add_argument('analysis_name', action='store', type=str)

    def handle(self, *args, **options):
        analysis_name = options.get('analysis_name')

        print(analysis_name)

        analysis_results = None
        if analysis_name == 'count_photos':
            analysis_results = count_photos()
        else:
            print('There is no such analysis with that name.')
            exit(1)

        print(analysis_results)

