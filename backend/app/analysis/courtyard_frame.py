import numpy as np
import cv2

from app.models import Photo

# MODEL = Photo

# from app.models import Photo, MapSquare
from pathlib import Path
from django.conf import settings

DARK_THRESHOLD = 0.2

def analyze(photo: Photo):
    """
    Determine if an image is a courtyard photo by identifying a dark frame around outer boundary
    of photo. Returns boolean.
    """
    image = photo.get_image_data()

    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(grayscale_image)
    #grayscale_image = [[0,0,0],[0,225,0],[0,0,0]] #tester image

    # Normalize image pixels to range from 0 to 1
    # Normalized values are used instead of absolute pixel values to account for
    # differences in brightness (across all photos) that may cause white areas in
    # some photos, like a piece of paper, to appear dark.
    normalized_grayscale_image = grayscale_image / np.max(grayscale_image)
    print("------------LALALALA------------")
    print(normalized_grayscale_image)

    # Montse's code
    # for top_row_pixel in normalized_grayscale_image[0]:
    #     if top_row_pixel > DARK_THRESHOLD:
    #         return False
    # for bottom_row_pixel in normalized_grayscale_image[-1]:
    #     if bottom_row_pixel > DARK_THRESHOLD:
    #         return False
    # for row in normalized_grayscale_image:
    #     if row[0] > DARK_THRESHOLD and row[-1] > DARK_THRESHOLD:
    #         return False
    # return True

    index = 0 # temp
    percent_passed = 0.9
    border_percentage = 0.005 #top and bottom 0.5% of photo
    length = len(normalized_grayscale_image[0])
    width = len(normalized_grayscale_image)
    border_num = int(border_percentage * min(length, width)) #number of pixels we want to check
    if border_num < 1:
        border_num = 1
    for pixel_top in normalized_grayscale_image[0]:
        if pixel_top > DARK_THRESHOLD:
            print("pixel_top:", pixel_top)
            return False
    for pixel_bottom in normalized_grayscale_image[-1]:
        print(index/length)
        if pixel_bottom > DARK_THRESHOLD:
            print("pixel_bottom:", pixel_bottom)
            return False
        index += 1
    for row in normalized_grayscale_image[1:len(normalized_grayscale_image)-2]:
        for pixel in range(border_num):
            if row[pixel] > DARK_THRESHOLD or row[::-1][pixel] > DARK_THRESHOLD:
                print("front pixel __ in row __:", row[pixel], row)
                print("back pixel __ in row __:", row[::-1][pixel], row)
                return False
    return True

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

