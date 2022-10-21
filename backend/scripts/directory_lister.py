import sys
from pathlib import Path


def convert(src_dir_path, dest_dir_path):
    """
    Python script for image conversion using Image Magick
    
    :param src_dir_path: Path object to directory containing subdirectories of images
    :param dest_dir_path: Path path object where output is intended to be saved in
    :param commands: (list of strings) commands to apply to images
    :return: None, output produced in new directory
    """

    for src_sub_dir in src_dir_path.iterdir():
        if not src_sub_dir.is_dir(): 
            continue

        dest_sub_dir = Path(dest_dir_path, src_sub_dir.name)
        if not dest_sub_dir.exists():
            dest_sub_dir.mkdir()

        # looping through old directory
        for src_image_path in src_sub_dir.iterdir():
            # print(src_image_path)
            if src_image_path.suffix.lower() != '.jp2' or not src_image_path.is_file():
                print(f"Skipping {src_image_path} because it is not a .jp2 file\n")
                continue

            dest_image_path = Path(dest_sub_dir, src_image_path.stem + '.jpg')
            if dest_image_path.exists(): 
                continue

if __name__ == "__main__":
    src_path = Path(sys.argv[1])
    dest_path = Path(sys.argv[1])

    convert(src_path, dest_path)

"""
# Example of command-line:
    python scripts/imageconversion.py /Users/bob/Desktop/TestImages /Users/bob/Desktop/newtest
"""
