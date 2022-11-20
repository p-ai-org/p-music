# first implementation of CNN for P-music
# @oscars47

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cnnhelperprep import *

# define directories---------
MAIN_DIR = '/home/oscar47/Desktop/P-ai'
SPEC_DIR = os.path.join(MAIN_DIR, 'spectrograms')
TRAIN_DIR = os.path.join(MAIN_DIR, 'train_data') # to store out .npy files

# call histogram function-------
#make_hist(SPEC_DIR, MAIN_DIR)

# call dataset gen functions-----------
# note depending on computer strength you may need to rescale the img height and width
# resize image by half
merged_df = pd.read_csv(os.path.join(MAIN_DIR, 'p-music/merged_features.csv'))

choice = input('do you want to (a) build spec ds or (b) build label ds?')
condition=True
while condition==True:
    if choice=='a':
        condition=False
        build_spec_ds(SPEC_DIR, img_height=256, img_width=500)
        
    elif choice=='b':
        condition=False
        build_label_ds(SPEC_DIR, merged_df)
    elif choice=='c':
        condition=False
        #print(np.zeros((256, 500)))
        print(os.path.isdir(MAIN_DIR))
    else:
        print('try again!')

# display results!
#if os.path.exists(os.path.join(TRAIN_DIR, 'val_x_ds.npy')):
    #val_x_ds = np.load(os.path.join(TRAIN_DIR, 'val_x_ds.npy'))
    #print(val_x_ds)
if os.path.exists(os.path.join(TRAIN_DIR, 'val_y_ds.npy')):
    val_y_ds = np.load(os.path.join(TRAIN_DIR, 'val_y_ds.npy'))
    print(val_y_ds[0])