# python file to download songs given song name and output directory
# @oscars47
# for spotipy need to go to developer.spotify.com
import os

from spotipykeys import keys
import spotdl
from spotdl import Spotdl

SPOTIPY_CLIENT_ID=keys['spotipy_client_id']
SPOTIPY_CLIENT_SECRET=keys['spotipy_client_secret']
SPOTIPY_REDIRECT_URI=keys['spotipy_redirect_url']

spotdl = Spotdl(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)

# method to download song based on song name
def download_song(song_name, song_dir):
    # call search method
    song = spotdl.search(['Famous'])
    # change directory
    os.chdir('song_dir')
    # call spotdl object
    results = spotdl.download_songs(song)
