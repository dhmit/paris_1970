import os
import sys
import csv
import math
import subprocess
from tqdm import tqdm

def rename(source_dir, destination_dir, commands=None):
    """
    Python script for file renaming

       :param source_dir: (str) path to directory containing images
               [ex. 'Users/bob/Desktop/']
       :param destination_dir: (str) path where output is intended to be saved in
               [ex. 'Users/bob/Desktop/new/']
       :return: None, output produced in new directory

    """
    count = 1
    command_str = ''
    for i in commands:
        command_str += i + ' '

    for file_name in tqdm(os.listdir(source_dir), bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}'):

        filename_parts = file_name.split('_')  # ["xyz", "039.jpg"]
        num_of_photo = int(filename_parts[-1].split('.')[0])  # "039" > 39
        p = math.ceil(num_of_photo / 2)

        if num_of_photo % 2 == 0:
            type_of_img = "photo"
        else:
            type_of_img = "slide"

        source = source_dir + "/" + file_name
        destination = destination_dir + "/" + str(p) + "_" + type_of_img + ".jpg"
        os.rename(source, destination)
        count += 1
        print(source, destination)

        cmd = f' {source_dir} {command_str}{destination_dir}'
        subprocess.run(cmd, shell=True, capture_output=True)

        with open('dictionary.csv', 'a+') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([source, destination])

    print("The renaming is over. Photos can be found in  " + destination_dir)


if __name__ == "__main__":
    script = sys.argv[0]
    source_dir_arg = sys.argv[1]
    destination_dir_arg = sys.argv[2]
    commands_arg = sys.argv[3:]
    rename(source_dir_arg, destination_dir_arg, commands_arg)

