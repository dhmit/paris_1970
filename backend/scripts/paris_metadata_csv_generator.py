import os
import subprocess
import sys
from pathlib import Path

IMG_URL_STUB = "=IMAGE(\"https://s3.us-east-1.amazonaws.com/paris1970-fa22-dev-assets/jpg-quality20/"


def main(src_dir_path, dest_dir_path):
    """
    Creates CSV file templates for the map square entry process
    """
    for src_sub_dir in src_dir_path.iterdir():
        if not src_sub_dir.is_dir(): continue

        map_square_folder_url = src_sub_dir.name
        folder_number = '_'.join(map_square_folder_url.split('_')[-2:])

        out_csv = open(Path(dest_dir_path, folder_number + '.csv'), 'w', encoding='utf-8')

        out_csv.write("Transcriber name\n")
        out_csv.write("Transcriber email\n")
        out_csv.write("Image,Map Square,Notes\n")

        for src_image_path in src_sub_dir.iterdir():
            if src_image_path.suffix.lower() != '.jpg' or not src_image_path.is_file():
                print(f"Skipping {src_image_path} because it is not a .jpg file\n")
                continue

            image_col = IMG_URL_STUB + map_square_folder_url + '/' + src_image_path.name + "\")"
            row = f'{image_col},,\n'
            out_csv.write(row)

        out_csv.close()

if __name__ == "__main__":
    src_dir_path = Path(sys.argv[1])
    dest_dir_path = Path(sys.argv[2])
    main(src_dir_path, dest_dir_path)
