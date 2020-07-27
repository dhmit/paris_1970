"""
These view functions and classes implement API endpoints
"""

# from pathlib import Path
# import json
# import csv

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Photo
from .serializers import PhotoSerializer


@api_view(['GET'])
def photo(request, photo_id):
    photo_obj = Photo.objects.get(pk=photo_id)
    serializer = PhotoSerializer(photo_obj)
    return Response(serializer.data)


