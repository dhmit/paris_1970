"""
Models for the paris_1970 app.

"""
import os
import json

from urllib.error import HTTPError
from http.client import RemoteDisconnected

from skimage import io
from PIL import Image

from django.db import models
from django.conf import settings


class Photo(models.Model):
    """
    This model holds the metadata for a single photo, which includes the
    source names, title, alt text. This model also contains a foreign key
    to the Map Square that the photo belongs to and the Photographer who
    took the photo.
    """

    # Use number and map_square to uniquely identify a photo
    # DO NOT use the database pk, as that may change as we rebuild the database
    number = models.IntegerField(null=True)  # NOT the database PK, but rather based on shelfmark
    map_square = models.ForeignKey('MapSquare', on_delete=models.CASCADE, null=True)
    photographer = models.ForeignKey('Photographer', on_delete=models.SET_NULL, null=True)

    cleaned_src = models.BooleanField(default=False)
    front_src = models.BooleanField(default=False)
    back_src = models.BooleanField(default=False)
    thumbnail_src = models.BooleanField(default=False)

    # We transcribe this metadata in the Google Sheet
    shelfmark = models.CharField(max_length=252)
    contains_sticker = models.BooleanField(null=True)
    alt = models.CharField(max_length=252)
    librarian_caption = models.CharField(max_length=252)
    photographer_caption = models.CharField(max_length=252)

    def has_valid_source(self):
        return (self.cleaned_src or
                self.front_src)

    def get_image_data(self, as_gray=False, use_pillow=False):
        """
        Get the image data via skimage's imread, for use in analyses

        We try for a local filepath first, as that's faster,
        and we fallback on Google Drive if there's nothing local.

        Optionally use Pillow instead (for pytorch analyses)
        and return as_gray

        TODO: implement as_gray for use_pillow
        """
        if not (self.cleaned_src or self.front_src):
            print(f'{self} has no front or binder src')
            return None

        source = os.path.join(
            settings.LOCAL_SRCS_DIR,
            str(self.map_square.number),
            f"{self.number}_photo.jpg"
        )

        try:
            if use_pillow:
                image = Image.open(source)
            else:
                image = io.imread(source, as_gray)
        except (HTTPError, RemoteDisconnected) as base_exception:
            raise Exception(
                f'Failed to download image data for {self} due to Google API rate limiting.'
            ) from base_exception
        return image

    class Meta:
        unique_together = ['number', 'map_square']


class MapSquare(models.Model):
    """
    This model contains data about a specific Map Square, which includes its name,
    a list of foreign keys to all the Photos that are in this Map Square, and
    the boundary of this Map Square.
    """
    name = models.CharField(max_length=252)
    number = models.IntegerField(null=True)
    boundaries = models.CharField(max_length=252)
    coordinates = models.CharField(max_length=252)


class Photographer(models.Model):
    """
    This model contains data about a single Photographer,
    which includes their name and the Map Square that this photographer was assigned to
    """
    name = models.CharField(max_length=252)
    number = models.IntegerField(null=True)
    map_square = models.ForeignKey(MapSquare, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=252, null=True)
    sentiment = models.CharField(max_length=252, null=True)


class AnalysisResult(models.Model):
    """
    This model is used to store analysis results
    The analysis_result field is used to store a stringify-ed version of JSON which will
    be converted to regular JSON in the serializer.
    """
    name = models.CharField(max_length=252)
    result = models.TextField(null=True)

    def parsed_result(self):
        return json.loads(self.result)

    class Meta:
        # Make this an abstract base class, which means that Django won't create a database
        # table for this model -- it's only here as a base class for classes below
        abstract = True


class CorpusAnalysisResult(AnalysisResult):
    """
    This model is used to store analysis results on the entire corpus.
    Right now, it doesn't do anything that AnalysisResult doesn't already do.
    """
    pass


class PhotoAnalysisResult(AnalysisResult):
    """
    This model is used to store an analysis result for a single Photo
    """
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'PhotoAnalysisResult {self.name} for photo with id {self.photo.id}'


class PhotographerAnalysisResult(AnalysisResult):
    """
    This model is used to store an analysis result for a single Photo
    """
    photographer = models.ForeignKey(Photo, on_delete=models.CASCADE, null=False)


class MapSquareAnalysisResult(AnalysisResult):
    """
    This model is used to store an analysis result for a single Photo
    """
    map_square = models.ForeignKey(MapSquare, on_delete=models.CASCADE, null=False)


class Cluster(models.Model):
    """
    This model is used to organize groups of similar photos
    """
    model_n = models.IntegerField(null=True)
    label = models.IntegerField(null=True)
    photos = models.ManyToManyField(Photo)

    class Meta:
        unique_together = ['model_n', 'label']
