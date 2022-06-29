import os
import subprocess
from tqdm import tqdm
import sys


def crop_border(old_path, new_path, fuzz_val='20'):
    """
    Python script for cropping white borders off slides using Image Magick

    :param old_path: (str) path to directory containing images
            [ex. 'Users/bob/Desktop/']
    :param new_path: (str) path where output is intended to be saved in
            [ex. 'Users/bob/Desktop/new/']
    :param fuzz_val: (str) percentage value for Image Magick fuzz command, default 20
            [ex. 55]
    :return: None, output produced in new directory
    """

    # creating new directory (and all intermediate-level directories) for output
    try:
        os.makedirs(new_path)
    except FileExistsError:
        pass

    # loop through images running command
    for img in tqdm(os.listdir(old_path), bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}'):
        # create new and old paths
        in_file = os.path.join(old_path, img)
        out_file = os.path.join(new_path, img)

        # formatting command
        # ex. magick convert Users/bob/Desktop/old/img3.jpg -bordercolor white -border 1 -fuzz 20%
        # -trim -background white Users/bob/Desktop/new/img3.jpg
        cmd = f'magick convert {in_file} -bordercolor white -border 1 -fuzz {fuzz_val}% -trim ' \
              f'-background white {out_file}'
        # adds 1 pixel wide white border, and trims based on fuzz (mean color distance)
        subprocess.run(cmd, shell=True, capture_output=True)


if __name__ == '__main__':
    """
    Examples of command-line:
        python scripts/cropborder.py /Users/bob/Desktop/TestImages /Users/bob/Desktop/newtest

        python scripts/cropborder.py /Users/bob/Desktop/TestImages /Users/bob/Desktop/newtest 55
    """

    script = sys.argv[0]  # python cropborder.py
    old_path_arg = sys.argv[1]  # argument 1 old_path
    new_path_arg = sys.argv[2]  # argument 2 new_path

    # default 20% fuzz
    if len(sys.argv) == 3:
        crop_border(old_path_arg, new_path_arg)
    else:
        # provided fuzz percentage
        fuzz_arg = sys.argv[3]  # argument 3 fuzz_val
        crop_border(old_path_arg, new_path_arg, fuzz_arg)



