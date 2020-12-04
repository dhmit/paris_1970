"""
resnet18_pairwise_similarity.py
"""
import torch
from torch import nn

from app.models import Photo
from app.analysis.photo_similarity import similarity_utils


MODEL = Photo


def analyze(photo: Photo):
    """
    Produce a list of all other photos by cosine similarity to this photo's feature vector
    """
    similarities = similarity_utils.analyze_similarity(photo, pairwise_distance)
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities


def pairwise_distance(photo_features, other_photo_features):
    """
    Compute the cosine similarity between two feature vectors.
    """
    pairwise_func = nn.MSELoss()
    similarity = pairwise_func(photo_features, other_photo_features)
    pairwise_mean = torch.mean(similarity).item()
    return pairwise_mean
