import requests
import mysql.connector

# Defining the username (Twitch channel name)
username = input("Enter channel name: ")
# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="siddharth",
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
                "Video ID" : video["id"],
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
            cursor.execute(insert_query, (username,twitch_user["Broadcaster ID"], twitch_user["Followers"]))

        conn.commit()

        # Close the database connection
        conn.close()

        print('Twitch user data saved to the MySQL database.')
    else:
        print(f'Error: {response_followers.status_code} - {response_followers.text}')
else:
    print(f'Error: {response_users.status_code} - {response_users.text}')



