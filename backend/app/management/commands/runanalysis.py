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
from app.models import PhotoAnalysisResult


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
                    stored_results = pickle.load(analysis_pickle)
            else:
                stored_results = {}

            analysis_func: Callable[[object], dict] = getattr(analysis_module, 'analyze')
            model = getattr(analysis_module, 'MODEL')

            # TODO(ra): currently we _assume_ all analyses are on Photos
            # Eventually we want to generalize to include analyses on MapSquares and Photographers
            analysis_result_model = PhotoAnalysisResult

            for model_instance in model.objects.all():
                print(f'Running {analysis_name} on {model} {model_instance.id}')
                instance_identifier = f'photo_{model_instance.number}_{model_instance.map_square}'

                if rerun or instance_identifier not in stored_results:
                    result = analysis_func(model_instance)
                else:
                    print('Using a found stored result. Pass the --rerun flag to rerun.')
                    result = stored_results[instance_identifier]

                    analysis_result = analysis_result_model(
                        name=analysis_name,
                        result=result,
                        photo=model_instance,
                    )
                    analysis_result.save()

                # Store the result
                stored_results[instance_identifier] = result

            # Save the analysis stored_results
            # TODO: handle case where analysis fails (this won't pickle if something fails)
            with open(result_path, 'wb') as analysis_pickle:
                pickle.dump(stored_results, analysis_pickle)
