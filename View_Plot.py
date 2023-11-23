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


#plot 2----------------------------------------------------------------------------------------------------------------------
import mysql.connector
from prettytable import PrettyTable
import matplotlib.pyplot as plt

# Your MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'siddharth',
    'database': 'global_database',
}

# Create a MySQL connection
conn = mysql.connector.connect(**DB_CONFIG)

try:
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # SQL command
    sql_command = """
        SELECT DISTINCT Platform, Title, View_Count, duration
        FROM social_media_Dashboard 
        ORDER BY View_Count DESC 
        LIMIT 10;
    """

    # Execute the SQL command
    cursor.execute(sql_command)

    # Fetch all the rows
    result = cursor.fetchall()

    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = ["Platform", "Title", "View_Count", "Duration"]

    # Add data to the table and collect data for the bar graph
    platforms = []
    view_counts = []
    durations = []

    for row in result:
        table.add_row(row)
        platforms.append(f"{row[0]} - {row[1]}")  # Combine Platform and Title for better readability
        view_counts.append(row[2])
        durations.append(row[3])

    # Print the formatted table
    print(table)

    # Define colors for each platform
    platform_colors = {'YouTube': 'red', 'DailyMotion': 'yellow', 'Twitch': 'violet'}

    # Create a bar graph for view counts with different colors for each platform
    fig, ax = plt.subplots()
    index = range(10)

    for i, platform in enumerate(platforms):
        ax.bar(platform, view_counts[i], color=platform_colors.get(platform.split(' - ')[0], 'gray'))

    ax.set_xlabel('Video')
    ax.set_ylabel('View Count')
    ax.set_title('Top 10 Videos - View Count')
    ax.set_xticks(platforms)
    ax.set_xticklabels(platforms, rotation=45, ha='right')

    # Add legend for platform colors in the top right corner
    legend_labels = [plt.Line2D([0], [0], marker='o', color='w', label=platform, markerfacecolor=color, markersize=10)
                     for platform, color in platform_colors.items()]

    ax.legend(handles=legend_labels, title='Platform Colors', loc='upper right')

    plt.show()

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()




# Plot 3-------------------------------------------------------------------------------------------------------------------
def query2():
    


    # Your MySQL database configuration
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'siddharth',
        'database': 'global_database',
    }

    # Create a MySQL connection
    conn = mysql.connector.connect(**DB_CONFIG)

    try:
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # SQL command
        sql_command = """
            SELECT
                'YouTube' AS Platform,
                SUM(View_Count) AS TotalViews
            FROM
                YouTube_Analytics.YouTube
            UNION ALL
            SELECT
                'DailyMotion' AS Platform,
                SUM(views_total) AS TotalViews
            FROM
                dailymotion.dailymotion_videos
            UNION ALL
            SELECT
                'Twitch' AS Platform,
                SUM(views) AS TotalViews
            FROM
                twitch.twitch_videos;
        """

        # Execute the SQL command
        cursor.execute(sql_command)

        # Fetch all the rows
        result = cursor.fetchall()

        # Extracting platform names and total views
        platforms = [row[0] for row in result]
        total_views = [row[1] for row in result]

        # Create a pie chart
        plt.pie(total_views, labels=platforms, autopct='%1.1f%%', startangle=140)
        plt.title('Total Views by Platform')
        plt.show()

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()



















