#create folders for each albums
# @lapcbws
#use spotdl in command line to download all the songs in an album
#import modules
import pandas as pd
import spotipy, time
from tqdm import tqdm
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotipykeys import keys

SPOTIPY_CLIENT_ID=keys['spotipy_client_id']
SPOTIPY_CLIENT_SECRET=keys['spotipy_client_secret']

#sp= spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))
auth_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# find album by name
# get the first album uri

# takes in list of albums; returns dictionary with album name as key and list of songs as value

def get_tracks(albums):
    print(len(albums))
    album_dict = {}
    #need to skip rows that don't have needed values - how?
    print('acquiring album and song data...')
    
    
    
    for i in tqdm(range(len(albums)), desc='loading albums...', position=0, leave=True):
        album_name =albums[i]
        # update progress every 20 loops
        # if i % 20 == 0:
        #     percent = round((i/len(albums))*100, 3)
        #     print('progress: ' + str(percent) + '%')
        
        try:
            results = sp.search(q = "album:" + album_name, type = "album")
            album_uri = results['albums']['items'][0]['uri']

            album_tracks_result = sp.album_tracks(album_uri)
            album_tracks = album_tracks_result['items'] 
            track_list = []
            for album_track in album_tracks:
                track_list.append(album_track['name'])
            album_dict[album_name] = track_list
        except:
            print('album %s could not be found' %album_name)
            

    return album_dict
