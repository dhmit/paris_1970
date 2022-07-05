"""
similarity_utils.py

Utility functions for each of the photo similarity analyses
"""
from pathlib import Path

import torch

from django.conf import settings

from app.models import Photo


def deserialize_tensor(photo, verbose=True):
    """
    Retrieve and deserialize the tensor that was generated for the input photo.
    """
    dir_path = Path(settings.ANALYSIS_PICKLE_PATH,
                    'resnet18_features',
                    str(photo.map_square.number))
    serialized_feature_vector_path = Path(dir_path, f'{photo.number}.pt')
    if not serialized_feature_vector_path.exists():
        if verbose:
            print(
                f'A feature vector for photo {photo.number} in map square {photo.map_square.number} '
                'was never serialized.'
                '\nPlease run resnet18_feature_vectors first.\n'
            )
        return None

    tensor = torch.load(serialized_feature_vector_path)
    return tensor


def analyze_similarity(photo: Photo, similarity_function, reverse=True):
    """
    Produce a list of all other photos by similarity to this photo's feature vector.
    Similarity is measured using similarity_function, a binary operation between feature
    vectors.

    reverse argument is needed because the output sort order from the sim function
    is sometimes ascending, sometimes descending
    """
    photo_features = deserialize_tensor(photo, verbose=True)
    if photo_features is None:
        return None

    similarities = []
    for other_photo in Photo.objects.all():
        other_photo_features = deserialize_tensor(other_photo, verbose=False)
        if other_photo_features is None:
            continue

        similarity_value = similarity_function(photo_features, other_photo_features)

        similarities.append(
            (other_photo.map_square.number, other_photo.number, similarity_value)
        )

    if similarities is not None:
        similarities.sort(key=lambda x: x[2], reverse=reverse)
        return similarities
    else:
        return []
