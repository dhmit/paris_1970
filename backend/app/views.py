"""
These view functions and classes implement API endpoints
"""
import ast
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q

from .models import (
    Photo,
    MapSquare,
    Photographer,
    CorpusAnalysisResult,
    PhotoAnalysisResult,
    Cluster,
)

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
def get_all_photographers(request):
    """
    API endpoint to get all photographers
    """
    photographers_obj = Photographer.objects.all()
    serializer = PhotographerSerializer(photographers_obj, many=True)
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
def all_analyses(request):
    """
    API endpoint to get all available analyses
    """
    photo_analysis_obj = PhotoAnalysisResult.objects.values_list('name').distinct()
    return Response([analysis[0] for analysis in photo_analysis_obj])


@api_view(['GET'])
def get_photos_by_analysis(request, analysis_name, object_name=None):
    """
    API endpoint to get photos sorted by analysis
    """
    analysis_obj = PhotoAnalysisResult.objects.filter(name=analysis_name)
    if len(analysis_obj) > 0:
        test_obj = analysis_obj[0].parsed_result()
        if type(test_obj) in [int, float, bool]:
            sorted_analysis_obj = sorted(
                analysis_obj, key=lambda instance: instance.parsed_result()
            )
        elif isinstance(test_obj,dict) and object_name:
            relevant_objects = [
                instance for instance in analysis_obj if object_name in instance.parsed_result()
            ]
            sorted_analysis_obj = sorted(
                relevant_objects, key=lambda instance: instance.parsed_result()[object_name]
            )
        elif type(test_obj) in [str, list, tuple, dict]:
            sorted_analysis_obj = sorted(
                analysis_obj, key=lambda instance: len(instance.parsed_result())
            )
    else:
        sorted_analysis_obj = analysis_obj
    sorted_photo_obj = [instance.photo for instance in sorted_analysis_obj]
    serializer = PhotoSerializer(sorted_photo_obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_photos_in_order(request):
    """
    API endpoint to get photos sorted by map square
    """
    analysis_obj = PhotoAnalysisResult.objects.filter(name="resnet18_cosine_similarity")
    sorted_analysis_obj = sorted(analysis_obj, key=lambda instance: instance.parsed_result())
    sorted_photo_obj = [instance.photo for instance in sorted_analysis_obj]
    serializer = PhotoSerializer(sorted_photo_obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_photo_by_similarity(request, map_square_number, photo_number):
    """
    API endpoint to get top 10 similar photos of a specific photo
    """

    photo_obj = Photo.objects.get(number=photo_number, map_square__number=map_square_number)
    analysis_obj_list = PhotoAnalysisResult.objects.filter(
        name="resnet18_cosine_similarity",
        photo=photo_obj,
    )

    similar_photos = []
    if analysis_obj_list:
        analysis_obj = analysis_obj_list[0]
        # splices the list of similar photos to get top 10 photos
        similarity_list = ast.literal_eval(analysis_obj.result)[:10]

        for simPhoto in similarity_list:
            map_square = simPhoto[0]
            id_number = simPhoto[1]
            similar_photos.append(
                Photo.objects.get(number=id_number, map_square__number=map_square)
            )

    serializer = PhotoSerializer(similar_photos, many=True)
    return Response(serializer.data)


def get_photos_by_cluster(request, number_of_clusters, cluster_number):
    """
    API endpoint to get clusters of similar photos
    """
    cluster = Cluster.objects.get(model_n=number_of_clusters, label=cluster_number)
    serializer = PhotoSerializer(cluster.photos.all(), many=True)
    return Response(serializer.data)


@api_view(['POST'])
def search(request):
    """
    API endpoint to search for photos that match the search query
    """
    query = json.loads(request.body)
    is_advanced = query['isAdvanced']

    if is_advanced:
        photographer = query['photographer'].strip()
        caption = query['caption'].strip()
        tags = query['tags'].strip()
        django_query = Q()
        if photographer != '':
            django_query &= Q(photographer__name__icontains=photographer)
        if caption != '':
            django_query &= Q(photographer_caption__icontains=caption) | \
                            Q(librarian_caption__icontains=caption)
        photo_obj = Photo.objects.filter(django_query)
    else:
        keyword = query['keyword'].strip()
        photo_obj = Photo.objects.filter(Q(photographer__name__icontains=keyword) |
                                         Q(photographer_caption__icontains=keyword) |
                                         Q(librarian_caption__icontains=keyword))

    serializer = PhotoSerializer(photo_obj, many=True)
    return Response(serializer.data)
