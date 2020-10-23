"""
resnet18_feature_vectors.py
"""
import sys
from pathlib import Path

import torch
from torch import nn

from django.conf import settings

from app.models import Photo

MODEL = Photo


def deserialize_tensor(photo):
    dir_path = Path(settings.ANALYSIS_PICKLE_PATH,
                    'resnet18_features',
                    str(photo.map_square.number))
    serialized_feature_vector_path = Path(dir_path, f'{photo.number}.pt')
    if not serialized_feature_vector_path.exists():
        print(
            f'A feature vector for photo {photo.number} in map square {photo.map_square.number} '
            'was never serialized.'
            '\nPlease run resnet18_feature_vectors first.\n'
        )
        return None

    tensor = torch.load(serialized_feature_vector_path)
    return tensor


def analyze(photo: Photo):
    """
    Produce a list of all other photos by cosine similarity to this photo's feature vector
    """
    photo_features = deserialize_tensor(photo)

    similarities = []
    for other_photo in Photo.objects.all():
        other_photo_features = deserialize_tensor(other_photo)
        if other_photo_features is None:
            continue

        cosine_similarity_func = nn.CosineSimilarity(dim=1)
        cosine_similarity = cosine_similarity_func(photo_features, other_photo_features)
        cosine_similarity_mean = torch.mean(cosine_similarity).item()

        similarities.append(
            (photo.map_square.number, photo.number, cosine_similarity_mean)
        )

    similarities.sort(key=lambda x: x[2])  # sort by cosine_similarity,
    return similarities
