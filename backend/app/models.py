"""
Models for the paris_1970 app.

"""
from django.db import models


class Photo(models.Model):
    """
    This model holds the metadata for a single photo, which includes the
    source names, title, alt text. This model also contains a foreign key
    to the Map Square that the photo belongs to and the Photographer who
    took the photo.
    """
    number = models.IntegerField(null=True)
    shelfmark = models.CharField(max_length=252)
    contains_sticker = models.BooleanField(null=True)
    front_src = models.CharField(max_length=252)
    back_src = models.CharField(max_length=252)
    binder_src = models.CharField(max_length=252)
    alt = models.CharField(max_length=252)
    librarian_caption = models.CharField(max_length=252)
    photographer_caption = models.CharField(max_length=252)
    map_square = models.ForeignKey('MapSquare', on_delete=models.SET_NULL, null=True)
    photographer = models.ForeignKey('Photographer', on_delete=models.SET_NULL, null=True)


class MapSquare(models.Model):
    """
    This model contains data about a specific Map Square, which includes its name,
    a list of foreign keys to all the Photos that are in this Map Square, and
    the boundary of this Map Square.
    """
    name = models.CharField(max_length=252)
    number = models.IntegerField(null=True)
    boundaries = models.CharField(max_length=252)


class Photographer(models.Model):
    """
    This model contains data about a single Photographer, which includes the name, type, sentiment,
    list of Photos taken by this Photographer, and the Map Square that this photographer was
    assigned to
    """
    name = models.CharField(max_length=252)
    number = models.IntegerField(null=True)
    type = models.CharField(max_length=252)
    sentiment = models.CharField(max_length=252)
    map_square = models.ForeignKey('MapSquare', on_delete=models.SET_NULL, null=True)
