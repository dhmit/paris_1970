"""
These view functions and classes implement API endpoints
"""
import ast
import json
import os
import math

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q, FloatField
from django.db.models.functions import Cast

from config.settings.base import YOLO_DIR
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
    MapSquareSerializerWithoutPhotos,
    PhotographerSerializer,
    PhotographerSearchSerializer,
    CorpusAnalysisResultsSerializer
)

ANALYSIS_TAGS = {
    'detail_fft2': 'detail_fft2',
    'find_vanishing_point': 'find_vanishing_point',
    'foreground_percentage': 'foreground_percentage',
    'combined_indoor': 'indoor_analysis.combined_indoor',
    'courtyard_frame': 'indoor_analysis.courtyard_frame',
    'find_windows': 'indoor_analysis.find_windows',
    'gradient_analysis': 'indoor_analysis.gradient_analysis',
    'local_variance': 'local_variance',
    'mean_detail': 'mean_detail',
    'photographer_caption_length': 'photographer_caption_length',
    'resnet18_cosine_similarity': 'photo_similarity.resnet18_cosine_similarity',
    'resnet18_mean_squares_similarity': 'photo_similarity.resnet18_mean_squares_similarity',
    'resnet18_pairwise_similarity': 'photo_similarity.resnet18_pairwise_similarity',
    'pop_density_detection': 'pop_density_detection',
    'portrait_detection': 'portrait_detection',
    'stdev': 'stdev',
    'text_ocr': 'text_ocr',
    'whitespace_percentage': 'whitespace_percentage',
    'yolo_model': 'yolo_model'
}


@api_view(['GET'])
def photo(request, map_square_number, photo_number):
    """
    API endpoint to get a photo with a map square number of map_square_number
    and photo number of photo_number
    """
    photo_obj = Photo.objects.get(number=photo_number, map_square__number=map_square_number)
    serializer = PhotoSerializer(photo_obj)
    return Response(serializer.data)


