"""
Models for the paris_1970 app.

"""
from urllib.error import HTTPError
from http.client import RemoteDisconnected

from skimage import io

from django.db import models


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
    map_square = models.ForeignKey('MapSquare', on_delete=models.CASCADE)
    photographer = models.ForeignKey('Photographer', on_delete=models.SET_NULL, null=True)

    # These are computed and set by syncdb: could be null if a photo is missing a side
    cleaned_src = models.CharField(max_length=252, null=True)
    front_src = models.CharField(max_length=252, null=True)
    back_src = models.CharField(max_length=252, null=True)
    binder_src = models.CharField(max_length=252, null=True)
    cleaned_local_path = models.CharField(max_length=252, null=True)
    front_local_path = models.CharField(max_length=252, null=True)
    back_local_path = models.CharField(max_length=252, null=True)
    binder_local_path = models.CharField(max_length=252, null=True)

    # We transcribe this metadata in the Google Sheet
    shelfmark = models.CharField(max_length=252)
    contains_sticker = models.BooleanField(null=True)
    alt = models.CharField(max_length=252)
    librarian_caption = models.CharField(max_length=252)
    photographer_caption = models.CharField(max_length=252)

    def get_image_data(self):
        """
        Get the image data via skimage's imread, for use in analyses
        We try for a local filepath first, as that's faster,
        and we fallback on Google Drive if there's nothing local.
        """
        if self.cleaned_local_path:
            source = self.cleaned_local_path
        elif self.front_local_path:
            source = self.front_local_path
        elif self.binder_local_path:
            source = self.binder_local_path
        elif self.cleaned_src:
            source = self.cleaned_src
        elif self.front_src:
            source = self.front_src
        elif self.binder_src:
            source = self.binder_src
        else:
            print(f'{self} has no front or binder src')
            return None
        try:
            image = io.imread(source)
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


class Photographer(models.Model):
    """
    This model contains data about a single Photographer,
    which includes their name and the Map Square that this photographer was assigned to
    """
    name = models.CharField(max_length=252)
    number = models.IntegerField(null=True)
    map_square = models.ForeignKey(MapSquare, on_delete=models.SET_NULL, null=True)


class AnalysisResult(models.Model):
    """
    This model is used to store analysis results
    The analysis_result field is used to store a stringify-ed version of JSON which will
    be converted to regular JSON in the serializer.
    """
    name = models.CharField(max_length=252)
    result = models.DecimalField(null=True, decimal_places=4, max_digits=10)

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
