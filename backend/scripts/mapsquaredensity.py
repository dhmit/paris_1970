import os
import json

def measure_square_density(image_path):
    """
    Python script for counting the number of images in each map square

    :param image_path: The path to the image directory

    :return: The path to a JSON file containing a dictionary associating each map square number
    ID to the number of images within
    """

    counts = {}

    map_square_list = os.listdir(image_path)    # This is a list of the names of each of the directories in image_path (i.e. the map square names).

    for map_square in map_square_list:
        map_square_dir = image_path+"\\"+map_square
        image_list = os.listdir(map_square_dir) # This is a list of the image file names in map_square_dir
        count = len(image_list)
        counts[map_square] = count

    with open(r'C:\Users\Ayden\Documents\GitHub\paris_1970\backend\data\counts.json',
              'w') as json_file: # This converts the dictionary into JSON and
        # stores it in a json file.
        json.dump(counts, json_file)

    # The output file is stored in the data folder in \backend.

measure_square_density(r"C:\Users\Ayden\Documents\GitHub\paris_1970\assets\images\photos")
