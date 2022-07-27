"""
Tests for the main app.
"""
from pathlib import Path

from django.test import TestCase
from django.conf import settings
from django.urls import reverse

import os
import json

from app.models import Photo, PhotoAnalysisResult, MapSquare, Photographer, Cluster, \
    CorpusAnalysisResult
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
        for i in range(3):
            map_square = MapSquare.objects.create(number=i + 1, coordinates="24, 25")
            photographer = Photographer.objects.create(map_square=map_square, number=i + 1,
                                                       name=names[i])
            path = os.path.join(settings.TEST_PHOTOS_DIR, f"{i + 1}")
            os.mkdir(path, mode=0o755)
            # in each map square, create 4 empty photos and some PhotoAnalysisResult
            # objects for each photo, and add photo to either cluster 0 or 1 (photo_number mod 2)
            for j in range(4):
                photo = Photo.objects.create(number=j + 1, map_square=map_square,
                                             photographer=photographer, front_src=True)

                with open(os.path.join(path, f"{j + 1}_photo.jpg"), "w+") as f:
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
                Cluster.objects.get(label=j % 2).photos.add(photo)
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

    def initTest(self, name, args=[]):
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
        current_photos_in_square = len(os.listdir(directory))
        path = os.path.join(directory, f"{current_photos_in_square + 1}_photo.jpg")
        with open(path, "w+") as f:
            pass

        # create new Photo object in database as well as a few PhotoAnalysisResult objects
        photo = Photo(number=photo_number, map_square=map_square, front_src=True)
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

        self.assertEqual(photo.has_valid_source(), True)

        for photo in Photo.objects.all():
            self.assertEqual(photo.has_valid_source(), True)

    def test_get_all_photos(self):
        res = self.initTest("all_photos")
        assert len(res) == 12
        assert res[-1]["id"] == 12

    def test_get_map_squares(self):
        # get all
        res = self.initTest("all_map_squares")
        assert len(res) == 3
        assert res[-1]["num_photos"] == 4

        # get one
        res2 = self.initTest("map_square", args=[3])
        assert {key: res[-1][key] for key in res[-1].keys() if key != "num_photos"} \
               == {key: res2[key] for key in res2.keys() if key != "photos"}
        assert len(res2["photos"]) == 4

    def test_get_one_photo(self):
        res = self.initTest("photo", args=[2, 2])
        assert res["number"] == 2 and res["map_square_number"] == 2

    def test_get_all_tags(self):
        names = ["Bob Frenchman", "Waddle Dee", "Kaito KID"]
        res = self.initTest("get_tags")
        assert "person" and "bicycle" and "stop sign" in res["tags"]
        assert (name in res["photographers"] for name in names)

    def test_get_photographers(self):
        names = ["Bob Frenchman", "Waddle Dee", "Kaito KID"]
        # get all
        resall = self.initTest("all_photographers")
        photographer_names = [entry["name"] for entry in resall]
        assert (name in photographer_names for name in names)

        # get one, try 1 2 3
        for i in (1, 2, 3):
            resone = self.initTest("photographer", args=[i])
            assert len(resone["photos"]) == 4

    def test_prev_next_photos(self):
        # need to decrease number of tries, currently too many
        photo = self.add_photo(MapSquare.objects.get(number=1), "example")
        self.assertEqual(photo.has_valid_source(), True)

        for i in range(3):
            for j in range(4):
                res = self.initTest("previous_next_photos", args=[i + 1, j + 1])
                assert len(res) == 2
                if (i, j) == (0, 0):
                    assert res[0] == ""

    def test_get_arrondissement(self):
        # change num_arrondisements to be the number of arrond in the database as necessary
        num_arrondissements = 2

        # get all
        res = self.initTest("get_arrondissement")
        assert len(res) == num_arrondissements

        # get each
        for i in range(num_arrondissements):
            res = self.initTest("get_one_arrondissement", args=[i + 1])
            assert len(res) == 2

    def test_cluster(self):
        # test that both clusters return photos that were initially added to to them
        res = self.initTest("clustering", args=[2, 0])
        assert len(res) == 6
        assert (photo['number'] % 2 == 0 for photo in res)

        res = self.initTest("clustering", args=[2, 1])
        assert len(res) == 6
        assert (photo['number'] % 2 == 0 for photo in res)

    def test_search(self):
        def one_search(keyword, isAdvanced=False, data={}):
            if data == {}:
                data = {
                    "keyword": keyword,
                    "isAdvanced": isAdvanced
                }
            response = self.client.post(reverse("search"), json.dumps(data),
                                        content_type="application/json")
            assert response.status_code == 200
            return response.json()

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
        res = self.initTest("all_analyses")
        assert all(analysis in res for analysis in ["yolo_model", "resnet18_cosine_similarity",
                                                    "photo_similarity.resnet18_cosine_similarity"])

    def test_get_photos_by_analysis(self):
        # just analysis
        res = self.initTest("get_photos_by_analysis", args=["yolo_model"])
        assert len(res) == 12

        # analysis and object
        # TODO: FIGURE OUT IF THIS IS INTENTIONAL OR NOT: when specifiying object in this api
        #  call, for the yolo model at least, it doesn't take actual objects bc that's one more
        #  layer into the dictionary, instead takes keys 'boxes' or 'labels'
        res = self.initTest("get_photos_by_analysis", args=["yolo_model", "boxes"])
        assert len(res) == 12

    def test_get_corpus_analysis(self):
        res = self.initTest("get_corpus")
        assert len(res) == 1

    def test_similarity(self):
        # all photos by map square, retrieved by resnet18_cosine_similarity
        res = self.initTest("all_photos_in_order")
        assert len(res) == 12

    def test_similar_photos(self):
        # supposed to pull top 10 similar photos from list saved in "photo_similarity
        # .resnet18_cosine_similarity" PhotoAnalysisObject for given photo. Here, returns an
        # empty list since aforementioned object is empty
        res = self.initTest("similar_photos", args=[1, 1, 10])
        assert res == []
