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
        spreadsheet_range = 'Sheet1!A:D'

        print_header(f'Will import range {spreadsheet_range}')

        # TODO(ra): clean up authentication pickling routines --
        # do we even want to cache auth to disk? probably not...

        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_API_CREDENTIALS_FILE,
            SCOPES
        )
        creds = flow.run_local_server(port=8080)

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
            header = values[0]
            values_as_a_dict = [{header[i]: entry for i, entry in enumerate(row)}
                                for row in values[1:]]

            for row in values_as_a_dict:
                print(row)
                photo = Photo(
                    title=row["title"],
                    front_src=row["front_src"],
                    back_src=row["back_src"],
                    alt=row["alt"],
                )
                photo.save()
