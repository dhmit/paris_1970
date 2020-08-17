"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
from rest_framework import serializers
from .models import Photo, MapSquare, Photographer


class PhotoSerializer(serializers.ModelSerializer):
    """
    Serializes a photo
    """
    photographer = serializers.SerializerMethodField()
    map_square = serializers.SerializerMethodField()

    def get_photographer(self, instance):
        return PhotographerForPhotosSerializer(instance.photographer).data

    def get_map_square(self, instance):
        return MapSquareForPhotosSerializer(instance.map_square).data

    class Meta:
        model = Photo
        fields = ['id', 'number', 'front_src', 'back_src', 'binder_src', 'alt', 'photographer',
                  'map_square', 'shelfmark', 'librarian_caption', 'photographer_caption',
                  'contains_sticker', 'white_space_ratio_front', 'white_space_ratio_back',
                  'white_space_ratio_binder']


class MapSquareSerializer(serializers.ModelSerializer):
    """
    Serializes a map square
    """
    photos = serializers.SerializerMethodField()

    def get_photos(self, instance):
        photo_obj = Photo.objects.filter(map_square__number=instance.number)
        return PhotosForMapSquareSerializer(photo_obj, many=True).data

    class Meta:
        model = MapSquare
        fields = ['id', 'photos', 'boundaries', 'name', 'number']


class PhotographerSerializer(serializers.ModelSerializer):
    """
    Serializes a photographer
    """
    photos = serializers.SerializerMethodField()
    map_square = serializers.SerializerMethodField()

    def get_photos(self, instance):
        photo_obj = Photo.objects.filter(photographer__number=instance.number)
        return PhotoForPhotographerSerializer(photo_obj, many=True).data

    def get_map_square(self, instance):
        return MapSquareForPhotosSerializer(instance.map_square).data

    class Meta:
        model = Photographer
        fields = ['id', 'name', 'number', 'type', 'sentiment', 'photos', 'map_square']


# These methods are used to avoid an infinite recursion depth
class PhotographerForPhotosSerializer(serializers.ModelSerializer):
    """
    Serializes a Photographer for the Photo model, but without a reference to the list of photos
    or the map square
    """
    class Meta:
        model = Photographer
        fields = ['id', 'name', 'number', 'type', 'sentiment']


class PhotoForPhotographerSerializer(serializers.ModelSerializer):
    """
    Serializes a Photo for the Photographer model, but without a reference to the photographer
    """
    map_square = serializers.SerializerMethodField()

    def get_map_square(self, instance):
        return MapSquareForPhotosSerializer(instance.map_square).data

    class Meta:
        model = Photo
        fields = ['id', 'front_src', 'back_src', 'binder_src', 'alt', 'map_square', 'number',
                  'shelfmark', 'librarian_caption', 'photographer_caption', 'contains_sticker']


class MapSquareForPhotosSerializer(serializers.ModelSerializer):
    """
    Serializes a Map Square for the Photo model, but without a reference to the list of photos
    """
    class Meta:
        model = MapSquare
        fields = ['id', 'name', 'number', 'boundaries']


class PhotosForMapSquareSerializer(serializers.ModelSerializer):
    """
    Serializes a Photo for the Map Square model, but without a reference to the map square
    """
    photographer = serializers.SerializerMethodField()

    def get_photographer(self, instance):
        return PhotographerForPhotosSerializer(instance.photographer).data

    class Meta:
        model = Photo
        fields = ['id', 'number', 'front_src', 'back_src', 'binder_src', 'alt', 'photographer',
                  'shelfmark', 'librarian_caption', 'photographer_caption', 'contains_sticker']
