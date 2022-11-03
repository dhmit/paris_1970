"""
Tests for the main app.
"""


# pylint: skip-file

"""
NOTE(Ryaan 2022-08-30):
    These tests need some cleanup but for now we're skipping pylint tests on them
    until someone can get in and give them a good scrub.
"""

from pathlib import Path

from django.test import TestCase
from django.conf import settings
from django.urls import reverse

import os
import json

from app.models import Photo, PhotoAnalysisResult, MapSquare, Photographer, Cluster, CorpusAnalysisResult
from app.analysis import yolo_model
from app.analysis.photo_similarity import resnet18_cosine_similarity, resnet18_feature_vectors


class MainAPITests(TestCase):
    """
    Backend TestCase. API Calls
    """

    def setUp(self):
        """
        Create dummy database entries and corresponding files in TEST_PHOTOS_DIR
        """
        names = ["Bob Frenchman", "Waddle Dee", "Kaito KID"]

        # create 2 clusters, 1 CorpusAnalysisResult object
        Cluster.objects.create(model_n=2, label=0)
        Cluster.objects.create(model_n=2, label=1)
        CorpusAnalysisResult.objects.create(name="corpus_analysis_result", result=json.dumps(''))

        # create 3 map squares
        for i in range(1, 4):
            map_square = MapSquare.objects.create(number=i, coordinates="24, 25")
            photographer = Photographer.objects.create(map_square=map_square, number=i,
                                                       name=names[i-1], approx_loc="Popstar")
            test_photos_dir = Path(settings.TEST_PHOTOS_DIR, str(i))
            Path(test_photos_dir).mkdir(exist_ok=True, mode=0o755)

            # in each map square, create 4 empty photos and some PhotoAnalysisResult
            # objects for each photo, and add photo to either cluster 0 or 1 (photo_number mod 2)
            for photo_num in range(1, 5):
                photo = Photo.objects.create(
                        number=photo_num,
                        folder=1,
                        map_square=map_square,
                        photographer=photographer
                        )

                photo_path = Path(test_photos_dir, f"{photo_num}_photo.jpg")
                with open(photo_path, "w+") as f:
                    pass

                yolo_result = {"boxes": [{"label": "car", "x_coord": 710, "y_coord": 645,
                                          "width": 135, "height": 82, "confidence": 90}],
                               "labels": {"car": 1}}

                PhotoAnalysisResult.objects.create(name="yolo_model", result=json.dumps(
                    yolo_result), photo=photo)
                PhotoAnalysisResult.objects.create(name="resnet18_cosine_similarity", result=
                json.dumps([]),
                                                   photo=photo)
                PhotoAnalysisResult.objects.create(name="photo_similarity.resnet18_cosine_"
                                                        "similarity", result=json.dumps([]),
                                                   photo=photo)
                Cluster.objects.get(label=photo_num % 2).photos.add(photo)
        assert MapSquare.objects.count() == 3
        assert Photographer.objects.count() == 3
        assert Photo.objects.count() == 12

    def tearDown(self):
        """
        Remove TEST_PHOTOS_DIR files.
        """
        for i in range(3):
            path = os.path.join(settings.TEST_PHOTOS_DIR, f"{i + 1}", "")
            for j in range(len(os.listdir(path))):
                os.remove(os.path.join(path, f"{j + 1}_photo.jpg"))
            os.rmdir(path)

    def _test_get_api_endpoint(self, name, args=[]):
        """
        Performs basic GET api call for given parameters and,
        after checking for success, returns json() version of the response
        :param name: str
        :param args: list of arguments for the call
        :return:
        """
        response = self.client.get(reverse(name, args=args))
        assert response.status_code == 200
        return response.json()

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
        directory = os.path.join(settings.TEST_PHOTOS_DIR, f"{map_square.number}", "")
        os.makedirs(directory, exist_ok=True)
        current_photos_in_square = len(os.listdir(directory))
        path = os.path.join(directory, f"{current_photos_in_square + 1}_photo.jpg")
        fp = open(path, "x")
        fp.close()
        assert os.path.exists(path)

        # create new Photo object in database as well as a few PhotoAnalysisResult objects
        photo = Photo(number=photo_number, folder=1, map_square=map_square)
        photo.save()

        PhotoAnalysisResult.objects.create(name="yolo_model", result=json.dumps({"boxes": [],
                                                                                 "labels": {}}),
                                           photo=photo)
        PhotoAnalysisResult.objects.create(name="resnet18_cosine_similarity", result=
        json.dumps([]), photo=photo)
        PhotoAnalysisResult.objects.create(name="photo_similarity.resnet18_cosine_similarity",
                                           result=json.dumps([]), photo=photo)
        Cluster.objects.get(label=photo_number % 2).photos.add(photo)
        return photo

    # testing database retrieval

    def test_photo_functions(self):
        photo = self.add_photo(MapSquare.objects.get(number=1), "example")
        self.assertTrue(photo.has_valid_source(photo_dir=settings.TEST_PHOTOS_DIR))

        for photo in Photo.objects.all():
            self.assertTrue(photo.has_valid_source(photo_dir=settings.TEST_PHOTOS_DIR))

    def test_get_all_photos(self):
        res = self._test_get_api_endpoint("all_photos")
        assert len(res) == 12
        assert res[-1]["id"] == 12

    def test_get_map_squares(self):
        # get all
        all_map_squares_res = self._test_get_api_endpoint("all_map_squares")
        assert len(all_map_squares_res) == 3
        assert all_map_squares_res[-1]["num_photos"] == 4

        # get one
        res2 = self._test_get_api_endpoint("map_square", args=[3])


        # check that getting all map squares and getting one map square returns the same list of keys,
        # except those that we remove below that we expect to be different
        all_map_squares_keys = list(all_map_squares_res[-1].keys())
        single_map_square_keys = list(res2.keys())

        all_map_squares_keys.remove('num_photos')
        single_map_square_keys.remove('photos')
        single_map_square_keys.remove('photographers')

        assert all_map_squares_keys == single_map_square_keys
        assert len(res2["photos"]) == 4

    def test_get_one_photo(self):
        map_square_num = 2
        folder_num = 1
        photo_num = 2
        res = self._test_get_api_endpoint("photo", args=[map_square_num, folder_num, photo_num])
        assert res["number"] == photo_num
        assert res["map_square_number"] == map_square_num 
        assert res["folder"] == folder_num

    def x_test_get_all_tags(self):
        names = ["Bob Frenchman", "Waddle Dee", "Kaito KID"]
        res = self._test_get_api_endpoint("get_tags")
        assert "person" and "bicycle" and "stop sign" in res["tags"]
        assert (name in res["photographers"] for name in names)

    def test_get_photographers(self):
        names = ["Bob Frenchman", "Waddle Dee", "Kaito KID"]
        # get all
        resall = self._test_get_api_endpoint("all_photographers")
        photographer_names = [entry["name"] for entry in resall]
        assert (name in photographer_names for name in names)

        # get one, try 1 2 3
        for i in (1, 2, 3):
            resone = self._test_get_api_endpoint("photographer", args=[i])
            assert len(resone["photos"]) == 4
            assert resone["approx_loc"] == "Popstar"

    def test_prev_next_photos(self):
        # need to decrease number of tries, currently too many
        photo = self.add_photo(MapSquare.objects.get(number=1), "example")
        self.assertTrue(photo.has_valid_source(photo_dir=settings.TEST_PHOTOS_DIR))

        for map_square_num in range(1, 4):
            for photo_num in range(1, 5):
                res = self._test_get_api_endpoint("previous_next_photos", args=[map_square_num, 1, photo_num])
                assert len(res) == 2
                if (map_square_num, photo_num) == (1, 1):
                    assert res[0] == ""

    def test_get_arrondissement(self):
        # change num_arrondisements to be the number of arrond in the database as necessary
        num_arrondissements = 2

        # get all
        res = self._test_get_api_endpoint("get_arrondissement")
        assert len(res) == num_arrondissements

        # get each
        for i in range(1, num_arrondissements + 1):
            res = self._test_get_api_endpoint("get_one_arrondissement", args=[i])
            assert len(res) == 2

    def test_cluster(self):
        # test that both clusters return photos that were initially added to to them
        res = self._test_get_api_endpoint("clustering", args=[2, 0])
        assert len(res) == 6
        assert (photo['number'] % 2 == 0 for photo in res)

        res = self._test_get_api_endpoint("clustering", args=[2, 1])
        assert len(res) == 6
        assert (photo['number'] % 2 == 0 for photo in res)

    def x_test_search(self):
        def one_search(keyword, isAdvanced=False, data={}):
            if data == {}:
                data = {
                    "keywords": keyword,
                    "isAdvanced": isAdvanced
                }
            url = "/api/search?query={}".format(json.dumps(data))
            response = self.client.get(url, content_type="application/json")
            assert response.status_code == 200
            # return response.json()

        res = one_search(keyword="Bob Frenchman")
        assert len(res) == 4

        res = one_search(keyword="Waddle Bob")
        assert len(res) == 0

        res = one_search(keyword="car")
        assert len(res) == 12

        data = {"photographerName": "Bob Frenchman", 'photographerId': '1', 'caption': '',
                'tags': ['car'], 'analysisTags': ['yolo_model'], 'sliderSearchValues':
                    {'Object Detection Confidence': (0, 100)}, 'isAdvanced': True}
        res = one_search(None, True, data)
        assert len(res) == 4

    # testing similarity/analysis functions

    def test_all_analyses(self):
        res = self._test_get_api_endpoint("all_analyses")
        assert all(analysis in res for analysis in ["yolo_model", "resnet18_cosine_similarity",
                                                    "photo_similarity.resnet18_cosine_similarity"])

    def test_get_photos_by_analysis(self):
        # just analysis
        res = self._test_get_api_endpoint("get_photos_by_analysis", args=["yolo_model"])
        assert len(res) == 12

        # analysis and object
        # TODO: FIGURE OUT IF THIS IS INTENTIONAL OR NOT: when specifiying object in this api
        #  call, for the yolo model at least, it doesn't take actual objects bc that's one more
        #  layer into the dictionary, instead takes keys 'boxes' or 'labels'
        res = self._test_get_api_endpoint("get_photos_by_analysis", args=["yolo_model", "boxes"])
        assert len(res) == 12

    def test_get_corpus_analysis(self):
        res = self._test_get_api_endpoint("get_corpus")
        assert len(res) == 1

    def test_similarity(self):
        # all photos by map square, retrieved by resnet18_cosine_similarity
        res = self._test_get_api_endpoint("all_photos_in_order")
        assert len(res) == 12

    def test_similar_photos(self):
        # supposed to pull top 10 similar photos from list saved in "photo_similarity
        # .resnet18_cosine_similarity" PhotoAnalysisObject for given photo. Here, returns an
        # empty list since aforementioned object is empty
        res = self._test_get_api_endpoint("similar_photos", args=[1, 1, 1, 10])
        assert res == []
