from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
import data_extract.top_trending_artists_extract as de
import subprocess
import os
from dotenv import load_dotenv

load_dotenv(os.path.dirname(os.getcwd())+"/.env")


default_args={
    'owner' : 'airflow',
    'depends_on_past' : False,
    'email_on_failure' : False,
    'email_on_retry' : False,
}

dag=DAG(
    'TOP_20_ARTISTS_ETL',
    default_args=default_args,
    description='An ETL work flow with python and plsql',
    start_date=datetime(2024,4,7),
    catchup=False,
)

def run_web_scrape_extract():
    script_path=str(os.getenv("PROJECT_PATH"))+"data_extract/top_trending_artists_extract.py"
    result=subprocess.run(["python",script_path],capture_output=True,text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)

def run_spotify_artist_details_extract():
    script_path=str(os.getenv("PROJECT_PATH"))+"data_extract/artist_details_extract.py"
    result=subprocess.run(["python",script_path],capture_output=True,text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)

def run_spotify_artist_albums_extract():
    script_path=str(os.getenv("PROJECT_PATH"))+"data_extract/artist_albums_details_extract.py"
    result=subprocess.run(["python",script_path],capture_output=True,text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)

def run_spotify_artist_track_extract():
    script_path=str(os.getenv("PROJECT_PATH"))+"data_extract/album_tracks_extract.py"
    result=subprocess.run(["python",script_path],capture_output=True,text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)

task1 = PythonOperator(
    task_id='scrape_data_from_wikipedia',
    python_callable=run_web_scrape_extract,
    dag=dag,
)

task2 = PythonOperator(
    task_id='spotify_artist_details_extract',
    python_callable=run_spotify_artist_details_extract,
    dag=dag,
)

task3 = PythonOperator(
    task_id='spotify_artist_albums_extract',
    python_callable=run_spotify_artist_albums_extract,
    dag=dag,
)

task4 = PythonOperator(
    task_id='spotify_artist_track_extract',
    python_callable=run_spotify_artist_track_extract,
    dag=dag,
)

dummy_wait_task_1=DummyOperator(task_id='load_wait_task', dag=dag)

def run_artist_details_load(file_path,table_name,delimiter):
    script_path=str(os.getenv("PROJECT_PATH"))+"utility/load_data_files.py"
    file_path=file_path
    table_name=table_name
    delimiter=delimiter
    result=subprocess.run(["python",script_path,file_path,table_name,delimiter],capture_output=True,text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


task5=PythonOperator(
    task_id='artist_details_load',
    python_callable=run_artist_details_load,
    op_args=[str(os.getenv("DATA_FILE_PATH"))+'artist_details.txt','artist_details',','],
    dag=dag,
)

task6=PythonOperator(
    task_id='artist_album_details_load',
    python_callable=run_artist_details_load,
    op_args=[str(os.getenv("DATA_FILE_PATH"))+'artist_album_details.txt','artist_albums','|'],
    dag=dag,
)

task7=PythonOperator(
    task_id='album_tracks_load',
    python_callable=run_artist_details_load,
    op_args=[str(os.getenv("DATA_FILE_PATH"))+'album_tracks.txt','album_tracks','|'],
    dag=dag,
)

dummy_wait_task_2=DummyOperator(task_id='test_wait_task', dag=dag)

def validate_data():
    script_path=str(os.getenv("PROJECT_PATH"))+"tests/validation_test.py"
    result=subprocess.run(["python",script_path],capture_output=True,text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)

task8=PythonOperator(
    task_id='run_test_to_validate_data',
    python_callable=validate_data,
    dag=dag,
)

###extract  tasks ###
task1 >> task2 
task2 >> task3
task3 >> task4

####LOAD TASKS ####
dummy_wait_task_1<< [task2,task3,task4]
task5 << dummy_wait_task_1
task6 << dummy_wait_task_1
task7 << dummy_wait_task_1

##### TEST TASKS #####
dummy_wait_task_2<<[task5,task6,task7]
task8<< dummy_wait_task_2
