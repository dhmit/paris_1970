"""
This file controls the administrative interface for paris_1970 app
"""

from django.contrib import admin
from .models import Photo, MapSquare, Photographer, CorpusAnalysisResult

admin.site.register(Photo)
admin.site.register(MapSquare)
admin.site.register(Photographer)
admin.site.register(CorpusAnalysisResult)
