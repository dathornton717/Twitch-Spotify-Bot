from base64 import b64encode
from dotenv import load_dotenv
from .track import Track

import os
import requests
import urllib.parse

base_accounts_url = "https://accounts.spotify.com"
base_api_url = "https://api.spotify.com"

load_dotenv()

def get_currently_playing():
    url = f"{base_api_url}/v1/me/player/currently-playing"

    retry_count = 0
    while retry_count < 2:
        headers = {
            "Authorization": f"Bearer {os.getenv('SPOTIFY_ACCESS_TOKEN', '')}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            if not response.json()["is_playing"]:
                return None
            name = response.json()["item"]["name"]
            artist = response.json()["item"]["artists"][0]["name"]
            return Track(name, artist)
        elif response.status_code == 401 or response.status_code == 400:
            refresh_access_token()
            retry_count = retry_count + 1
        else:
            print(f"Something went wrong: {response.text}")
    raise Exception(f"Failed to get currently playing")

def search(artist, track, limit):
    url = f"{base_api_url}/v1/search"

    retry_count = 0
    while retry_count < 2:
        headers = {
            "Authorization": f"Bearer {os.getenv('SPOTIFY_ACCESS_TOKEN', '')}",
            "Content-Type": "application/json"
        }
        params = {
            "type": "track"
        }

        search = ""
        token = ""

        if artist != "":
            search = f"{search}{token}artist:{artist}"
            token = " "

        if track != "":
            search = f"{search}{token}track:{track}"
            token = " "

        params["q"] = search
        params["limit"] = limit
        response = requests.get(url, headers = headers, params = params)
        if response.status_code == 200:
            items = response.json()["tracks"]["items"]
            if len(items) > 0:
                tracks = []
                for item in items:
                    name = item["name"]
                    artist = item["artists"][0]["name"]
                    uri = item["uri"]
                    tracks.append(Track(name, artist, uri))
                return tracks
        elif response.status_code == 401 or response.status_code == 400:
            refresh_access_token()
            retry_count = retry_count + 1
        else:
            print(f"Something went wrong: {response.text}")
    raise Exception(f"Failed song search")
    
def queue_first_successful_song(track_list):
    url = f"{base_api_url}/v1/me/player/queue"

    retry_count = 0
    while retry_count < 2:
        headers = {
            "Authorization": f"Bearer {os.getenv('SPOTIFY_ACCESS_TOKEN', '')}",
            "Content-Type": "application/json"
        }

        for track in track_list:
            params = {
                "uri": track.uri
            }
            response = requests.post(url, headers = headers, params = params)
            if response.status_code == 204:
                return track
            elif response.status_code == 401 or response.status_code == 400:
                refresh_access_token()
                retry_count = retry_count + 1
            else:
                print(f"Something went wrong: {response.text}")
    raise Exception(f"Failed to queue up any song")

def refresh_access_token():
    print("Refreshing Access Token")
    url = f"{base_accounts_url}/api/token"
    clients = bytes(os.getenv("SPOTIFY_CLIENT_ID") + ":" + os.getenv("SPOTIFY_CLIENT_SECRET"), encoding="utf-8")
    encoded_clients = b64encode(clients).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_clients}"
    }
    code = os.getenv("SPOTIFY_API_CODE")
    body = {
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("SPOTIFY_REFRESH_TOKEN")
    }

    response = requests.post(url, headers = headers, data = body)
    if response.status_code == 200:
        os.environ["SPOTIFY_ACCESS_TOKEN"] = response.json()["access_token"]
    else:
        print(f"Failed to refresh access token: {response.text}")