import requests
import json

# Get the channel name from the user
channel_name = input("Enter the channel name: ")

# Defining the API endpoint and headers for getting the broadcaster id
url_users = 'https://api.twitch.tv/helix/users'
params_users = {'login': channel_name}
headers_users = {
    'Authorization': 'Bearer sgmzzxu0ruk860hex7fcc8a6z37exe',
    'Client-Id': 'emf8vrnqgh7qj5g3fj1tcq6izpl8r8',
}

# Making the API request to get the broadcaster id
response_users = requests.get(url_users, params=params_users, headers=headers_users)

# Checking if the request was successful
if response_users.status_code == 200:
    data_users = response_users.json()
    broadcaster_id = data_users['data'][0]['id']

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
        
        # Define the file name
        get_followers = 'temp.json'

        # Writing the raw JSON data to a JSON file
        with open(get_followers, 'w', encoding='utf-8') as jsonfile:
            json.dump(data_followers, jsonfile, ensure_ascii=False, indent=4)

        print(f'Followers details saved to {get_followers}')
    else:
        print(f'Error: {response_followers.status_code} - {response_followers.text}')
else:
    print(f'Error: {response_users.status_code} - {response_users.text}')







#Getting Channel details
url = 'https://api.twitch.tv/helix/channels'
params = {'broadcaster_id': broadcaster_id}
# Define headers with your OAuth2 bearer token and client ID
headers = {
    'Authorization': 'Bearer sgmzzxu0ruk860hex7fcc8a6z37exe',
    'Client-Id': 'emf8vrnqgh7qj5g3fj1tcq6izpl8r8'
}

# Make the GET request     https://api.twitch.tv/helix/channels?broadcaster_id=37402112' \
response = requests.get(url, params=params, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Define the CSV file name
    details = 'temp.json'

    # Write the raw JSON data to a JSON file
    with open(details, 'a', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

    print(f'Channel details saved to {details}')
else:
    print(f'Error: {response.status_code} - {response.text}')




#Getting videos based on views--------------------------------------------------------------------------------------------------
# Define the API endpoint and headers
url = 'https://api.twitch.tv/helix/clips'
params = {
    'broadcaster_id': broadcaster_id,
    'first': '5',
}
headers = {
    'Authorization': 'Bearer sgmzzxu0ruk860hex7fcc8a6z37exe',
    'Client-Id': 'emf8vrnqgh7qj5g3fj1tcq6izpl8r8',
}

# Make the API request
response = requests.get(url, params=params, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Define the CSV file name
    csv_filename = 'temp.json'

    # Write the raw JSON data to a JSON file
    with open(csv_filename, 'a', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

    print(f'Videos details saved to {csv_filename}')
else:
    print(f'Error: {response.status_code} - {response.text}')
#-------------------------------------------------------------------------------------------------------------------------------