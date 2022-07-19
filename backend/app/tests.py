"""
Tests for the main app.
"""
from pathlib import Path

from django.test import TestCase
from django.conf import settings
from django.urls import reverse

import shutil
import os
import tempfile
import stat

from app.models import Photo, MapSquare, Photographer


class MainAPITests(TestCase):
    """
    Backend TestCase. API Calls
    """

    # def setUp(self):
    #     super().setUp()
    #     do any setup here

    def setUp(self):
        super().setUp()
        names = ['Bob Frenchman', 'Waddle Dee', 'Kaito KID']
        os.umask(0)
        for i in range(3):
            map_square = MapSquare.objects.create(number=i + 1, coordinates='24, 25')
            photographer = Photographer.objects.create(map_square=map_square, number=i + 1,
                                                       name=names[i])
            path = os.path.join(settings.TEST_PHOTOS_DIR, f'{i + 1}')
            os.mkdir(path, mode=0o755)
            for j in range(4):
                photo = Photo.objects.create(number=j + 1, map_square=map_square,
                                             photographer=photographer)
                with open(os.path.join(path, f'{j + 1}_photo.jpg'), 'w+') as f:
                    pass

        assert MapSquare.objects.count() == 3
        assert Photographer.objects.count() == 3
        assert Photo.objects.count() == 12
        # print(os.listdir(settings.TEST_PHOTOS_DIR))

    def tearDown(self):
        for i in range(3):
            path = os.path.join(settings.TEST_PHOTOS_DIR, f'{i + 1}', "")
            for j in range(len(os.listdir(path))):
                os.remove(os.path.join(path, f'{j + 1}_photo.jpg'))
            os.rmdir(path)

    def add_photo(self, map_square, photo_name_or_path):
        """
        Creates a Photo object and adds it to self.photo_dict given
        the name of the photo or path relative to settings.TEST_PHOTOS_DIR
        """

        if Photo.objects.exists():
            photo_number = Photo.objects.last().number + 1
        else:
            photo_number = 0

        # create new file in test directory
        directory = os.path.join(settings.TEST_PHOTOS_DIR, f'{map_square.number + 1}', "")
        current_photos_in_square = len(os.listdir(directory))
        path = os.path.join(directory, f'{current_photos_in_square + 1}_photo.jpg')
        with open(path, 'w+') as f:
            pass

        # create new entry in database
        photo = Photo(number=photo_number, map_square=map_square)

        if isinstance(photo_name_or_path, str):
            photo.front_src = True
        elif isinstance(photo_name_or_path, Path):
            photo.front_src = True

        photo.save()
        return photo

    def test_photo_functions(self):
        photo = self.add_photo(MapSquare.objects.get(number=1), 'example')
        self.assertEqual(photo.has_valid_source(), True)

        print(photo.get_image_local_filepath(src_dir=settings.TEST_PHOTOS_DIR), 'end')

    def test_get_all_photos(self):
        response = self.client.get(reverse("all_photos"))
        assert response.status_code == 200

        res = response.json()
        assert len(res) == 12
        assert res[-1]['id'] == 12

    def test_get_map_squares(self):
        # get all
        response = self.client.get(reverse('all_map_squares'))
        assert response.status_code == 200

        res = response.json()
        assert len(res) == 3
        assert res[-1]['num_photos'] == 4

        # get one
        response = self.client.get(reverse('map_square', args=[3]))
        assert response.status_code

        res2 = response.json()
        assert {key: res[-1][key] for key in res[-1].keys() if key != 'num_photos'} \
               == {key: res2[key] for key in res2.keys() if key != 'photos'}
        assert len(res2['photos']) == 4

    def test_get_one_photo(self):
        response = self.client.get(reverse("photo", args=[2, 2]))
        assert response.status_code == 200

        res = response.json()
        assert res['number'] == 2 and res['map_square_number'] == 2

    def test_get_all_tags(self):
        names = ['Bob Frenchman', 'Waddle Dee', 'Kaito KID']
        response = self.client.get(reverse('get_tags'))
        assert response.status_code == 200

        res = response.json()
        # print('BEGIN', res, 'END')
        assert 'person' and 'bicycle' and 'stop sign' in res['tags']
        assert (name in res['photographers'] for name in names)

    def test_get_photographers(self):
        names = ['Bob Frenchman', 'Waddle Dee', 'Kaito KID']
        # get all
        responseall = self.client.get(reverse('all_photographers'))
        assert responseall.status_code == 200

        resall = responseall.json()
        photographer_names = [entry['name'] for entry in resall]
        assert (name in photographer_names for name in names)
        # print(responseall.content.decode())

        # get one, try 1 2 3
        for i in (1, 2, 3):
            responseone = self.client.get(reverse('photographer', args=[i]))
            assert responseone.status_code == 200

            resone = responseone.json()
            assert len(resone['photos']) == 4

    def test_prev_next_photos(self):
        # need to decrease number of tries, currently too many
        for i in range(3):
            for j in range(4):
                response = self.client.get(reverse('previous_next_photos', args=[i + 1, j + 1]))
                assert response.status_code == 200

                res = response.json()
                assert len(res) == 2
                if (i, j) == (0, 0):
                    assert res[0] == ''

    # testing similarity/analysis functions

    def x_test_all_analyses(self):
        response = self.client.get(reverse('all_analyses'))
        assert response.status_code == 200
        print(response.json())

    def x_test_similarity(self):
        # all photos
        response = self.client.get(reverse('all_photos_in_order'))
        assert response.status_code == 200

        res = (response.json())
        assert len(res) == 12







