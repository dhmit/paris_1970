"""
This file controls the administrative interface for paris_1970 app
"""
import os
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    CorpusAnalysisResult,
    MapSquare,
    MapSquareAnalysisResult,
    Photo,
    PhotoAnalysisResult,
    Photographer,
    PhotographerAnalysisResult,
)


class MapSquareAdmin(admin.ModelAdmin):
    """
    MapSquare Admin
    """
    list_display = ('id', 'number', 'show_coordinates', 'count_photos', 'boundaries')
    search_fields = ['id', 'number']
    readonly_fields = ('all_photos',)

    def show_coordinates(self, obj):
        """
        Returns coordinates of map square in (x,y) format
        """
        return '(' + obj.coordinates + ')'

    show_coordinates.short_description = 'Coordinates'

    def count_photos(self, obj):
        """
        Returns an integer representing the number taken of that map square
        """

        # filter for all photo objects with obj's map square number
        # TODO(ra): use the reverse relationship and count() here
        photo_obj = Photo.objects.filter(map_square__number=obj.number)
        return len(photo_obj)

    count_photos.short_description = 'Number of Photos'

    @staticmethod
    def all_photos(obj):
        """
        Displays all images taken at that map square
        """
        link = ''
        # filter for all photo objects of obj map square
        # TODO(ra): use the reverse relationship here
        photo_obj = Photo.objects.filter(map_square__number=obj.number)
        for photo in photo_obj:
            # path to photo
            obj_path = os.path.join(settings.AWS_S3_PHOTOS_DIR, str(obj.number),
                                    str(photo.number) + '_photo.jpg')
        


            # path to photo's admin change page
            photo_path = os.path.join('/admin/app/photo', str(photo.id))
            link += '<a target="blank" href="{photo_url}"> <img src="{url}" ' \
                    'width="90px"></a>'.format(photo_url=photo_path, url=obj_path) + '\n'
        return mark_safe(link)


class PhotoAdmin(admin.ModelAdmin):
    """
    Photo Admin
    """
    list_display = ('id', 'number', 'photo_thumbnail', 'map_square_number',
                    'photographer_info', 'librarian_caption', 'photographer_caption')
    search_fields = ['number', 'map_square__id', 'photographer__id', 'photographer__name']

    readonly_fields = ('photo_thumbnail', 'photo_slide')

    def map_square_number(self, obj):
        """
        Returns map square number
        """
        link = os.path.join('/admin/app/mapsquare', str(obj.map_square.id))
        cmd = '<a target="blank" href="{url}">{title}</a>'.format(url=link,
                                                                  title=obj.map_square.number)
        return mark_safe(cmd)

    map_square_number.short_description = 'Map Square'
    map_square_number.admin_order_field = 'map_square__number'

    def photographer_info(self, obj):
        """
        Returns photographer number (and name if available)
        """
        if obj.photographer:
            if obj.photographer.name:
                title = str(obj.photographer.id) + ' (' + obj.photographer.name + ')'
            else:
                title = str(obj.photographer.id) + ' (-)'
            link = os.path.join('/admin/app/photographer', str(obj.photographer.id))
            cmd = '<a target="blank" href="{url}">{title}</a>'.format(url=link, title=title)
            return mark_safe(cmd)
        else:
            return None

    photographer_info.short_description = 'Photographer'

    def photo_thumbnail(self, obj):
        """
        Displays thumbnail of photo obj
        """

        # taking photos from local dir
        obj_path = os.path.join(settings.AWS_S3_PHOTOS_DIR, str(obj.map_square.number),
                                str(obj.number) + '_photo.jpg')
        return mark_safe(
            '<a target="blank" href="{url}"> <img src="{url}" width="90px"></a>'.format(
                url=obj_path))

    photo_thumbnail.short_description = 'Photo'

    def photo_slide(self, obj):
        """
        Displays slide of photo obj
        """

        # taking photos from local dir
        obj_path = os.path.join(settings.AWS_S3_PHOTOS_DIR, str(obj.map_square.number),
                                str(obj.number) + '_slide.jpg')
        return mark_safe('<a target="blank" href="{url}"> <img src="{url}" width="90px" '
                         '></a>'.format(url=obj_path))

    photo_slide.short_description = 'Slide'


class PhotographerAdmin(admin.ModelAdmin):
<<<<<<< Updated upstream
    list_display = ["id", "name", "number", "approx_loc", "map_square"]
    search_fields = ['id', 'number', "name", "approx_loc", "map_square__number"]
    
    def map_square(self, obj):
        """
        Returns map square number
        """
        link = os.path.join('/admin/app/mapsquare', str(obj.map_square.id))
        cmd = '<a target="blank" href="{url}">{title}</a>'.format(url=link,
                                                                  title=obj.map_square.number)
        return mark_safe(cmd)
    map_square.short_description = 'Map Square'
=======
    list_display = ["id", "name", "number"]

class PhotoAnalysisResultAdmin(admin.ModelAdmin):
    """
    Photo Analysis Result
    """
    list_display = ('id','number','distance','photo_analysis_result','map_square_number',
                    'photo_thumbnail','photographer__name','photographer_info')
    search_fields = ['id','number','map_square_number','photo_thumbnail','photographer__name',
                    'photographer_info']
    readonly_fields = ('photo_thumbnail','photo_analysis_result')
    
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'PhotoAnalysisResult {self.name} for photo with id {self.photo.id}'

    import os
    import json
    from math import sin, cos, sqrt, atan2, radians

    from django.conf import settings
    from .models import Photo

    MODEL = Photo

    DATA_PATH = os.path.join(settings.BACKEND_DATA_DIR, "photographer_locations.json")

    def lat_lon_distance(coord1, coord2):
        """
        Returns the distance in kilometers between two (latitude, longitude) coordinates.
        Calculated using the haversine formula
        """
        # Approximate radius of earth in km
        earth_radius = 6373.0

        lat1, lon1, lat2, lon2 = [radians(d) for d in coord1 + coord2]
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Intermediate calculation variables
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = earth_radius * c
        return distance

    def analyze(photo: Photo):
        with open(DATA_PATH, 'r', encoding="utf-8") as file:
            photographer_locations = json.load(file)
        photographer = photo.photographer
        if not (photographer and photographer_locations.get(str(photographer.number))):
            return -1
        photo_coords = tuple([float(c) for c in photo.map_square.coordinates.split(', ')])
        location = photographer_locations.get(str(photographer.number))
        photographer_coords = (float(location['lat']), float(location['lon']))
        return lat_lon_distance(photo_coords, photographer_coords)
>>>>>>> Stashed changes

admin.site.register(CorpusAnalysisResult)
admin.site.register(MapSquare, MapSquareAdmin)
admin.site.register(MapSquareAnalysisResult)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoAnalysisResult)
admin.site.register(Photographer, PhotographerAdmin)
admin.site.register(PhotographerAnalysisResult)
