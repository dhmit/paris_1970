"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

import pickle
import os

import cv2
from sklearn.cluster import KMeans

from django.conf import settings
from django.core.management.base import BaseCommand

from app.common import print_header
from app.models import Photo
from app.models import Cluster


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
            help='Number of different clusters the model tries to group the photos into',
        )
        parser.add_argument(
            '--limit',
            type=int,
            action='store',
            help='Number of photos to run the clustering over (mostly for prototyping runs)',
        )
        parser.add_argument(
            '--resize',
            action='store',
            type=int,
            nargs=2,
            metavar=('h', 'w'),
            default=(416, 416),
        )
        parser.add_argument(
            '--random_state',
            action='store',
            default=0,
            help='Used for kmeans centroid initialization'
        )
        parser.add_argument('--use_pickled', action='store_true')

    def handle(self, *args, **options):
        # pylint: disable=too-many-locals
        number_of_clusters = options.get('n_clusters')
        limit = options.get('limit', None)
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
            # Collect photos that have a valid source in the order that labels were originally
            # assigned
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
            print_header("Preparing reformatted photos (This might take a couple of minutes)...")
            reformatted_photos = []
            if use_pickled and os.path.exists(photos_path):
                print('Loading pickled reformatted photos.')
                with open(photos_path, 'rb') as photos_pickle:
                    reformatted_photos = pickle.load(photos_pickle)
            else:
                valid_photos = [photo for photo in Photo.objects.all() if photo.has_valid_source()]
                if limit:
                    valid_photos = valid_photos[:limit]
                num_photos = len(valid_photos)
                for i, photo in enumerate(valid_photos):
                    try:
                        grayscale_image = photo.get_image_data(as_gray=True)
                        reformatted_photo = cv2.resize(grayscale_image, dimensions).flatten() / 255
                        reformatted_photos.append(reformatted_photo)
                        print(f'Reformatted {i} of {num_photos} photos.')
                    except Exception as e:
                        print(f'Error: {e}')
                        print(f'Skipping photo number {photo.number}, map square '
                              f'{photo.map_square.number}')

                # TODO: handle case where analysis fails (this won't pickle if something fails)
                # Save reformatted_photos
                with open(photos_path, 'wb') as photos_pickle:
                    pickle.dump(reformatted_photos, photos_pickle)
            print("Done!")

            print_header("Generating labels...")
            kmeans = KMeans(
                n_clusters=number_of_clusters, random_state=random_state
            ).fit(reformatted_photos)
            labels = kmeans.labels_
            print("Done!")

        # Get clusters
        clusters = Cluster.objects.filter(model_n=number_of_clusters)
        if not clusters:
            clusters = []
            for i in range(number_of_clusters):
                cluster = Cluster(model_n=number_of_clusters, label=i)
                cluster.save()
                clusters.append(cluster)
        else:
            # Reset clusters if they exist to prevent previous photos from remaining in the
            # cluster if they should not be
            for cluster in clusters:
                cluster.photos.remove(*cluster.photos.all())

        # Add photos to clusters
        print('Adding photos to clusters')
        for photo, label in zip(valid_photos, labels):
            label = int(label)
            clusters[label].photos.add(photo)
            clusters[label].save()

        # Save labels
        # TODO: handle case where analysis fails (this won't pickle if something fails)
        with open(labels_path, 'wb') as labels_pickle:
            photo_ids = [f'{photo.number}_{photo.map_square.number}' for photo in valid_photos]
            pickle.dump([labels, photo_ids], labels_pickle)
