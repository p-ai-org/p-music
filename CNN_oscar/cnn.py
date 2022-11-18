# file to implement the cnn
# @oscars47
# first call mastercnn prep to generate np arrays; then run this file

import os
import numpy as np
from keras import layers
from keras.models import Model, Sequential, load_model
from keras.callbacks import ModelCheckpoint

# define directories---------
MAIN_DIR = '/home/oscar47/Desktop/P-ai'
TRAIN_DIR = os.path.join(MAIN_DIR, 'train_data') # to store out .npy files

# get np arrays for training!
train_x_ds = np.load(MAIN_DIR, 'train_x_ds.npy') 
val_x_ds = np.load(MAIN_DIR, 'val_x_ds.npy') 
train_y_ds = np.load(MAIN_DIR, 'train_y_ds.npy') 
val_y_ds = np.load(MAIN_DIR, 'val_y_ds.npy')

# define cnn

