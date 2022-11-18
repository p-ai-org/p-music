# file to generate training and validation datasets
# @oscars47

import os, cv2 # note to install cv2 run "git config pull.rebase false"
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# get spec dataset
def build_spec_ds(album_path, img_height, img_width):
    albums = os.listdir(album_path)
    all_albums_spec_ls = [] # init list to hold the subarrays of aubarrays per album per song

    for i in tqdm(range(len(albums)), desc='loading albums (upper)...', position=0, leave=True):
        album = albums[i]
        if os.path.isdir(album): # if it's a valid directory
            songs = os.listdir(album)
            albums_spec_ls = [] # list to hold song np.arrays for a given album
            for j in tqdm(range(len(songs)), desc='inner song loop...', position=1, leave=True):
                song = songs[j]
                if (song.endswith('.png')) or (song.endswith('jpeg')): # confirm we're loading images
                    img = cv2.imread(os.path.join(album_path, song))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # HSV color option is best for object tracking
                    img = cv2.resize(img, (img_width, img_height))
                    albums_spec_ls.append(np.array(img))

                    # NEED TO CHECK WE HAVENT EXCEEDED NUMBER OF ALLOWED SPECTROGRAMS
                    
                     
            # convert the list to np.array and append to main list
            all_albums_spec_ls.append(np.array(albums_spec_ls))
            
    # split ds 80-20
    index = int(len(all_albums_spec_ls)*0.8)
    train_img_list = all_albums_spec_ls[:index]
    val_img_list = all_albums_spec_ls[index:]
   
    train_x_ds = np.array(train_img_list)
    val_x_ds = np.array(val_img_list)

    # preprocess here
    train_x_ds = train_x_ds.astype('float32')
    train_x_ds /= 255 # rescale by 255 bc rgb

    val_ds = train_x_ds.astype('float32')
    val_ds /= 255
    
    return train_x_ds, val_x_ds

# takes in ds
def build_label_ds(album_path, ds):
    albums = os.listdir(album_path)
    # extract the features we want
    #     Metacritic Critic Score (Metacritic Reviews), 
    #     Metacritic User Score (Metacritic User Reviews),
    #     AOTY Critic Score (AOTY Critic Reviews), 
    #     AOTY User Score (AOTY User Reviews)

    # define list to hold all np.arrays for each song
    total_scores = []

    for i in tqdm(range(len(albums)), desc='loading scores...', position=0, leave=True):
        album = albums[i]
        if os.path.isdir(album): # if it's a valid directory
            album_scores = [] # initialize list to store scores for a particular album
            album_row = ds.loc[ds['Album']==album]
            mccs = album_row['Metacritic Critic Score'].to_list()[0]
            mccr = album_row['Metacritic Reviews'].to_list()[0]
            mcus = album_row['Metacritic User Score'].to_list()[0]
            mcur = album_row['Metacritic User Reviews'].to_list()[0]
            aotycs = album_row['AOTY Critic Score'].to_list()[0]
            aotycr = album_row['AOTY Critic Reviews'].to_list()[0]
            aotyus = album_row['AOTY User Score'].to_list()[0]
            aotyur = album_row['AOTY User Reviews'].to_list()[0]

            # append raw scores
            album_scores.append(mccs, mcus, aotycs, aotyus)

            # now compute weighted mean
            num_reviews = mccr + mcur + aotycr + aotyur
            weighted_mean = (mccr / num_reviews)*mccs + (mcur / num_reviews)*mcus + (aotycr / num_reviews)*aotycs + (aotyur / num_reviews) * aotyus
            # append!
            album_scores.append(weighted_mean)

            # now convert to np.array and add to total_scores
            total_scores.append(np.array(album_scores))
    
    # split 80-20
    index = int(len(total_scores)*0.8)
    train_y_list = total_scores[:index]
    val_y_list = total_scores[index:]

    train_y_list = np.array(train_y_list)
    val_y_list = np.array(val_y_list)

    return train_y_list, val_y_list


# function to make histogram
def make_hist(input, output):
    num_songs = []
    for subpath in os.listdir(input):
        total_path = os.path.join(input, subpath)
        if os.path.isdir(total_path):
            num_songs.append(len(os.listdir(total_path)))

    print('min', min(num_songs), 'max', max(num_songs), 'median', np.median(num_songs))
    # plot a histogram
    plt.figure(figsize=(10, 5))
    plt.hist(num_songs, color='magenta', bins=100)
    plt.xlabel('Number of songs per album')
    plt.ylabel('Number of albums')
    plt.savefig(os.path.join(output, 'song_hist.jpeg'))
    