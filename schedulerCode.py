import requests
import urllib.parse
from datetime import datetime, timedelta
import mysql.connector

def DAILYMOTION ():
    # Function to fetch video details for a public user within the last 30 days
    def get_public_user_video_data(username):
        encoded_username = urllib.parse.quote(username, safe='')  # URL encode the username
        url = f'https://api.dailymotion.com/user/{encoded_username}/videos'

        # Calculate the timestamp for 30 days ago
        thirty_days_ago = (datetime.now() - timedelta(days=30)).timestamp()

        params = {
            'fields': 'id,title,views_total,likes_total,duration,tags,created_time,rating',
            'limit': 100,  # You can adjust the limit as needed
        }

        video_data = []
        while url:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                videos = data.get('list', [])

                # Filter videos created within the last 30 days
                filtered_videos = [video for video in videos if video.get('created_time') >= thirty_days_ago]

                video_data.extend(filtered_videos)

                url = data.get('paging', {}).get('next')
            else:
                print(f'Error fetching video data: {response.status_code} - {response.text}')
                break

        return video_data


    # Public user's Dailymotion username (without spaces or special characters)
    username = "XboxViewTV"

    # MySQL connection configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Himanshu@1809',
    }
    db_name = "dailymotion"


    # Function to create the database and fetch video details for a public user within the last 30 days
    def create_and_use_database(db_name):
        # Establish a MySQL connection without specifying a database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        cursor.execute(create_db_query)

        # Use the created database
        use_db_query = f"USE {db_name}"
        cursor.execute(use_db_query)

        # Close the connection to create the database and switch to it
        conn.close()

        # Re-establish the connection with the specified database
        db_config['database'] = db_name
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Clear all rows from the MySQL table
        cursor.execute('DELETE FROM dailymotion_videos;')
        conn.commit()

        # Create a table for video data in MySQL
        create_table_query = """
        CREATE TABLE IF NOT EXISTS dailymotion_videos (
            title TEXT,
            views_total INT,
            likes_total INT,
            rating FLOAT,
            duration INT,
            tags TEXT,
            created_time DATETIME
        )
        """
        cursor.execute(create_table_query)

        # Fetch video data for the public user within the last 30 days
        video_data = get_public_user_video_data(username)

        if video_data:
            # Insert video data into the MySQL table
            insert_query = """
            INSERT INTO dailymotion_videos (title, views_total, likes_total, rating, duration, tags, created_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            for video in video_data:
                # Generate a UUID for the video as the video_id
                title = video.get('title')
                views_total = video.get('views_total')
                likes_total = video.get('likes_total')
                rating = video.get('rating', None)
                duration = video.get('duration')
                tags = ', '.join(video.get('tags', []))
                created_time = datetime.fromtimestamp(video.get('created_time')).strftime('%Y-%m-%d %H:%M:%S')

                data = (title, views_total, likes_total, rating, duration, tags, created_time)
                cursor.execute(insert_query, data)

            conn.commit()
            print(
                f"Video data for {username} created in the last 30 days has been successfully inserted into the MySQL database.")

        # Close the database connection
        conn.close()


    # Create and use the 'dailymotion' database
    create_and_use_database('dailymotion')


def TWITCH():
    import requests
    import mysql.connector

    # Defining the username (Twitch channel name)
    #username = input("Enter channel name: ")
    username = 'xboxviewTV'
    # Connect to the MySQL database
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Himanshu@1809"
        )

        # Create the "twitch" database if it doesn't exist
        create_db_query = "CREATE DATABASE IF NOT EXISTS twitch;"
        cursor = conn.cursor()
        cursor.execute(create_db_query)
        conn.commit()
        conn.close()

        # Reconnect to the "twitch" database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Himanshu@1809",
            database="twitch"
        )

        # Defining the API endpoint and headers for getting the broadcaster ID
        url_users = 'https://api.twitch.tv/helix/users'
        params_users = {'login': username}
        headers_users = {
            'Authorization': 'Bearer sgmzzxu0ruk860hex7fcc8a6z37exe',
            'Client-Id': 'emf8vrnqgh7qj5g3fj1tcq6izpl8r8',
        }
        # Making the API request to get the broadcaster ID
        response_users = requests.get(url_users, params=params_users, headers=headers_users)
        # Checking if the request was successful
        if response_users.status_code == 200:
            data_users = response_users.json()
            broadcaster_id = data_users['data'][0]['id']
            # Defining the API endpoint and headers for getting the user's videos
            url_videos = 'https://api.twitch.tv/helix/videos'
            params_videos = {'user_id': broadcaster_id}
            headers_videos = {
                'Authorization': 'Bearer sgmzzxu0ruk860hex7fcc8a6z37exe',
                'Client-Id': 'emf8vrnqgh7qj5g3fj1tcq6izpl8r8',
            }
            # Making the API request to get the user's videos
            response_videos = requests.get(url_videos, params=params_videos, headers=headers_videos)

            # Checking if the request was successful
            if response_videos.status_code == 200:
                videos_data = response_videos.json()
                cursor = conn.cursor()
                # Create a table to store video details if it doesn't exist
                create_table_query = "CREATE TABLE IF NOT EXISTS twitch_videos (id INT AUTO_INCREMENT PRIMARY KEY,username varchar(255), video_id VARCHAR(255), title VARCHAR(255), description TEXT, url VARCHAR(255), published_at varchar(255), views INT, language VARCHAR(255), duration varchar(255));"
                cursor.execute(create_table_query)

                # Iterate through the videos and store their details in the database
                for video in videos_data['data']:
                    video_id = video['id']
                    video_details = {
                        "Video ID": video["id"],
                        'Title': video['title'],
                        'Description': video['description'],
                        'URL': video['url'],
                        'Published at': video['published_at'],
                        'Views': video['view_count'],
                        'Language': video['language'],
                        'Duration': video['duration'],
                    }

                    # Check if a record for this video already exists in the database
                    check_query = "SELECT * FROM twitch_videos WHERE video_id = %s;"
                    cursor.execute(check_query, (video_details['Video ID'],))
                    existing_record = cursor.fetchone()

                    if existing_record:
                        # If a record exists, update it with the new details
                        update_query = "UPDATE twitch_videos SET username=%s, title = %s, description = %s, url = %s, published_at = %s, views = %s, language = %s, duration = %s WHERE video_id = %s;"
                        cursor.execute(update_query, (
                            username,
                            video_details['Title'], video_details['Description'], video_details['URL'],
                            video_details['Published at'], video_details['Views'], video_details['Language'],
                            video_details['Duration'], video_details['Video ID']
                        ))
                    else:
                        # If no record exists, insert a new record for this video
                        insert_query = "INSERT INTO twitch_videos (username,video_id, title, description, url, published_at, views, language, duration) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s);"
                        cursor.execute(insert_query, (
                            username,
                            video_details['Video ID'], video_details['Title'], video_details['Description'],
                            video_details['URL'], video_details['Published at'], video_details['Views'],
                            video_details['Language'], video_details['Duration']
                        ))

                conn.commit()

                # Close the database connection

                print('Twitch video details saved to the MySQL database.')
            else:
                print(f'Error: {response_videos.status_code} - {response_videos.text}')
        else:
            print(f'Error: {response_users.status_code} - {response_users.text}')

        # Define the API endpoint and headers for getting the broadcaster ID
        url_users = 'https://api.twitch.tv/helix/users'
        params_users = {'login': username}
        headers_users = {
            'Authorization': 'Bearer sgmzzxu0ruk860hex7fcc8a6z37exe',
            'Client-Id': 'emf8vrnqgh7qj5g3fj1tcq6izpl8r8',
        }

        # Making the API request to get the broadcaster ID
        response_users = requests.get(url_users, params=params_users, headers=headers_users)

        # Checking if the request was successful
        if response_users.status_code == 200:
            data_users = response_users.json()
            broadcaster_id = data_users['data'][0]['id']
            # Store the broadcaster ID in the twitch_user dictionary
            twitch_user = {
                "Broadcaster ID": broadcaster_id,
            }
            # Defining the API endpoint and headers for getting the followers
            url_followers = 'https://api.twitch.tv/helix/channels/followers'
            params_followers = {'broadcaster_id': broadcaster_id}
            headers_followers = {
                'Authorization': 'Bearer sgmzzxu0ruk860hex7fcc8a6z37exe',
                'Client-Id': 'emf8vrnqgh7qj5g3fj1tcq6izpl8r8',
            }
            # Making the API request to get the followers
            response_followers = requests.get(url_followers, params=params_followers, headers=headers_followers)
            # Checking if the request was successful
            if response_followers.status_code == 200:
                data_followers = response_followers.json()

                # Add followers data to the twitch_user dictionary
                twitch_user["Followers"] = data_followers["total"]

                cursor = conn.cursor()
                # Create a table to store Twitch user data if it doesn't exist
                create_table_query = "CREATE TABLE IF NOT EXISTS twitch_users (id INT AUTO_INCREMENT PRIMARY KEY,username varchar(255), broadcaster_id VARCHAR(255), followers INT);"
                cursor.execute(create_table_query)

                # Check if a record for this user already exists in the database
                check_query = "SELECT * FROM twitch_users WHERE broadcaster_id = %s;"
                cursor.execute(check_query, (twitch_user["Broadcaster ID"],))
                existing_record = cursor.fetchone()

                if existing_record:
                    # If a record exists, update it with the new follower count
                    update_query = "UPDATE twitch_users SET followers = %s WHERE broadcaster_id = %s;"
                    cursor.execute(update_query, (twitch_user["Followers"], twitch_user["Broadcaster ID"]))
                else:
                    # If no record exists, insert a new record for this user
                    insert_query = "INSERT INTO twitch_users (username,broadcaster_id, followers) VALUES (%s,%s, %s);"
                    cursor.execute(insert_query, (username, twitch_user["Broadcaster ID"], twitch_user["Followers"]))

                conn.commit()

                # Close the database connection
                conn.close()

                print('Twitch user data saved to the MySQL database.')
            else:
                print(f'Error: {response_followers.status_code} - {response_followers.text}')
        else:
            print(f'Error: {response_users.status_code} - {response_users.text}')

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")



def YOUTUBE():
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
    # channel_name = input("Enter the name of the YouTube channel: ")
    channel_name = "xboxviewtv"

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
        # # date_range_choice = input("Enter the option (1-6): ")
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

            # # Save data to a CSV file
            # file_name = f"{channel_name}.csv"
            # df.to_csv(file_name, index=False)

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

                print(f"Data inserted into the MySQL table 'YouTube'.")

            except mysql.connector.Error as e:
                print(f"Error: {e}")

            finally:
                cursor.close()
                conn.close()

        else:
            print("Invalid date range choice. Please enter a valid option (1-6).")

DAILYMOTION()
TWITCH()
YOUTUBE()