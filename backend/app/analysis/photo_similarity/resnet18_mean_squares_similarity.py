"""
resnet18_mean_squares_similarity.py
"""
import torch
from torch import nn

from app.models import Photo
from app.analysis.photo_similarity import similarity_utils
from similarity_utils import analyze_similarity


MODEL = Photo


def analyze(photo: Photo):
    """
    Produce a list of all other photos by cosine similarity to this photo's feature vector
    """
    similarities = analyze_similarity(photo, mean_squares)
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities


def mean_squares(photo_features, other_photo_features):
    """
    Compute the cosine similarity between two feature vectors.
    """
    mean_squares_func = nn.MSELoss()
    similarity = mean_squares_func(photo_features, other_photo_features)
    mean_squares_average = torch.mean(similarity).item()
    return mean_squares_average
