# python file to download songs given song name and output directory
# @oscars47
# for spotipy need to go to developer.spotify.com, create app, get client ID and secret ID; then type "export CLIENT_ID = " in terminal to set an environment variable

import os

from spotipykeys import keys

import spotdl
from spotdl import Spotdl

SPOTIPY_CLIENT_ID=keys['spotipy_client_id']
SPOTIPY_CLIENT_SECRET=keys['spotipy_client_secret']
SPOTIPY_REDIRECT_URI=keys['spotipy_redirect_uri']

spotdl = Spotdl(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

# method to download song based on song name
def download_song(song_name, song_dir):
    #print(song_dir)
    # call search method
    try:
        song = spotdl.search([song_name])
        # change directory
        os.chdir(song_dir)
        # call spotdl object
        # don't want to redownload
        if not(os.path.exists(os.path.join(song_dir, song_name, '.mp3'))):
            results = spotdl.download_songs(song)
        # return the song object
        return song
    except:
        print('song %s could not be found' %song_name)
    