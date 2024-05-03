# At the minimmum lets check if the table have data to work with i.e not empty
import pytest
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(os.path.dirname(os.getcwd())+"/.env")

# need connection and curosor object

@pytest.fixture(scope="module") #making it executed only once, making a database connection object.
def db_connection():
    connection=psycopg2.connect(host=os.getenv('HOST'),port=os.getenv('PORT'),dbname='artists_db',user='postgres',password=os.getenv('PASSWORD'))
    yield connection
    connection.close() # teardown fuction i.e closed irespective of the test cases success or not 

@pytest.fixture(scope="function") #executed for each test case function
def db_cursor(db_connection):
    cursor=db_connection.cursor()
    yield cursor
    cursor.close()
 
def test_artist_details_table_load_check(db_cursor):
    db_cursor.execute("select count(*) from artist_details")
    count=db_cursor.fetchone()[0]
    assert count>0

def test_artist_albums_table_load_check(db_cursor):
    db_cursor.execute("select count(*) from artist_albums")
    count=db_cursor.fetchone()[0]
    assert count>0

def test_album_tracks_table_load_check(db_cursor):
    db_cursor.execute("select count(*) from album_tracks")
    count=db_cursor.fetchone()[0]
    assert count>0