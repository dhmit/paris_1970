"""
This file controls the administrative interface for paris_1970 app
"""

from django.contrib import admin
from .models import (Post, Category,)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post,PostAdmin)
admin.site.register(Category)
