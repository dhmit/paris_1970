import os
import subprocess
import sys
from pathlib import Path

from tqdm import tqdm


def convert(src_dir_path, dest_dir_path, commands=['-quality', '20%']):
    """
    Python script for image conversion using Image Magick
    
    :param src_dir_path: Path object to directory containing subdirectories of images
    :param dest_dir_path: Path path object where output is intended to be saved in
    :param commands: (list of strings) commands to apply to images
    :return: None, output produced in new directory
    """

    magick_commands = []
    for src_sub_dir in src_dir_path.iterdir():
        if not src_sub_dir.is_dir(): continue

        dest_sub_dir = Path(dest_dir_path, src_sub_dir.name)
        if not dest_sub_dir.exists():
            dest_sub_dir.mkdir()

        magick_args = ' ' .join(commands)

        # looping through old directory
        for src_image_path in src_sub_dir.iterdir():
            # print(src_image_path)
            if src_image_path.suffix.lower() != '.jp2' or not src_image_path.is_file():
                print(f"Skipping {src_image_path} because it is not a .jp2 file\n")
                continue

            dest_image_path = Path(dest_sub_dir, src_image_path.stem + '.jpg')
            if dest_image_path.exists(): continue

            # formatting command
            # ex. magick Users/bob/Desktop/old/square.jpg -quality 20% Users/bob/Desktop/new/square.jpg
            cmd = f'magick "{src_image_path}" {magick_args} "{dest_image_path}"'
            magick_commands.append(cmd)

    # Once we compute all the commands, we use subprocess.Popen to run them in parallel
    batch_size = 35
    for min_job_idx in range(0, len(magick_commands), batch_size):
        max_job_idx = min_job_idx+batch_size
        batch_cmds = magick_commands[min_job_idx:max_job_idx]
        print("--------------------------------------------------------------------------------")
        print(f"| Processing {min_job_idx} to {max_job_idx} of {len(magick_commands)}")
        print("--------------------------------------------------------------------------------")
        procs = [subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in batch_cmds]
        for proc in tqdm(procs): proc.wait()

if __name__ == "__main__":
    src_dir_path = Path(sys.argv[1])
    dest_dir_path = Path(sys.argv[2])
    commands_arg = sys.argv[3:]

    convert(src_dir_path, dest_dir_path, commands_arg)

"""
# Example of command-line:
    python scripts/imageconversion.py /Users/bob/Desktop/TestImages /Users/bob/Desktop/newtest
"""
