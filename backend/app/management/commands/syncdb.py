"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""


import pickle
import os
import tqdm
from textwrap import dedent

from django.contrib.auth.models import User
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from app.models import Photo, MapSquare, Photographer

# The scope of our access to the Google Sheets Account
# TODO: reduce this scope, if possible, to only access a single specified sheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly']

# Our metadata spreadsheet lives here:
# https://docs.google.com/spreadsheets/d/1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I/edit#gid=0
METADATA_SPREADSHEET_ID = '1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I'


def print_header(header_str):
    print(dedent(f'''
        ################################################################################
        # {header_str}
        ################################################################################
    '''))


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
            image['name']: f"https://drive.google.com/file/d/{image['id']}/view?usp=sharing"
            for image in images
        }
    return lookup_dict


MODEL_NAME_TO_MODEL = {"Photo": Photo, "MapSquare": MapSquare, "Photographer": Photographer}


class Command(BaseCommand):
    help = 'Syncs local db with data from project Google Sheet'

    def add_arguments(self, parser):
        parser.add_argument('--range', action='store', type=str)

    def handle(self, *args, **options):
        # The order of these ranges matter. The Photographer model needs to have foreign keys to
        # the MapSquare database, so we add the Map Squares first
        spreadsheet_ranges = ['MapSquare', 'Photographer', 'Photo']

        print_header(f'''Will import ranges {", ".join(spreadsheet_ranges)}. (If nothing
          is happening, please try again.)''')

        # Settings for pickle file

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(settings.GOOGLE_TOKEN_FILE):
            with open(settings.GOOGLE_TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.GOOGLE_API_CREDENTIALS_FILE,
                    SCOPES
                )
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open(settings.GOOGLE_TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        sheets_service = build('sheets', 'v4', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        print_header('Getting the URL for all photos (This might take a couple of minutes)...')
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

        if os.path.exists(settings.DB_PATH):
            print_header('Deleting existing db...')
            os.remove(settings.DB_PATH)
            print('\nDone!')

        print_header('Rebuilding db from migrations...')
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
                if model_name == 'Photo' or model_name == 'Photographer':
                    map_square_name = row.get('map_square', '')
                    # Returns the object that matches or None if there is no match
                    row['map_square'] = \
                        MapSquare.objects.filter(name=map_square_name).first()

                if model_name == 'Photo':
                    map_square_num = row.get('map_square_number', '')
                    front_src = row.get('front_src', '')
                    back_src = row.get('back_src', '')
                    map_square_folder = photo_url_lookup.get(map_square_num, '')
                    if map_square_folder:
                        row['front_src'] = map_square_folder.get(front_src, '')
                        row['back_src'] = map_square_folder.get(back_src, '')
                    photographer_name = row.get('photographer', '')
                    row['photographer'] = \
                        Photographer.objects.filter(name=photographer_name).first()
                print(row)
                # model_instance = MODEL_NAME_TO_MODEL[model_name](**row)
                # model_instance.save()
