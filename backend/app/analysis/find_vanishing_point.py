"""

find_vanishing_point.py

analysis to find significant lines in image and filter lines to find place where most lines
intersect, which should be the vanishing point
"""

import numpy as np
import cv2

from app.models import Photo


def analyze(photo: Photo):
    """
    Given a photo, returns the coordinate of the vanishing point,
    where the vanishing point is the point that has the minimum sum of
    distances to all detected lines in the photo
    """
    image = photo.get_image_data()
    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lines = auto_canny(grayscale_image)

    filter_lines = []
    # Filters out vertical and horizontal lines
    for line in lines[1]:
        point_1_x, point_1_y, point_2_x, point_2_y = line[0]

        # if line is not horizontal
        if point_2_x != point_1_x:
            # find angle of line from horizontal
            theta = abs(np.arctan((point_2_y - point_1_y) / (point_2_x - point_1_x)))

            # only add line into filter_lines if the angle is NOT within epsilon of
            # horizontal/vertical
            epsilon = np.pi / 16
            if (
                abs(theta - np.pi / 2) > 2 * epsilon
                and theta > epsilon
            ):
                filter_lines.append({
                    '1_x': int(point_1_x),
                    '1_y': int(point_1_y),
                    '2_x': int(point_2_x),
                    '2_y': int(point_2_y),
                })

        else:
            pass

    van_point = find_van_coord_intersections(filter_lines)

    return {
        'vanishing_point_coord': van_point,
        'line_coords': filter_lines,
    }


def auto_canny(image):
    """
    Applies the Canny and HoughLinesP functions from OpenCV to the given
    image and returns the result

    :param image: an image
    :return: a list containing the binary image from Canny and the set of
             lines from HoughLinesP

    TODO: Optimize parameters for Canny and HoughLinesP instead of hard-coding them
    """

    edged = cv2.Canny(image, 150, 255, 3)
    lines = cv2.HoughLinesP(edged, 1, np.pi / 180, 80, 30, maxLineGap=100)

    # return the edges and lines
    return [edged, lines]


def find_van_coord_intersections(lines):
    """
    Find the approximate vanishing point of the image by choosing the most representative point
    from the largest cluster of intersections between lines in 'lines'
    :param lines: list of lists containing start and end points of all filtered lines
    :return: the average coordinate of the largest cluster of intersections
    """
    intersections = {}
    max_line_amount = 300
    distance_tolerance = 30
    # return None if the image likely has many unnecessary lines (e.g. if there's a tree)
    # or if the image has less than 2 lines
    if len(lines) > max_line_amount or len(lines) < 2:
        return None

    # For each pair of lines, finds the intersection and checks to see if it's within the tolerance
    # from an existing intersection. If so, adds the intersection to the corresponding cluster,
    # else creates a new cluster.
    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            intersection = find_intersection_between_two_lines((lines[i], lines[j]))
            if intersection is not None:
                found = False
                for coord, current_intersection in intersections.items():
                    # finds distance between current intersection and past intersections
                    distance = ((intersection[0] - coord[0]) ** 2 + (intersection[1] - coord[1]) **
                                2) ** (1
                                                                                                / 2)
                    if distance < distance_tolerance:
                        current_intersection.append(intersection)
                        found = True
                if not found:
                    intersections[intersection] = [intersection]
    max_frequency = 0
    van_point_list = []

    # finds the largest cluster of intersections
    for coord, intersection in intersections.items():
        if len(intersection) > max_frequency:
            max_frequency = len(intersection)
            van_point_list = intersection

    if max_frequency == 0:
        return None
    sum_point = [0, 0]

    # finds the average of all coordinates in the largest cluster
    for point in van_point_list:
        sum_point[0] += point[0]
        sum_point[1] += point[1]

    sum_point[0] = round(sum_point[0] / max_frequency)
    sum_point[1] = round(sum_point[1] / max_frequency)

    return {
        'x': sum_point[0],
        'y': sum_point[1],
    }


