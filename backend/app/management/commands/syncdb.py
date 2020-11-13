"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

# Python standard library
import io
import pickle
import os
from textwrap import dedent
from pathlib import Path

# 3rd party
import tqdm
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Django
from django.contrib.auth.models import User
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

# Ours
from app.models import Photo, MapSquare, Photographer
from app.common import print_header

# The scope of our access to the Google API Account
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
]


# Our metadata spreadsheet lives here:
# https://docs.google.com/spreadsheets/d/1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I/edit#gid=0
METADATA_SPREADSHEET_ID = '1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I'
PHOTO_FOLDER_ID = '1aiY1nFJn6T7khu5dhIs3U2o8RdHBu6V7'

# Sides of a photo
SIDES = ['cleaned', 'front', 'back', 'binder']

MODEL_NAME_TO_MODEL = {"Photo": Photo, "MapSquare": MapSquare, "Photographer": Photographer}


def authorize_google_apps():
    """
    Authorization flow for letting our application talk with the Google API
    """
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(settings.GOOGLE_TOKEN_FILE):
        with open(settings.GOOGLE_TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_API_CREDENTIALS_FILE,
                SCOPES
            )
            credentials = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open(settings.GOOGLE_TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return credentials


def create_lookup_dict(drive_service):
    """
    Creates a quick look up dictionary to get the image URL using map square number and source name
    :param credentials: Credentials object for drive service
    :return Look up dictionary to get the image URL using map square number and source name
    """
    # Resource object for interacting with the google API

    # Get list of files in google drive folder
    results = drive_service.files().list(
        q=f"'{PHOTO_FOLDER_ID}' in parents",
        fields="nextPageToken, files(id, name)"
    ).execute()

    # List of dictionaries containing id and name of map square folder in the google drive
    map_square_folders = results.get('files', [])

    lookup_dict = {}
    # tqdm is a library that shows a progress bar
    for map_square in tqdm.tqdm(map_square_folders):
        result = drive_service.files().list(
            q=f"'{map_square['id']}' in parents",
            fields="files(id, name)"
        ).execute()
        images = result.get('files', [])

        # Creates a dictionary mapping photo number to a list of the photo sources belonging to
        # that number
        map_square_dict = {}
        for image in images:
            photo_number = image['name'].split('_')[0]
            photo_drive_file_ids = map_square_dict.get(photo_number, {})
            filename = image['name']
            filename = filename.replace('JPG', 'jpg').replace('jpeg', 'jpg')
            photo_drive_file_ids[filename] = image['id']
            map_square_dict[photo_number] = photo_drive_file_ids

        lookup_dict[map_square['name']] = map_square_dict
    return lookup_dict

# pylint: disable=too-many-arguments
def add_photo_srcs(
    model_kwargs,
    map_square_number,
    map_square_folder,
    photo_number,
    drive_service,
    local_download,
    redownload,
    verbose,
):
    """
    Takes the map square folder and the photo number to dynamically adds the Google Drive urls
    into the model kwargs
    :param model_kwargs: Dictionary of keyword arguments to be used in creating the model
    :param map_square_folder: Dictionary of photo sources with keys of photo_number
    :param photo_number: The number of the desired photo in the map_square_folder
    :param local_download: should we download the photos locally?
    """
    # pylint: disable=too-many-locals
    photo_drive_file_ids = map_square_folder.get(str(photo_number), '')
    if photo_drive_file_ids == '':
        return

    for side in SIDES:
        drive_file_id = photo_drive_file_ids.get(f'{photo_number}_{side}.jpg', '')

        if drive_file_id:
            src_url = f"https://drive.google.com/uc?id={drive_file_id}&export=download"
            model_kwargs[f'{side}_src'] = src_url

            if local_download:
                request = drive_service.files().get_media(fileId=drive_file_id)
                Path(settings.LOCAL_PHOTOS_DIR).mkdir(exist_ok=True)
                local_map_square_dir = Path(settings.LOCAL_PHOTOS_DIR, map_square_number)
                local_map_square_dir.mkdir(exist_ok=True)
                local_photo_path = Path(local_map_square_dir, f'{photo_number}_{side}.jpg')

                if (not local_photo_path.exists()) or redownload:
                    if verbose:
                        print(f'Downloading map square {map_square_number}, photo {photo_number}, '
                              f'side {side}')
                    out_file = io.FileIO(local_photo_path, mode='wb')
                    downloader = MediaIoBaseDownload(out_file, request)
                    done = False
                    while done is False:
                        _, done = downloader.next_chunk()

                model_kwargs[f'{side}_local_path'] = local_photo_path

        else:
            model_kwargs[f'{side}_src'] = None
            model_kwargs[f'{side}_local_path'] = None


def call_sheets_api(spreadsheet_ranges, sheets_service):
    """
    Creates list of list of spreadsheet rows
    """
    databases = []
    sheet = sheets_service.spreadsheets()
    for spreadsheet_range in spreadsheet_ranges:
        get_values_cmd = \
            sheet.values().get(spreadsheetId=METADATA_SPREADSHEET_ID, range=spreadsheet_range)
        result = get_values_cmd.execute()
        values = result.get('values', [])
        databases.append(values)
    return databases


def populate_database(
    model_name,
    values_as_a_dict,
    photo_url_lookup,
    drive_service,
    local_download,
    redownload,
    verbose,
):
    """
    Adds model instances to the database based on the data imported from the google spreadsheet
    :param model_name: Name of the model to create an instance of
    :param values_as_a_dict: List of dictionaries representing spreadsheet rows in the form of
    { column names: cell values }
    :param photo_url_lookup: Dictionary of map square folders in the form of a dictionary
    """
    # pylint: disable=too-many-locals
    for row in values_as_a_dict:
        # Filter column headers for model fields
        model_fields = MODEL_NAME_TO_MODEL[model_name]._meta.get_fields()
        model_field_names = [field.name for field in model_fields]

        model_kwargs = {}
        for header in row.keys():
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------
            # BREAKPOINTS HERE ---------------------------------------------------------------------

            if header in model_field_names or header == 'map_square_number':
                # Check if value in column is a number
                value = row[header]
                if header in ['number', 'map_square_number', 'photographer']:
                    if header == 'map_square_number':
                        header = 'map_square'
                    try:
                        value = int(value)
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

        if model_name in ['Photo', 'Photographer']:
            map_square_number = model_kwargs.get('map_square', None)
            # Returns the object that matches or None if there is no match
            model_kwargs['map_square'] = \
                MapSquare.objects.filter(number=map_square_number).first()

        if model_name == 'Photo':
            # Gets the Map Square folder and the photo number to look up the URLs
            map_square_number = str(row.get('map_square_number', ''))
            map_square_folder = photo_url_lookup.get(map_square_number, '')
            photo_number = row.get('number', '')

            if map_square_folder:
                add_photo_srcs(
                    model_kwargs,
                    map_square_number,
                    map_square_folder,
                    photo_number,
                    drive_service,
                    local_download,
                    redownload,
                    verbose,
                )

            # Get the corresponding Photographer objects
            photographer_number = model_kwargs.get('photographer', None)
            model_kwargs['photographer'] = \
                Photographer.objects.filter(number=photographer_number).first()

        if verbose:
            print(f'Creating {model_name} with kwargs: {model_kwargs}\n')

        model_instance = MODEL_NAME_TO_MODEL[model_name](**model_kwargs)
        model_instance.save()


class Command(BaseCommand):
    """
    Custom django-admin command used to sync the local db with data from project Google Sheet
    """
    help = 'Syncs local db with data from project Google Sheet and Google Drive'

    def add_arguments(self, parser):
        parser.add_argument('--local', action='store_true')
        parser.add_argument('--redownload', action='store_true')
        parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        # pylint: disable=too-many-locals
        local_download = options.get('local')
        redownload = options.get('redownload')
        verbose = options.get('verbose')

        # redownload always does local_download
        if redownload and not local_download:
            local_download = True

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
            if file not in ['__init__.py', '__pycache__']:
                file_path = os.path.join(settings.MIGRATIONS_DIR, file)
                os.remove(file_path)
        print('Done!')

        # Rebuild database
        print_header('Rebuilding db from migrations...')
        call_command('makemigrations')
        call_command('migrate')
        print('Done!')

        # THIS IS JUST FOR PROTOTYPING NEVER EVER EVER EVER IN PRODUCTION do this
        User.objects.create_superuser('admin', password='adminadmin')

        # The order of these ranges matter. The Photographer model needs to have foreign keys to
        # the MapSquare database, so we add the Map Squares first
        spreadsheet_ranges = ['MapSquare', 'Photographer', 'Photo']

        print_header(f'''Will import ranges {", ".join(spreadsheet_ranges)}. (If nothing
          is happening, please try again.)''')

        # Create resource objects for interacting with the google API
        credentials = authorize_google_apps()
        sheets_service = build('sheets', 'v4', credentials=credentials)
        drive_service = build('drive', 'v3', credentials=credentials)

        # Call the Sheets API to get metadata values
        databases = call_sheets_api(spreadsheet_ranges, sheets_service)

        # Call Drive API to create a lookup dictionary for photo urls
        print_header('Getting the URL for all photos (This might take a couple of minutes)...')
        photo_url_lookup = create_lookup_dict(drive_service)

        if not databases:
            print_header('No data found.')
            return

        for model_name, values in zip(spreadsheet_ranges, databases):
            print_header(f'{model_name}: Importing these values from the spreadsheet')

            header = values[0]
            values_as_a_dict = [dict(zip(header, row)) for row in values[1:]]
            populate_database(
                model_name,
                values_as_a_dict,
                photo_url_lookup,
                drive_service,
                local_download,
                redownload,
                verbose,
            )
