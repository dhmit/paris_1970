"""
This file controls the administrative interface for paris_1970 app
"""
import os
from django.db import models
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

class PhotoInline(admin.TabularInline):
    model = Photo
    exclude = ('alt', 'contains_sticker', 'librarian_caption')
    #readonly_fields= ('photo_slide',)

    """
    def photo_slide(self,obj):
        #Displays slide of photo obj

        # taking photos from local dir
        obj_path = obj.get_slide_url()
        return mark_safe('<a target="blank" href="{url}"> <img src="{url}" width="90px"></a>'.format(url=obj_path))
    """

class MapSquareAdmin(admin.ModelAdmin):
    """
    MapSquare Admin
    """
    inlines = [PhotoInline,]
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
            obj_path = photo.get_photo_url()
            link += '<a target="blank" href="{photo_url}"> <img src="{url}" ' \
                    'width="90px"></a>'.format(photo_url=obj_path, url=obj_path) + '\n'
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
        return mark_safe(
            '<a target="blank" href="{url}"> <img src="{url}" width="90px"></a>'.format(
                url=obj.get_photo_url()))

    photo_thumbnail.short_description = 'Photo'

    def photo_slide(self, obj):
        """
        Displays slide of photo obj
        """

        return mark_safe('<a target="blank" href="{url}"> <img src="{url}" width="90px" '
                         '></a>'.format(url=obj.get_photo_url()))

    photo_slide.short_description = 'Slide'


class PhotographerAdmin(admin.ModelAdmin):
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


admin.site.register(CorpusAnalysisResult)
admin.site.register(MapSquare, MapSquareAdmin)
admin.site.register(MapSquareAnalysisResult)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoAnalysisResult)
admin.site.register(Photographer, PhotographerAdmin)
admin.site.register(PhotographerAnalysisResult)
