# https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow

import sys
import os
from requests import get,post
import base64
from dotenv import load_dotenv
import json

load_dotenv()

#get token from spotify web api using client_id and  clinet_secret generated when app is created in spotify account


def get_spotify_token():
    base_url='https://accounts.spotify.com/api/token'
    client_cred_byte_string= (os.getenv('CLIENT_ID')+':'+os.getenv('CLIENT_SECRET')).encode('utf-8')
    client_cred_base64=str(base64.b64encode(client_cred_byte_string),'utf-8') #converting back to str from byte string b'sdfn' to 'sdfn'
    headers={
             "Authorization" : "Basic "+ client_cred_base64,
             "Content-Type"  : "application/x-www-form-urlencoded"
            }
    data={"grant_type": "client_credentials"}

    post_result=post(base_url,headers=headers,data=data)
    json_result=json.loads(post_result.content)
    access_token=json_result['access_token']
    return access_token

def auth_token_header(token):
    return {
        'Authorization': "Bearer " + token}