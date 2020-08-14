"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

import os
import tqdm
from textwrap import dedent

from django.contrib.auth.models import User
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from googleapiclient.discovery import build

from app.models import Photo, MapSquare, Photographer
from app.common import print_header
from app.google_api import load_creds
from app.google_api import SCOPES

# Our metadata spreadsheet lives here:
# https://docs.google.com/spreadsheets/d/1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I/edit#gid=0
METADATA_SPREADSHEET_ID = '1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I'



def create_lookup_dict(drive_service, map_square_folders):
    """
    Creates a quick look up dictionary to get the image URL using map square number and source name
    """
    lookup_dict = {}
    # tqdm is a library that shows a progress bar
    for map_square in tqdm.tqdm(map_square_folders):
        result = drive_service.files().list(
            q=f"'{map_square['id']}' in parents",
            fields="files(id, name)"
        ).execute()
        images = result.get('files', [])
        lookup_dict[map_square['name']] = {
            #  <img src = "https://drive.google.com/uc?id=0Bzgk4zncCwI7aDZCSHY4YU0zNUF&export=download">

            image['name']: f"https://drive.google.com/uc?id={image['id']}&export=download"
            for image in images
        }
    return lookup_dict


def add_photo_srcs(model_kwargs, map_square_folder, photo_srcs):
    """
    Takes a list of photo sources and dynamically adds the Google Drive urls into the model kwargs
    """
    for src in photo_srcs:
        try:
            side = src.split("_")[1].split(".")[0]  # Gets front, back, or binder from the src
        except IndexError:
            print_header(f"The photo with source {src} is not named in the correct format")
        model_kwargs[f"{side}_src"] = map_square_folder.get(src, '')


MODEL_NAME_TO_MODEL = {"Photo": Photo, "MapSquare": MapSquare, "Photographer": Photographer}


class Command(BaseCommand):
    help = 'Syncs local db with data from project Google Sheet'

    def handle(self, *args, **options):
        # Delete database
        if os.path.exists(settings.DB_PATH):
            print_header('Deleting existing db...')
            try:
                os.remove(settings.DB_PATH)
            except PermissionError:
                # weird indentation because turns out dedent nests weirdly...
                print_header('Permission Error')
                print(dedent('''
                    Unable to delete the database file while the backend is running.
                    Please stop the "Run backend" process and try again.
                '''))

                return

        # Delete all migrations
        for file in os.listdir(settings.MIGRATIONS_DIR):
            if file != '__init__.py' and file != '__pycache__':
                file_path = os.path.join(settings.MIGRATIONS_DIR, file)
                os.remove(file_path)
        print('Done!')

        # The order of these ranges matter. The Photographer model needs to have foreign keys to
        # the MapSquare database, so we add the Map Squares first
        spreadsheet_ranges = ['MapSquare', 'Photographer', 'Photo']

        print_header(f'''Will import ranges {", ".join(spreadsheet_ranges)}. (If nothing
          is happening, please try again.)''')

        # Settings for pickle file

        creds = load_creds(SCOPES)

        sheets_service = build('sheets', 'v4', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        print_header('Getting the URL for all photos (This might take a couple of minutes)...')
        # Create a lookup dictionary to get photo urls using Drive API
        results = drive_service.files().list(
            q="'1aiY1nFJn6T7khu5dhIs3U2o8RdHBu6V7' in parents",
            fields="nextPageToken, files(id, name)"
        ).execute()
        items = results.get('files', [])
        photo_url_lookup = create_lookup_dict(drive_service, items)

        # Call the Sheets API
        databases = []
        sheet = sheets_service.spreadsheets()
        for spreadsheet_range in spreadsheet_ranges:
            get_values_cmd = \
                sheet.values().get(spreadsheetId=METADATA_SPREADSHEET_ID, range=spreadsheet_range)
            result = get_values_cmd.execute()
            values = result.get('values', [])
            databases.append(values)

        # Rebuild database
        print_header('Rebuilding db from migrations...')
        call_command('makemigrations')
        call_command('migrate')
        print('Done!')

        # THIS IS JUST FOR PROTOTYPING NEVER EVER EVER EVER IN PRODUCTION do this
        superuser = User.objects.create_superuser('admin', password='adminadmin')
        if not databases:
            print_header('No data found.')
            return

        for model_name, values in zip(spreadsheet_ranges, databases):
            print_header(f'{model_name}: Importing these values from the spreadsheet')

            header = values[0]
            values_as_a_dict = [{header_val: entry for header_val, entry in zip(header, row)}
                                for row in values[1:]]

            for row in values_as_a_dict:
                # print(row)
                # Filter column headers for model fields
                model_fields = MODEL_NAME_TO_MODEL[model_name]._meta.get_fields()
                model_field_names = [field.name for field in model_fields]
                model_kwargs = {}
                for header in row.keys():
                    if header in model_field_names or header == 'map_square_number':
                        # Check if value in column is a number
                        value = row[header]
                        if header in ['number', 'map_square_number', 'photographer']:
                            try:
                                value = int(value)
                                if header == 'map_square_number':
                                    header = 'map_square'
                            except ValueError:
                                continue
                        # Evaluate value as a boolean
                        elif header == 'contains_sticker':
                            if value.lower() == 'yes':
                                value = True
                            elif value.lower() == 'no':
                                value = False
                            elif value.isdigit() and 0 <= int(value) <= 1:
                                value = bool(value)
                            else:
                                continue
                        model_kwargs[header] = value

                # If no model fields found, do not create model instance
                if len(model_kwargs) == 0:
                    continue

                if model_name == 'Photo' or model_name == 'Photographer':
                    map_square_number = model_kwargs.get('map_square', None)
                    # Returns the object that matches or None if there is no match
                    model_kwargs['map_square'] = \
                        MapSquare.objects.filter(number=map_square_number).first()

                if model_name == 'Photo':
                    # Looks up the Photo URL of the front and back
                    map_square_number = str(row.get('map_square_number', ''))
                    srcs = row.get('srcs', '')
                    photo_srcs = []
                    if ',' in srcs:
                        for src in srcs.split(','):
                            # strip removes whitespace from beginning or end of string in case
                            # the person who entered the data added extra spaces
                            photo_srcs.append(src.strip())
                    else:
                        photo_srcs.append(srcs)
                    map_square_folder = photo_url_lookup.get(map_square_number, '')

                    if map_square_folder:
                        add_photo_srcs(model_kwargs, map_square_folder, photo_srcs)

                    # Get the corresponding Photographer objects
                    photographer_number = model_kwargs.get('photographer', None)
                    model_kwargs['photographer'] = \
                        Photographer.objects.filter(number=photographer_number).first()

                print_header("Final model_kwargs: " + str(model_kwargs))

                model_instance = MODEL_NAME_TO_MODEL[model_name](**model_kwargs)
                model_instance.save()
