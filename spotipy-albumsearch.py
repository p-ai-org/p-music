
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
# get the first album uri

album_names = album_data['Album']
album_dict = {}
#need to skip rows that don't have needed values - how?
for album_name in album_names[:100]:
    results = sp.search(q = "album:" + album_name, type = "album")
    try:
        album_uri = results['albums']['items'][0]['uri']
    except:
        print("")
    album_tracks_result = sp.album_tracks(album_uri)
    album_tracks = album_tracks_result['items'] 
    track_list = []
    for album_track in album_tracks:
        track_list.append(album_track['name'])
    album_dict[album_name] = track_list

print(album_dict)
