"""
resnet18_pairwise_similarity.py
"""
import torch
from torch import nn

from app.models import Photo
from app.analysis.photo_similarity import similarity_utils



def analyze(photo: Photo, feature_vector_dicts):
    """
    Produce a list of all other photos by cosine similarity to this photo's feature vector
    """
    return similarity_utils.analyze_similarity(photo, feature_vector_dicts, pairwise_distance, reverse=True)


def pairwise_distance(photo_features, other_photo_features):
    """
    Compute the cosine similarity between two feature vectors.
    """
    pairwise_func = nn.MSELoss()
    similarity = pairwise_func(photo_features, other_photo_features)
    pairwise_mean = torch.mean(similarity).item()
    return pairwise_mean
