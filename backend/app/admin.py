"""
This file controls the administrative interface for paris_1970 app
"""

from django.contrib import admin
from .models import (
    CorpusAnalysisResult,
    MapSquare,
    MapSquareAnalysisResult,
    Photo,
    PhotoAnalysisResult,
    Photographer,
    PhotographerAnalysisResult,
)

admin.site.register(CorpusAnalysisResult)
admin.site.register(MapSquare)
admin.site.register(MapSquareAnalysisResult)
admin.site.register(Photo)
admin.site.register(PhotoAnalysisResult)
admin.site.register(Photographer)
admin.site.register(PhotographerAnalysisResult)
