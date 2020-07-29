"""
Models for the paris_1970 app.

"""
from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=252)
    front_src = models.CharField(max_length=252)
    back_src = models.CharField(max_length=252)
    alt = models.CharField(max_length=252)
    map_square = models.ForeignKey('MapSquare', on_delete=models.SET_NULL, null=True)


class MapSquare(models.Model):
    name = models.CharField(max_length=252)
    photo_ids = models.ManyToManyField(
        'Photo',
        blank=True,
    )
    boundaries = models.CharField(max_length=252)


class Photographer(models.Model):
    name = models.CharField(max_length=252)
    type = models.CharField(max_length=252)
    sentiment = models.CharField(max_length=252)
    photo_ids = models.ManyToManyField(
        'Photo',
        blank=True,
    )
    map_square = models.ForeignKey('MapSquare', on_delete=models.SET_NULL, null=True)
