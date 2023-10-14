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
    'database': 'YouTube_Analytics'
}

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

    # Calculate the date in the past based on the user's choice
    if date_range == '1_month':
        past_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
    elif date_range == '1_week':
        past_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m:%dT%H:%M:%SZ')
    elif date_range == '15_days':
        past_date = (datetime.now() - timedelta(days=15)).strftime('%Y-%m:%dT%H:%M:%SZ')
    else:
        past_date = None

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=upload_id,
        maxResults=50
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
                maxResults=50
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
                comment_count=comment_count
            )
            stats_list.append(stats_dict)

    return stats_list

# Ask the user to enter a channel name
channel_name = input("Enter the name of the YouTube channel: ")

# Initialize the YouTube API
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Search for the channel by name
CHANNEL_ID = search_channel_by_name(youtube, channel_name)

if CHANNEL_ID:
    # Get channel statistics
    channel_stats = get_channel_stats(youtube, CHANNEL_ID)
    upload_id = channel_stats[0]['contentDetails']['relatedPlaylists']['uploads']

    # Ask the user to choose a date range
    date_range = input("Choose a date range (1_month, 1_week, 15_days): ")

    if date_range in ['1_month', '1_week', '15_days']:
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
                Reactions INT
            );
            '''
            cursor.execute(create_table_query)
            conn.commit()

            # Insert data into the MySQL table
            for row in df.itertuples(index=False):
                cursor.execute(
                    'INSERT INTO YouTube (Title, Description, Published, Tag_Count, View_Count, Like_Count, Dislike_Count, Comment_Count, Reactions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (row.title, row.description, row.published, row.tag_count, row.view_count, row.like_count, row.dislike_count, row.comment_count, row.reactions)
                )
            conn.commit()

            print(f"Data saved as '{file_name}' and inserted into the MySQL table 'youtube_data'.")

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

    else:
        print("Invalid date range choice. Please choose from 1_month, 1_week, or 15_days.")
