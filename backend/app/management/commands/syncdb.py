"""
Django management command syncdb

Syncs local db with data from project Google Sheet

TODO(ra): link Google Sheet here
"""


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

from app.models import Photo

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
        # TODO: get the range dynamically -- iterate until we hit a blank row
        maybe_range = options.get('range', '')
        if maybe_range:
            # TODO: validate that this will work
            spreadsheet_range = 'Sheet1!' + maybe_range
        else:
            spreadsheet_range = 'Sheet1!A2:D5'

        print_header(f'Will import range {spreadsheet_range}')

        # TODO(ra): clean up authentication pickling routines --
        # do we even want to cache auth to disk? probably not...

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
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
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        get_values_cmd = \
            sheet.values().get(spreadsheetId=METADATA_SPREADSHEET_ID, range=spreadsheet_range)
        result = get_values_cmd.execute()
        values = result.get('values', [])

        # TODO(ra): handle case where the server is running and using the db
        if os.path.exists(settings.DB_PATH):
            print_header('Deleting existing db...')
            os.remove(settings.DB_PATH)
            print('\nDone!')

        print_header('Rebuilding db from migrations...')
        call_command('migrate')
        print('Done!')

        # THIS IS JUST FOR PROTOTYPING NEVER EVER EVER EVER IN PRODUCTION do this
        superuser = User.objects.create_superuser('admin', password='adminadmin')

        if not values:
            print_header('No data found.')
        else:
            print_header('Importing these values from the spreadsheet')

            # TODO: can we get the data as a dictionary per row (with a header) rather than a list?
            for row in values:
                print(row)
                photo = Photo(
                    title=row[0],
                    front_src=row[1],
                    back_src=row[2],
                    alt=row[3],
                )
                photo.save()
