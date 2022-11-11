# imports ----------------------------
import pandas as pd
import os
from tqdm import tqdm
from os import path
from spotipykeys import keys
import spotipy
from spotipy.oauth2 import SpotifyOAuth


#first let's specify the directories where we'll be saving our chunks
# NOTE: YOU WILL NEED TO DEFINE THE PATH TO YOUR CSV AND CHANGE THE SONG/SPEC PATHS IN ORDER FOR THIS TO WORK!

scope = 'user-library-read playlist-modify-public'

SPOTIPY_CLIENT_ID=keys['spotipy_client_id']
SPOTIPY_CLIENT_SECRET=keys['spotipy_client_secret']
SPOTIPY_REDIRECT_URI=keys['spotipy_redirect_uri']

sp= spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, 
    redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
    )

# 1. load csv ----------------------
data = pd.read_csv('merged_features.csv')
# extract column with names

album_list = data['Album'].to_list()

# set song, spectrogram outputs
song_dest = 'C:\p-ai\songs'
spec_dest = 'C:\p-ai\spectrograms'

# make directories
if not(path.exists(song_dest)):
    print('making song dir!')
    os.makedirs(path.join(song_dest))
if not(path.exists(spec_dest)):
    print('making spec dir!')
    os.makedirs(path.join(spec_dest))

# call our other files
from downloadsongs_MARWAN_VERS import *
from findalbums_MARWAN_VERS import *
from generatespectrograms import *

def append_as_dict(album_name, as_dict, sp):
    '''
    This function takes in an as_dict and album_name, does a spotify search for it
    and adds the result into the as_dict.
    '''

    #now we search spotify for the album
    try:
       search_results = sp.search(q="album:" + album_name, type="album") 
       album_uri = search_results['albums']['items'][0]['uri']
       album_track_results = sp.album_tracks(album_uri)
       album_tracks = album_track_results['items']
       album_track_list = []
       for album_track in album_tracks:
            album_track_list.append(album_track['name'])
       as_dict[album_name] = album_track_list
    except:
        print("album %s not found :(" % album_name)
    return as_dict

#now that the directories are made let's make folders for each of the albums.
def generate_album_folders(album_list, song_dest, spec_dest, sp):

    #first let's define an empty dictionary which we will be appending too
    as_dict = {}
    #let's experiment with getting the first album
    as_dict = append_as_dict(album_list[0], as_dict, sp)

    #now let's write a loop that generates as_dict
    for i in tqdm(range(len(album_list)), desc = "as_dict progres...", position=0, leave=True):
        as_dict = append_as_dict(album_list[i], as_dict, sp)


    #now return the album_dict
    return as_dict

as_dict = generate_album_folders(album_list, song_dest, spec_dest, sp)
print(as_dict)