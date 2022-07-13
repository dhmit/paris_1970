"""
This file controls the administrative interface for paris_1970 app
"""
from django.conf import settings
import os
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
        photo_obj = Photo.objects.filter(map_square__number=obj.number)
        for photo in photo_obj:
            # path to photo
            obj_path = os.path.join(settings.LOCAL_PHOTOS_DIR, str(obj.number),
                                    str(photo.number)+'_photo.jpg')

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
        cmd = '<a target = "blank" href = "{url}">{title}</a>'.format(url=link, title= obj.map_square.number)
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
            cmd = '<a target = "blank" href = "{url}">{title}</a>'.format(url=link, title=title)
            return mark_safe(cmd)
        else:
            return
    photographer_info.short_description = 'Photographer'

    def photo_thumbnail(self, obj):
        """
        Displays thumbnail of photo obj
        """

        # taking photos from local dir
        obj_path = os.path.join(settings.LOCAL_PHOTOS_DIR, str(obj.map_square.number),
                                str(obj.number)+'_photo.jpg')
        return mark_safe('<a target = "blank" href = "{url}"> <img src="{url}" width="90px" '
                         '></a>'.format(url=obj_path))
    photo_thumbnail.short_description = 'Photo'

    def photo_slide(self, obj):
        """
        Displays slide of photo obj
        """

        # taking photos from local dir
        obj_path = os.path.join(settings.LOCAL_PHOTOS_DIR, str(obj.map_square.number),
                                str(obj.number)+'_slide.jpg')
        return mark_safe('<a target = "blank" href = "{url}"> <img src="{url}" width="90px" '
                         '></a>'.format(url=obj_path))
    photo_slide.short_description = 'Slide'


admin.site.register(CorpusAnalysisResult)
admin.site.register(MapSquare, MapSquareAdmin)
admin.site.register(MapSquareAnalysisResult)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoAnalysisResult)
admin.site.register(Photographer)
admin.site.register(PhotographerAnalysisResult)
