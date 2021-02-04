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
        except ModuleNotFoundError as err:
            print(err)
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

            num_computed = 0
            save_threshold = 20 # Number of analyses that need to be done before pickling

            for model_instance in model_instances:
                # NOTE: These identifiers assume that the photo number and map square number are
                #       not None
                print_msg = f'Running {analysis_name} on {model} {model_instance.id} '\
                            f'(Photo number: {model_instance.number}, '\
                            f'Map square: {model_instance.map_square.number})'
                instance_identifier = f'photo_{model_instance.number}_' \
                                      f'{model_instance.map_square.number}'

                should_run_analysis = True
                if use_pickled:
                    if instance_identifier in stored_results:
                        print(f'Using stored results on (Photo number: {model_instance.number}, '\
                              f'Map square: {model_instance.map_square.number})')
                        result = stored_results[instance_identifier]
                        should_run_analysis = False
                    else:
                        print('No stored result was found, so recomputing.')

                if should_run_analysis:
                    print(print_msg)
                    try:
                        result = analysis_func(model_instance)
                    except:  # pylint: disable=bare-except
                        print(f'Photo number {model_instance.number} failed. Skipping.')

                analysis_result = analysis_result_model(
                    name=analysis_name,
                    result=json.dumps(result),
                    photo=model_instance,
                )
                analysis_result.save()

                # Store the result
                stored_results[instance_identifier] = result
                num_computed += 1

                # Quick save the analysis results so far in case of failure
                if num_computed == save_threshold:
                    num_computed = 0
                    with open(result_path, 'wb') as analysis_pickle:
                        pickle.dump(stored_results, analysis_pickle)

            # Save the analysis stored_results
            # TODO: handle case where analysis fails (this won't pickle if something fails)
            with open(result_path, 'wb') as analysis_pickle:
                pickle.dump(stored_results, analysis_pickle)
