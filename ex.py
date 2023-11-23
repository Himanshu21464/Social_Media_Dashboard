
import requests
import urllib.parse
from datetime import datetime, timedelta
import mysql.connector
import editdistance

db_config = {
    'host': 'localhost',
    'database': 'global_database',
    'user': 'root',
    'password': 'Shi@1862000',
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
                print("\n")

# Close the cursor and connection
cursor.close()
conn.close()
