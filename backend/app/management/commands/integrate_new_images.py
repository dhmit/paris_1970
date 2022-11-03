import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from app.models import Photo, MapSquare

class Command(BaseCommand):
    """
    django-admin command that reloads all of our images
    from the original folder hierarchy containing the structure
    documented in the app.Photo model
    """
    def add_arguments(self, parser):
        parser.add_argument('source_dir', action='store', type=str)
        parser.add_argument('--delete_existing', action='store_true')

    def handle(self, *args, **options):
        source_dir_path = Path(options.get('source_dir'))
        delete_existing = options.get('delete_existing')

        if delete_existing:
            user_sure_input = input("Are you sure? Input 'delete' to delete everything, or anything else to quit.\n")
            if user_sure_input == 'delete':
                print('Deleting all Photo objects...\n')
                Photo.objects.all().delete()
            else:
                return

        print(f'Recreating Photo objects from src directory {source_dir_path}...\n')
        for src_sub_dir in source_dir_path.iterdir():
            if not src_sub_dir.is_dir(): 
                continue

            for src_image_path in src_sub_dir.iterdir():
                # print(src_image_path)
                if src_image_path.suffix.lower() != '.jpg' or not src_image_path.is_file():
                    print(f"Skipping {src_image_path} because it is not a .jpg file\n")
                    continue

                # Structure of the filenames:
                # BHVP_PH_CetaitParis_DP_MAP-SQUARE_FOLDER_IMG-FILE-NUMBER
                # IMG-FILE-NUMBERs alternate slide_1, photo_1, slide_2, photo_2, etc.
                src_filename = src_image_path.stem
                # print(src_filename)
                _, _, _, _, map_square_num, folder_num, file_num = src_filename.split('_')
                file_num = int(file_num)
                folder_num = int(folder_num)
                map_square_num = int(map_square_num)
                file_num = int(file_num)

                if file_num % 2: 
                    # since we only need one Photo per pair of images
                    continue
                else:
                    photo_num = file_num / 2
                    map_square_obj = MapSquare.objects.get(number=map_square_num)
                    Photo.objects.create(number=photo_num,
                                         map_square=map_square_obj,
                                         folder=folder_num)
