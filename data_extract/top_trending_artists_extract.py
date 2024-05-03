from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import json
import datetime as dt
from utility import run_check

load_dotenv(os.path.dirname(os.getcwd())+"/.env")

url="https://en.wikipedia.com/wiki/List_of_most-streamed_artists_on_Spotify#2024"
#print(table)

exec_script_nm=os.path.basename(__file__)
curr_dt=dt.datetime.now().strftime('%Y-%m-%d')

run_check_flag,data=run_check.run_check(exec_script_nm,curr_dt)

def table_data_extract(url):
    try: 
        response=requests.get(url) 
        if response.status_code==200:
            soup=BeautifulSoup(response.text,"html.parser")
            table=soup.find_all('table',{'class':"wikitable sortable"})[1]
            wiki_table_data=[]
            rows=table.find_all('tr')
            for row in rows:
                row_data=[]
                cells=row.find_all(['th','td'])
                for cell in cells:
                    row_data.append(cell.text.strip())
                if row_data:
                    wiki_table_data.append(row_data)
        return wiki_table_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while accessing the URL {url}: {e}")

def get_top_followed_artists(wiki_table_data):
    artist_list=[]
    for artist in wiki_table_data[1:21]:
        artist_list.append(artist[1])
    with open(str(os.getenv('DATA_FILE_PATH'))+"top_20_followed_artist.txt",'w') as f:
        print('\n'.join(artist_list),file=f)

def main():
    if __name__ == "__main__":
        if run_check_flag!='Y' :
            print ("Started wikibedia Web Scraping for top 20 artists ...")
            wiki_table_data=table_data_extract(url)
            get_top_followed_artists(wiki_table_data)
            print ("Data extraction for top 20 artists completed ...")
            with open(os.getenv('RUN_CHECK_FILE_PATH')+"job_ctrl_log.json",'w') as json_file:
                json.dump(data,json_file,indent=4)
        else:
            print("Extract completed for today...: ",data)


main()


