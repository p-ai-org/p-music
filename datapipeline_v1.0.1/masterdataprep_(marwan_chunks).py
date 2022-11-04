# file to handle data prep for our model
# @oscars47

#----------------------------
# 1. Pass top 5000 csv to findalbums, which generates subdirectories corresponding to each album name, along with csv containing names of songs

# 2. For each song within each album directory
#   a. Call downloadsongs 
#   b. Call generatespectrograms

# 3. Build dataset with tf.keras.utils.image_dataset_from_directory -- later

# imports ----------------------------
import pandas as pd
import os
from os import path
from downloadsongs import *
from findalbums import *
from generatespectrograms import *

# 1. load csv ----------------------
data = pd.read_csv('merged_features.csv')
# extract column with names
_N = 1000 # Download albums from 1000 onwards....
album_list = data['Album'].to_list()[_N:] 
#print(album_list)

# set song, spectrogram outputs
song_dest = '/Volumes/PHLUID/p-ai/songs'
spec_dest = '/Volumes/PHLUID/p-ai/spectrograms'
#print(spec_dest)

# make directories
if not(path.exists(song_dest)):
    print('making song dir!')
    os.makedirs(path.join(song_dest))
if not(path.exists(spec_dest)):
    os.makedirs(path.join(spec_dest))

# function to call for each chunk of album data
def get_data(album_list):
    # first get album-song dict
    as_dict = get_tracks(album_list)

    # now go through each album; create subdirectory in songs; download songs
    print('downloading songs and converting to spectrograms...')
    for i, album_name in enumerate(album_list):
        # get rid of spaces
        # name_split = album_name.split(' ')
        # album_name_label = ''
        # for part in name_split:
        #     album_name_label+=part

        percent = round((i/len(album_list))*100, 3)
        print ('total progress: ' + str(percent) + '%', end="\r")
        
        album_dir = path.join(song_dest, album_name)
        # see if it exists or not -- this gives error
        if not(path.isdir(album_dir)):
            #print(album_dir)
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
        get_spectrograms_master_clipped(album_dir, outpath)
    
# break up album list into 4 chunks
list_al = []
i_step = int(len(album_list[_N:]) / 4)
for i in range(2,4):
    al = album_list[i + _N:(i+1)*i_step +_N]
    list_al.append(al)

# now call each of the al on get_data
for i, al in enumerate(list_al):
    print('-----------')
    print('running chunk %i' %i)
    get_data(al)


