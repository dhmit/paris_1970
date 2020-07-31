"""
Django management command syncdb

Syncs local db with data from project Google Sheet

TODO(ra): link Google Sheet here
"""


import pickle
import os.path

from django.core.management.base import BaseCommand
from django.conf import settings

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
METADATA_SPREADSHEET_ID = '1R4zBXLwM08yq_d4R9_JrDSGThpoaI46_Vmn9tDu8w9I'
SAMPLE_RANGE_NAME = 'Sheet1!A1:A2'


class Command(BaseCommand):
    help = 'Syncs local db with data from project Google Sheet'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Hello, world!'))

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
            sheet.values().get(spreadsheetId=METADATA_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        result = get_values_cmd.execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            for row in values:
                print(row)
