import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings
from oauth2client.client import flow_from_clientsecrets


# The scope of our access to the Google Sheets Account
# TODO: reduce this scope, if possible, to only access a single specified sheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly']


def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))


def load_creds(scopes):
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
                scopes
            )
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open(settings.GOOGLE_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds
