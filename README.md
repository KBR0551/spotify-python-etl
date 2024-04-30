# spotify-python-etl
simple ETL project using Python, Postgres and Apache Airflow 


In the following repo, you will find a simple ETL datapipe line using..
1) Python to do ETL
2) Prostgress Database to store data
3) Apache Airflow for orchestration i.e running pipeline
4) Pytest to perform basic test

The gaol is to get top 20 artists from wikipedia using python webscraping, grab the 20 artists and extact artist details, artist albums, artist album tracks from spotify, we will run this as a daily job which trucates and load data, and query data using SQL

You will need to create a copy from the .env.example and call it .env. There you can put your personal information like (API client_id, client_secret, database username, port, password, data file path, etc.). 

# Spotify API
Here we will use the Spotify API, i.e extract data by making API calls, you will need client_id & client_secret to generate accesss token, the genrated access token will be used to make a web API call and retrive required data.

Details on how to setup cleint_id & client_secret can be found in this link: https://developer.spotify.com/documentation/web-api/tutorials/getting-started

# Architecture
<img width="858" alt="image" src="https://github.com/KBR0551/spotify-python-etl/assets/98926998/41c1f332-c5ee-4378-8210-5a9b6e162d75">

# Data Model

<img width="934" alt="image" src="https://github.com/KBR0551/spotify-python-etl/assets/98926998/7464dd1c-9d89-44cc-8aa0-c2b902a48ab3">

# Airflow Schedule run
<img width="657" alt="image" src="https://github.com/KBR0551/spotify-python-etl/assets/98926998/3c3221ae-4c46-4dfa-9782-e6b8947d5b6e">

# Code directories
1) utility- contains commonly used scripts like token generator,table load etc.
2) data_extract- contains scripts to extract from data endpoints.
3) tests- contains pytests
4) dags- Airflow dags for orchestration

# Setup and Execution Steps
