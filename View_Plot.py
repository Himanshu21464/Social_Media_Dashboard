import mysql.connector
import matplotlib
import matplotlib.pyplot as plt



# Function to fetch data from the social_media_dashboard view
def fetch_view_counts(platform):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Himanshu@1809",
            database="global_database"
        )

        # Create a cursor
        cursor = conn.cursor()

        # Fetch view counts from the social_media_dashboard view
        query = "SELECT View_Count FROM social_media_Dashboard WHERE Platform = %s;"
        cursor.execute(query, (platform,))

        # Extract view counts into a list and reverse it
        view_counts = [row[0] for row in cursor.fetchall()][::-1]

        # Close the cursor and the connection
        cursor.close()
        conn.close()

        return view_counts

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []

# Fetch view counts from social_media_dashboard view for Twitch, Dailymotion, and YouTube
twitch_view_counts = fetch_view_counts("Twitch")
dailymotion_view_counts = fetch_view_counts("Dailymotion")
youtube_view_counts = fetch_view_counts("YouTube")

# Plotting
plt.figure(figsize=(10, 6))

plt.plot(twitch_view_counts, label='Twitch')
plt.plot(dailymotion_view_counts, label='Dailymotion')
plt.plot(youtube_view_counts, label='YouTube')

plt.title('View Counts from Different Platforms')
plt.xlabel('Video Index')
plt.ylabel('View Count')
plt.legend()
plt.savefig("Plot.png", dpi=300)
plt.show()
