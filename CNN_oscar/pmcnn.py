# first implementation of CNN for P-music
# @oscars47

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from keras import layers
# from keras.models import Model, Sequential, load_model
# from keras.callbacks import ModelCheckpoint

# load in spectograms, get stats -- plot histogram! ----
MAIN_DIR = '/Volumes/PHLUID/P-ai'
DATA_DIR = os.path.join(MAIN_DIR, 'spectrograms')

num_songs = []
for subpath in os.listdir(DATA_DIR):
    total_path = os.path.join(DATA_DIR, subpath)
    if os.path.isdir(total_path):
        num_songs.append(len(os.listdir(total_path)))

print('min', min(num_songs), 'max', max(num_songs), 'median', np.median(num_songs))
# plot a histogram
plt.figure(figsize=(10, 5))
plt.hist(num_songs, color='magenta', bins=100)
plt.xlabel('Number of songs per album')
plt.ylabel('Degeneracy')
os.chdir(MAIN_DIR)
plt.savefig('song_hist.jpeg')

# extract column from merged dataset with album name. np array of with output score as single element in list------------
data = pd.read_csv('merged_features.csv')

# initializing new dataframe
# raw_total = pd.DataFrame({'album':[], 'rating':[]})

# data prep-------------------

# extract column with names
for subpath in os.listdir(DATA_DIR):
    total_path = os.path.join(DATA_DIR, subpath)
    if os.path.isdir(total_path):
        try:
            album_row = data.loc[data['Album']==subpath]
            #load images by calling other function; calculate score
            #append this to total x (array of arrays of images converted to normalized numpy) nd y (1d array of 1d arrays containing score) datasets; will do 80-20 split
        except:
            print('album %s could not be found in the data!' %subpath)

# can predict each of the 3 scores plus combined

# implement bayesian NN