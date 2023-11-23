from datetime import datetime, timedelta
from googleapiclient.discovery import build
import os
import pandas as pd
import mysql.connector

# Your MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Himanshu@1809',
}

# Database and table names
DATABASE_NAME = 'YouTube_Analytics'
TABLE_NAME = 'YouTube'

API_KEY = "AIzaSyBPwWMVAa5gdo6pPo7_mrQeZkKoZO5FCiY"  # Replace with your YouTube Data API Key

# Function to search for a YouTube channel by name
def search_channel_by_name(youtube, channel_name):
    request = youtube.search().list(
        q=channel_name,
        type="channel",
        part="id"
    )
    response = request.execute()

    if 'items' in response:
        # Assuming the first result is the desired channel
        channel_id = response['items'][0]['id']['channelId']
        return channel_id
    else:
        print(f"No channel found with the name '{channel_name}'.")
        return None

# Function to get channel statistics
def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()

    return response['items']

# Function to get a list of video IDs from the channel's uploads playlist
def get_video_list(youtube, upload_id, date_range):
    video_list = []

    # Initialize max_results
    max_results = None

    # Calculate the date in the past and set max_results based on the user's choice
    if date_range == '1_week':
        past_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
    elif date_range == '15_days':
        past_date = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%dT%H:%M:%SZ')
    elif date_range == '30_days':
        past_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
    elif date_range == 'last_10_videos':
        max_results = 10
        past_date = None  # Get all videos
    elif date_range == 'last_50_videos':
        max_results = 50
        past_date = None  # Get all videos
    elif date_range == 'all_videos':
        max_results = None  # Get all videos
        past_date = None  # Get all videos
    else:
        print("Invalid date range choice.")
        return []

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=upload_id,
        maxResults=max_results if max_results is not None else 50
    )

    next_page = True
    while next_page:
        response = request.execute()
        data = response['items']

        for video in data:
            published_date = video['contentDetails']['videoPublishedAt']

            # Check if the video was published within the date range
            if past_date is None or published_date >= past_date:
                video_id = video['contentDetails']['videoId']
                if video_id not in video_list:
                    video_list.append(video_id)

        if 'nextPageToken' in response.keys():
            next_page = True
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=upload_id,
                pageToken=response['nextPageToken'],
                maxResults=max_results if max_results is not None else 50
            )
        else:
            next_page = False

    return video_list


# Function to get details of videos
def get_video_details(youtube, video_list):
    stats_list = []

    for i in range(0, len(video_list), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_list[i:i + 50]
        )

        data = request.execute()
        for video in data['items']:
            title = video['snippet']['title']
            published = video['snippet']['publishedAt']
            description = video['snippet']['description']

            # Get video duration in ISO 8601 format
            duration = video['contentDetails']['duration']

            # Check if 'tags' field exists and handle it gracefully
            if 'tags' in video['snippet']:
                tags = video['snippet']['tags']
                tag_count = len(tags)
            else:
                tags = []
                tag_count = 0

            view_count = video['statistics'].get('viewCount', 0)
            like_count = video['statistics'].get('likeCount', 0)
            dislike_count = video['statistics'].get('dislikeCount', 0)
            comment_count = video['statistics'].get('commentCount', 0)
            stats_dict = dict(
                title=title,
                description=description,
                published=published,
                tag_count=tag_count,
                view_count=view_count,
                like_count=like_count,
                dislike_count=dislike_count,
                comment_count=comment_count,
                duration=duration  # Added video duration
            )
            stats_list.append(stats_dict)

    return stats_list
# Ask the user to enter a channel name
#channel_name = input("Enter the name of the YouTube channel: ")
channel_name = "soul regaltos"

# Initialize the MySQL connection
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Create the MySQL database if it doesn't exist
try:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    conn.commit()
    print(f"Database '{DATABASE_NAME}' created successfully!!!")
except mysql.connector.Error as e:
    print(f"Error creating the database: {e}")

# Use the created database
cursor.execute(f"USE {DATABASE_NAME}")

# Create the MySQL table if it doesn't exist
create_table_query = f'''
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    Title VARCHAR(255),
    Description TEXT,
    Published TEXT,
    Tag_Count INT,
    View_Count INT,
    Like_Count INT,
    Dislike_Count INT,
    Comment_Count INT,
    Reactions INT,
    Duration VARCHAR(10)
);
'''
try:
    cursor.execute(create_table_query)
    conn.commit()
    print(f"Created table '{TABLE_NAME}'")
except mysql.connector.Error as e:
    print(f"Error creating the table: {e}")

# Initialize the YouTube API
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Search for the channel by name
CHANNEL_ID = search_channel_by_name(youtube, channel_name)

if CHANNEL_ID:
    # Get channel statistics
    channel_stats = get_channel_stats(youtube, CHANNEL_ID)
    upload_id = channel_stats[0]['contentDetails']['relatedPlaylists']['uploads']

    # # Ask the user to choose a date range
    # print("Choose a date range:")
    # print("1. Last 1 week")
    # print("2. Last 15 days")
    # print("3. Last 30 days")
    # print("4. Last 10 videos")
    # print("5. Last 50 videos")
    # print("6. All videos")
    #date_range_choice = input("Enter the option (1-6): ")
    date_range_choice = '3'

    if date_range_choice in ['1', '2', '3', '4', '5', '6']:
        date_ranges = {
            '1': '1_week',
            '2': '15_days',
            '3': '30_days',
            '4': 'last_10_videos',
            '5': 'last_50_videos',
            '6': 'all_videos'
        }
        date_range = date_ranges[date_range_choice]
        video_list = get_video_list(youtube, upload_id, date_range)
        video_data = get_video_details(youtube, video_list)

        df = pd.DataFrame(video_data)
        df['title_length'] = df['title'].str.len()
        df["view_count"] = pd.to_numeric(df["view_count"])
        df["like_count"] = pd.to_numeric(df["like_count"])
        df["dislike_count"] = pd.to_numeric(df["dislike_count"])
        df["comment_count"] = pd.to_numeric(df["comment_count"])
        df["reactions"] = df["like_count"] + df["dislike_count"] + df["comment_count"] + df["comment_count"]

        # Save data to a CSV file
        file_name = f"{channel_name}.csv"
        df.to_csv(file_name, index=False)

        # Connect to MySQL and save the data to a table
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Use the created database
            cursor.execute(f"USE {DATABASE_NAME}")

            # Clear all rows from the MySQL table
            cursor.execute('DELETE FROM YouTube;')
            conn.commit()

            # Create a MySQL table if it doesn't exist
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS YouTube (
                Title VARCHAR(255),
                Description TEXT,
                Published TEXT,
                Tag_Count INT,
                View_Count INT,
                Like_Count INT,
                Dislike_Count INT,
                Comment_Count INT,
                Reactions INT,
                Duration VARCHAR(10)
            );
            '''
            cursor.execute(create_table_query)
            conn.commit()

            # Insert data into the MySQL table
            for row in df.itertuples(index=False):
                cursor.execute(
                    'INSERT INTO YouTube (Title, Description, Published, Tag_Count, View_Count, Like_Count, Dislike_Count, Comment_Count, Reactions, Duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (row.title, row.description, row.published, row.tag_count, row.view_count, row.like_count,
                     row.dislike_count, row.comment_count, row.reactions, row.duration)
                )
            conn.commit()

            print(f"Data saved as '{file_name}' and inserted into the MySQL table 'YouTube'.")

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

    else:
        print("Invalid date range choice. Please enter a valid option (1-6).")