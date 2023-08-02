import json
import os

from rest_framework.renderers import JSONRenderer

from django.shortcuts import render
from django.conf import settings

from app.view_helpers import (
    get_map_squares_by_arondissement,
    photo_tag_helper,
    tag_helper,
    get_all_yolo_tags
)

from app.models import Photo, MapSquare
from app.serializers import SimplePhotoSerializer


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
    with open(os.path.join(settings.BACKEND_DATA_DIR, 'about.json'),
              encoding='utf-8') as f:
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
    arrondissement_data = get_map_squares_by_arondissement()
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


def explore_view(request):
    """
    Explore page
    """
    arrondissements_data = get_map_squares_by_arondissement()
    arrondissements_with_photos = []

    # For each arrondissement in the data, check if there are corresponding photos in the database
    for arr in arrondissements_data['arrondissements']:
        if Photo.objects.filter(map_square__number__in=arr['map_square_numbers']).exists():
            arrondissements_with_photos.append(arr['number'])

    context = {
        'page_metadata': {
            'title': 'Explore'
        },
        'component_name': 'Explore',
        'component_props': {
            'objects': get_all_yolo_tags(),
            'arrondissements': arrondissements_with_photos
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


def similar_photos_view(request, map_square_number,
                        folder_number, photo_number):
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
    photo = Photo.objects.get(number=photo_number,
                              folder=folder_number,
                              map_square__number=map_square_number)
    photographer = photo.photographer

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


def tag_view(request, tag_name, page=1):
    """
    Tag page, specified by tag_name
    """
    sorted_photo_obj, result_count, page_count = tag_helper(tag_name,
                                                            page=page)
    serializer = SimplePhotoSerializer(sorted_photo_obj, many=True)
    print('we are here')
    # there's probably a much simpler way...
    photo_data = JSONRenderer().render(serializer.data).decode("utf-8")
    context = {
        'page_metadata': {
            'title': 'Tag View'
        },
        'component_name': 'TagView',
        'component_props': {
            'tagName': tag_name,
            'tagPhotos': photo_data,
            'totalNumPhotos': result_count,
            'pageNum': page,
            'numPages': page_count,
        }
    }

    return render_view(request, context)
