"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

import pickle
import os
from tqdm import tqdm

import cv2
from sklearn.cluster import KMeans

from django.conf import settings
from django.core.management.base import BaseCommand

from app.common import print_header
from app.models import Photo
from app.models import Cluster


def get_reformatted_photos(photo_path):


class Command(BaseCommand):
    """
    Custom django-admin command used to run an analysis from the app/analysis folder
    """
    help = 'Create clusters corresponding to a kmeans model fit to all photos in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'n_clusters',
            type=int,
            action='store',
            help="Number of different clusters the model tries to group the photos into",
        )
        parser.add_argument('--random_state', action='store', default=0)
        parser.add_argument('--use_pickled', action='store_true')
        parser.add_argument('--resize', action='store', default=(416, 416), metavar=('w', 'h'),
                            nargs=2, type=int)

    def handle(self, *args, **options):
        number_of_clusters = options.get('n_clusters')
        random_state = options.get('random_state')
        use_pickled = options.get('use_pickled')
        dimensions = tuple(options.get('resize'))

        labels_path = os.path.join(settings.ANALYSIS_PICKLE_PATH,
                                   f'{number_of_clusters}_{dimensions}_model.pickle')
        photos_path = os.path.join(settings.ANALYSIS_PICKLE_PATH,
                                   f'{dimensions}_photos.pickle')
        valid_photos = []
        if use_pickled and os.path.exists(labels_path):
            with open(labels_path, 'rb') as labels_pickle:
                labels, photo_ids = pickle.load(labels_pickle)
            for photo_id in photo_ids:
                number, map_square_number = photo_id.split('_')
                valid_photos.append(
                    Photo.objects.filter(
                        number=int(number),
                        map_square__number=int(map_square_number)
                    )[0]
                )
        else:
            # Create Kmeans model and get labels
            print_header("Preparing reformatted photos...")
            if os.path.exists(photos_path):
                with open(photos_path, 'rb') as photos_pickle:
                    stored_photos = pickle.load(photos_pickle)
            else:
                stored_photos = None
            photos = Photo.objects.all()
            valid_photos = [photo for photo in Photo.objects.all() if photo.has_valid_source()]
            reformatted_photos = []
            for i, photo in enumerate(photos):
                grayscale_image = photo.get_image_data(True)
                if grayscale_image is None:
                    continue
                if stored_photos:
                    reformatted_photo = stored_photos[i]
                else:
                    reformatted_photo = cv2.resize(grayscale_image, dimensions).flatten() / 255
                reformatted_photos.append(reformatted_photo)
                valid_photos.append(photo)
            print('')
            print("Done!")
            kmeans = KMeans(
                n_clusters=number_of_clusters, random_state=random_state
            ).fit(reformatted_photos)
            labels = kmeans.labels_

        # Get clusters
        clusters = list(Cluster.objects.filter(model_n=number_of_clusters))
        if not clusters:
            for i in range(number_of_clusters):
                clusters.append(Cluster(model_n=number_of_clusters, label=i))
                clusters[i].save()
        else:
            for cluster in clusters:
                cluster.photos.remove(*cluster.photos.all())

        # Add photos to clusters
        for photo, label in zip(valid_photos, labels):
            clusters[label].photos.add(photo)
            clusters[label].save()

        # Save the analysis stored_results
        # TODO: handle case where analysis fails (this won't pickle if something fails)
        with open(labels_path, 'wb') as labels_pickle:
            photo_ids = [f'{photo.number}_{photo.map_square.number}' for photo in valid_photos]
            pickle.dump([labels, photo_ids], labels_pickle)
        with open(photos_path, 'wb') as photos_pickle:
            pickle.dump(reformatted_photos, photos_pickle)
