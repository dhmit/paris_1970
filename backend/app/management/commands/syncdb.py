"""
Django management command syncdb

Syncs local db with data from project Google Sheet
s"""


import pickle
import os
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
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Our metadata spreadsheet lives here:
# https://docs.google.com/spreadsheets/d/1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I/edit#gid=0
METADATA_SPREADSHEET_ID = '1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I'


def print_header(header_str):
    print(dedent(f'''
        ################################################################################
        # {header_str}
        ################################################################################
    '''))


class Command(BaseCommand):
    help = 'Syncs local db with data from project Google Sheet'

    def add_arguments(self, parser):
        parser.add_argument('--range', action='store', type=str)

    def handle(self, *args, **options):
        spreadsheet_ranges = ['MapSquare!A:B', 'Photographer!A:D', 'Photo!A:F']

        print_header(f'Will import ranges {", ".join(spreadsheet_ranges)}')

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

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        databases = []
        sheet = service.spreadsheets()
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
        else:
            for m, values in enumerate(databases):
                model_name = spreadsheet_ranges[m].split('!')[0]
                print_header(f'{model_name}: Importing these values from the spreadsheet')

                header = values[0]
                values_as_a_dict = [{header[i]: entry for i, entry in enumerate(row)}
                                    for row in values[1:]]

                for row in values_as_a_dict:
                    print(row)
                    if model_name == 'Photo' or model_name == 'Photographer':
                        map_square_name = row['map_square_obj']
                        row['map_square_obj'] = MapSquare.objects.get(name=map_square_name)
                    if model_name == 'Photo':
                        photographer_name = row['photographer_obj']
                        row['photographer_obj'] = Photographer.objects.get(name=photographer_name)
                    model_instance = eval(f'{model_name}(**row)')
                    model_instance.save()
