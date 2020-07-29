"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
from rest_framework import serializers
from .models import Photo, MapSquare, Photographer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'front_src', 'back_src', 'alt', 'title', 'photographer_obj', 'map_square']


class MapSquareSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapSquare
        fields = ['id', 'photo_ids', 'boundaries', 'name']


class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ['id', 'name', 'type', 'sentiment', 'photo_ids', 'map_square']
