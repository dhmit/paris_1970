"""
similarity_utils.py

Utility functions for each of the photo similarity analyses
"""
from pathlib import Path

import torch

from django.conf import settings

from app.models import Photo, PhotoAnalysisResult


def get_tensor_for_image(photo, verbose=True):
    """
    Retrieve and deserialize the tensor that was generated for the input photo.
    """

    try:
        analysis = photos.analyses.filter(name='photo_similarity.resnet18_feature_vectors')
    except PhotoAnalysisResult.DoesNotExist:
        if verbose:
            print(
                f'A feature vector for photo {photo.number} in map square {photo.map_square.number} '
                'was never serialized.'
                '\nPlease run resnet18_feature_vectors first.\n'
            )
        return None

    feature_vector_list = analysis.parsed_result()
    if feature_vector_list:  # for testing, this might be None
        tensor = torch.FloatTensor(feature_vector_list)
        return tensor
    else:
        return None


def analyze_similarity(photo: Photo, similarity_function, reverse=True):
    """
    Produce a list of all other photos by similarity to this photo's feature vector.
    Similarity is measured using similarity_function, a binary operation between feature
    vectors.

    reverse argument is needed because the output sort order from the sim function
    is sometimes ascending, sometimes descending
    """
    photo_features = get_tensor_for_image(photo, verbose=True)
    if photo_features is None:
        return []

    similarities = []
    for other_photo in Photo.objects.all().prefetch_related('analyses'):
        other_photo_features = get_tensor_for_image(other_photo, verbose=False)
        if other_photo_features is None:
            continue

        similarity_value = similarity_function(photo_features, other_photo_features)

        similarities.append({
            'number': other_photo.number,
            'map_square_number': other_photo.map_square.number,
            'folder_number': other_photo.folder,
            'alt': other_photo.alt,
            'similarity': similarity_value
        })

    similarities.sort(key=lambda x: x['similarity'], reverse=reverse)
    return similarities[1:]  # First photo will be current photo (100% similarity), remove it
