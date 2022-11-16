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
def generate_as_dict(album_list, song_dest, spec_dest, sp):

    #first let's define an empty dictionary which we will be appending too
    as_dict = {}

    #now let's write a loop that generates as_dict
    for i in tqdm(range(len(album_list)), desc = "as_dict progres...", position=0, leave=True):
        as_dict = append_as_dict(album_list[i], as_dict, sp)


    #now return the album_dict
    return as_dict


def create_chunks(album_list):
    '''
    This function will create the chunks necessary for us to begin generating the dataset.
    '''
    # break up album list into 16 chunks------------------
    chunk_num = 16
    list_al = []
    i_step = int(len(album_list) / chunk_num)
    chunk_data = pd.DataFrame({'chunk':[], 'start index':[], 'end index':[], 'num songs':[]})
    for i in range(chunk_num):
        start_index = i*i_step
        # if end eindex is within bounds of the album list
        if (i+1)*i_step <= len(album_list)-1:
            end_index = (i+1)*i_step
            al = album_list[start_index:end_index]
        else:
            end_index =len(album_list)
            al = album_list[start_index:end_index]
        # update df
        chunk_data = chunk_data.append({'chunk': i, 'start index': start_index, 'end index': end_index, 'num songs': len(al)}, ignore_index=True)
        list_al.append(al)
    return list_al, chunk_data


def make_album_directories(as_dict, song_dest, spec_dest, sp):
    '''
    This function will create the album directories given an as_dict...
    '''

    #first change to the song_dest folder..
    os.chdir(song_dest)

    #now for each "album_name" in the as_dict we will create the corresponding folder..
    for i in tqdm(range(len(as_dict.keys())), desc = "creating album_dirs progress...", position=0, leave=True):
        album_name = list(as_dict.keys())[i]
        #we must first clean the album name...
        clean_album_name = album_name.replace(" ", "_")
        clean_album_name = "".join(e for e in clean_album_name if (e.isalnum() or e == "_"))
        #Now we create a directory for each album
        os.mkdir(clean_album_name)

    
def download_songs(as_dict, song_dest, spec_dest, sp):
    '''
    This function takes an as_dict and downloads the songs into the corresponding folder.
    '''

    #first let's make sure we're in the song_directory
    os.chdir(song_dest)
    #next we will iterate through the album_names in our dict
    for i in tqdm(range(len(as_dict.keys())), desc = "downloading songs progress...", position=0, leave=True):
        album_name = list(as_dict.keys())[i]
        #we must first clean the album name...
        clean_album_name = album_name.replace(" ", "_")
        clean_album_name = "".join(e for e in clean_album_name if (e.isalnum() or e == "_"))
        
        #If we find a dir with the "clean album name" we will change into that directory and download all the songs
        album_dir = song_dest + '/' + clean_album_name
        dir_exists = os.path.isdir(album_dir)
        if (dir_exists):
            os.chdir(album_dir)
            song_list = as_dict[album_name]
            #now we loop through the song_lists and download the songs
            for i in tqdm(range(len(song_list)), desc= "downloading " + album_name + " songs...", position=0, leave=True):
                download_song(song_list[i], song_dest, sp)
        else:
            print("album not found :(")


            
            

def main(album_list, song_dest, spec_dest, sp):
    '''
    This function will do what is necessary to create our directory of chunks
    '''
    chunked_album_list, chunk_data = create_chunks(album_list)
    #Determine which chunks we want to download...
    chunks_to_download = [9]
    chunks_to_download = [chunked_album_list[i] for i in chunks_to_download]

    #Now let's create a new chunk_album_dicts, which is a list of album_dicts
    chunk_album_dicts = [generate_as_dict(i,song_dest, spec_dest, sp) for i in chunks_to_download]

    #Now using each of these chunks we must make directories, which we can do with the following...
    for as_dict in chunk_album_dicts:
        make_album_directories(as_dict, song_dest, spec_dest, sp)

    #now that we've made all the directories we must download each of the songs into the corresponding songs folder
    for as_dict in chunk_album_dicts:
        download_songs(as_dict, song_dest, spec_dest, sp)

    return chunk_album_dicts


chunk_album_dicts = main(album_list, song_dest, spec_dest, sp)
print(chunk_album_dicts)