import numpy as np
import cv2

from app.models import Photo, MapSquare
from pathlib import Path
from django.conf import settings

def analyze(photo: Photo):
    """
    Determine if an image is a courtyard photo by identifying a dark frame around outer boundary
    of photo. Returns boolean.
    """
    image = photo.get_image_data()
    print("This is working")
    return image


map_square = MapSquare()
map_square.save()


photo_0 = Photo(number=1, map_square=map_square)
test_photo_path = Path(settings.TEST_PHOTOS_DIR, '100x100_500px-white_500px-black.jpg')
photo_0.front_local_path = test_photo_path
photo_0.save()

photo_1 = Photo(number=2, map_square=map_square)
photo_1.save()

print(analyze(photo_0))
print("This is working! I can print!")
