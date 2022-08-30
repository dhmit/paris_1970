import os
import subprocess
import sys

from tqdm import tqdm


def convert(old_path, new_path, old_filetype, new_filetype, commands=None):
    """
    Python script for image conversion using Image Magick
    
    :param old_path: (str) path to directory containing images
            [ex. 'Users/bob/Desktop/']
    :param new_path: (str) path where output is intended to be saved in
            [ex. 'Users/bob/Desktop/new/']
    :param old_filetype: (str) image format of input images
            [ex. 'TIF']
    :param new_filetype: (str) desired output image format
            [ex. 'jpg']
    :param commands: (list) commands to apply to images, default = None
            [ex. ['-quality, '20%']
    :return: None, output produced in new directory
    """

    # creating new directory for output
    try:
        os.mkdir(new_path)
    except FileExistsError:
        pass

    # str of commands to apply to images
    command_str = ''
    for i in commands:
        command_str += i + ' '

    # looping through old directory
    for tif_path in tqdm(os.listdir(old_path), bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}'):
        old_type = os.path.join(old_path, tif_path)
        if os.path.isfile(old_type) and old_type.endswith(old_filetype):
            # formatting new filename ex. '/square.jpg'
            name = os.path.splitext(tif_path)[0] + "." + new_filetype
            new_type = os.path.join(new_path, name)

            # formatting command
            # ex. magick Users/bob/Desktop/old/square.jpg -quality 20%
            # Users/bob/Desktop/new/square.jpg
            cmd = f'magick {old_type} {command_str}{new_type}'
            subprocess.run(cmd, shell=True, capture_output=True, check=True)


if __name__ == "__main__":
    script = sys.argv[0]  # python imageconversion.py
    old_path_arg = sys.argv[1]  # argument 1 old_path
    new_path_arg = sys.argv[2]  # argument 2 new_path
    old_file_arg = sys.argv[3]  # argument 3 old_filetype
    new_file_arg = sys.argv[4]  # argument 4 new_filetype
    commands_arg = sys.argv[5:]  # argument 5 commands
    convert(old_path_arg, new_path_arg, old_file_arg, new_file_arg, commands_arg)

"""
# Example of command-line:

    python scripts/imageconversion.py /Users/bob/Desktop/TestImages /Users/bob/Desktop/newtest
    TIF JPG -thumbnail 300x90
"""
