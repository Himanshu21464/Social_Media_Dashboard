import mysql.connector
import matplotlib.pyplot as plt

# Function to fetch data from a table and return a list of view counts
def fetch_view_counts(database, table):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Himanshu@1809",
            database=database
        )

        # Create a cursor
        cursor = conn.cursor()

        # Fetch view counts from the specified table
        query1 = "SELECT View_Count FROM YouTube;"
        query2 = "SELECT views FROM twitch_videos;"
        query3 = "SELECT views_total FROM dailymotion_videos;"

        if(database=="twitch"):
            cursor.execute(query2)
        elif(database=="dailymotion"):
            cursor.execute(query3)
        elif(database=="YouTube_Analytics"):
            cursor.execute(query1)


        # Extract view counts into a list and reverse it
        view_counts = [row[0] for row in cursor.fetchall()][::-1]

        # Close the cursor and the connection
        cursor.close()
        conn.close()

        return view_counts

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []

# Fetch view counts from Twitch, Dailymotion, and YouTube_Analytics tables
twitch_view_counts = fetch_view_counts("twitch", "twitch_videos")
dailymotion_view_counts = fetch_view_counts("dailymotion", "dailymotion_videos")
youtube_view_counts = fetch_view_counts("YouTube_Analytics", "YouTube")

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(twitch_view_counts, label='Twitch')
plt.plot(dailymotion_view_counts, label='Dailymotion')
plt.plot(youtube_view_counts, label='YouTube')

plt.title('View Counts from Different Platforms')
plt.xlabel('Video Index')
plt.ylabel('View Count')
plt.legend()
plt.savefig("PLot.png", dpi=1000)
