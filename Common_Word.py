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

    # SQL command to select video titles from your table (replace 'your_table' with the actual table name)
    sql_command = "SELECT Title FROM social_media_Dashboard"

    # Execute the SQL command
    cursor.execute(sql_command)

    # Fetch all the rows
    result = cursor.fetchall()

    # Extract titles into a list
    video_titles = [row[0] for row in result]

    # Function to clean and split title into words
    def get_words(title):
        return re.findall(r'\b\w+\b', title)

    # Count word frequencies
    word_freq = Counter(word for title in video_titles for word in get_words(title))

    # Group titles by most common words
    grouped_titles = {word: [] for word, _ in word_freq.most_common()}
    for title in video_titles:
        for word in get_words(title):
            if word in grouped_titles:
                grouped_titles[word].append(title)

    # Print grouped titles
    for word, titles in grouped_titles.items():
        print(f"Word: {word}")
        for title in titles:
            print(f"  - {title}")

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
