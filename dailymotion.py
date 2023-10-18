import requests
import urllib.parse
from datetime import datetime, timedelta
import mysql.connector

# Public user's Dailymotion username (without spaces or special characters)
username = "XboxViewTV"

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shi@1862000',
    'database': 'dailymotion'
}

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

# Establish a MySQL connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

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
    INSERT INTO dailymotion_videos ( title, views_total, likes_total, rating, duration, tags, created_time)
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
    print(f"Video data for {username} created in the last 30 days has been successfully inserted into the MySQL database.")

# Close the database connection
conn.close()