"""_photo_url()
These view functions and classes implement API endpoints
"""
import ast
import json
import os
import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings

from app import view_helpers

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
    SimplePhotoSerializer,
    MapSquareSerializer,
    MapSquareSerializerWithoutPhotos,
    PhotographerSerializer,
    PhotographerSearchSerializer,
    CorpusAnalysisResultsSerializer
)


# TODO(ra): See if we can move this elsewhere.
PHOTOGRAPHER_SEARCH_ORDER_BY = [
    "Name: ascending", 
    "Name: descending", 
    "Location: ascending", 
    "Location: descedning", 
    "Map Square #: ascending", 
    "Map Square #: descending"
]

@api_view(['GET'])
def photo(request, map_square_number, folder_number, photo_number):
    """
    API endpoint to get a photo with a map square number of map_square_number
    and photo number of photo_number
    """
    photo_obj = Photo.objects.get(number=photo_number, folder=folder_number, map_square__number=map_square_number)
    serializer = PhotoSerializer(photo_obj)
    return Response(serializer.data)


@api_view(['GET'])
def previous_next_photos(request, map_square_number, folder_number, photo_number):
    """
    API endpoint to get the previous and next photos given the map square number and
    photo number of the current photo
    """
    photo_obj = Photo.objects.get(number=photo_number,
                                  folder=folder_number,
                                  map_square__number=map_square_number)
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
    map_square_obj = MapSquare.objects.all().prefetch_related("photo_set")
    serializer = MapSquareSerializerWithoutPhotos(map_square_obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_photographers(request):
    """
    API endpoint to get a list of photographers based on a search query that looks the photographers by name 
    If not given a search query it will return the first 50 photographers sorted by name

    TODO: Add pagination for both cases (when given a search query and when nothing is given) 
    so that the user is sent the first 50 results and they can view more results as they scroll down the page.
    """

    def parse_order_by(order_by):
        if order_by not in PHOTOGRAPHER_SEARCH_ORDER_BY:
            return None

        field, asc = order_by.split(":")
        field = field.strip().lower()
        asc = asc.strip().lower()
        if field == "location":
            field = "approx_loc"
        elif field == "map square #":
            field = "map_square"
        
        asc = asc == 'ascending'
        
        return f'{"" if asc else "-"}{field}'

    # Pulling the params from the request
    name = request.GET.get("name", None)
    location = request.GET.get("location", None)
    map_square = request.GET.get("square", None)
    name_start = request.GET.get("name_starts_with", None)
    order_by = request.GET.get("order_by", None)

    # Pagination params
    page_number = request.GET.get("page", None)
    count_per_page = 50 

    search_params = {}
    
    # Validating and adding all of the params
    name = name.strip()
    location = location.strip()
    map_square = map_square.strip()

    if name:
        search_params["name__icontains"] = name
    if location:
        search_params["approx_loc"] = location 
    if map_square:
        map_square = int(map_square)
        search_params["map_square"] = map_square 
    
    # Planning to check for multiple name starts for this field 
    # Implmenetaiton example in this stackoverflow entry 
    #  (https://stackoverflow.com/questions/5783588/django-filter-on-same-option-with-multiple-possibilities)
    if name_start is not None and name_start.strip() != "":
        search_params["name__istartswith"] = name_start 

    order_by_field = parse_order_by(order_by)

    if len(search_params) == 0:
        matching_photographers = Photographer.objects.all()
    else:
        matching_photographers = Photographer.objects.filter(**search_params)

    matching_photographers.prefetch_related("photo_set")

    if order_by_field is not None:
        matching_photographers = matching_photographers.order_by(order_by_field)
    photographers_paginator = Paginator(matching_photographers, count_per_page)
    current_page = photographers_paginator.get_page(page_number)

    serialized_photographers = (
        PhotographerSearchSerializer(current_page.object_list, many=True)
    ) # add pagination here
    res = Response({
        "page_number": page_number,
        "results": serialized_photographers.data,
        "is_last_page": not current_page.has_next()
    })
    return res


@api_view(['GET'])
def get_search_photographers_dropdown_options(request):
    """
    API endpoint to get a list of photographers based on a search query that looks the photographers by name 
    If not given a search query it will return the first 50 photographers sorted by name

    TODO: Add pagination for both cases (when given a search query and when nothing is given) 
    so that the user is sent the first 50 results and they can view more results as they scroll down the page.
    """
    locations = sorted(
        filter(
            lambda x: x is not None, 
            list(
                set(Photographer.objects.all().values_list('approx_loc', flat=True))
            )
        )
    )

    squares = sorted(
        filter(
            lambda x: x is not None, 
            list(
                set(Photographer.objects.all().values_list('map_square_id', flat=True))
            )
        )
    )

    nameStartsWith = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    photographer_search_options = {
        "locations": locations,
        "squares": squares,
        "nameStartsWith": nameStartsWith,
        "orderBy": PHOTOGRAPHER_SEARCH_ORDER_BY
    }

    res = Response(photographer_search_options)
    return res

@api_view(['GET'])
def get_photographer(request, photographer_number=None):
    """
    API endpoint to get a photographer based on the photographer_id
    If given photographer_number, GETs associated phhotographer, else, returns all
    """
    if photographer_number:
        photographer_obj = Photographer.objects.get(number=photographer_number)
    else:
        photographer_obj = Photographer.objects.all()
    serializer = PhotographerSerializer(photographer_obj, many=photographer_number is None)
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
    API endpoint to get photos sorted by analysis (specified by analysis_name)
    Filters photos from analysis by object_name if given
    """
    analysis_obj = PhotoAnalysisResult.objects.filter(name=analysis_name)
    sorted_analysis_obj = analysis_obj
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
    sorted_photo_obj = [instance.photo for instance in sorted_analysis_obj]
    serializer = PhotoSerializer(sorted_photo_obj, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_images_with_text(request):
    """
    API endpoint to get photos that have text on them, according to our text_ocr analysis.
    """
    ocr_results = PhotoAnalysisResult.objects.filter(name='text_ocr')

    photos_with_text = []

    for result_obj in ocr_results:
        text_data = result_obj.parsed_result()
        if text_data:
            # TODO(ra) probably use a serializer instead but we're working fast...
            photos_with_text.append({
                'photo_page_url': result_obj.photo.get_photo_page_url(),
                'photo_url': result_obj.photo.get_photo_url(),
                'alt': result_obj.photo.alt,
                'text': text_data,
            })

    return Response(photos_with_text)



def format_photo(photo_obj, photo_values_to_keep):
    formatted_photo = {}
    for value in photo_values_to_keep:
        formatted_photo[value] = photo_obj[value]


def tag_helper(tag_name, page=None):
    all_yolo_results = list(PhotoAnalysisResult.objects.filter(name='yolo_model'))

    result_count = len(all_yolo_results)

    # TODO(ra) Fix the results per page math... it looks like it's stepping through src
    # photo indexes
    results_per_page = 20

    if page:
        first_result = results_per_page * (page-1)
        last_result = first_result + results_per_page*2
        print(first_result, last_result)
        results = all_yolo_results[first_result:last_result]
    else:
        results = all_yolo_results

    if result_count == 0:
        return []

    relevant_objects = []
    for result in results:
        data = result.parsed_result()
        if tag_name in data['labels']:
            relevant_objects.append(result)

    # sort by confidence
    by_confidence = []
    for result in relevant_objects:
        data = result.parsed_result()
        confidence = 0
        for box in data['boxes']:
            # an image may have several tag_name in labels, find greatest confidence
            if box['label'] == tag_name:
                confidence = max(confidence, box['confidence'])
        by_confidence.append((result, confidence))

    sorted_analysis_obj = sorted(by_confidence, key=lambda obj: obj[1], reverse=True)
    return [result[0].photo for result in sorted_analysis_obj]


@api_view(['GET'])
def get_photos_by_tag(request, tag_name):
    """
    API endpoint to get all photos associated with a tag (specified by tag_name)
    """
    sorted_photo_obj = tag_helper(tag_name)
    serializer = PhotoSerializer(sorted_photo_obj, many=True)
    return Response(serializer.data)


def photo_tag_helper(map_square_number, folder_number, photo_number):
    photo_obj = Photo.objects.get(number=photo_number, folder=folder_number, map_square__number=map_square_number)
    analysis_obj = PhotoAnalysisResult.objects.filter(name='yolo_model', photo=photo_obj)
    if analysis_obj:
        parsed_obj = analysis_obj[0].parsed_result()
        return list(parsed_obj['labels'])
    else:
        return None


@api_view(['GET'])
def get_photo_tags(request, map_square_number, folder_number, photo_number):
    """
    Given a specific photo, identified by map_square_number and photo_number, outputs the tags
    identified in that photo
    """
    return photo_tag_helper(map_square_number, folder_number, photo_number)


@api_view(['GET'])
def get_all_photos_in_order(request):
    """
    API endpoint to get photos sorted by map square, for similarity analysis
    """
    analysis_obj = PhotoAnalysisResult.objects.filter(name="resnet18_cosine_similarity")
    sorted_analysis_obj = sorted(analysis_obj, key=lambda instance: instance.parsed_result())
    sorted_photo_obj = [instance.photo for instance in sorted_analysis_obj]
    serializer = PhotoSerializer(sorted_photo_obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_photo_by_similarity(request, map_square_number, folder_number, photo_number, num_similar_photos):
    """
    API endpoint to get top similar photos of a specific photo, specified by map_square_number
    and photo_number
    Number of similar photos to GET specified by num_similar_photos
    """

    try:
        analysis_obj = PhotoAnalysisResult.objects.get(
            name="photo_similarity.resnet18_cosine_similarity",
            photo__number=photo_number,
            photo__map_square__number=map_square_number,
            photo__folder=folder_number,
        )
    except PhotoAnalysisResult.DoesNotExist:
        return Response("No such image", status=status.HTTP_204_NO_CONTENT)

    # splices the list of similar photos to get top 'num_similar_photos' photos
    similarity_list = analysis_obj.parsed_result()[:num_similar_photos]

    similar_photos = []
    for similar_photo in similarity_list:
        photo = (Photo.objects.prefetch_related('map_square')
                              .get(number=similar_photo['number'],
                                   map_square__number=similar_photo['map_square_number'],
                                   folder=similar_photo['folder_number']))
        similar_photos.append(photo)

    serializer = SimplePhotoSerializer(similar_photos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_photos_by_cluster(request, number_of_clusters, cluster_number):
    """
    TODO: not needed?
    API endpoint to get clusters of similar photos
    """
    cluster = Cluster.objects.get(model_n=number_of_clusters, label=cluster_number)
    serializer = PhotoSerializer(cluster.photos.all(), many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search(request):
    """
    API endpoint to search for photos that match the search query
    Post request
    """
    query = json.loads(request.GET.get('query', '{}'))

    between_quotes = r'(?<=\").*?(?=\")'
    special_characters = r'.?!,@#$%^&*_+<>/\'();:|`~\-\[\]\{\}'
    keywords = re.findall(
        rf'({between_quotes}|[\w{special_characters}]+)', query.get('keywords', '')
    )

    # This shouldn't be necessary in most recent pylint,
    # but older pylint doesn't understand the | below
    # pylint: disable=unsupported-binary-operation
    django_query = Q()
    photo_obj = Photo.objects.all()
    for keyword in keywords:
        sub_query = Q(
            Q(photographer__name=keyword)
            | Q(photographer_caption__icontains=keyword)
            | Q(librarian_caption__icontains=keyword)
            | Q(photoanalysisresult__name='yolo_model',
                photoanalysisresult__result__icontains=keyword)
        )
        if keyword.isdigit():
            sub_query |= Q(photographer__number=int(keyword))
        django_query &= sub_query

    photo_obj = photo_obj.filter(django_query).distinct()

    def tag_confidence(photo_obj):
        analysis_result = PhotoAnalysisResult.objects.filter(
            name='yolo_model',
            photo=photo_obj,
        ).first()
        if not analysis_result:
            return 100
        yolo_dict = analysis_result.parsed_result()
        max_confidence = max(
            [box['confidence'] for box in yolo_dict['boxes'] if box['label'] in keywords],
            default=100
        )
        return max_confidence

    photo_obj = sorted(photo_obj, key=tag_confidence, reverse=True)
    serializer = PhotoSerializer(photo_obj, many=True)
    return Response({
        'keywords': ', '.join([f'"{keyword}"' for keyword in keywords]),
        'searchData': serializer.data
    })


@api_view(['GET'])
def get_arrondissements_geojson(request, arr_number=None):
    """
    API endpoint to get the entries for each tract on the 1940s census
    :param request:
    :param arr_number:
    :return: Response
    """
    data = view_helpers.get_arrondissement_geojson()

    if arr_number is not None:
        # Get data for a single unique arrondissement
        arrondissement = next(filter(
            lambda el: el['properties']['c_ar'] == arr_number, data['features']
        ))
        data['features'] = [arrondissement]

    sorted_features = sorted(data['features'], key=lambda arr: arr['properties']['c_ar'])
    data['features'] = sorted_features
    return Response(data)


@api_view(['GET'])
def get_arrondissements_map_squares(request, arr_number=None):
    """
    API endpoint to get all of the map square numbers in arrondissements
    :param request:
    :param arr_number:
    :return: Response
    """
    data = view_helpers.get_map_square_data()

    if arr_number is not None:
        # Get data for a single unique arrondissement
        data['arrondissements'] = [data['arrondissements'][arr_number - 1]]

    return Response(data)


@api_view(['GET'])
def get_photo_distances(request, photographer_number):
    photo_data = [
        {
            'number': analysis_result.photo.number,
            'mapSquareNumber': analysis_result.photo.map_square.number,
            'distance': analysis_result.parsed_result()
        }
        for analysis_result in PhotoAnalysisResult.objects.filter(
            name='photographer_dist',
            photo__photographer__number=photographer_number
        )
    ]

    sorted_photo_data = sorted(
        photo_data, key=lambda data: data['distance'], reverse=True
    )
    return Response(sorted_photo_data)




# app views
def render_view(request, context):
    context.setdefault('component_props', {})
    return render(request, 'index.html', context)


def index(request):
    """
    Home page
    """

    context = {
        'page_metadata': {
            'title': 'Home page'
        },
        'component_name': 'HomePage'
    }

    return render_view(request, context)


def about(request):
    """
    About page
    """
    with open(os.path.join(settings.BACKEND_DATA_DIR, 'about.json'), encoding='utf-8') as f:
        about_text = json.load(f)

    context = {
        'page_metadata': {
            'title': 'About'
        },
        'component_name': 'About',
        'component_props': {
            'text': about_text
        }
    }

    return render_view(request, context)


def map_page(request):
    arrondissement_data = view_helpers.get_map_square_data()
    context = {
        'page_metadata': {
            'title': 'Map Page'
        },
        'component_name': 'MapPage',
        'component_props': {
            'arrondissement_data': json.dumps(arrondissement_data),
        }
    }

    return render_view(request, context)


def search_view(request):
    """
    Search page
    """
    context = {
        'page_metadata': {
            'title': 'Search'
        },
        'component_name': 'Search'
    }

    return render_view(request, context)


def map_square_view(request, map_square_number):
    """
    Map square page, specified by map_square_num
    """
    context = {
        'page_metadata': {
            'title': 'Map Square View'
        },
        'component_name': 'MapSquareView',
        'component_props': {
            'mapSquareNumber': map_square_number
        }
    }
    return render_view(request, context)

def text_ocr_view(request):
    """
    Sketchy prototype view for viewing all the text ocr photos
    """
    context = {
        'page_metadata': {
            'title': 'Text OCR'
        },
        'component_name': 'TextOCRView',
    }
    return render_view(request, context)

def similar_photos_view(request, map_square_number, folder_number, photo_number):
    """
    Sketchy prototype view for viewing all the images similar to a given image
    """
    context = {
        'page_metadata': {
            'title': 'Similar Photos'
        },
        'component_name': 'SimilarityView',
        'component_props': {
            'mapSquareNumber': map_square_number,
            'folderNumber': folder_number,
            'photoNumber': photo_number,
        }
    }
    return render_view(request, context)


def photographer_view(request, photographer_number):
    """
    Photographer page, specified by photographer_num
    """
    context = {
        'page_metadata': {
            'title': 'Photographer View'
        },
        'component_name': 'PhotographerView',
        'component_props': {
            'photographerNumber': photographer_number
        }
    }
    return render_view(request, context)


def photographer_list_view(request):
    """
    Photographer list page
    """
    photos_dir = os.path.join(settings.AWS_S3_PHOTOS_DIR, 'photographers')
    # serializer = PhotographerSearchSerializer(
    #     Photographer.objects.all().order_by('name'), many=True)

    context = {
        'page_metadata': {
            'title': 'Photographer List View'
        },
        'component_name': 'PhotographerListView',
        'component_props': {
            'photoListDir': photos_dir
        }
    }

    return render_view(request, context)


def photo_view(request, map_square_number, folder_number, photo_number):
    """
    Photo page, specified by map_square_number, folder_number, photo_num
    """
    tag_data = photo_tag_helper(map_square_number, folder_number, photo_number)
    photographer = Photo.objects.get(number=photo_number,
                                     folder=folder_number,
                                     map_square__number=map_square_number).photographer

    context = {
        'page_metadata': {
            'title': 'Photo View'
        },
        'component_name': 'PhotoView',
        'component_props': {
            'mapSquareNumber': map_square_number,
            'photoNumber': photo_number,
            'folderNumber': folder_number,
            'photoTags': tag_data,
            'photographer_name': "",
            'photographer_number': ""
        }
    }

    if photographer:
        context['component_props']['photographer_name'] = photographer.name
        context['component_props']['photographer_number'] = photographer.number

    return render_view(request, context)


def tag_view(request, tag_name, page=None):
    """
    Tag page, specified by tag_name
    """
    sorted_photo_obj = list(tag_helper(tag_name, page=page))
    serializer = SimplePhotoSerializer(sorted_photo_obj, many=True)
    # there's probably a much simpler way...
    photo_data = JSONRenderer().render(serializer.data).decode("utf-8")
    context = {
        'page_metadata': {
            'title': 'Tag View'
        },
        'component_name': 'TagView',
        'component_props': {
            'tagName': tag_name,
            'tagPhotos': photo_data
        }
    }

    return render_view(request, context)
