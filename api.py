from dotenv import load_dotenv
import os
import base64 
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auto_string = client_id + ":" + client_secret
    auth_bytes = auto_string.encode("utf-8")
    auto_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auto_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token
   

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    artist_id = json_result["artists"]["items"][0]["id"]
    return artist_id

def get_user_profile_image(token, artist_name):
    artist_id = search_for_artist(token, artist_name)
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    image_url = json_result["images"][0]["url"]
    image_data = get(image_url).content
    with open(f"{artist_name}.jpg", "wb") as f:
        f.write(image_data)

def search_for_album(token, album_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={album_name}&type=album&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    album_id = json_result["albums"]["items"][0]["id"]
    return album_id

def get_album_cover_image(token, album_name):
    album_id = search_for_album(token, album_name)
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    image_url = json_result["images"][0]["url"]
    image_data = get(image_url).content
    with open(f"{album_name}.jpg", "wb") as f:
        f.write(image_data)


token = get_token()
choice = 0
while choice not in [1, 2]:
        choice = int(input("\nDo you wish to get the photo of an artist or of an album?\n\n1. Artist\n2. Album\nEnter 1 or 2: "))

if choice == 1:
    artista = input("\n Whose profile picture do you want to get, of which artist?")
    get_user_profile_image(token, artista)
elif choice == 2:
    album = input("\n Which album would you like to get the cover of?")
    get_album_cover_image(token, album)