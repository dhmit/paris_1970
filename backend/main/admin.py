"""
This file controls the administrative interface for paris_1970 main
"""

from django.contrib import admin
from .models import Photo, MapSquare, Photographer

admin.site.register(Photo)
admin.site.register(MapSquare)
admin.site.register(Photographer)
