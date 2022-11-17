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
    Cluster,
)


class PhotoSerializer(serializers.ModelSerializer):
    """
    Serializes a photo
    """
    photographer_name = serializers.SerializerMethodField()
    photographer_number = serializers.SerializerMethodField()
    map_square_number = serializers.SerializerMethodField()
    analyses = serializers.SerializerMethodField()
    map_square_coords = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    slide_url = serializers.SerializerMethodField()
    photo_page_url = serializers.SerializerMethodField()

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
    def get_photo_url(instance):
        return instance.get_photo_url()

    @staticmethod
    def get_photo_page_url(instance):
        return instance.get_photo_page_url()

    @staticmethod
    def get_slide_url(instance):
        return instance.get_slide_url()

    @staticmethod
    def get_analyses(instance):
        analyses = PhotoAnalysisResult.objects.filter(photo=instance)
        analysis_results = PhotoAnalysisResultSerializer(analyses, many=True).data
        analyses_dict = {}
        for analysis_result in analysis_results:
            name = analysis_result['name']
            result = json.loads(analysis_result['result'])
            if name == "photo_similarity.resnet18_cosine_similarity":
                analyses_dict[name] = result[:10]
            else:
                analyses_dict[name] = result
            
        return analyses_dict

    @staticmethod
    def get_map_square_coords(instance):
        if instance.map_square.coordinates.split(', ') != ['']:
            return {dim: float(c)
                    for dim, c in zip(['lat', 'lng'], instance.map_square.coordinates.split(', '))
                    }
        else:
            return {}

    class Meta:
        model = Photo
        fields = [
            'id', 'number', 'folder', 'map_square_number',
            'alt', 'photographer_name', 'photographer_number',
            'shelfmark', 'librarian_caption', 'photographer_caption',
            'contains_sticker', 'analyses', 'map_square_coords', 'slide_url', 'photo_url',
            'photo_page_url'
        ]


class SimplePhotoSerializer(PhotoSerializer):
    class Meta:
        model = Photo
        fields = [
            'number', 'map_square_number', 'folder', 'photographer_number',  'photographer_name'
        ]


class MapSquareSerializer(serializers.ModelSerializer):
    """
    Serializes a map square
    """
    photos = serializers.SerializerMethodField()
    photographers = serializers.SerializerMethodField()

    @staticmethod
    def get_photos(instance):
        photo_queryset = instance.photo_set.all()
        return PhotoSerializer(photo_queryset, many=True).data

    @staticmethod
    def get_photographers(instance):
        photographers = Photographer.objects.filter(map_square=instance)
        return PhotographerSerializer(photographers, many=True).data

    class Meta:
        model = MapSquare
        fields = ['id', 'photos', 'photographers', 'boundaries', 'name', 'number', 'coordinates']


class MapSquareSerializerWithoutPhotos(serializers.ModelSerializer):
    """
    Serializes a map square without the photos for landing page (faster loading time)
    """
    num_photos = serializers.SerializerMethodField()

    @staticmethod
    def get_num_photos(instance):
        num_photos = instance.photo_set.all().count()
        return num_photos

    class Meta:
        model = MapSquare
        fields = ['id', 'num_photos', 'boundaries', 'name', 'number', 'coordinates']


class PhotographerSerializer(serializers.ModelSerializer):
    """
    Serializes a photographer
    """
    photos = serializers.SerializerMethodField()
    map_square = serializers.SerializerMethodField()

    @staticmethod
    def get_photos(instance):
        photo_queryset = instance.photo_set.all()
        return PhotoSerializer(photo_queryset, many=True).data

    @staticmethod
    def get_map_square(instance):
        return MapSquareForPhotosSerializer(instance.map_square).data

    class Meta:
        model = Photographer
        fields = ['id', 'name', 'number', 'type', 'sentiment', 'photos', 'map_square', 'approx_loc']


class PhotographerSearchSerializer(serializers.ModelSerializer):
    """
    Serializes a photographer for the search page
    """
    example_photo_src = serializers.SerializerMethodField()

    @staticmethod
    def get_example_photo_src(instance):
        # TODO(ra): Maybe this should be random?
        example_photo = instance.photo_set.first()
        if example_photo:
            return example_photo.get_photo_url()
        else:
            return None

    class Meta:
        model = Photographer
        fields = ['id', 'name', 'number', 'example_photo_src']


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
        fields = ['id', 'alt', 'map_square', 'number', 'shelfmark', 'librarian_caption',
                  'photographer_caption', 'contains_sticker',
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
    result = serializers.SerializerMethodField()

    @staticmethod
    def get_result(instance):
        return json.loads(instance.result)

    class Meta:
        model = CorpusAnalysisResult
        fields = ['name', 'result']


class PhotoAnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoAnalysisResult
        fields = ['name', 'result']


class ClusterSerializer(serializers.ModelSerializer):
    """
    Serializes a cluster
    """

    class Meta:
        model = Cluster
        fields = ['model_n', 'label', 'photos']
