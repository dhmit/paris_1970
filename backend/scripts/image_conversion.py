import subprocess
import sys
import argparse
from pathlib import Path

from tqdm import tqdm

IMAGE_EXTENSIONS = ['.jpg', '.jp2']


def convert(src_dir_path, dest_dir_path, args):
    """
    Python script for image conversion using Image Magick
    
    :param src_dir_path: Path - path object to directory containing subdirectories of images
    :param dest_dir_path: Path - path object where output is intended to be saved in
    :param argparse Namespace - Namespace containing parsed command line arguments
        :param output_type: str - indicating type of resizing to conduct [web, highres, thumbnail, none (if no presets desired)]
        :param valid_exts: (list of str) - image extensions to convert
        :param output_ext: str - extension of output images
        :param custom_args: (list of str) - optional imagemagick args to apply after args associated with specified output type
    :return: None - output produced in new directory
    """
    output_type = args.type
    trim = args.trim
    valid_exts = args.cvt_exts
    output_ext = args.out_ext
    custom_args = args.custom_args

    if output_type == 'web':
        commands = ['-quality 20%', '-resize 25%']
    elif output_type == 'highres':
        commands = ['-quality 20%']
    elif output_type == 'thumbnail':
        commands = ['-resize 100>']  # Resize largest dimension to 100 while keeping aspect ratio
    elif output_type == "none":
        commands = []
    else:
        raise Exception(
            f'output_type "{output_type}" is not recognized.\noutput_type should be one of: highres, web, thumbnail, none'
        )
    commands += custom_args

    if trim:
        commands = ['-bordercolor black -fuzz 20% -trim -format jpg'] + commands

    magick_commands = []
    for src_sub_dir in src_dir_path.iterdir():
        if not src_sub_dir.is_dir(): 
            continue

        dest_sub_dir = Path(dest_dir_path, src_sub_dir.name)
        if not dest_sub_dir.exists():
            dest_sub_dir.mkdir()

        magick_args = ' '.join(commands)

        # looping through old directory
        for src_image_path in src_sub_dir.iterdir():
            # print(src_image_path)
            if src_image_path.suffix.lower() not in valid_exts or not src_image_path.is_file():
                print(f"Skipping {src_image_path} because it is not a recognized image file\n")
                continue

            dest_image_path = Path(dest_sub_dir, src_image_path.stem + f".{output_ext}")
            if dest_image_path.exists(): 
                continue

            # formatting command
            # ex. magick Users/bob/Desktop/old/square.jpg -quality 20% Users/bob/Desktop/new/square.jpg
            cmd = f'magick "{src_image_path}" {magick_args} "{dest_image_path}"'
            magick_commands.append(cmd)

    # Once we compute all the commands, we use subprocess.Popen to run them in parallel
    batch_size = 35
    for min_job_idx in range(0, len(magick_commands), batch_size):
        max_job_idx = min_job_idx + batch_size
        batch_cmds = magick_commands[min_job_idx:max_job_idx]
        print("--------------------------------------------------------------------------------")
        print(f"| Processing {min_job_idx} to {max_job_idx} of {len(magick_commands)}")
        print("--------------------------------------------------------------------------------")
        procs = [subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in batch_cmds]
        for proc in tqdm(procs): 
            proc.wait()

if __name__ == "__main__":
    """
    Usage:
    python imageconversion.py PATH_TO/SOURCE_IMG_FOLDER PATH_TO/DEST_IMAGE_FOLDER 
    --type web --trim --custom_args optional_img_magick_flags
    """
    parser = argparse.ArgumentParser(
        description='Python script for image conversion of paris_1970 source photos using Image Magick')
    parser.add_argument('src_dir_path', type=str,
                        help='PATH_TO/SOURCE_IMG_FOLDER')
    parser.add_argument('dest_dir_path', type=str,
                        help='PATH_TO/DEST_IMAGE_FOLDER')
    parser.add_argument('--type', type=str, default='none',
                        help='''image resizing:
                        web=-quality 20% -resize 25%
                        highres=-quality 20%
                        thumbnail=-resize 100> (Resize largest dimension to 100 keeping aspect ratio)
                        none=[no presets]''')
    parser.add_argument('--trim', default=False, action="store_true", help='trim black borders from image')
    parser.add_argument('--cvt_exts', type=str, nargs='+', default=IMAGE_EXTENSIONS,
                        help='image extensions to convert')
    parser.add_argument('--out_ext', type=str, default="jpg",
                        help='extension of output images')
    parser.add_argument('--custom_args', type=str, nargs='+', default=[],
                        help='optional imagemagick commands')
    args = parser.parse_args()

    convert(Path(args.src_dir_path), Path(args.dest_dir_path), args)
