# imports ----------------------------
import pandas as pd
import os
from tqdm import tqdm
from os import path
from spotipykeys import keys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from spotdl import Spotdl


#first let's specify the directories where we'll be saving our chunks
# NOTE: YOU WILL NEED TO DEFINE THE PATH TO YOUR CSV AND CHANGE THE SONG/SPEC PATHS IN ORDER FOR THIS TO WORK!

scope = 'user-library-read playlist-modify-public'

SPOTIPY_CLIENT_ID=keys['spotipy_client_id']
SPOTIPY_CLIENT_SECRET=keys['spotipy_client_secret']
SPOTIPY_REDIRECT_URI=keys['spotipy_redirect_uri']

sp= Spotdl(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, user_auth=False)

#Now we will open our file
json_file = open("data.json", "w")
json_file.write("Hello :)")
json_file.close()

