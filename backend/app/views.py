"""
These view functions and classes implement API endpoints
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Photo, MapSquare, Photographer, CorpusAnalysisResult
from .serializers import (
    PhotoSerializer,
    MapSquareSerializer,
    PhotographerSerializer,
    CorpusAnalysisResultsSerializer,
)


@api_view(['GET'])
def photo(request, photo_id):
    """
    API endpoint to get a photo with a primary key of photo_id
    """
    photo_obj = Photo.objects.get(pk=photo_id)
    serializer = PhotoSerializer(photo_obj)
    return Response(serializer.data)


@api_view(['GET'])
def all_photos(request):
    """
    API endpoint to get all photos in the database
    """
    photo_obj = Photo.objects.all()
    serializer = PhotoSerializer(photo_obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_map_square(request, map_square_id):
    """
    API endpoint to get a map square from its map_square_id in the database
    """
    map_square_obj = MapSquare.objects.get(pk=map_square_id)
    serializer = MapSquareSerializer(map_square_obj)
    return Response(serializer.data)


@api_view(['GET'])
def all_map_squares(request):
    """
    API endpoint to get all map squares in the database
    """
    map_square_obj = MapSquare.objects.all()
    serializer = MapSquareSerializer(map_square_obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_photographer(request, photographer_id):
    """
    API endpoint to get a photographer based on the photographer_id
    """
    photographer_obj = Photographer.objects.get(pk=photographer_id)
    serializer = PhotographerSerializer(photographer_obj)
    return Response(serializer.data)


@api_view(['GET'])
def get_corpus_analysis_results(request):
    """
    API endpoint to get corpus analysis results
    """
    corpus_analysis_obj = CorpusAnalysisResult.objects.all()
    serializer = CorpusAnalysisResultsSerializer(corpus_analysis_obj, many=True)
    return Response(serializer.data)
