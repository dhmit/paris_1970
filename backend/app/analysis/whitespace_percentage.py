"""

calc_whitespace.py - analysis to calculate ratio of pixels above a certain threshold value (0.6)
to the size of the image

"""

from urllib.error import HTTPError
from http.client import RemoteDisconnected
from textwrap import dedent

from skimage import io
import numpy as np
import cv2

from app.models import Photo

MODEL = Photo

WHITESPACE_THRESHOLD = .6


def analyze(photo: Photo):
    """
    Calculates the whitespace for all sides of the photos in the database

    :returns A dictionary of photo ids with values of { model fields: updated values } to be
    assigned to photo instances
    """
    # Calculate the whitespace % for each photo
    # If src is blank or not a url, then the ratio will not be calculated
    if photo.front_src:
        url = photo.front_src
    elif photo.binder_src:
        url = photo.binder_src
    else:
        print(f'Photo with id {photo.id} has no front or binder src')
        return None

    try:
        # Get the image from the source url:
        # Will raise ValueError if src url is '' (No image source for side)
        # Will raise FileNotFound error if src is just a filename rather than a url
        # (imread will attempt to load the file from the current working directory)
        image = io.imread(url)

        # Convert image to grayscale
        # (Changes image array shape from (height, width, 3) to (height, width))
        # (Pixels (image[h][w]) will be a value from 0 to 255)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Normalize image pixels to range from 0 to 1
        # Normalized values are used instead of absolute pixel values to account for
        # differences in brightness (across all photos) that may cause white areas in
        # some photos, like a piece of paper, to appear dark.
        normalized_gray_image = gray_image / np.max(gray_image)

        # Count number of pixels that have a value greater than the WHITESPACE_THRESHOLD
        # n.b. this threshold was arbitrarily chosen
        # (uses numpy broadcasting and creates an array of boolean values (0 and 1))
        number_of_pixels = (normalized_gray_image > WHITESPACE_THRESHOLD).sum()

        # Percentage of pixels above the threshold to the total number of pixels in the photo
        # (Prevent larger images from being ranked as being composed mostly of whitespace,
        # just because they are larger)
        whitespace_percentage = number_of_pixels / gray_image.size * 100

        return whitespace_percentage

    except (ValueError, FileNotFoundError):
        pass

    except (HTTPError, RemoteDisconnected) as base_exception:
        raise Exception(dedent(f'''
            *** Right now, the analysis breaks after too many http requests, so it may not
            calculate whitespace for all the photos, even the first time. If it stops
            working, you will have to wait a while before it is successfully able to make
            requests again. ***
            ''')) from base_exception
