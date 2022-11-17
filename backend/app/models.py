"""
Models for the paris_1970 app.

"""
import json

from pathlib import Path

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

    # The source image filenames have the following structure:
    # BHVP_PH_CetaitParis_DP_MAP-SQUARE-NUMBER_FOLDER-NUMBER_FILE-NUMBER

    # The FILE-NUMBER comes in pairs, but numbered straight through. e.g., 
    # BHVP_PH_CetaitParis_DP_0031_01_001 -- this is a scan of the slide, including its frame
    # BHVP_PH_CetaitParis_DP_0031_01_002 -- this is a high quality scan of the photo itself
    # We collapse these two into a single number: 1
    # The next pair (01_003 and 01_004) become photo 2, etc.
    number = models.IntegerField()

    # Furthermore, many map squares contained multiple folders.
    # These folders seemed meaningful -- they often represent boundary points between photographers.
    folder = models.IntegerField()

    # The original full filename of the SLIDE as provided to us by 
    # e.g., "BHVP_PH_CetaitParis_DP_0031_01_001"
    shelfmark = models.CharField(max_length=252)

    map_square = models.ForeignKey('MapSquare', on_delete=models.CASCADE, null=True)
    photographer = models.ForeignKey('Photographer', on_delete=models.SET_NULL, null=True)

    # TODO(ra 2022-10-28): We are likely to drop a bunch of these old metadata fields.
    contains_sticker = models.BooleanField(null=True)
    alt = models.CharField(max_length=252)
    librarian_caption = models.CharField(max_length=252)
    photographer_caption = models.CharField(max_length=252)

    def get_image_data(self, as_gray=False, use_pillow=False, photos_dir=settings.LOCAL_PHOTOS_DIR):
        """
        Get the image data via skimage's imread, for use in analyses

        Optionally use Pillow instead (for pytorch analyses)
        and return as_gray

        TODO: implement as_gray for use_pillow
        """
        photo_path = self.image_local_filepath(photos_dir=photos_dir)
        if use_pillow:
            image = Image.open(photo_path)
        else:
            image = io.imread(photo_path, as_gray)

        return image

    def image_local_filepath(self, photos_dir=settings.LOCAL_PHOTOS_DIR):
        photo_path = Path(photos_dir, self.folder_name, self.photo_filename)
        if photo_path.exists():
            return photo_path
        else:
            return None

    def has_valid_source(self, photos_dir=settings.LOCAL_PHOTOS_DIR):
        photo_path = self.image_local_filepath(photos_dir=photos_dir) 
        return photo_path is not None

    @property
    def photo_file_number(self):
        return self.number*2

    @property
    def slide_file_number(self):
        return self.number*2 - 1

    @property
    def folder_name(self):
        """ returns the folder name in the format given by BHVP """
        return f'BHVP_PH_CetaitParis_DP_{self.map_square.number:04}_{self.folder:02}'

    @property
    def slide_filename(self):
        return f'BHVP_PH_CetaitParis_DP_{self.map_square.number:04}_{self.folder:02}_{self.slide_file_number:03}.jpg'

    @property
    def photo_filename(self):
        return f'BHVP_PH_CetaitParis_DP_{self.map_square.number:04}_{self.folder:02}_{self.photo_file_number:03}.jpg'

    def get_photo_url(self):
        return settings.AWS_S3_PHOTOS_DIR + '/' + self.folder_name + '/' + self.photo_filename

    def get_slide_url(self):
        return settings.AWS_S3_PHOTOS_DIR + '/' + self.folder_name + '/' + self.slide_filename

    def get_photo_page_url(self):
        return f'/photo/{self.map_square.number}/{self.folder}/{self.number}/'

    class Meta:
        unique_together = ['number', 'folder', 'map_square']


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
    
    def __str__(self):
        return "Map Square " + str(self.number)

class Photographer(models.Model):
    """
    This model contains data about a single Photographer,
    which includes their name and the Map Square that this photographer was assigned to
    """
    name = models.CharField(max_length=252)
    number = models.IntegerField(null=True)
    approx_loc = models.CharField(max_length=252, null=True, blank=True)
    map_square = models.ForeignKey(MapSquare, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=252, null=True)
    sentiment = models.CharField(max_length=252, null=True)

    def __str__(self):
        return self.name + " (" + str(self.number) + ")"

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
    
    def __str__(self):
        return self.name

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
