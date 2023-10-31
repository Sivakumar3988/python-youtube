import streamlit as st
import googleapiclient.discovery
import pymongo
import psycopg2
import json
def insert_data_into_mongodb(youtube_data):
    
      
    
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["YouTubeDemo"]
    collection = db["YouTubeData"]
    
    inserted_data = collection.insert_one(youtube_data)
    print(inserted_data)
    client.close()
    return True;
st.title("YouTube Data Retrieval App")

# Define the youtube_data dictionary outside the if block
youtube_data = {}

# Create input fields for the YouTube channel and video IDs
channel_id = st.text_input("Enter YouTube Channel ID")

# Create a button to trigger data retrieval
if st.button("Get YouTube Data"):
    api_key = "AIzaSyAu3-6bHqP__8S--oQ63CFq8_0m5jzvMVc"  # Replace with your actual API key
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Retrieve channel data
    channel_request = youtube.channels().list(
        part="snippet,statistics,contentDetails", 
        id=channel_id)
    channel_response = channel_request.execute()

    channel_data = {
        "Channel_Name": channel_response['items'][0]['snippet']['title'],
        "Channel_Id": channel_id,
        "Subscription_Count": channel_response['items'][0]['statistics']['subscriberCount'],
        "Channel_Views": channel_response['items'][0]['statistics']['viewCount'],
        "Channel_Description": channel_response['items'][0]['snippet']['description'],
        "Playlist_Id": channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    }

    youtube_data["Channel_Name"] = channel_data

    # Retrieve playlist ID
    playlist_id = channel_data["Playlist_Id"]

    # Initialize next_page_token for playlist items
    next_page_token = None

    while True:
        # Retrieve videos in the playlist with pagination
        playlistresponse = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=playlist_id,
            pageToken=next_page_token,
            maxResults=50
        ).execute()

        for item in playlistresponse['items']:
            video_id = item['snippet']['resourceId']['videoId']

            # Retrieve video data
            video_request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
            video_response = video_request.execute()

            try:
                like_count = video_response['items'][0]['statistics']['likeCount']
            except KeyError:
                like_count = 0

            video_data = {
                "Video_Id": video_id,
                "Video_Name": video_response['items'][0]['snippet']['title'],
                "Video_Description": video_response['items'][0]['snippet']['description'],
                "Tags": video_response['items'][0]['snippet']['tags'] if 'tags' in video_response['items'][0]['snippet'] else [],
                "PublishedAt": video_response['items'][0]['snippet']['publishedAt'],
                "View_Count": video_response['items'][0]['statistics']['viewCount'],
                "Like_Count": like_count,
                "Favorite_Count": video_response['items'][0]['statistics'].get('favoriteCount', 0),
                "Comment_Count": video_response['items'][0]['statistics'].get('commentCount', 0),
                "Duration": video_response['items'][0]['contentDetails']['duration'],
                "Thumbnail": video_response['items'][0]['snippet']['thumbnails']['default']['url'],
                "Caption_Status": video_response['items'][0]['contentDetails'].get('caption', 'Not Available')
            }

            youtube_data[video_id] = video_data

            # Initialize next_page_token for comments
            next_page_token_comments = None
             # Retrieve comment data
            while True:
                try:
                    comments_request = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults=50,  # Adjust this as needed
                        pageToken=next_page_token_comments
                    )

                    comments_response = comments_request.execute()

                    comments_data = {}

                    for comment in comments_response.get('items', []):
                        comment_id = comment['id']
                        comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                        comment_author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
                        comment_published_at = comment['snippet']['topLevelComment']['snippet']['publishedAt']

                        comment_info = {
                            "Comment_Id": comment_id,
                            "Comment_Text": comment_text,
                            "Comment_Author": comment_author,
                            "Comment_PublishedAt": comment_published_at
                        }

                        comments_data[comment_id] = comment_info

                    youtube_data[video_id]["Comments"] = comments_data

                    next_page_token_comments = comments_response.get('nextPageToken')

                    if not next_page_token_comments:
                        break
                except googleapiclient.errors.HttpError as e:
                    if "disabled comments" in str(e).lower():
                        break

        next_page_token = playlistresponse.get('nextPageToken')

        if not next_page_token:
            break

    # Print the structured YouTube data
    st.subheader("Structured YouTube Data:")
    insert_data_into_mongodb(youtube_data)
    st.json(youtube_data)
    youtube_data.pop("_id")
    # Now, you can use youtube_data for PostgreSQL or any further processing

    db_params = {
        "database": "FinalProject",
        "user": "postgres",
        "password": "1234",
        "port": "5432",
    }

    # Create a connection to PostgreSQL
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()


# Define your data for insertion
    channel_id = channel_data["Channel_Id"]
    channel_name = channel_data["Channel_Name"]
    channel_views = channel_data["Channel_Views"]
    channel_description = channel_data["Channel_Description"]

# Define your INSERT statement
    insert_query = "INSERT INTO Channel (channel_id, channel_name, channel_views, channel_description) VALUES (%s, %s, %s, %s);"

# Execute the INSERT statement
    cursor.execute(insert_query, (channel_id, channel_name, channel_views, channel_description))
    playlist_id = channel_data["Playlist_Id"]
    playlist_name = channel_name  # Replace with actual playlist name

    playlist_insert_query = """
        INSERT INTO Playlist (playlist_id, playlist_name, channel_id)
        VALUES (%s, %s, %s)
    """

    cursor.execute(playlist_insert_query, (playlist_id, playlist_name, channel_data["Channel_Id"]))


    for video_id, video_data in youtube_data.items():
    #    st.json(video_data)
       if video_id == "Channel_Name":
        continue

    # Insert Playlist data
    
    # Insert Video data
       video_insert_query = """
        INSERT INTO Video (video_id, video_name, video_description, published_at, view_count, like_count, favorite_count, comment_count, duration, thumbnail_url, caption_status, playlist_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

       video_values = (
        video_data["Video_Id"],
        video_data["Video_Name"],
        video_data["Video_Description"],
        video_data["PublishedAt"],
        video_data["View_Count"],
        video_data["Like_Count"],
        video_data["Favorite_Count"],
        video_data["Comment_Count"],
        video_data["Duration"],
        video_data["Thumbnail"],
        video_data["Caption_Status"],
        playlist_id,
       )

       cursor.execute(video_insert_query, video_values)

    # Insert Comment data
       if "Comments" in video_data:
                     for comment_id, comment_info in video_data["Comments"].items():
                                    comment_insert_query = """
                                      INSERT INTO Comment (comment_id, comment_text, comment_author, comment_published_at, video_id)
                                      VALUES (%s, %s, %s, %s, %s)
                                              """

                                    comment_values = (
                                                      comment_id,
                                                      comment_info["Comment_Text"],
                                                      comment_info["Comment_Author"],
                                                      comment_info["Comment_PublishedAt"],
                                                      video_data["Video_Id"],
                                                         )

                                    cursor.execute(comment_insert_query, comment_values)


    conn.commit()
    # Close the database connection
    cursor.close()
    conn.close()
    

    # Inform the user about the data insertion
    st.success("YouTube data has been inserted into PostgreSQL")