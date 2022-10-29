# file to handle data prep for our model
# @oscars47

#----------------------------
# 1. Pass top 5000 csv to FindAlbums, which generates subdirectories corresponding to each album name, along with csv containing names of songs

# 2. For each song within each album directory
#   a. Call DownloadSongs 
#   b. Call GenerateSpectrograms

# 3. Build dataset with tf.keras.utils.image_dataset_from_directory

# imports ----------------------------
import pandas as pd
import os
from os import path
from downloadsongs import *
from findalbums import *
from generatespectrograms import *

# 1. load csv ----------------------
data = pd.read_csv('rym_top_5000_all_time.csv')
# extract column with names
album_list = data['Album'].to_list()[4:6]
print(album_list)

# set song, spectrogram outputs
song_dest = '/Volumes/PHLUID/p-ai/songs'
spec_dest = '/Volumes/PHLUID/p-ai/spectrograms'
print(spec_dest)

#2. call helper functions------------
# first get album-song dict
as_dict = get_tracks(album_list)
print(as_dict)

# make directories
# os.makedirs(path.join(song_dest))
# os.makedirs(path.join(spec_dest))

# now go through each album; create subdirectory in songs; download songs
for i, album_name in enumerate(album_list):
    # get rid of spaces
    # name_split = album_name.split(' ')
    # album_name_label = ''
    # for part in name_split:
    #     album_name_label+=part
    
    album_dir = path.join(song_dest, album_name)
    # see if it exists or not -- this gives error
    if not(path.isdir(album_dir)):
        print(album_dir)
        os.mkdir(album_dir)
    # now access each song in the album dict
    songs = as_dict[album_name]
    # download each song and save to directory
    for song in songs:
        download_song(song, album_dir)
        # set outgoing path
        outpath = path.join(spec_dest, album_name)
        if not(path.isdir(outpath)):
            os.mkdir(outpath)
        # get spectrograms
        get_spectrograms(album_dir, outpath)
    # now get spectrograms
    percent = round((i/len(album_list))*100, 3)
    print ('progress: ' + str(percent) + '%', end="\r")
    
    