def find_intersection_between_two_lines(lines):
    """
    Determines the coordinates of the intersection between two lines, or None if no intersection
    :param lines: contains a tuple of two lines where:
        lines[0]: 4-elem list x1, y1, x2, y2 -> starting and ending coordinates of line 1
        lines[1]: 4-elem list x1, y1, x2, y2 -> starting and ending coordinates of line 2
    :return: coordinates of intersection point on image or None if does not exist or lines parallel
    """
    # coords for line 1
    line1_x_coord_1 = lines[0]["1_x"]
    line1_y_coord_1 = lines[0]["1_y"]
    line1_x_coord_2 = lines[0]["2_x"]
    line1_y_coord_2 = lines[0]["2_y"]

    # coords for line 2
    line2_x_coord_1 = lines[1]["1_x"]
    line2_y_coord_1 = lines[1]["1_y"]
    line2_x_coord_2 = lines[1]["2_x"]
    line2_y_coord_2 = lines[1]["2_y"]

    # standard form of the line: ax + by + c = 0

    x1_coefficient = (line1_y_coord_2 - line1_y_coord_1) / (line1_x_coord_2 - line1_x_coord_1) * -1
    x2_coefficient = (line2_y_coord_2 - line2_y_coord_1) / (line2_x_coord_2 - line2_x_coord_1) * -1

    if x1_coefficient == x2_coefficient:
        return None

    standard_form_constant1 = -line1_y_coord_1 - x1_coefficient * line1_x_coord_1
    standard_form_constant2 = -line2_y_coord_1 - x2_coefficient * line2_x_coord_1

    intersection_x = (standard_form_constant2 - standard_form_constant1) \
        / (x1_coefficient - x2_coefficient)
    intersection_y = -x1_coefficient * intersection_x - standard_form_constant1

    return intersection_x, intersection_y

# THESE ARE UNUSED FUNCTIONS THAT MIGHT BE HELPFUL FOR FUTURE PROJECTS #

# def find_van_coord(lines, x_pix=0, y_pix=0):
#     """
#     Given a filtered list of significant lines and the dimensions of the image,
#     finds the point that is closest to all lines on average.
#
#     :param lines: list of significant lines
#     :param x_pix: width of the image
#     :param y_pix: height of the image
#     :return: tuple with: index 0 = vanishing point coordinates
#                          index 1 = sum of distances from VP to all lines
#     TODO: If there is no vanishing point within the photo, return None or "offscreen"
#     TODO: Change method/metric used to find vanishing point to improve accuracy
#     """
#     step = int(y_pix/10)
#     coords_to_dists_from_lines = {}
#
#     # Iterate through pixels in image by step amount,
#     # store total distance from each pixel to all lines detected in image
#     # in coords_to_dists_from_lines dict
#     for i in range(0, x_pix, step):
#         for j in range(0, y_pix, step):
#             for line in lines:
#                 distance_from_coord_to_line = find_dist_from_point_to_line(i, j, line)
#                 # add or update distance from this point to line
#                 if (i, j) in coords_to_dists_from_lines:
#                     coords_to_dists_from_lines[(i, j)] += distance_from_coord_to_line
#                 else:
#                     coords_to_dists_from_lines[(i, j)] = distance_from_coord_to_line
#     if len(coords_to_dists_from_lines) != 0:
#         min_coord = (0, 0)
#         for coord in coords_to_dists_from_lines: # find coord with minimum distance sum to lines
#             if coords_to_dists_from_lines[coord] <= coords_to_dists_from_lines[min_coord]:
#                 # will always include (0,0) so no key errors
#                 min_coord = coord
#         return (min_coord, coords_to_dists_from_lines[min_coord])
#     return (0, 0), 0

# def find_dist_from_point_to_line(xcoord, ycoord, line):
#     """
#     Find distance from point with (xcoord, ycoord) to a line
#     :param xcoord: x-coordinate of point
#     :param ycoord: y-coordinate of point
#     :param line: line defined by (x1,y1),(x2,y2)
#     :return: shortest distance from point with given coords to line
#     """
#     line_x_coord_1, line_y_coord_1, line_x_coord_2, line_y_coord_2 = line[0]
#     # standard form of the line: ax + by + c = 0
#     x_coeff = (line_y_coord_2 - line_y_coord_1) / (line_x_coord_2 - line_x_coord_1) * \
#               - 1
#     standard_form_constant = -line_y_coord_1 - x_coeff * line_x_coord_1
#     return abs(x_coeff * xcoord + ycoord + standard_form_constant) / (x_coeff ** 2 + 1 ** 2) ** .5
