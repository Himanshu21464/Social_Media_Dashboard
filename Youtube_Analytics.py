import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'Youtube_Analytics.json'
CREDENTIALS_FILE = 'youtube_analytics_credentials.pickle'  # Name of the file to store/load credentials

def get_authenticated_service():
    # Try to load credentials from a file
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'rb') as token:
            credentials = pickle.load(token)
    else:
        # If credentials file doesn't exist, perform OAuth2 authentication
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        # Save the credentials to a file for future runs
        with open(CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(credentials, token)
    # Build the service using the obtained credentials
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def execute_api_request(client_library_function, **kwargs):
    response = client_library_function(**kwargs).execute()
    print(response)

if __name__ == '__main__':
    # Disable OAuthlib's HTTPs verification when running locally.
    # *DO NOT* leave this option enabled when running in production.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    youtubeAnalytics = get_authenticated_service()
    execute_api_request(
        youtubeAnalytics.reports().query,
        ids='channel==MINE',
        startDate='2020-01-01',
        endDate='2022-10-01',
        metrics='estimatedMinutesWatched,views,likes,subscribersGained',
        dimensions='day',
        sort='day'
    )
