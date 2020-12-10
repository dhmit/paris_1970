"""
URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL configuration
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app.common import render_react_view
from app.views import (
    photo,
    all_photos,
    all_map_squares,
    get_photographer,
    get_map_square,
    get_corpus_analysis_results,
    get_photos_by_analysis
)


def react_view_path(route, component_name):
    """ Convenience function for React views """
    return path(
        route,
        render_react_view,
        {
            'component_name': component_name,
        },
    )


urlpatterns = [
    # Django admin page
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/photo/<int:map_square_number>/<int:photo_number>/', photo),
    path('api/photographer/<int:photographer_number>/', get_photographer),
    path('api/map_square/<int:map_square_number>/', get_map_square),
    path('api/corpus_analysis/', get_corpus_analysis_results),
    path('api/all_photos/', all_photos),
    path('api/all_map_squares/', all_map_squares),
    path('api/analysis/<str:analysis_name>/', get_photos_by_analysis),
    path('api/analysis/<str:analysis_name>/<str:object_name>/', get_photos_by_analysis),
    # path('api/faster_rcnn_object_detection/<str:object_name>/', get_photos_by_object_rcnn),
    # path('api/model/<str:model_name>/<str:object_name>/', get_photos_by_object),


    # React views
    react_view_path('', 'IndexView'),
    react_view_path('photo/<int:mapSquareNumber>/<int:photoNumber>/', 'PhotoView'),
    react_view_path('photographer/<int:photographerNumber>/', 'PhotographerView'),
    react_view_path('map_square/<int:mapSquareNumber>/', 'MapSquareView'),
    react_view_path('about/', 'About'),
    react_view_path('analysis/<str:analysisName>/', 'AnalysisView'),
    react_view_path('analysis/<str:analysisName>/<str:objectName>', 'AnalysisView'),
]
