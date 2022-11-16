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
make_hist(SPEC_DIR, MAIN_DIR)

# call dataset gen functions-----------
# note depending on computer strength you may need to rescale the img height and width
train_x_ds, val_x_ds = build_spec_ds(SPEC_DIR, img_height=512, img_width=1000)
# save as .npy for later!
np.save(os.path.join(TRAIN_DIR, 'train_x_ds.npy'), train_x_ds)
np.save(os.path.join(TRAIN_DIR, 'val_x_ds.npy'), val_x_ds)

# define the merged csv-----------------
# extract column from merged dataset with album name. np array of with output score as single element in list------------
merged_df = pd.read_csv(os.path.join(MAIN_DIR, 'p-music/merged_features.csv'))

train_y_ds, val_y_ds = build_label_ds(SPEC_DIR, merged_df)
# save as .npy for later!
np.save(os.path.join(TRAIN_DIR, 'train_y_ds.npy'), train_x_ds)
np.save(os.path.join(TRAIN_DIR, 'val_y_ds.npy'), val_x_ds)