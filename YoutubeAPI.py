import streamlit as st
import psycopg2

# Initialize your Streamlit app and title
st.title("YouTube Data Analysis")

# Create a connection to PostgreSQL
db_params = {
    "database": "FinalProject",
    "user": "postgres",
    "password": "1234",
    "port": "5432",
}

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Define SQL queries for different options
queries = {
    '1. All the videos and the Channel Name': """
        SELECT C.channel_name, V.video_name
        FROM Channel C
        JOIN Playlist P ON C.channel_id = P.channel_id
        JOIN Video V ON P.playlist_id = V.playlist_id;
    """,
    '2. Channels with the most number of videos': """
        SELECT C.channel_name, COUNT(V.video_id) AS video_count
        FROM Channel C
        JOIN Playlist P ON C.channel_id = P.channel_id
        JOIN Video V ON P.playlist_id = V.playlist_id
        GROUP BY C.channel_name
        ORDER BY video_count DESC;
    """,
    '3. 10 most viewed videos': """
        SELECT video_name, view_count
        FROM Video
        ORDER BY view_count DESC
        LIMIT 10;
    """,
    '4. Comments in each video': """
        SELECT video_name, comment_count
        FROM Video;
    """,
    '5. Videos with the highest likes': """
        SELECT video_name, like_count
        FROM Video
        ORDER BY like_count DESC
        LIMIT 10;
    """,
    '6. Likes of all videos': """
        SELECT SUM(like_count) AS total_likes
        FROM Video;
    """,
    '7. Views of each channel': """
        SELECT C.channel_name, SUM(V.view_count) AS total_views
        FROM Channel C
        JOIN Playlist P ON C.channel_id = P.channel_id
        JOIN Video V ON P.playlist_id = V.playlist_id
        GROUP BY C.channel_name;
    """,
    '8. Videos published in the year 2022': """
        SELECT video_name, published_at
        FROM Video
        WHERE published_at >= '2022-01-01' AND published_at < '2023-01-01';
    """,
    '9. Average duration of all videos in each channel': """
        SELECT C.channel_name, AVG(duration_to_seconds(V.duration)) AS avg_duration_seconds
        FROM Channel C
        JOIN Playlist P ON C.channel_id = P.channel_id
        JOIN Video V ON P.playlist_id = V.playlist_id
        GROUP BY C.channel_name;
    """,
    '10. Videos with the highest number of comments': """
        SELECT video_name, comment_count
        FROM Video
        ORDER BY comment_count DESC
        LIMIT 10;
    """
}


# Select the analysis option
analysis_option = st.selectbox('Select an analysis option:', list(queries.keys()))
# Execute the selected SQL query
if  st.button("Run Analysis"):
    st.subheader("Analysis Result:")
    query = queries.get(analysis_option, None)
    if query:
       cursor.execute(query)
       result = cursor.fetchall()
       st.write(result)
    else:
       st.write("Analysis option not implemented.")

# Close the database connection
conn.close()
