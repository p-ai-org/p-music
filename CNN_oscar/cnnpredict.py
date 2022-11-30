# file to predict album ratings based on trained cnn/b-cnn
# @oscar47

import os
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# load in directories--------
MAIN_DIR = '/home/oscar47/Desktop/P-ai/'
MODEL_PATH = os.path.join(MAIN_DIR, 'models')
TRAIN_DIR = os.path.join(MAIN_DIR, 'train_data')
OUT_DIR = os.path.join(MAIN_DIR, 'out_data')

# load in model!-------------
model = load_model(os.path.join(MODEL_PATH, 'trim13.h5'))


# load the x and y extra data----
extra_x_ds = np.load(os.path.join(TRAIN_DIR, 'extra_x_ds_2.npy'))
extra_y_ds = np.load(os.path.join(TRAIN_DIR, 'extra_y_ds.npy'))
val_x_ds = np.load(os.path.join(TRAIN_DIR, 'val_x_ds_2.npy'))
val_y_ds = np.load(os.path.join(TRAIN_DIR, 'val_y_ds.npy'))
train_x_ds = np.load(os.path.join(TRAIN_DIR, 'train_x_ds_2.npy'))
train_y_ds = np.load(os.path.join(TRAIN_DIR, 'train_y_ds.npy'))

# function to manage predictions. takes in model------------
# model is model file, input is x data, targets is y data, albums is albums names, outpath is where to store df; savename is what to call file
def model_predict(model, input, targets, outpath):
    predictions = model.predict(input) # this will be an np array of 1 element arrays containing the scores; need to convert to list
    # print(predictions)
    # print(targets)
    predictions_ls = []
    targets_ls = []
    for i in range(len(predictions)):
        predictions_ls.append(np.argmax(predictions[i]))
        targets_ls.append(np.argmax(targets[i]))
    
    # now create dataframe to compare the results vs targets
    results = pd.DataFrame()
    #results['album'] = albums
    results['actual score'] = targets_ls
    results['predicted score'] = predictions_ls

    print(targets_ls)

    get_confusion_matrix(targets_ls, predictions_ls)

    # save!
    print('saving!')
    results.to_csv(os.path.join(outpath, savename))

def get_confusion_matrix(output_targets, output_preds):
    # create a confusion matrix to illustrate results
    cm = confusion_matrix(output_targets, output_preds)
    cm_df = pd.DataFrame(cm, index = list(range(6, 11, 1)), columns = list(range(6, 11, 1)))
    # compute accuracy
    accuracy = 0
    for i in range(len(cm)):
        for j in range(len(cm[i])):
            if i ==j:
                accuracy += cm[i][j]
    accuracy /= len(output_preds) # divide total correct by total obs
    cm_norm_df = cm_df / cm_df.sum() # divide each column by the sum for that column to determine relative precentage
    # plot
    plt.figure(figsize=(10,7))
    sns.heatmap(cm_norm_df, cmap = 'viridis', annot=True)
    plt.title('trim13 - train, accuracy = %f'%np.round(accuracy, 4), fontsize=20)
    plt.ylabel('Actual variable class', fontsize=16)
    plt.xlabel('Predicted variable class', fontsize=16)
    #plt.savefig(os.path.join(DATA_DIR, 'confusion_acc_v0.0.1.jpeg'))
    plt.show()

# album names (last 15%)-----------
# albums_df = pd.read_csv(os.path.join(TRAIN_DIR, 'extra_albums.csv'))
# albums = albums_df['album'].to_list()
# savename = 'silver4_results.csv'

model_predict(model, train_x_ds, train_y_ds, OUT_DIR)




savename='train_results.csv'
#print(train_y_ds)
#model_predict(model, train_x_ds, train_y_ds, OUT_DIR, savename)