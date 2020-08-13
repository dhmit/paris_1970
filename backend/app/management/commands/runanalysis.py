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
from app.common import print_header


class Command(BaseCommand):
    help = 'Run an analysis'

    def add_arguments(self, parser):
        parser.add_argument('analysis_name', action='store', type=str)

    def handle(self, *args, **options):
        analysis_name = options.get('analysis_name')

        try:
            analysis_module = import_module(f'.{analysis_name}', package='app.analysis')
        except ModuleNotFoundError:
            print_header('There is no analysis with that name.')
            exit(1)

        if analysis_module:
            # TODO(ra): check for the existence of an already pickled analysis
            # and provide a command line flag to rerun optionally or load from pickle

            analysis_func: Callable[[], dict] = getattr(analysis_module, 'analysis')
            analysis_results = analysis_func()
            for k in analysis_results.keys():
                photo = Photo.objects.get(pk=k)
                new_attributes = analysis_results.get(k)
                for field in new_attributes.keys():
                    value = new_attributes.get(field)
                    setattr(photo, field, value)
                photo.save()
            # TODO(ra): pickle the analysis

        print(analysis_results)

