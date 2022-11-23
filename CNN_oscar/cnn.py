# file to implement the cnn
# @oscars47
# first call mastercnn prep to generate np arrays; then run this file

import os
import numpy as np
from keras import layers
from keras.models import Model, Sequential, load_model
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
import wandb
from wandb.keras import WandbCallback


# define directories---------
MAIN_DIR = '/home/oscar47/Desktop/P-ai'
TRAIN_DIR = os.path.join(MAIN_DIR, 'train_data') # to store out .npy files

# get np arrays for training!------
train_x_ds = np.load(os.path.join(TRAIN_DIR, 'train_x_ds_2.npy')) 
val_x_ds = np.load(os.path.join(TRAIN_DIR, 'val_x_ds_2.npy')) 
train_y_ds = np.load(os.path.join(TRAIN_DIR, 'train_y_ds.npy')) 
val_y_ds = np.load(os.path.join(TRAIN_DIR, 'val_y_ds.npy'))

# define shape of incoming and outgoing factors
input_shape = train_x_ds[0].shape
output_shape = train_y_ds[0].shape
print(input_shape, output_shape)

print(val_x_ds.shape)
print(val_y_ds.shape)

# define cnn---------------
def build_model(input_shape, size1, size2, size3, dense1, learning_rate):
    model = Sequential() # initialize Sequential model object so we can add layers sequentially
    #model.add(layers.InputLayer(input_shape)) # add the shape of our input x training vectors
    # add a sequence of 5 convolutional layers, alternating Conv2D and MaxPooling
    model.add(layers.Conv2D(size1, (3, 3), activation='relu', input_shape = input_shape)) # the (3,3) is size of the kernel -- this is a hyperparam we can use wanb to investigate as well
    model.add(layers.MaxPool2D((2,2)))

    model.add(layers.Conv2D(size2, (3, 3), activation='relu'))
    model.add(layers.MaxPool2D((2,2)))

    model.add(layers.Conv2D(size3, (3, 3), activation='relu'))
    model.add(layers.MaxPool2D((2,2)))

    model.add(layers.Flatten()) # convert array to vector
    model.add(layers.Dense(dense1, activation='relu')) # add a final dense layer
    model.add(layers.Dense(1)) # match output size: which should just be size 1 (a single number)

    optimizer = Adam(learning_rate = learning_rate) # compile the model!
    model.compile(optimizer=optimizer, loss='mse')

    return model

# function for training
def train(config=None):
    with wandb.init(config=config):
    # If called by wandb.agent, as below,
    # this config will be set by Sweep Controller
      config = wandb.config

      #pprint.pprint(config)

      #initialize the neural net; 
      global model
      model = build_model(input_shape, config.size_1,  config.size_2, config.size_3,  
              config.dense1, config.learning_rate)
      
      #now run training
      history = model.fit(
        train_x_ds, train_y_ds,
        batch_size = config.batch_size,
        validation_data=(val_x_ds, val_y_ds),
        epochs=config.epochs,
        callbacks=[WandbCallback()] #use callbacks to have w&b log stats; will automatically save best model                     
      )

def train_custom():
   global model
   model = build_model(input_shape, 32,  32, 32, 32, 0.01)
      
   #now run training
   history = model.fit(
      train_x_ds, train_y_ds,
      batch_size = 32,
      validation_data=(val_x_ds, val_y_ds),
      epochs=3,
      #callbacks=[WandbCallback()] #use callbacks to have w&b log stats; will automatically save best model                     
   )

# set dictionary with random search; optimizing val_loss--------------------------
sweep_config= {
    'method': 'random',
    'name': 'val_accuracy',
    'goal': 'maximize'
}

sweep_config['metric']= 'val_accuracy'
parameters_dict = {
    'epochs': {
       'distribution': 'int_uniform',
       'min': 20,
       'max': 100
    },
    # for build_dataset
     'batch_size': {
       'values': [32, 64, 96, 128]
    },
    'size_1': {
       'distribution': 'int_uniform',
       'min': 64,
       'max': 256
    },
    'size_2': {
       'distribution': 'int_uniform',
       'min': 64,
       'max': 256
    },'size_3': {
       'distribution': 'int_uniform',
       'min': 64,
       'max': 256
    },
    'dense1': {
       'distribution': 'int_uniform',
       'min': 64,
       'max': 256
    },
    'learning_rate':{
         #uniform distribution between 0 and 1
         'distribution': 'uniform', 
         'min': 0,
         'max': 0.1
     }
}

# append parameters to sweep config
sweep_config['parameters'] = parameters_dict 

#train_custom()

# login to wandb----------------
wandb.init(project="Oscar CNN1", entity="p-ai")

# initialize sweep agent
sweep_id = wandb.sweep(sweep_config, project="Oscar CNN1", entity="p-ai")
wandb.agent(sweep_id, train, count=100)