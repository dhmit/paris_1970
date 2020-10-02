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
from app.models import PhotoAnalysisResult


class Command(BaseCommand):
    """
    Custom django-admin command used to run an analysis from the app/analysis folder
    """
    help = 'Run an analysis'

    def add_arguments(self, parser):
        parser.add_argument('analysis_name', action='store', type=str)
        parser.add_argument('--use_pickled', action='store_true')
        parser.add_argument('--run_one', action='store_true')

    def handle(self, *args, **options):
        # pylint: disable=too-many-locals
        analysis_name = options.get('analysis_name')
        use_pickled = options.get('use_pickled')
        run_one = options.get('run_one')

        try:
            analysis_module = import_module(f'.{analysis_name}', package='app.analysis')
        except ModuleNotFoundError:
            print_header('There is no analysis with that name.')
            sys.exit(1)

        if analysis_module:
            result_path = os.path.join(settings.ANALYSIS_PICKLE_PATH, f'{analysis_name}.pickle')
            if os.path.exists(result_path):
                with open(result_path, 'rb') as analysis_pickle:
                    stored_results = pickle.load(analysis_pickle)
            else:
                stored_results = {}

            analysis_func: Callable[[object], dict] = getattr(analysis_module, 'analyze')
            model = getattr(analysis_module, 'MODEL')

            # TODO(ra): currently we assume all analyses are on Photos
            # Eventually we want to generalize to include analyses on MapSquares and Photographers
            analysis_result_model = PhotoAnalysisResult

            # delete existing db instances
            analysis_result_model.objects.filter(name=analysis_name).delete()

            if run_one:
                # in a list because this has to be iterable for the loop below...
                model_instances = [model.objects.first()]
            else:
                model_instances = model.objects.all()

            for model_instance in model_instances:
                print(f'Running {analysis_name} on {model} {model_instance.id} '
                      f'(Photo number: {model_instance.number}, '
                      f'Map square: {model_instance.map_square.number})')
                instance_identifier = f'photo_{model_instance.number}_{model_instance.map_square}'

                if use_pickled:
                    if instance_identifier in stored_results:
                        result = stored_results[instance_identifier]
                    else:
                        print('No stored result was found, so recomputing.')
                        result = analysis_func(model_instance)

                else:
                    result = analysis_func(model_instance)

                analysis_result = analysis_result_model(
                    name=analysis_name,
                    result=json.dumps(result),
                    photo=model_instance,
                )
                analysis_result.save()

                # Store the result
                stored_results[instance_identifier] = result

            # Save the analysis stored_results
            # TODO: handle case where analysis fails (this won't pickle if something fails)
            with open(result_path, 'wb') as analysis_pickle:
                pickle.dump(stored_results, analysis_pickle)
