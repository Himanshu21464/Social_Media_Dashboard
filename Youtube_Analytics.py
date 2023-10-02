import os
import csv
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'Youtube_Analytics.json'
CREDENTIALS_FILE = 'youtube_analytics_credentials.pickle'  # Name of the file to store/load credentials
CSV_FILE = 'youtube_analytics_data.csv'  # Name of the CSV file to save data

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
    return response

def save_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header
        header = data.get('columnHeaders', [])
        if header:
            header_row = [header_item['name'] for header_item in header]
            csv_writer.writerow(header_row)

        # Write data rows
        rows = data.get('rows', [])
        for row in rows:
            csv_writer.writerow(row)

if __name__ == '__main__':
    # Disable OAuthlib's HTTPs verification when running locally.
    # *DO NOT* leave this option enabled when running in production.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    youtubeAnalytics = get_authenticated_service()
    response_data = execute_api_request(
        youtubeAnalytics.reports().query,
        ids='channel==MINE',
        startDate='2020-01-01',
        endDate='2023-10-01',
        metrics='estimatedMinutesWatched,views,likes,comments,dislikes,shares,subscribersGained',
        dimensions='day',
        sort='day'
    )

    # Save the data to a CSV file
    save_to_csv(response_data, CSV_FILE)

    print(f'Data saved to {CSV_FILE}')
