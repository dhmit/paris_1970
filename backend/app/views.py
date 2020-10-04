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
def photo(request, map_square_number, photo_number):
    """
    API endpoint to get a photo with a primary key of photo_id
    """
    photo_obj = Photo.objects.get(number=photo_number, map_square__number=map_square_number)
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
def get_map_square(request, map_square_number):
    """
    API endpoint to get a map square from its map_square_id in the database
    """
    map_square_obj = MapSquare.objects.get(number=map_square_number)
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
def get_photographer(request, photographer_number):
    """
    API endpoint to get a photographer based on the photographer_id
    """
    photographer_obj = Photographer.objects.get(number=photographer_number)
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


@api_view(['GET'])
def get_photos_by_analysis(request, analysis_name):
    """
    API endpoint to get photos sorted by analysis
    """
    photo_obj = Photo.objects.filter(photoanalysisresult__name=analysis_name)
    sorted_photo_obj = photo_obj.order_by('photoanalysisresult__result')
    serializer = PhotoSerializer(sorted_photo_obj, many=True)
    return Response(serializer.data)
