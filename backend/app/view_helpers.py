import os
import json
import math
from collections import Counter

from django.conf import settings

from app.models import Photo, PhotoAnalysisResult


def get_map_squares_by_arondissement():
    """
    Reading list of hand-compiled json data
    for each arrondissement
    """
    json_path = os.path.join(settings.BACKEND_DATA_DIR, 'arrondissements_map_squares.json')
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_arrondissement_geojson():
    """
    Reading list of geojson data for each arrondissement
    """
    geojson_path = os.path.join(settings.BACKEND_DATA_DIR, 'arrondissements.geojson')
    with open(geojson_path, encoding='utf-8') as f:
        data = json.load(f)
    return data


def photo_tag_helper(map_square_number, folder_number, photo_number):
    photo_obj = Photo.objects.get(number=photo_number, folder=folder_number, map_square__number=map_square_number)
    analysis_obj = PhotoAnalysisResult.objects.filter(name='yolo_model', photo=photo_obj)
    if analysis_obj:
        parsed_obj = analysis_obj[0].parsed_result()
        return list(parsed_obj['labels'])
    else:
        return None


def tag_helper(tag_name, page=None):
    print('tag helper here')
    all_yolo_results = PhotoAnalysisResult.objects.filter(name='yolo_model')

    if not all_yolo_results.count():
        return []

    relevant_results = []
    print('yolo results here: ', len(all_yolo_results))
    for result in all_yolo_results:
        data = result.parsed_result()
        if tag_name in data['labels']:
            relevant_results.append(result)

    print('relevant results: ', len(relevant_results))

    # TODO(ra) Fix the results per page math... it looks like it's stepping through src
    # photo indexes
    results_per_page = 20
    result_count = len(relevant_results)
    page_count = math.ceil(result_count / results_per_page)

    if page:
        first_result = results_per_page * (page-1)
        last_result = first_result + results_per_page
        print(first_result, last_result)
        relevant_results_this_page = relevant_results[first_result:last_result]
    else:
        relevant_results_this_page = relevant_results

    print(relevant_results_this_page)

    # sort by confidence
    by_confidence = []
    for result in relevant_results_this_page:
        data = result.parsed_result()
        confidence = 0
        for box in data['boxes']:
            # an image may have several tag_name in labels, find greatest confidence
            if box['label'] == tag_name:
                confidence = max(confidence, box['confidence'])
        by_confidence.append((result, confidence))

    sorted_analysis_obj = sorted(by_confidence, key=lambda obj: obj[1], reverse=True)
    return [result[0].photo for result in sorted_analysis_obj], result_count, page_count


def get_all_yolo_tags():
    yolo_results = PhotoAnalysisResult.objects.filter(name='yolo_model')

    tag_counter = Counter()
    for result in yolo_results:
        data = result.parsed_result()
        tags = data['labels']
        tag_counter.update(tags)

    # Sort tags by frequency (highest to least)
    sorted_tags = sorted(tag_counter.items(), key=lambda x: x[1], reverse=True)

    out = [tag for tag, count in sorted_tags]

    return out


def tag_confidence(photo_obj, analysis_result, tag):
    """ given a photo object and a tag, get the maximum confidence of that tag"""
    if not analysis_result:
        return 100

    yolo_dict = analysis_result.parsed_result()

    # there might be multiple boxes labeled with this tag,
    # so pick the max confidence
    confidence = max(
        [box['confidence'] for box in yolo_dict['boxes'] if box['label'] == tag],
        default=100
    )
    return confidence
