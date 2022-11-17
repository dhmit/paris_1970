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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from app import views
from app.common import render_react_view
from blog import views as blog_views


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

    # Photos
    path('api/photo/<int:map_square_number>/<int:folder_number>/<int:photo_number>/', views.photo, name="photo"),
    path('api/prev_next_photos/<int:map_square_number>/<int:folder_number>/<int:photo_number>/',
         views.previous_next_photos, name="previous_next_photos"),
    path('api/similar_photos/<int:map_square_number>/<int:folder_number>/<int:photo_number>/<int:num_similar_photos>/',
         views.get_photo_by_similarity, name="similar_photos"),
    path('api/all_photos/', views.all_photos, name="all_photos"),

    # Photographers
   	path('api/search_photographers/', views.search_photographers),
   	path('api/search_photographers/dropdown_options', views.get_search_photographers_dropdown_options),
    path('api/photographer/', views.get_photographer, name="all_photographers"),
    
    path('api/photographer/<int:photographer_number>/', views.get_photographer,
         name='photographer'),

    # Map Squares
    path('api/map_square/<int:map_square_number>/', views.get_map_square, name="map_square"),
    path('api/all_map_squares/', views.all_map_squares, name="all_map_squares"),

    # Tags
    path('api/tag/<str:tag_name>/', views.get_photos_by_tag, name="get_photos_by_tag"),

    # Analyses
    path('api/all_analyses/', views.all_analyses, name='all_analyses'),
    path('api/similarity/', views.get_all_photos_in_order, name="all_photos_in_order"),
    path('api/analysis/<str:analysis_name>/', views.get_photos_by_analysis,
         name="get_photos_by_analysis"),
    path('api/analysis/<str:analysis_name>/<str:object_name>/', views.get_photos_by_analysis,
         name="get_photos_by_analysis"),
    path('api/corpus_analysis/', views.get_corpus_analysis_results, name="get_corpus"),
    path('api/clustering/<int:number_of_clusters>/<int:cluster_number>/',
         views.get_photos_by_cluster, name="clustering"),
    path('api/text_ocr/', views.get_images_with_text),

    path('api/search/', views.search, name="search"),


    # Arrondissements
    path('api/arrondissements_geojson/', views.get_arrondissements_geojson,
         name="get_arrondissement"),
    path('api/arrondissements_geojson/<int:arr_number>/',
         views.get_arrondissements_geojson, name="get_one_arrondissement"),
    path('api/arrondissements_map_squares/', views.get_arrondissements_map_squares),
    path('api/arrondissements_map_squares/<int:arr_number>', views.get_arrondissements_map_squares),

    # Distances
    path('api/get_photo_distances/<int:photographer_number>/',
         views.get_photo_distances, name="get_photo_distances"),
    # path('api/faster_rcnn_object_detection/<str:object_name>/', views.get_photos_by_object_rcnn),
    # path('api/model/<str:model_name>/<str:object_name>/', views.get_photos_by_object),
    # path('api/faster_rcnn_object_detection/<str:object_name>/',
    # views.get_photos_by_object_rcnn),
    # path('api/model/<str:model_name>/<str:object_name>/', views.get_photos_by_object),

    # View Pages
    path('', views.index),
    path('map/', views.map_page),
    path('about/', views.about),
    path('search/', views.search_view),
    # Photographers
    path('photographers/', views.photographer_list_view),
    path('photographer/<int:photographer_number>/', views.photographer_view),

    # Photos
    path('photo/<int:map_square_number>/<int:folder_number>/<int:photo_number>/', views.photo_view),

    # blog urls
    path(f'{settings.BLOG_ROOT_URL}/', blog_views.blog_home_page, name="blog_home"),
    path(f'{settings.BLOG_ROOT_URL}/<str:slug>/', blog_views.blog_post,
         name='blog-detail'),

    # Map Squares
    path('map_square/<int:map_square_number>/', views.map_square_view),
    path('text_ocr/', views.text_ocr_view),

    # path('clustering/<int:num_of_clusters>/<int:cluster_num>/', views.cluster_view),
    # BFlog urls
    # Log in/out urls
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Tags
    path('tag/<str:tag_name>/', views.tag_view),

]
