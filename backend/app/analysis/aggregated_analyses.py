"""
Module to aggregate analysis results for photos
"""

import os

from functools import reduce
from app.models import PhotoAnalysisResult

from django.conf import settings

CLASS_NAMES_DIR = os.path.join(settings.YOLO_DIR, 'coco.names')
with open(CLASS_NAMES_DIR, "r") as file:
    CLASS_NAMES = [line.strip() for line in file.readlines()]


def statistics_analysis(analysis_name, stat_func, photo_filter=lambda i, photo: True):
    """

    :param analysis_name:
    :param stat_func:
    :param photo_filter:
    :return:
    """

    analysis_result_objects = PhotoAnalysisResult.objects.filter(name=analysis_name)
    if not analysis_result_objects:
        raise Exception(f'Analysis "{analysis_name}" has not been run or does not exist.')

    analysis_results = [
        result_object.parsed_result()
        for i, result_object in enumerate(analysis_result_objects)
        if photo_filter(i, result_object.photo)
    ]

    return stat_func(analysis_results)


# def yolo_labels(yolo_dict):
#     yield from yolo_dict.get("labels", {})


# example
def frequent_objects(num=None):
    """
    *Args {
            dictionaries -> list: list of dictionaries of a set photos
            num -> int: requested number of common objects
          }

    return a list of /num/ common objects in those photos
    """

    def run(dictionaries):
        nonlocal num
        result = {}

        # create a dictionary to map objects to
        # number of times it appears in photos
        for photo_dictionary in dictionaries:
            for obj in photo_dictionary.get("labels", {}):
                result.setdefault(obj, 0)
                result[obj] = + 1

        # Group by quantity
        quantity_groups = {}
        for label, quantity in result.items():
            quantity_groups.setdefault(quantity, [])
            quantity_groups[quantity].append(label)

        # get a list of reversed sorted values
        # sorted_values = sorted(quantity_groups, key=lambda label: result[label],
        #                        reverse=True)
        result_labels = []
        if num is None:
            num = len(result)

        for quantity in sorted(quantity_groups, reverse=True):
            if len(result_labels) == num:
                break
            result_labels += quantity_groups[quantity]

        return result_labels

    return run


def objects_in_common():
    def run(yolo_dicts):
        objects = set(CLASS_NAMES)
        quantities = {}
        for yolo_dict in yolo_dicts:
            yolo_labels = yolo_dict.get('labels', {})
            objects &= set(yolo_labels)
            # Increase quantity for objects in common
            for label in objects:
                quantities.setdefault(label, 0)
                quantities[label] += yolo_labels[label]
        return sorted(objects, key=lambda obj_label: quantities[obj_label], reverse=True)

    return run


def object_percentage(object_labels, any_objects=True):

    if type(object_labels) is str:
        object_labels = [object_labels]

    def run(yolo_dicts):
        nonlocal object_labels

        matches = 0
        for yolo_dict in yolo_dicts:
            objects = set(yolo_dict.get('labels', {}))
            common = objects & set(object_labels)

            matches += (
                (any_objects and len(common) > 0) or
                (not any_objects and len(common) == len(object_labels))
            )

        return round(100 * matches / len(yolo_dicts), 2)

    return run


def max_object_density(object_name):
    def run(yolo_dicts):
        densities = [object_density(object_name, yolo_dict) for yolo_dict in yolo_dicts]
        return max(densities)

    return run


def person_density_calc(photo):
    return object_density("person", PhotoAnalysisResult.objects.filter(
        name="yolo_model", photo=photo
    ).first().parsed_result())
