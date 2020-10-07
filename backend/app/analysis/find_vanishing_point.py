"""

vanishing_point_finder.py

analysis to find significant lines in image and filter lines to find place where most lines
intersect, which should be the vanishing point
"""

import numpy as np
import cv2

from matplotlib import pyplot as plt
from app.models import Photo

MODEL = Photo


def analyze(photo: Photo):
    """
    Calculate the whitespace % for a given Photo
    """
    image = photo.get_image_data()
    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lines = auto_canny(grayscale_image)

    plt.subplot(122), plt.imshow(lines[0], cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()

    filter_lines = []
    for l in lines[1]:
        try:
            x1, y1, x2, y2 = l[0]
            theta = abs(np.arctan((y2 - y1) / (x2 - x1)))
            # NEED TO ALTER RANGE VALUES
            epsi = np.pi / 16
            if (x2 - x1) != 0 and abs(theta - np.pi / 2) > 2 * epsi and theta > epsi:
                cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 3, 8)
                filter_lines.append(l)
        except ZeroDivisionError:
            pass
    van_point = find_van_coord(filter_lines, image.shape[0], image.shape[1])
    print(van_point)
    scale = 10
    print(van_point[1]/scale)
    cv2.circle(image, van_point[0], 50, (255, 0, 0), 10, 8)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', image)
    # cv2.waitKey()
    return None


def auto_canny(image, sigma=0.00001):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, 150, 255, 3)
    lines = cv2.HoughLinesP(edged, 1, np.pi / 180, 80, 30, maxLineGap=250)

    # return the edged image
    return [edged, lines]


def find_van_coord(lines, x_pix=0, y_pix=0):
    step = 50
    std = {}
    for i in range(0, x_pix, step):
        for j in range(0, y_pix, step):
            for l in lines:
                x1, y1, x2, y2 = l[0]
                # standard form of the line: ax + by + c = 0
                a = (y2 - y1) / (x2 - x1) * - 1
                b = 1
                c = -y1 - a * x1
                d = abs(a * i + b * j + c) / (a ** 2 + b ** 2) ** .5
                if (i, j) in std:
                    std[(i, j)] += d
                else:
                    std[(i, j)] = d
    if len(std) != 0:
        # mean = sum(std.values())/len(std)
        # for i in std:
        #     std[i] = ((std[i] - mean)**2/len(std))**.5
        min_coord = (0, 0)
        for coord in std:
            if std[coord] <= std[min_coord]:
                min_coord = coord
        return (min_coord, std[min_coord])
    return (0, 0)
