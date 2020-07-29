"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
from rest_framework import serializers
from .models import Photo, MapSquare


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'front_src', 'back_src', 'alt', 'title']


class MapSquareSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    def get_photos(self, instance):
        return PhotoSerializer(instance.photo_ids, many=True).data

    class Meta:
        model = MapSquare
        fields = ['id', 'photos', 'photo_ids', 'boundaries', 'name']
