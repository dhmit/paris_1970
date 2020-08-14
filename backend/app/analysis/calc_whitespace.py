"""

calc_whitespace.py - analysis to calculate ratio of pixels above a certain threshold value (0.6)
to the size of the image

"""
import unittest
import os
import time
from skimage import io
import numpy as np
import cv2
from app.models import Photo
from app.google_api import load_creds, callback
from googleapiclient.discovery import build
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
from django.conf import settings

from google import auth
from oauth2client.client import OAuth2Credentials

from app.google_api import SCOPES

def analysis() -> dict:
    # creds = load_creds(['https://www.googleapis.com/auth/drive'])
    creds = GoogleCredentials.from_json(settings.GOOGLE_API_CREDENTIALS_FILE)
    drive_service = build('drive', 'v3', credentials=creds)
    PROJECT = 'paris-1970'
    request = drive_service.instances().list(project=PROJECT)
    response = request.execute()

    print(response)

    file_id = '1zbeULibx8nZkhRlBkslso7M0lOVudKQH'

    # print(type(drive_service))
    # print(drive_service.permissions)

    batch = drive_service.new_batch_http_request(callback=callback)
    domain_permission = {
        'type': 'domain',
        'role': 'reader',
        'domain': '127.0.0.1'
    }
    batch.add(drive_service.permissions().create(
        fileId=file_id,
        body=domain_permission,
        fields='id',
    ))
    batch = creds.authorize(batch)
    batch.execute()
    print(batch)
    return {}


def analysisfd() -> dict:
    result = {}
    for photo in Photo.objects.all():
        photo_srcs = {'front_src': photo.front_src, 'back_src': photo.back_src,
                      'binder_src': photo.binder_src}
        new_attributes = {}
        for side in ['front', 'back', 'binder']:
            try:
                url = photo_srcs[side + '_src']
                print(url)

                # Get image, will raise ValueError if src url is ''
                # will raise FileNotFound error if src is just a filename
                image = io.imread(url)

                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                normalized_gray_image = gray_image / np.max(gray_image)
                number_of_pixels = (normalized_gray_image > .6).sum()
                white_space_ratio = number_of_pixels / gray_image.size
                new_attributes[f'white_space_ratio_{side}'] = white_space_ratio
                print(f'Successfully calculated whitespace ratio for photo {photo.id} {side}')
            except (ValueError, FileNotFoundError):
                pass
        result[photo.id] = new_attributes
    return result


class TestSampleAnalysis(unittest.TestCase):
    """
    Test cases to make sure things are running properly
    """

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()  # run the tests
