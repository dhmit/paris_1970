"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

from importlib import import_module
from typing import Callable
import pickle
import os
import tqdm
from textwrap import dedent

from django.conf import settings
from django.core.management.base import BaseCommand

from app.models import Photo


class Command(BaseCommand):
    help = 'Run an analysis'

    def add_arguments(self, parser):
        parser.add_argument('analysis_name', action='store', type=str)

    def handle(self, *args, **options):
        analysis_name = options.get('analysis_name')

        analysis_module = import_module(f'.{analysis_name}', package='app.analysis')

        if analysis_module:
            # TODO(ra): check for the existence of an already pickled analysis
            # and provide a command line flag to rerun optionally or load from pickle

            analysis_func: Callable[[], dict] = getattr(analysis_module, 'analysis')
            model_field = getattr(analysis_module, 'model_field')
            analysis_results = analysis_func()
            for k in analysis_results.keys():
                photo = Photo.objects.get(pk=k)
                v = analysis_results.get(k)
                setattr(photo, model_field, v)
                photo.save()
            # TODO(ra): pickle the analysis

        else:
            print('There is no such analysis with that name.')
            exit(1)

        print(analysis_results)

