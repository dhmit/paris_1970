"""

detail_fft2.py

analysis to calculate the level of detail by examining frequency of change in photo color
"""

from numpy.fft import fft2
import cv2

from app.models import Photo

def analyze(photo: Photo):
    """
    Calculate the standard deviation of pixels in the image using the fast fourier transform
    """
    image = photo.get_image_data()

    # Convert image to grayscale
    # (Changes image array shape from (height, width, 3) to (height, width))
    # (Pixels (image[h][w]) will be a value from 0 to 255)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Take the 2-dimensional fourier transform of the image
    image_fft2 = fft2(grayscale_image)

    # Calculate frequency coefficients
    row_coefficients = abs(image_fft2.sum(axis=1)) / image_fft2.shape[1]
    column_coefficients = abs(image_fft2.sum(axis=0)) / image_fft2.shape[0]

    highest_frequencies = [row_coefficients[-1], column_coefficients[-1]]
    detail_score = (highest_frequencies[0] * highest_frequencies[1]) + min(highest_frequencies)

    detail_score = round(detail_score / 10**7, 10)

    return detail_score
