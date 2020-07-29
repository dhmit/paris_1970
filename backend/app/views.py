"""
These view functions and classes implement API endpoints
"""

# from pathlib import Path
# import json
# import csv

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Photo, MapSquare, Photographer
from .serializers import PhotoSerializer, MapSquareSerializer, PhotographerSerializer


@api_view(['GET'])
def photo(request, photo_id):
    photo_obj = Photo.objects.get(pk=photo_id)
    serializer = PhotoSerializer(photo_obj)
    return Response(serializer.data)


@api_view(['GET'])
def all_photos(request):
    photo_obj = Photo.objects.all()
    serializer = PhotoSerializer(photo_obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def all_map_squares(request):
    map_square_obj = MapSquare.objects.all()
    serializer = MapSquareSerializer(map_square_obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def all_photographers(request):
    photographer_obj = Photographer.objects.all()
    serializer = PhotographerSerializer(photographer_obj, many=True)
    return Response(serializer.data)

