import json
import random
from math import ceil

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q, Prefetch
from django.core.paginator import Paginator

from app.view_helpers import (
    get_map_squares_by_arondissement,
    get_arrondissement_geojson,
    tag_confidence
)

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
    SimplePhotoSerializerForCollage,
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


def tag_helper(tag_name, page=None):
    all_yolo_results = PhotoAnalysisResult.objects.filter(name='yolo_model')

    if not all_yolo_results.count():
        return []

    relevant_results = []
    print('yolo results here: ', len(all_yolo_results))
    for result in all_yolo_results:
        data = result.parsed_result()
        if tag_name in data['labels']:
            relevant_results.append(result)

    print('relevant results: ', len(relevant_results))

    # TODO(ra) Fix the results per page math... it looks like it's stepping
    # through src photo indexes
    results_per_page = 20
    result_count = len(relevant_results)
    page_count = ceil(result_count / results_per_page)

    if page:
        first_result = results_per_page * (page-1)
        last_result = first_result + results_per_page
        print(first_result, last_result)
        relevant_results_this_page = relevant_results[first_result:last_result]
    else:
        relevant_results_this_page = relevant_results

    print(relevant_results_this_page)

    # sort by confidence
    by_confidence = []
    for result in relevant_results_this_page:
        data = result.parsed_result()
        confidence = 0
        for box in data['boxes']:
            # an image may have several tag_name in labels, find greatest confidence
            if box['label'] == tag_name:
                confidence = max(confidence, box['confidence'])
        by_confidence.append((result, confidence))

    sorted_analysis_obj = sorted(by_confidence, key=lambda obj: obj[1], reverse=True)
    return [result[0].photo for result in sorted_analysis_obj], result_count, page_count


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
    )
    # add pagination here
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



@api_view(['GET'])
def get_photos_by_tag(request, tag_name):
    """
    API endpoint to get all photos associated with a tag (specified by tag_name)
    """
    sorted_photo_obj, _, _ = tag_helper(tag_name)
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
def get_random_photos(request):

    photos = list(Photo.objects.all())
    print(photos)
    random_photos = random.sample(photos, 9)
    serializer = SimplePhotoSerializerForCollage(random_photos, many=True)
    return Response(serializer.data)

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



@api_view(['POST'])
def explore(request):
    """
    API endpoint for the explore view, which gives users a filtered view
    to all of the photos in the collection
    """
    tag = request.data.get('selectedTag')
    page = int(request.data.get('page', 1))
    page_size = int(request.data.get('pageSize', 10))

    ALL = 'All'

    query = Q()

    # Filter by tags
    if tag != ALL:
        query |= Q(analyses__name='yolo_model', analyses__result__icontains=tag)

    if tag != ALL:
        prefetch = Prefetch('analyses', queryset=PhotoAnalysisResult.objects.filter(name='yolo_model'))
        photos = Photo.objects.filter(query).prefetch_related(prefetch).distinct()
        photos_with_analysis = [
            {
                'photo': photo,
                'analysis_result': list(photo.analyses.all())[0] if photo.analyses.all() else None
            }
            for photo in photos]

        photos_with_analysis.sort(key=lambda item: tag_confidence(item['photo'], item['analysis_result'], tag))

        # Extract sorted photos from the photos_with_analysis list
        photos = [item['photo'] for item in photos_with_analysis]

    else:
        photos = Photo.objects.filter(query).distinct()

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_photos = photos[start_idx:end_idx]
    total_pages = -(-len(photos) // page_size)  # This is a way to do ceiling division in Python

    photo_serializer = SimplePhotoSerializer(paginated_photos, many=True)

    return Response({
        'photos': photo_serializer.data,
        'currentPage': page,
        'totalPages': total_pages,
        'totalCount': len(photos),
    })


@api_view(['GET'])
def apply_filters(tag_request):
    """
    Given a particular request object that would specifically correlate to tag information, returns
    search queries corresponding to tag information. Backend filter bar in case current implementation doesn't work.
    """
    applied_query = json.loads(tag_request.GET.get('query', '{}'))


    tags_applied = [x for x in applied_query if applied_query[x]]
    all_photo_data = []

    for tag in tags_applied:
        all_photo_data += tag_helper(tag)

    tag_serializer = PhotoSerializer(all_photo_data, many=True)

    return Response(tag_serializer.data)


@api_view(['GET'])
def get_arrondissements_geojson(request, arr_number=None):
    """
    API endpoint to get the entries for each tract on the 1940s census
    :param request:
    :param arr_number:
    :return: Response
    """
    data = get_arrondissement_geojson()

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
    data = get_map_squares_by_arondissement()

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
