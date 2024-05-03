#Truncate and load data to tables

import psycopg2
import sys
from dotenv import load_dotenv
import os
load_dotenv(os.path.dirname(os.getcwd())+"/.env")


print(os.getenv('HOST'),os.getenv('PORT'),os.getenv('USER'),os.getenv('PASSWORD'))

connection=psycopg2.connect(host=os.getenv('HOST'),port=os.getenv('PORT'),dbname='artists_db',user='postgres',password=os.getenv('PASSWORD'))
 
cursor=connection.cursor()

file_path=sys.argv[1]

#'/python_spotify_api/artist_details.txt'  ##path inside the docker container file needed to be moved inside the docker container
table_name=sys.argv[2]

#'artist_details'
delimiter=sys.argv[3]
#','

delete_sql=f"delete from {table_name};"

cursor.execute(delete_sql)

connection.commit()

print(f"Data deleted successfully from {table_name}")

print(f"Starting load for: {table_name} from file: {file_path}......")

load_sql=f"COPY {table_name} FROM '{file_path}' DELIMITER '{delimiter}';"

cursor.execute(load_sql)

connection.commit()

cursor.close()
connection.close()

print(f"Load completed for: {table_name}......")

