"""
combined_indoor.py - analysis to determine if an image was taken indoors
or outdoors

:return: boolean, True if the photo is indoors, False otherwise
"""

from app.models import Photo
from app.analysis.indoor_analysis import courtyard_frame, find_windows, gradient_analysis


def analyze(photo: Photo):
    """
    Determine if a given image was taken indoors
    """
    windows_present = find_windows.analyze(photo)
    sky_detected = gradient_analysis.analyze(photo)
    has_courtyard_frame = courtyard_frame.analyze(photo)

    # image is considered taken indoors if two out of the three functions
    # find the image to have indoor elements
    return (not windows_present and not sky_detected) \
        or (not windows_present and has_courtyard_frame) \
        or (not sky_detected and has_courtyard_frame)
