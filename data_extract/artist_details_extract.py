#Artist_details
    #Artist_id
    #artist_name
    #artist_followers
    #popularity

#spotify API end-point : https://api.spotify.com/v1/artists/{id}

from utility import spotify_token_gen ,run_check#(custom utilities)
import requests
import json
import os
from dotenv import load_dotenv
import datetime as dt

load_dotenv(os.path.dirname(os.getcwd())+"/.env")

exec_script_nm=os.path.basename(__file__)
curr_dt=dt.datetime.now().strftime('%Y-%m-%d')

run_check_flag,data=run_check.run_check(exec_script_nm,curr_dt)

token=spotify_token_gen.get_spotify_token()
headers=spotify_token_gen.auth_token_header(token)

top_artists_file=str(os.getenv('DATA_FILE_PATH'))+"top_20_followed_artist.txt"

def search_for_artist_id(artist_name):
    base_url='https://api.spotify.com/v1/search'
    query=f"?q={artist_name}&type=artist&limit=1"
    query_url=base_url+query
    data=requests.get(query_url,headers=headers)
    json_data=json.loads(data.content)
    id=json_data['artists']['items'][0]['id']
    followers=json_data['artists']['items'][0]['followers']['total']
    popularity=json_data['artists']['items'][0]['popularity']
    
    #return('Not Artist found' if len(json_data['artists']['items'])==0 else json_data['artists']['items'][0]['id'])

    return id,artist_name,followers,popularity

if __name__ == "__main__":
    if run_check_flag!='Y':
         print ("Data extraction for artist_details started ...")
         with open(top_artists_file,'r') as file:
            with open(str(os.getenv('DATA_FILE_PATH'))+'artist_details.txt','w') as f:
                for artist in file:
                    print(','.join(map(str,search_for_artist_id(artist.strip()))),file=f)
         print ("Data extraction for artist_details completed ...")
         with open(os.getenv('RUN_CHECK_FILE_PATH')+"job_ctrl_log.json",'w') as json_file:
                json.dump(data,json_file,indent=4)
    else:
         print("Extract completed for today...: ",curr_dt)
