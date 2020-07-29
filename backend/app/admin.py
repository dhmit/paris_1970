"""
This file controls the administrative interface for paris_1970 app
"""

from django.contrib import admin
from .models import Photo, MapSquare

admin.site.register(Photo)
admin.site.register(MapSquare)
