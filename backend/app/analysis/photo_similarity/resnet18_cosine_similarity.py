"""
resnet18_cosine_similarity.py
"""
import torch
from torch import nn

from app.models import Photo
from app.analysis.photo_similarity import similarity_utils


def analyze(photo: Photo):
    """
    Produce a list of all other photos by cosine similarity to this photo's feature vector
    """
    return similarity_utils.analyze_similarity(photo, cosine_similarity)


def cosine_similarity(photo_features, other_photo_features):
    """
    Compute the cosine similarity between two feature vectors.
    """
    cosine_similarity_func = nn.CosineSimilarity(dim=1)
    similarity = cosine_similarity_func(photo_features, other_photo_features)
    cosine_similarity_mean = torch.mean(similarity).item()
    return cosine_similarity_mean
