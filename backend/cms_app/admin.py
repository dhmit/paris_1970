"""
This file controls the administrative interface for paris_1970 app
"""

from django.contrib import admin
from .models import BlogPost


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(BlogPost,PostAdmin)
