# Album_tracks	
# Album_id	string
# album_track_id	string
# album_track_name	string
# track_duration	integer
# ENDPOINT https://api.spotify.com/v1/albums/{id}/tracks


from datetime import datetime
from utility import spotify_token_gen,run_check
import requests
import json
import time
import datetime as dt
import os
from dotenv import load_dotenv


load_dotenv(os.path.dirname(os.getcwd())+"/.env")

exec_script_nm=os.path.basename(__file__)
curr_dt=dt.datetime.now().strftime('%Y-%m-%d')

run_check_flag,data=run_check.run_check(exec_script_nm,curr_dt)

token=spotify_token_gen.get_spotify_token()
headers=spotify_token_gen.auth_token_header(token)

def search_album_tracks(album_id):
    base_url=f'https://api.spotify.com/v1/albums/{album_id}/tracks' 
    data=requests.get(base_url,headers=headers)
    if data.status_code==429: #to avoid max api call's per second 
        if 'Retry-After' in data.headers:
            wait_time=int(data.headers['Retry-After'])
            print(f"max api call limit reached, will try after {wait_time} seconds.")
            time.sleep(wait_time)
            return  search_album_tracks(album_id)
    tracks=json.loads(data.content)
    album_tracks=[]
    for track in tracks['items']:
        album_tracks.append([track['id'], track['name'].replace('|',''),album_id,'{:.1f}'.format(track['duration_ms']/60000)])
    return album_tracks # do to eliminate dublicates rows 

def album_tracks():
     with open(str(os.getenv('DATA_FILE_PATH'))+"artist_album_details.txt",'r') as file:
        lines=file.readlines()
        tracks=[]
        for line in lines:
             print(line.split("|")[0])
             tracks.append(search_album_tracks(line.split("|")[0]))
        unique_tracks=set() #using set to remove duplicates, i found while developing
        for i in range(0,len(tracks)):
            for j in range(0,len(tracks[i])):
                unique_tracks.add('|'.join(map(str,tracks[i][j])))

        with open(str(os.getenv('DATA_FILE_PATH'))+'/album_tracks.txt','w') as f:
            for track in unique_tracks:
                print(track,file=f)


if __name__ == "__main__":
    if run_check_flag!='Y':
        print ("Data extraction for album_tracks started ...")
        album_tracks()
        print ("Data extraction for album_tracks completed ...")
        with open(os.getenv('RUN_CHECK_FILE_PATH')+"job_ctrl_log.json",'w') as json_file:
                json.dump(data,json_file)
    else:
        print("Extract completed for today...: ",data)

