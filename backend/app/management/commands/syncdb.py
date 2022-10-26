"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

# Python standard library
import csv
import io
import os
import pickle
from textwrap import dedent
from pathlib import Path

# 3rd party
import cv2
import tqdm
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
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
    'https://www.googleapis.com/auth/drive',
]

# Our metadata spreadsheet lives here:
# https://docs.google.com/spreadsheets/d/1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I/edit#gid=0
METADATA_SPREADSHEET_ID = '1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I'
PHOTO_FOLDER_ID = '1aiY1nFJn6T7khu5dhIs3U2o8RdHBu6V7'

GOOGLE_API_CREDENTIALS_FILE = os.path.join(settings.SETTINGS_DIR, 'google_api_credentials.json')

# Sides of a photo
SIDES = ['cleaned', 'front', 'back', 'binder', 'thumbnail']

MODEL_NAME_TO_MODEL = {"Photo": Photo, "MapSquare": MapSquare, "Photographer": Photographer}


def authorize_google_apps(cli_auth):
    """
    Authorization flow for letting our application talk with the Google API

    cli_auth: if False, launches a browser and does the auth that way
              if True, gives instructions for copy/pasting a code
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
                GOOGLE_API_CREDENTIALS_FILE,
                SCOPES
            )
            if cli_auth:
                credentials = flow.run_console()
            else:
                credentials = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open(settings.GOOGLE_TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return credentials


def create_lookup_dict(drive_service):
    """
    Creates a quick look up dictionary to get the image URL using map square number and source name
    :param drive_service: the Google drive service
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
        map_square_dict = {'GOOGLE_DRIVE_MAP_SQUARE_FOLDER_ID': map_square['id']}
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
    create_thumbnails
):
    """
    Takes the map square folder and the photo number to dynamically adds the Google Drive urls
    into the model kwargs

    :param model_kwargs: Dictionary of keyword arguments to be used in creating the model
    :param map_square_number: the map square number
    :param map_square_folder: Dictionary of photo sources with keys of photo_number
    :param photo_number: The number of the desired photo in the map_square_folder
    :param drive_service: the Google Drive service
    :param local_download: should we download the photos locally if we do not have them already?
    :param redownload: should we redownload all photos locally?
    :param verbose: should we print verbose messages
    :param create_thumbnails: should we create thumbnails and upload it to Google Drive?
    """
    # TODO(ra): this needs refactoring out into component parts -- has gotten too bloated
    # pylint: disable=too-many-locals
    photo_drive_file_ids = map_square_folder.get(str(photo_number), '')
    if photo_drive_file_ids == '':
        return

    already_made_thumbnail = False

    for side in SIDES:

        drive_file_id = photo_drive_file_ids.get(f'{photo_number}_{side}.jpg', '')

        if drive_file_id:
            src_url = f"https://drive.google.com/uc?id={drive_file_id}&export=download"
            model_kwargs[f'{side}_src'] = src_url

            if side == 'thumbnail':
                continue  # we do not want to download thumbnails

            if local_download:
                request = drive_service.files().get_media(fileId=drive_file_id)
                Path(settings.AWS_S3_PHOTOS_DIR).mkdir(exist_ok=True)
                local_map_square_dir = Path(settings.AWS_S3_PHOTOS_DIR, map_square_number)
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

                # Create thumbnails only on the cleaned image
                if create_thumbnails and side in ['cleaned', 'front']:
                    thumbnail_id = photo_drive_file_ids.get(f'{photo_number}_thumbnail.jpg', '')
                    if thumbnail_id != '' or already_made_thumbnail:
                        already_made_thumbnail = True
                        return  # We already have that thumbnail in drive

                    # Create thumbnail from existing local file
                    img = cv2.imread(str(local_photo_path))
                    thumbnail_dims = (500, 500) # Is this a good thumbnail size?
                    thumbnail_img = cv2.resize(img, thumbnail_dims)
                    thumbnail_path = Path(local_map_square_dir, f'{photo_number}_thumbnail.jpg')
                    cv2.imwrite(str(thumbnail_path), thumbnail_img)

                    file_metadata = {'name': f'{photo_number}_thumbnail.jpg'}
                    media = MediaFileUpload(thumbnail_path, mimetype='image/jpeg')
                    # Uploads the thumbnail to your personal Drive
                    file = drive_service.files().create(body=file_metadata,
                                                        media_body=media,
                                                        fields='id').execute()
                    # Sets the parent of that file to the DH Paris 1970 Photo Folder in Google Drive
                    folder_id = map_square_folder['GOOGLE_DRIVE_MAP_SQUARE_FOLDER_ID']
                    drive_service.files().update(fileId=file.get('id'),
                                                 addParents=folder_id,
                                                 fields='id, parents').execute()

                    # Remove the temporary thumbnail image in local storage
                    os.remove(thumbnail_path)

                    already_made_thumbnail = True
        else:
            model_kwargs[f'{side}_src'] = None
            if side != 'thumbnail':
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


def create_map_square(map_square_count, mp_coords_dict, verbose):
    """
    Final step to create map squares. Factored out for now because it's called twice:
    once to create map squares that are explicitly specified in the spreadsheet,
    and a second time to create the missing map squares.

    TODO: refactor out the rest of the map square creation code out of populate_database into
    this function.
    """
    if map_square_count in mp_coords_dict.keys():
        temp_model_coordinates = mp_coords_dict[map_square_count]
    else:
        temp_model_coordinates = '0.0, 0.0'

    temp_model_kwargs = {
        'number': map_square_count,
        'name': f'map square {map_square_count}',
        'coordinates': temp_model_coordinates
    }

    if verbose:
        print(f'Creating map square with kwargs: {temp_model_kwargs}\n')

    model_instance = MapSquare(**temp_model_kwargs)
    model_instance.save()


