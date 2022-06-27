"""
Models for the paris_1970 app.

"""
import os
from django.db import models
from django.conf import settings


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
