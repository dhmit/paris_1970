import numpy as np
import cv2

from app.models import Photo

MODEL = Photo

from app.models import Photo

def analyze(photo: Photo):
    """
    Determine if an image is a courtyard photo by identifying a dark frame around outer boundary
    of photo. Returns boolean.
    """
    image = photo.get_image_data()

    # Convert image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalize image pixels to range from 0 to 1
    normalized_grayscale_image = grayscale_image / np.max(grayscale_image)

    # Montse's code
    # for top_row_pixel in normalized_grayscale_image[0]:
    #     if top_row_pixel > DARK_THRESHOLD:
    #         return False
    # for bottom_row_pixel in normalized_grayscale_image[-1]:
    #     if bottom_row_pixel > DARK_THRESHOLD:
    #         return False
    # for row in normalized_grayscale_image:
    #     if row[0] > DARK_THRESHOLD and row[-1] > DARK_THRESHOLD:
    #         return False
    # return True

    #setting up variables
    counter = 0
    failed = []
    borders_passed = []
    percent_failed = 0.20
    border_percentage = 0.05 #top and bottom 0.5% of photo
    length = len(normalized_grayscale_image[0])
    width = len(normalized_grayscale_image)
    border_num = int(border_percentage * min(length, width)) #number of pixels we want to check
    if border_num < 1:
        border_num = 1

    ## Using average pixel as threshold ##
    # num_of_pixels = 0
    # sum_of_pixel = 0
    # for row in normalized_grayscale_image:
    #     for pixel in row:
    #         sum_of_pixel += pixel
    #         num_of_pixels += 1
    # DARK_THRESHOLD = sum_of_pixel / num_of_pixels
    # print(DARK_THRESHOLD)

    ## Using half of highest pixel as threshold ##
    max_pixel = 0
    for row in normalized_grayscale_image:
        for pixel in row:
            if pixel > max_pixel:
                max_pixel = pixel
    DARK_THRESHOLD = max_pixel * 0.5

    ## Evaluating the top border ##
    for rows_top in range(border_num):
        for pixel_top in normalized_grayscale_image[rows_top]:
            if pixel_top > DARK_THRESHOLD:
                failed.append(pixel_top)
            counter += 1
    if len(failed) > percent_failed * counter:
        borders_passed.append(False)
    else:
        borders_passed.append(True)
    counter = 0
    del(failed[0:len(failed)])

    ## Evaluating the bottom border ##
    for rows_bottom in range(border_num):
        for pixel_bottom in normalized_grayscale_image[::-1][rows_bottom]:
            if pixel_bottom > DARK_THRESHOLD:
                failed.append(pixel_bottom)
            counter += 1
    if len(failed) > percent_failed * counter:
        borders_passed.append(False)
    else:
        borders_passed.append(True)
    counter = 0
    del(failed[0:len(failed)])

    ## Evaluting the left border ##
    for row in normalized_grayscale_image[1:len(normalized_grayscale_image)-2]:
        for pixel in range(border_num):
            if row[pixel] > DARK_THRESHOLD:
                failed.append(row[pixel])
            counter += 1
    if len(failed) > percent_failed * counter:
        borders_passed.append(False)
    else:
        borders_passed.append(True)
    counter = 0
    del(failed[0:len(failed)])

    ## Evaluating the right border ##
    for row in normalized_grayscale_image[1:len(normalized_grayscale_image) - 2]:
        for pixel in range(border_num):
            if row[::-1][pixel] > DARK_THRESHOLD:
                failed.append(row[pixel])
            counter += 1
    if len(failed) > percent_failed * counter:
        borders_passed.append(False)
    else:
        borders_passed.append(True)

    ## Determining how many borders passed the test ##
    true_counter = 0
    for val in borders_passed:
        if val:
            true_counter += 1
    if true_counter >= 3:
        return True
    else:
        return False