def populate_database(
    model_name,
    values_as_a_dict,
    photo_url_lookup,
    drive_service,
    local_download,
    redownload,
    verbose,
    create_thumbnails
):
    """
    Adds model instances to the database based on the data imported from the google spreadsheet
    :param model_name: Name of the model to create an instance of
    :param values_as_a_dict: List of dictionaries representing spreadsheet rows in the form of
    { column names: cell values }
    :param photo_url_lookup: Dictionary of map square folders in the form of a dictionary
    :param drive_service: the Google Drive service
    :param local_download: should we download the photos locally if we do not have them already?
    :param redownload: should we redownload all photos locally?
    :param verbose: should we print verbose messages
    :param create_thumbnails: should we create thumbnails and upload it to Google Drive?
    """
    # TODO(ra): @refactor -- this function has gotten bloated bc the handling code
    # for the different models has diverged a lot over the course of the semester
    # Probably needs to be separated into a single function per model
    # Disabling these pylint checks now for expedience, but needs a cleanup
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    if model_name == "MapSquare":
        map_square_count = 1
        # Opens Map_Page_Output.csv and creates a dictionary with the map square
        # number as the key and the coordinates as the value
        map_page_output_path = Path(settings.BACKEND_DATA_DIR, 'map_page_output.csv')
        with open(map_page_output_path, encoding='utf-8') as mp_coords_csv:
            mp_coords_reader = csv.reader(mp_coords_csv)
            mp_coords_dict = {}
            for line in mp_coords_reader:
                try:
                    mp_coords_dict[int(line[0])] = line[1] + ", " + line[2]
                except ValueError:  # missing coords
                    continue

    for row in values_as_a_dict:
        # Filter column headers for model fields
        model_fields = MODEL_NAME_TO_MODEL[model_name]._meta.get_fields()
        model_field_names = [field.name for field in model_fields]

        model_kwargs = {}
        for header in row.keys():
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

        # Loads the appropriate coordinates from the CSV into the map Square
        # model. If they aren't there, it sets the coordinates into the default
        # values: '0.0, 0.0'
        if len(model_kwargs) != 0 and model_name == 'MapSquare':
            if model_kwargs['number'] in mp_coords_dict:
                model_kwargs['coordinates'] = mp_coords_dict[model_kwargs['number']]
            else:
                model_kwargs['coordinates'] = '0.0, 0.0'

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
            photographer_name = row.get('photographer_name', '').strip()

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
                    create_thumbnails
                )

            # Get the corresponding Photographer objects
            photographer_number = model_kwargs.get('photographer', None)
            if photographer_number is not None:
                model_kwargs['photographer'] = \
                    Photographer.objects.filter(number=photographer_number).first()

            if photographer_name != '' and 'photographer' not in model_kwargs:
                model_kwargs['photographer'] = \
                    Photographer.objects.filter(name=photographer_name).first()

        # Creates models for all of the MapSquares not listed in the spreadsheet between the
        # previous row and the current one
        if model_name == "MapSquare":
            while map_square_count != model_kwargs['number']:
                create_map_square(map_square_count, mp_coords_dict, verbose)
                map_square_count += 1
            map_square_count += 1

        if verbose:
            print(f'Creating {model_name} with kwargs: {model_kwargs}\n')

        model_instance = MODEL_NAME_TO_MODEL[model_name](**model_kwargs)
        model_instance.save()

        # When the last row in the spreadsheet is reached, creates MapSquare models for all
        # remaining, absent MapSquares (total: 1,755)
        if (model_name == 'MapSquare'
            and model_kwargs['number'] == int(values_as_a_dict[-1]['number'])
        ):
            while map_square_count <= 1755:
                create_map_square(map_square_count, mp_coords_dict, verbose)
                map_square_count += 1


class Command(BaseCommand):
    """
    Custom django-admin command used to sync the local db with data from project Google Sheet
    """
    help = 'Syncs local db with data from project Google Sheet and Google Drive'

    def add_arguments(self, parser):
        parser.add_argument('--local', action='store_true')
        parser.add_argument('--create_thumbnails', action='store_true')
        parser.add_argument('--redownload', action='store_true')
        parser.add_argument('--verbose', action='store_true')
        parser.add_argument('--quick', action='store_true')
        parser.add_argument('--cli_auth', action='store_true')

    def handle(self, *args, **options):
        # pylint: disable=too-many-locals
        local_download = options.get('local')
        create_thumbnails = options.get('create_thumbnails')
        redownload = options.get('redownload')
        verbose = options.get('verbose')
        quick = options.get('quick')
        cli_auth = options.get('cli_auth')

        if create_thumbnails and not local_download:
            local_download = True

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

        if quick:
            return

        # The order of these ranges matter. The Photographer model needs to have foreign keys to
        # the MapSquare database, so we add the Map Squares first
        spreadsheet_ranges = ['MapSquare', 'Photographer', 'Photo']

        print_header(f'''Will import ranges {", ".join(spreadsheet_ranges)}.\n # (If nothing
          is happening, please try again.)''')

        # Create resource objects for interacting with the google API
        credentials = authorize_google_apps(cli_auth)

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
            # Sorts the rows in the spreadsheet by the map square number [MapSquare ONLY]
            if model_name == 'MapSquare':
                values = [values[0]] + sorted(values[1:], key=lambda x: int(x[0]))
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
                create_thumbnails
            )
