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
from tqdm import tqdm
from os import path

# NOTE: YOU WILL NEED TO DEFINE THE PATH TO YOUR CSV AND CHANGE THE SONG/SPEC PATHS IN ORDER FOR THIS TO WORK!

# 1. load csv ----------------------
data = pd.read_csv('merged_features.csv')
# extract column with names
#_N = 1000 # I'm grabbing first 1000 songs
album_list = data['Album'].to_list()
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

from downloadsongs import *
from findalbums import *
from generatespectrograms import *

# function to call for each chunk of album data
def get_data(albums):

    # first get album-song dict
    as_dict = get_tracks(albums)

    # now go through each album; create subdirectory in songs; download songs
    print('downloading songs and converting to spectrograms...')

    for i in tqdm (range(len(albums)), desc='chunk progress...', position=0, leave=True): #can't use enumerate for alive_bar
        album_name = albums[i]
        # get rid of spaces
        # name_split = album_name.split(' ')
        # album_name_label = ''
        # for part in name_split:
        #     album_name_label+=part

        # percent = round((i/len(album_list))*100, 3)
        # print ('total progress: ' + str(percent) + '%', end="\r")
        
        album_dir = path.join(song_dest, album_name)
        # see if it exists or not -- this gives error
        if not(path.isdir(album_dir)):
            #print(album_dir)
            os.mkdir(album_dir)
        # now access each song in the album dict
        songs = as_dict[album_name]
        # download each song and save to directory
        # define progressbars

        print(songs)
        
       
        for j in tqdm (range(len(songs)), desc='getting album songs...', position=1, leave=True):
            song = songs[j]
            download_song(song, album_dir)
            # set outgoing path
            outpath = path.join(spec_dest, album_name)
            if not(path.isdir(outpath)):
                os.mkdir(outpath)
                # update progress bar
                
        # get spectrograms
        get_spectrograms_master_clipped(album_dir, outpath)
        
        


    
# break up album list into 16 chunks
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

#get_data(list_al[3])

# # now call each of the al on get_data
# # for i, al in enumerate(list_al):
# #     print('-----------')
# #     print('running chunk %i' %i)
# #     get_data(al)

# # # can call on each chunk individually
# # get_data(list_al[0])

# # get user input
print('chunk data:')
print(chunk_data)
#print(len(album_list))
print(len(list_al))
choice = input("do you want to run on (a) all chunks or (b) on one chunk? type 'a' or 'b':")

if choice=='a': # do everything
    for i in tqdm (range(len(list_al)), desc='total progress', position=0, leave=True):
        al = list_al[i]
        get_data(al)
elif choice=='b': #now prompt for what chunk
    condition=True
    while condition == True:
        chunk_index = input('type index of desired chunk:')
        if int(chunk_index) <= len(list_al)-1:
            print('running on chunk', chunk_index)
            get_data(al)
            condition = False
        else:
            print('please enter a valid chunk.')


