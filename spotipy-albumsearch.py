#create folders for each albums
#use spotdl in command line to download all the songs in an album
#import modules I need
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import requests

#read album data from excel file using pandas
album_data = pd.read_csv(r"C:\Users\이서현\pai\pmusic\rym_top_5000_all_time.csv")
album_data.head()

scope = 'user-library-read playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = cred.client_id, client_secret = cred.client_secret, redirect_uri = cred.redirect_uri,
    scope=scope))

# find album by name
# get external urls

album_names = album_data['Album']
url_list = []
#need to skip rows that don't have needed values - how?
for album_name in album_names:
    results = sp.search(q = "album:" + album_name, type = "album")
    try:
        album_url = results['albums']['items'][0]['external_urls']['spotify']
    except: 
        print("link doesn't exist")
    url_list.append(album_url)
