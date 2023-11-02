# pytProject Name: YouTube Data Harvesting and Warehousing

Description: This project is aimed at creating a user-friendly application that allows users to access and analyze data from various YouTube channels. The application uses Streamlit for the user interface, Python for scripting, Google API Client for YouTube data retrieval, MongoDB for data storage, and PostgreSQL for structured data management.

Tools and Libraries Used:

1)Streamlit: A Python library for creating a user-friendly interface that enables users to interact with the application for data retrieval and analysis.

2)Python: The primary programming language for data retrieval, processing, analysis, and visualization.

3)Google API Client: A Python library used to communicate with various Google APIs, with the main purpose of interacting with YouTube's Data API v3 for retrieving channel details, video specifics, and comments.

4)MongoDB: A document database known for its scalability and ability to store structured or unstructured data.

5)PostgreSQL: An open-source and feature-rich database management system used for storing and managing structured data.

Required Libraries:

1.googleapiclient.discovery

2.streamlit

3.psycopg2

4.pymongo

Key Features:

-Retrieve channel and video data from YouTube using the YouTube API.

-Store data in MongoDB for data lake capabilities.

-Migrate data from the data lake to PostgreSQL for efficient querying and analysis.

-Search and retrieve data from PostgreSQL using different search options.
