"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
from rest_framework import serializers
from .models import Photo, MapSquare, Photographer


class PhotoSerializer(serializers.ModelSerializer):

    photographer = serializers.SerializerMethodField()
    map_square = serializers.SerializerMethodField()

    def get_photographer(self, instance):
        return PhotographerForPhotosSerializer(instance.photographer_obj).data

    def get_map_square(self, instance):
        return MapSquareForPhotosSerializer(instance.map_square_obj).data

    class Meta:
        model = Photo
        fields = ['id', 'front_src', 'back_src', 'alt', 'title', 'photographer', 'map_square']


# This is to avoid an infinite recursion depth
class PhotographerForPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ['id', 'name', 'type', 'sentiment']


class MapSquareForPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapSquare
        fields = ['id', 'name', 'photo_ids', 'boundaries']


class MapSquareSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    def get_photos(self, instance):
        return PhotoSerializer(instance.photo_ids, many=True).data

    class Meta:
        model = MapSquare
        fields = ['id', 'photos', 'photo_ids', 'boundaries', 'name']


class PhotographerSerializer(serializers.ModelSerializer):

    photos = serializers.SerializerMethodField()
    map_square = serializers.SerializerMethodField()

    def get_photos(self, instance):
        return PhotoSerializer(instance.photo_ids, many=True).data

    def get_map_square(self, instance):
        return MapSquareSerializer(instance.map_square_obj).data

    class Meta:
        model = Photographer
        fields = ['id', 'name', 'type', 'sentiment', 'photos', 'map_square']
