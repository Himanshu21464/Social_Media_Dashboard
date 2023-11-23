import subprocess

from datetime import datetime, timedelta
import mysql.connector
import editdistance
from prettytable import PrettyTable
import matplotlib.pyplot as plt
print("--------------------------------------------------Hello!! Welcome to Social Media Dashboard---------------------------------------------------------")

username="xbox"
password="xbox"
def menu():
    print("1. Get details of videos at all platform")
    print("2. Get total views at each platform")
    print("3. Analyse the view counts at each platform")
    print("4. Get top 10 videos at all platforms")
    print("5. Get total watch duration of each platform")
    print("6. Exit")


def login():
    user=""
    passw=""
    while((user!="xbox")|(passw!="xbox")):
        print("Please enter your username: ")
        user=input()
        print("Please enter your password: ")
        passw=input()
        if((user!="xbox")|(passw!="xbox")):
            print("Wrong credentials!!!\nTry again....\n")
    print("Hi! Xbox....")
    print("Hang on we are fetching your data.........")
    #subprocess.run(["python", "C:/Users/siddh/OneDrive/Desktop/datafetching.py"])

def query1():
    db_config = {
        'host': 'localhost',
        'database': 'global_database',
        'user': 'root',
        'password': 'siddharth',
    }

    conn = mysql.connector.connect(**db_config)

    # Create a cursor
    cursor = conn.cursor()

    # Execute the query to fetch the view count from the social_media_Dashboard view
    query = "SELECT * FROM social_media_Dashboard"
    cursor.execute(query)

    # Fetch all the rows
    rows = cursor.fetchall()

    # Display the results
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            for k in range(j + 1, len(rows)):
                title1 = rows[i][1]
                title2 = rows[j][1]
                title3 = rows[k][1]
                platform1 = rows[i][0]
                platform2 = rows[j][0]
                platform3 = rows[k][0]
                len1 = len(title1)
                len2 = len(title2)
                len3 = len(title3)
                avg = (len1 + len2 + len3) / 3
                distance1 = editdistance.eval(title1, title2)
                distance2 = editdistance.eval(title1, title3)
                distance3 = editdistance.eval(title2, title3)
                
            
                if (distance1 / avg) <= 0.8 and (distance2 / avg) <= 0.8 and (distance3 / avg) <= 0.8 and platform1 != platform2 and platform1 != platform3 and platform2 != platform3:
                    
                    print(f"Platform-1: {platform1} - Title: {title1} - View Count: {rows[i][5]} - Like Count: {rows[i][6]}")
                    print(f"Platform-2: {platform2} - Title: {title2} - View Count: {rows[j][5]} - Like Count: {rows[j][6]}")
                    print(f"Platform-3: {platform3} - Title: {title3} - View Count: {rows[k][5]} - Like Count: {rows[k][6]}")
                    if rows[i][5] >= rows[j][5] and rows[i][5] >= rows[k][5]:
                        best_platform = platform1
                    elif rows[j][5] >= rows[i][5] and rows[j][5] >= rows[k][5]:
                        best_platform = platform2
                    else:
                        best_platform = platform3
                    print(f"Best Platform for this content: {best_platform}")
                    print("\n")

    # Close the cursor and connection
    cursor.close()
    conn.close()

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

def query3():
    # Function to fetch data from the social_media_dashboard view
    def fetch_view_counts(platform):
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="siddharth",
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
    plt.show()

def query4():
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




def fetch_total_duration():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="siddharth",
            database="global_database"
        )

        # Create a cursor
        cursor = conn.cursor()

        # Fetch total duration for each platform
        query = """
        SELECT Platform, SEC_TO_TIME(SUM(TIME_TO_SEC(Duration))) AS Total_Duration
        FROM social_media_Dashboard
        GROUP BY Platform;
        """
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()

        # Close the cursor and the connection
        cursor.close()
        conn.close()

        return results

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []

login()
cont="y"
while(cont=="y"):
    menu()
    print("Chosse any one query: ")
    ch=int(input())
    if(ch==1):
        query1()
    elif(ch==2):
        query2()
    elif(ch==3):
        query3()
    elif(ch==4):
        query4()
    elif(ch==5):
        # Fetch total duration for each platform
        total_durations = fetch_total_duration()

        # Convert duration to seconds
        total_durations_seconds = [(platform[0], timedelta(hours=platform[1].seconds // 3600, minutes=(platform[1].seconds // 60) % 60, seconds=platform[1].seconds % 60)) for platform in total_durations]

        # Plotting
        labels = [platform[0] for platform in total_durations_seconds]
        durations_seconds = [duration[1].total_seconds() for duration in total_durations_seconds]

        plt.pie(durations_seconds, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Total Duration Distribution by Platform')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()
    elif(ch==6):
        cont="n"
    else:
        print("Wrong choice!!!")
    
