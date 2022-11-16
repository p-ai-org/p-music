import os, cv2
import numpy as np
import pandas as pd

# get image dataset
def build_img_ds(img_path, img_height, img_width):
    img_list = []
    for file in os.listdir(img_path):
        #print(file)
        if file.endswith('.jpg'):
            img = cv2.imread(os.path.join(img_path, file))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # HSV color option is best for object tracking
            img = cv2.resize(img, (img_width, img_height))
            #img_list.append([img])
            img_list.append(np.array(img))

    # split ds 80-20
    index = int(len(img_list)*0.8)
    train_img_list = img_list[:index]
    val_img_list = img_list[index:]
   
    train_ds = np.array(train_img_list)
    val_ds = np.array(val_img_list)

    # preprocess here
    train_ds = train_ds.astype('float32')
    train_ds /= 255

    val_ds = train_ds.astype('float32')
    val_ds /= 255
    
    return train_ds, val_ds

def build_label_ds(ds_path):
    # read csv
    df = pd.read_csv(ds_path)
    # extract the features we want
    