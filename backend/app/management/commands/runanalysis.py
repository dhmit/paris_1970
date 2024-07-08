"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

import sys
import json

from importlib import import_module

from django.core.management.base import BaseCommand

from app.common import print_header
from app.models import Photo, PhotoAnalysisResult


def photo_id_str(photo):
    return f'{photo.map_square.number}_{photo.folder}-{photo.number}'


class Command(BaseCommand):
    """
    Custom django-admin command used to run an analysis over the whole dataset from the app/analysis folder
    optionally overwriting existing work
    """
    help = 'Run an analysis'

    def add_arguments(self, parser):
        parser.add_argument('analysis_name', action='store', type=str)
        parser.add_argument('--run_one', action='store_true')
        parser.add_argument('--overwrite', action='store_true')
        parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        # pylint: disable=too-many-locals
        analysis_name: str = options.get('analysis_name')
        run_one = options.get('run_one')
        overwrite = options.get('overwrite')
        verbose = options.get('verbose')

        running_similarity = '_similarity' in analysis_name

        try:
            analysis_module = import_module(f'.{analysis_name}', package='app.analysis')
        except ModuleNotFoundError as err:
            print(err)
            print_header('There is no analysis with that name.')
            sys.exit(1)

        analysis_func = (
            getattr(analysis_module, 'get_analyze')()  # For modules with setup across photos (yolo)
            if hasattr(analysis_module, "get_analyze")
            else getattr(analysis_module, 'analyze')
        )

        if run_one:
            # in a list because this has to be iterable for the loop below...
            photos = [Photo.objects.first()]
            num_photos = 1
        else:
            photos = Photo.objects.all()
            num_photos = photos.count()

        print_header(f'Running {analysis_name} on {num_photos} photos')

        feature_vectors = []
        if running_similarity:
            print('Gathering feature vectors...')

            feature_vector_results = (
                PhotoAnalysisResult.objects.filter(name='photo_similarity.resnet18_feature_vectors')
                                           .prefetch_related('photo', 'photo__map_square'))
            for result in feature_vector_results:
                feature_vectors.append({
                    'vector': result.parsed_result(),
                    'map_square_number': result.photo.map_square.number,
                    'folder_number': result.photo.folder,
                    'photo_number': result.photo.number,
                })


        photos_done = 0
        for photo in photos:
            if verbose:
                print(f'\nRunning on {photo_id_str(photo)}')

            if not photo.has_valid_source():
                print(f'Photo {photo_id_str(photo)} - could not find a source image file. Skipping.')
                continue

            if verbose:
                print(photo.image_local_filepath())

            try:
                existing_analysis = PhotoAnalysisResult.objects.get(name=analysis_name, photo=photo)
            except PhotoAnalysisResult.DoesNotExist:
                existing_analysis = None

            if existing_analysis:
                if overwrite:
                    existing_analysis.delete()
                else:
                    print(f'Photo {photo_id_str(photo)} - an analysis exists and we are not overwriting. Skipping.')
                    continue

            try:
                if running_similarity:
                    result = analysis_func(photo, feature_vectors)
                else:
                    result = analysis_func(photo)


                result_json = json.dumps(result)
                analysis_result = PhotoAnalysisResult(name=analysis_name, result=result_json, photo=photo)
                analysis_result.save()
            except Exception as e:  # pylint: disable=bare-except
                err_msg = (
                        f'Photo {photo_id_str(photo)} - an error occured:'
                    + f'\nError: {e}.\nSkipping.'
                )
                print(err_msg)

            photos_done += 1
            if photos_done % 25 == 0:
                print(f'\nAnalyzed {photos_done} so far...')
