# file to predict album ratings based on trained cnn/b-cnn
# @oscar47

import os
import numpy as np
import pandas as pd
from keras.models import load_model

# load in directories--------
MAIN_DIR = '/home/oscar47/Desktop/P-ai/'
MODEL_PATH = os.path.join(MAIN_DIR, 'models')
TRAIN_DIR = os.path.join(MAIN_DIR, 'train_data')
OUT_DIR = os.path.join(MAIN_DIR, 'out_data')

# load in model!-------------
model = load_model(os.path.join(MODEL_PATH, 'floral7.h5'))


# load the x and y extra data----
extra_x_ds = np.load(os.path.join(TRAIN_DIR, 'extra_x_ds_2.npy'))
extra_y_ds = np.load(os.path.join(TRAIN_DIR, 'extra_y_ds.npy'))
val_x_ds = np.load(os.path.join(TRAIN_DIR, 'val_x_ds_2.npy'))
val_y_ds = np.load(os.path.join(TRAIN_DIR, 'val_y_ds.npy'))
train_x_ds = np.load(os.path.join(TRAIN_DIR, 'train_x_ds_2.npy'))
train_y_ds = np.load(os.path.join(TRAIN_DIR, 'train_y_ds.npy'))

# function to manage predictions. takes in model------------
# model is model file, input is x data, targets is y data, albums is albums names, outpath is where to store df; savename is what to call file
def model_predict(model, input, targets, albums, outpath, savename):
    predictions = model.predict(input) # this will be an np array of 1 element arrays containing the scores; need to convert to list
    # print(predictions)
    # print(targets)
    predictions_ls = []
    targets_ls = []
    for i in range(len(predictions)):
        predictions_ls.append(predictions[i][0])
        targets_ls.append(targets[i][0])
    
    # now create dataframe to compare the results vs targets
    results = pd.DataFrame()
    results['album'] = albums
    results['actual score'] = targets_ls
    results['predicted score'] = predictions_ls

    # save!
    print('saving!')
    results.to_csv(os.path.join(outpath, savename))

# album names (last 15%)-----------
albums_df = pd.read_csv(os.path.join(TRAIN_DIR, 'extra_albums.csv'))
albums = albums_df['album'].to_list()
savename = 'silver4_results.csv'
model_predict(model, extra_x_ds, extra_y_ds, albums, OUT_DIR, savename)
savename='train_results.csv'
#print(train_y_ds)
#model_predict(model, train_x_ds, train_y_ds, OUT_DIR, savename)