@api_view(['GET'])
def previous_next_photos(request, map_square_number, photo_number):
    """
    API endpoint to get the previous and next photos given the map square number and
    photo number of the current photo
    """
    photo_obj = Photo.objects.get(number=photo_number, map_square__number=map_square_number)
    resp = []
    if photo_obj.id > 1:
        previous_photo_object = Photo.objects.get(id=photo_obj.id - 1)
        previous_serialized = PhotoSerializer(previous_photo_object)
        resp.append(previous_serialized.data)
    else:
        resp.append("")

    if photo_obj.id < len(Photo.objects.all()):
        next_photo_object = Photo.objects.get(id=photo_obj.id + 1)
        next_serialized = PhotoSerializer(next_photo_object)
        resp.append(next_serialized.data)
    else:
        resp.append("")

    return Response(resp)


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
    API endpoint to get all map squares in the database for landing page
    """
    map_square_obj = MapSquare.objects.all()
    serializer = MapSquareSerializerWithoutPhotos(map_square_obj, many=True)
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
        elif isinstance(test_obj, dict) and object_name:
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
def get_photo_by_similarity(request, map_square_number, photo_number, num_similar_photos):
    """
    API endpoint to get top 10 similar photos of a specific photo
    """

    photo_obj = Photo.objects.get(number=photo_number, map_square__number=map_square_number)
    analysis_obj_list = PhotoAnalysisResult.objects.filter(
        name="photo_similarity.resnet18_cosine_similarity",
        photo=photo_obj,
    )

    similar_photos = []
    if analysis_obj_list:
        analysis_obj = analysis_obj_list[0]
        # splices the list of similar photos to get top 'num_similar_photos' photos
        similarity_list = ast.literal_eval(analysis_obj.result)[::-1][:num_similar_photos]

        for simPhoto in similarity_list:
            map_square = simPhoto[0]
            id_number = simPhoto[1]
            similar_photos.append(
                Photo.objects.get(number=id_number, map_square__number=map_square)
            )

    serializer = PhotoSerializer(similar_photos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_photos_by_cluster(request, number_of_clusters, cluster_number):
    """
    API endpoint to get clusters of similar photos
    """
    cluster = Cluster.objects.get(model_n=number_of_clusters, label=cluster_number)
    serializer = PhotoSerializer(cluster.photos.all(), many=True)
    return Response(serializer.data)


def get_analysis_value_ranges(analysis_names):
    """
    Function used to get the value ranges for the analysis search on the search page
    :return: Dictionary of 2-value lists representing the minimum and maximum values respectively,
    of the analysis.
    """
    value_ranges = {}
    all_results = PhotoAnalysisResult.objects.all()
    for analysis_name in analysis_names:
        analysis_results = all_results.filter(name=analysis_name)

        # Try sorting the values of the results and ignore the analysis name if the results
        # cannot be sorted (results of type dict or varying types)
        try:
            sorted_results = sorted(
                analysis_results, key=lambda instance: instance.parsed_result()
            )
        except TypeError:
            continue
        if not sorted_results:
            continue

        min_value = sorted_results[0].parsed_result()
        max_value = sorted_results[-1].parsed_result()

        # TODO: Add support for categorical values
        if type(min_value) in [int, float] and type(max_value) in [int, float]:
            value_ranges[analysis_name] = [math.floor(min_value), math.ceil(max_value)]

    return value_ranges


@api_view(['POST'])
def search(request):
    """
    API endpoint to search for photos that match the search query
    """
    # pylint: disable=too-many-locals
    query = json.loads(request.body)
    is_advanced = query['isAdvanced']

    if is_advanced:
        photographer_name = query['photographerName']
        photographer_num = query['photographerId']
        caption = query['caption'].strip()
        tags = query['tags']
        analysis_tags = query['analysisTags']
        slider_search_values = query['sliderSearchValues']
        print(slider_search_values)

        django_query = Q()
        photo_obj = Photo.objects.all()
        if photographer_name:
            django_query &= Q(photographer__name=photographer_name)

        if photographer_num:
            django_query &= Q(photographer__number=photographer_num)

        if caption:
            django_query &= Q(photographer_caption__icontains=caption) | \
                            Q(librarian_caption__icontains=caption)

        for tag in tags:
            django_query &= Q(photoanalysisresult__name='yolo_model') & \
                         Q(photoanalysisresult__result__icontains=tag)

        for analysis_tag in analysis_tags:
            photo_obj = photo_obj.filter(Q(photoanalysisresult__name=analysis_tag)).distinct()
            if slider_search_values.get(analysis_tag):
                min_value, max_value = slider_search_values[analysis_tag]
                print(f'Searching between {min_value} and {max_value} for {analysis_tag}')
                # Save the analysis results casted as float values to a new 'parsed_result' field
                photo_obj = photo_obj.annotate(
                    parsed_result=Cast('photoanalysisresult__result', FloatField())
                )
                # Filter for photos that have a result in the specified range
                photo_obj = photo_obj.filter(
                    Q(parsed_result__gte=min_value) &
                    Q(parsed_result__lte=max_value)
                )

        photo_obj = photo_obj.filter(django_query).distinct()
    else:
        keyword = query['keyword'].strip()
        photo_obj = Photo.objects.filter(Q(photographer__name__icontains=keyword) |
                                         Q(photographer__number__icontains=keyword) |
                                         Q(photographer_caption__icontains=keyword) |
                                         Q(librarian_caption__icontains=keyword) |
                                         (Q(photoanalysisresult__name='yolo_model') &
                                          Q(photoanalysisresult__result__icontains=keyword))
                                         ).distinct()
        # distinct is to prevent duplicates

    serializer = PhotoSerializer(photo_obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_tags(request):
    """
    API endpoint to get YOLO model tags, photographer data, and analysis tags for search
    """
    tags = []
    with open(os.path.join(YOLO_DIR, 'coco.names'), 'r') as file:
        tag = file.readline()
        while tag:
            tags.append(tag.strip())
            tag = file.readline()
    photographer_obj = Photographer.objects.all()
    photographer_serializer = PhotographerSearchSerializer(photographer_obj, many=True)
    return Response({
        'tags': tags,
        'photographers': photographer_serializer.data,
        'analysisTags': ANALYSIS_TAGS,
        'valueRanges': get_analysis_value_ranges(ANALYSIS_TAGS.keys())
    })
