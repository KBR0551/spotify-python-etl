# Artist_albums	
# Artist_id	string
# album_id	string
# album_name	string
# total_tracks	Integer
# release_date	date
# release_date_precision	string
# genres	list

from datetime import datetime
from utility import spotify_token_gen,run_check
import requests
import json
import os
import datetime as dt
from dotenv import load_dotenv

load_dotenv(os.path.dirname(os.getcwd())+"/.env")

exec_script_nm=os.path.basename(__file__)
curr_dt=dt.datetime.now().strftime('%Y-%m-%d')

run_check_flag,data=run_check.run_check(exec_script_nm,curr_dt)

token=spotify_token_gen.get_spotify_token()
headers=spotify_token_gen.auth_token_header(token)


def year_to_date(year):
    str_date=f"{year}-01-01"
    date=datetime.strptime(str_date,"%Y-%m-%d")
    formatted_date = date.strftime("%Y-%m-%d")
    return(formatted_date)

def search_artist_albums(artist_id,artist_name):
    base_url='https://api.spotify.com/v1/search'
    query=f"?q={artist_name}&type=album&limit=50&offset=0" #limiting to only 50 items
    query_url=base_url+query
    data=requests.get(query_url,headers=headers)
    json_data=json.loads(data.content)
    #print(len(json_data['albums']['items']))
    albums=[]
    for i in range(0,len(json_data['albums']['items'])):
            album_name=(json_data['albums']['items'][i]['name']).replace('|','')
            album_id=json_data['albums']['items'][i]['id']
            total_tracks=json_data['albums']['items'][i]['total_tracks']
            release_date_precision=json_data['albums']['items'][i]['release_date_precision']
            release_date=json_data['albums']['items'][i]['release_date']
            if release_date_precision=='year':  #cleaning date to date format
                release_date=year_to_date(release_date)  
            elif release_date_precision=='month':
                release_date='9999-12-31'
            else:
                release_date    
            albums.append([album_id,album_name,artist_id,total_tracks,release_date])
    return albums

    #return('Not Artist found' if len(json_data['artists']['items'])==0 else json_data['artists']['items'][0]['id'])

def artist_album_details():
    with open(str(os.getenv('DATA_FILE_PATH'))+"artist_details.txt",'r') as file:
        lines=file.readlines()
        with open(str(os.getenv('DATA_FILE_PATH'))+'artist_album_details.txt','w') as f:
            for line in lines:
                albums=search_artist_albums(line.split(",")[0],line.split(",")[1])
                for album in albums:
                    print('|'.join(map(str,album)),file=f)


if __name__ == "__main__":
    if run_check_flag!='Y':
        print ("Data extraction for album_details started ...")
        artist_album_details()
        print ("Data extraction for album_details completed ...")
        with open(os.getenv('RUN_CHECK_FILE_PATH')+"job_ctrl_log.json",'w') as json_file:
            json.dump(data,json_file)
    else:
        print("Extract completed for today...: ",data)



