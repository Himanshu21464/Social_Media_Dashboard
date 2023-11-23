import mysql.connector
from collections import Counter
import re

# Your MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Himanshu@1809',
    'database': 'global_database',
}

# Create a MySQL connection
conn = mysql.connector.connect(**DB_CONFIG)

try:
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # SQL command to select video titles, platform, and view count from your table
    sql_command = "SELECT Title, Platform, View_Count FROM social_media_Dashboard"

    # Execute the SQL command
    cursor.execute(sql_command)

    # Fetch all the rows
    result = cursor.fetchall()

    # Extract data into a list of dictionaries
    data = [{'title': row[0], 'platform': row[1], 'view_count': row[2]} for row in result]

    # Function to clean and split title into words
    def get_words(title):
        return re.findall(r'\b\w+\b', title)

    # Count word frequencies
    word_freq = Counter(word for entry in data for word in get_words(entry['title']))

    # Group entries by the number of common words (in descending order)
    grouped_entries = {tuple(sorted([word for word in get_words(entry['title']) if word in word_freq])): [] for entry in data}
    for entry in data:
        common_words = tuple(sorted([word for word in get_words(entry['title']) if word in word_freq]))
        grouped_entries[common_words].append(entry)

    # Print grouped entries with common words, titles, platform, and view count
    for words, entries in grouped_entries.items():
        num_common_words = len(words)
        common_words_str = ', '.join(words)

        print(f"\n\n-----------------Common Words ({num_common_words} words): {common_words_str}--------------------")
        # print("-------------------------------------------------------------------------------------------------")
        for entry in entries:
            print(f"  - Title: {entry['title']}, Platform: {entry['platform']}, View Count: {entry['view_count']}")

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
