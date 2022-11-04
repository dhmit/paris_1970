"""
Django management command sync_photo_metadata

In Fall 2022, we have a temporary metadata spreadsheet living on Google Sheets
that we're using to transcribe metadata for our photo collection.

Ryaan wrote a Google Apps Script thing that exports all of the data transcribed
there into a CSV file, and this management command imports it.

Our Django admin page team (Cindy, Lisa, Kingston) are currently working on
a tool within our actual app to replace all this workflow, so this is temporary.

"""

# Python standard library
from pathlib import Path
from dataclasses import dataclass

from django.conf import settings
from django.core.management.base import BaseCommand

from app.models import Photo, MapSquare, Photographer
from app.common import print_header

@dataclass
class PhotoMetadata:
    map_square_number: int
    folder_number: int
    photo_number: int
    full_text: str
    photographer_number: int
    street_name: str
    public_notes: str
    private_notes: str


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        metadata_csv_path = Path(settings.PROJECT_ROOT, 'map_square_metadata.csv')
        print(metadata_csv_path)

        photo_metadata_list: list[PhotoMetadata] = []
        with open(metadata_csv_path, encoding='utf-8') as csv_file:
            lines = csv_file.readlines()
            rows = lines[1:]
            for row in rows:
                split_row = [field.strip().strip('\"') for field in row.split('","')]

                map_square_number, folder_number, photo_number, full_text, photographer_number, street_name, public_notes, private_notes = split_row

                # ? in the photographer number means that we weren't sure but could infer from
                # context (i.e., the same hand as surrounding photographer numbers).
                # For now, we're not actually marking this in the db at all
                photographer_number = photographer_number.replace('?', '')

                try:
                    photographer_number = int(photographer_number)
                except ValueError:
                    print(f"Skipped {map_square_number}_{folder_number}_{photo_number} because of invalid photographer number {photographer_number}")
                    continue

                metadata = PhotoMetadata(map_square_number=int(map_square_number),
                                         folder_number=int(folder_number),
                                         photo_number=int(photo_number,),
                                         full_text=full_text, 
                                         photographer_number=photographer_number,
                                         street_name=street_name, 
                                         public_notes=public_notes,
                                         private_notes=private_notes)
                photo_metadata_list.append(metadata)
        
        for metadata in photo_metadata_list: 
            photo_number = metadata.photo_number
            map_square_number = metadata.map_square_number
            folder_number = metadata.folder_number
            photographer_number = metadata.photographer_number

            photo = Photo.objects.get(number=photo_number, map_square__number=map_square_number, folder=folder_number)
            if metadata.photographer_number:
                try:
                    photographer = Photographer.objects.get(number=photographer_number)
                    photo.photographer = photographer
                    photo.save()
                    print(f"Updated {map_square_number}_{folder_number}_{photo_number} with photographer number {photographer_number}.")
                except Photographer.DoesNotExist:
                    print(f"Photographer {metadata.photographer_number} does not exist! Skipping {map_square_number}_{folder_number}_{photo_number}.")
                    print(f"Need to check the photographer entry list.")
                    continue


