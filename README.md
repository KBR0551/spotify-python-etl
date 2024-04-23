# spotify-python-etl
simple ETL project using Python, Postgres and Apache Airflow 


In the following repo, you will find a simple ETL datapipe line using..
1) Python to do ETL
2) Prostgress Database to store data
3) Apache Airflow for orchestration i.e running pipeline
4) Pytest to perform basic test

The gaol is to get top 20 artists from wikipedia using python webscraping, grab the 20 artists and extact artist details, artist albums, artist album tracks from spotify, we will run this as a daily job which trucates and load data, and query data using SQL

You will need to create a copy from the .env.example and call it .env. There you can put your personal information like (API client_id, client_secret, database username, port, password, data file path, etc.). 
