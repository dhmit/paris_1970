"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

import sys
import pickle
import os

from importlib import import_module
from typing import Callable

from django.conf import settings
from django.core.management.base import BaseCommand

from app.common import print_header


class Command(BaseCommand):
    """
    Custom django-admin command used to run an analysis from the app/analysis folder
    """
    help = 'Run an analysis'

    def add_arguments(self, parser):
        parser.add_argument('analysis_name', action='store', type=str)
        parser.add_argument('--rerun', action='store', type=str)

    def handle(self, *args, **options):
        # pylint: disable=too-many-locals
        analysis_name = options.get('analysis_name')
        rerun = options.get('rerun') == 'rerun'

        try:
            analysis_module = import_module(f'.{analysis_name}', package='app.analysis')
        except ModuleNotFoundError:
            print_header('There is no analysis with that name.')
            sys.exit(1)

        if analysis_module:
            result_path = os.path.join(settings.ANALYSIS_PICKLE_PATH, f'{analysis_name}.pickle')
            if os.path.exists(result_path):
                with open(result_path, 'rb') as analysis_pickle:
                    past_results = pickle.load(analysis_pickle)
            else:
                past_results = {}

            analysis_func: Callable[[object], dict] = getattr(analysis_module, 'analysis')
            model = getattr(analysis_module, 'MODEL')

            for model_instance in model.objects.all():
                print(model_instance.id)
                instance_identifier = f'{model.__name__}_{model_instance.id}'

                if rerun or instance_identifier not in past_results:
                    analysis_results = analysis_func(model_instance)
                else:
                    analysis_results = past_results[instance_identifier]

                for attribute, value in analysis_results.items():
                    setattr(model_instance, attribute, value)
                    model_instance.save()

                # Store the result
                past_results[f'{model.__name__}_{model_instance.id}'] = analysis_results

                # Save the analysis results (not sure if we should do this inside of the loop for
                # cases when the analysis fails because of the limit on http requests)
                with open(result_path, 'wb') as analysis_pickle:
                    pickle.dump(past_results, analysis_pickle)
