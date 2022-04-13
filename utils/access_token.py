import os
import requests

from base64 import b64encode
from dotenv import load_dotenv

base_accounts_url = "https://accounts.spotify.com"

load_dotenv()

def get_access_token():
    url = f"{base_accounts_url}/api/token"
    code = os.getenv("SPOTIFY_API_CODE")
    redirect = "https://www.google.com"

    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect
    }

    clients = bytes(os.getenv("SPOTIFY_CLIENT_ID") + ":" + os.getenv("SPOTIFY_CLIENT_SECRET"), encoding="utf-8")
    encoded_clients = b64encode(clients).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_clients}"
    }

    response = requests.post(url, headers = headers, data = body)
    print(response.text)

if __name__ == "__main__":
    get_access_token()