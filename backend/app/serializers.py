"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
import json
from rest_framework import serializers
from .models import (
    CorpusAnalysisResult,
    MapSquare,
    Photo,
    PhotoAnalysisResult,
    Photographer,
)


class PhotoSerializer(serializers.ModelSerializer):
    """
    Serializes a photo
    """
    photographer_name = serializers.SerializerMethodField()
    photographer_number = serializers.SerializerMethodField()
    map_square_number = serializers.SerializerMethodField()
    analyses = serializers.SerializerMethodField()

    @staticmethod
    def get_photographer_name(instance):
        """ Photographer name for serialization """
        if instance.photographer:
            return instance.photographer.name
        else:
            return None

    @staticmethod
    def get_photographer_number(instance):
        """ Photographer number for serialization """
        if instance.photographer:
            return instance.photographer.number
        else:
            return None

    @staticmethod
    def get_map_square_number(instance):
        return instance.map_square.number

    @staticmethod
    def get_analyses(instance):
        analyses = PhotoAnalysisResult.objects.filter(photo=instance)
        return PhotoAnalysisResultSerializer(analyses, many=True).data

    class Meta:
        model = Photo
        fields = [
            'id', 'number', 'cleaned_src', 'front_src', 'back_src', 'binder_src',
            'thumbnail_src', 'alt', 'photographer_name', 'photographer_number',
            'map_square_number', 'shelfmark', 'librarian_caption', 'photographer_caption',
            'contains_sticker', 'analyses',
        ]


class MapSquareSerializer(serializers.ModelSerializer):
    """
    Serializes a map square
    """
    photos = serializers.SerializerMethodField()

    @staticmethod
    def get_photos(instance):
        photo_obj = Photo.objects.filter(map_square__number=instance.number)
        return PhotoSerializer(photo_obj, many=True).data

    class Meta:
        model = MapSquare
        fields = ['id', 'photos', 'boundaries', 'name', 'number']


class PhotographerSerializer(serializers.ModelSerializer):
    """
    Serializes a photographer
    """
    photos = serializers.SerializerMethodField()
    map_square = serializers.SerializerMethodField()

    @staticmethod
    def get_photos(instance):
        photo_obj = Photo.objects.filter(photographer__number=instance.number)
        return PhotoSerializer(photo_obj, many=True).data

    @staticmethod
    def get_map_square(instance):
        return MapSquareForPhotosSerializer(instance.map_square).data

    class Meta:
        model = Photographer
        fields = ['id', 'name', 'number', 'type', 'sentiment', 'photos', 'map_square']


class PhotoForPhotographerSerializer(serializers.ModelSerializer):
    """
    Serializes a Photo for the Photographer model, but without a reference to the photographer
    """
    map_square = serializers.SerializerMethodField()

    @staticmethod
    def get_map_square(instance):
        return MapSquareForPhotosSerializer(instance.map_square).data

    class Meta:
        model = Photo
        fields = ['id', 'front_src', 'back_src', 'binder_src', 'alt', 'map_square', 'number',
                  'shelfmark', 'librarian_caption', 'photographer_caption', 'contains_sticker',
                  ]


class MapSquareForPhotosSerializer(serializers.ModelSerializer):
    """
    Serializes a Map Square for the Photo model, but without a reference to the list of photos
    """

    class Meta:
        model = MapSquare
        fields = ['id', 'name', 'number', 'boundaries']


class CorpusAnalysisResultsSerializer(serializers.ModelSerializer):
    """
    Serializes the corpus analysis results. It converts the string version of JSON to regular
    JSON for the frontend to use.
    """
    analysis_result = serializers.SerializerMethodField()

    @staticmethod
    def get_analysis_result(instance):
        return json.loads(instance.analysis_result)

    class Meta:
        model = CorpusAnalysisResult
        fields = ['name', 'result']


class PhotoAnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoAnalysisResult
        fields = ['name', 'result']
