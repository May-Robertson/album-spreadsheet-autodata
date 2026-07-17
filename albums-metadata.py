import google.auth
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def get_values(spreadsheet_id, range_name):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        rows = result.get("values", [])
        print(f"{len(rows)} rows retrieved")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

from itertools import islice
def get_info(data):
    d2 = dict(islice(data.items(), 10))
    print(d2)
    






spreadsheet_id = os.environ.get("SPREADSHEET_ID")
print("SPREADSHEET ID IS: ", spreadsheet_id)

# ALBUM NAMES
albums_dict = get_values(spreadsheet_id, "A:A")

# ARTIST NAMES
artists_dict = get_values(spreadsheet_id, "B:B")

# (['range', 'majorDimension', 'values'])
print(albums_dict['values'][7])


a = list(map(" ".join,albums_dict['values']))
b = list(map(" ".join,artists_dict['values']))

print(type(a[7]))



data = {key: value for key, value in zip(a, b)}
# print(data.values())
# print(data.keys())
get_info(data)






# First we need to read in the ALBUM NAME and ARTIST NAME
# then we search an API for
#   GENRE TAGS
#   maybe duration and numnber of tracks idk lets just see whats there


# FROM SPOTIFY API
# album type
# total tracks
# Release date
# Genres

# idk if i want these but maybe
# label
# popularity

# lastfm tags? lets see if spotify has album tags too