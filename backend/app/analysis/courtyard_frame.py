import numpy as np
import cv2

from app.models import Photo

# MODEL = Photo

# from app.models import Photo, MapSquare
from pathlib import Path
from django.conf import settings

DARK_THRESHOLD = .3

def analyze(photo: Photo):
    """
    Determine if an image is a courtyard photo by identifying a dark frame around outer boundary
    of photo. Returns boolean.
    """
    image = photo.get_image_data()
    print("image", image)

    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("grayscale", grayscale_image)

    # Normalize image pixels to range from 0 to 1
    # Normalized values are used instead of absolute pixel values to account for
    # differences in brightness (across all photos) that may cause white areas in
    # some photos, like a piece of paper, to appear dark.
    normalized_grayscale_image = grayscale_image / np.max(grayscale_image)
    print("normalized", normalized_grayscale_image)

    for top_row_pixel in normalized_grayscale_image[0]:
        if top_row_pixel > DARK_THRESHOLD:
            return False
    for bottom_row_pixel in normalized_grayscale_image[-1]:
        if bottom_row_pixel > DARK_THRESHOLD:
            return False
    for row in normalized_grayscale_image:
        if row[0] > DARK_THRESHOLD and row[-1] > DARK_THRESHOLD:
            return False
    return True
    # Count number of pixels that have a value greater than the WHITESPACE_THRESHOLD
    # n.b. this threshold was arbitrarily chosen
    # (uses numpy broadcasting and creates an array of boolean values (0 and 1))
    number_of_pixels = (normalized_grayscale_image < DARK_THRESHOLD).sum()

    # Percentage of pixels above the threshold to the total number of pixels in the photo
    # (Prevent larger images from being ranked as being composed mostly of whitespace,
    # just because they are larger)

    dark_percentage = number_of_pixels / grayscale_image.size * 100

    return dark_percentage


# map_square = MapSquare()
# map_square.save()
#
# photo_0 = Photo(number=1, map_square=map_square)
# test_photo_path = Path(settings.TEST_PHOTOS_DIR, '100x100_500px-white_500px-black.jpg')
# photo_0.front_local_path = test_photo_path
# photo_0.save()
#
# photo_1 = Photo(number=2, map_square=map_square)
# photo_1.save()
#
# print(analyze(photo_0))
print("This is working! I can print!")

