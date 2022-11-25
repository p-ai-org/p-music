# file to generate training and validation datasets
# @oscars47

import os, cv2 # note to install cv2 run "git config pull.rebase false"
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

MAIN_DIR = '/home/oscar47/Desktop/P-ai'
TRAIN_DIR = os.path.join(MAIN_DIR, 'train_data') # to store out .npy files
SPEC_DIR = os.path.join(MAIN_DIR, 'spectrograms')

 # define classes of stars for ratings (0-10); the score is the index of the 1 in the 1-hot vector
global stars
stars = np.arange(11, dtype=int)

# get spec dataset
def build_spec_ds(album_path, img_height, img_width, part): # parts tells us to run first or second half
    albums = os.listdir(album_path)
     # for memory usage, split this process in half
    half_index = int(0.5*len(albums))
    if part==0:
        albums = albums[:half_index]
    elif part==1:
        albums = albums[half_index:]
    all_albums_spec_ls = [] # init list to hold the subarrays of aubarrays per album per song

    for i in tqdm(range(len(albums)), desc='loading albums (upper)...', position=0, leave=True):
        album = albums[i]
        if (os.path.isdir(os.path.join(album_path, album))) and (len(os.listdir(os.path.join(album_path, album))) >= 1): # if it's a valid directory
            songs = os.listdir(os.path.join(album_path, album))
            albums_spec_ls = [] # list to hold song np.arrays for a given album
            for j in tqdm(range(len(songs)), desc='inner song loop p.1...', position=1, leave=False):
                song = songs[j]
                if j >= 11:
                    break

                if (song.endswith('.png')) or (song.endswith('jpeg')): # confirm we're loading images
                    img = cv2.imread(os.path.join(album_path, album, song))
                    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY
                    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
                    img = cv2.resize(img, (img_width, img_height))

                    
                    # print(np.array(img).shape)
                    # print(np.array(img))
                    albums_spec_ls.append(np.array(img))

                    # NEED TO CHECK WE HAVENT EXCEEDED NUMBER OF ALLOWED SPECTROGRAMS
                    # use histogram to determine median number; append arrays of 0s for those that don't have enough
                
                if (len(songs) < 11) and (j==len(songs)-1): # if on last index and has below 11 songs
                    for k in tqdm(range(11-len(songs)), desc='padding deficient album...', position=1, leave=False):
                        #print(img_height)
                        albums_spec_ls.append(np.zeros(np.array(img).shape)) # 3 for 3 colors
                        #print(np.zeros((img_height, img_width, 3), dtype='float32').shape)
                
                     
            # concatenate the spectrograms horizontally!
            super_spectrogram = np.concatenate(albums_spec_ls, axis=1)
            #print(super_spectrogram.shape)
            all_albums_spec_ls.append(super_spectrogram)
        # all_albums_spec_ls.append(np.array(albums_spec_ls))
    #first split 85-15
    init_split_index = int(.85*len(all_albums_spec_ls))
    tv_albums_spec = all_albums_spec_ls[:init_split_index]
    extra_albums_spec = all_albums_spec_ls[init_split_index:]
            
    # split tv 80-20
    index = int(len(tv_albums_spec)*0.8)
    train_img_list = tv_albums_spec[:index]
    val_img_list = tv_albums_spec[index:]

   # for ls in train_img_list:
    #    print(ls.shape)
   
    train_x_ds = np.array(train_img_list, dtype='float16')
    print(train_x_ds.shape)
    val_x_ds = np.array(val_img_list, dtype='float16')

    extra_x_ds = np.array(extra_albums_spec, dtype='float16')

    # preprocess here
    train_x_ds /= 255 # rescale by 255 bc rgb
    val_x_ds /= 255
    extra_x_ds /= 255

    print(val_x_ds.shape)
    
    #save!!
    print('saving!')
    np.save(os.path.join(TRAIN_DIR, 'train_x_ds_'+str(part)+'.npy'), train_x_ds)
    np.save(os.path.join(TRAIN_DIR, 'val_x_ds_'+ str(part)+'.npy'), val_x_ds)
    np.save(os.path.join(TRAIN_DIR, 'extra_x_ds_'+str(part)+'.npy'), extra_x_ds)

def find_star(score):
    if (score >=0) and (score < 0.05):
        return 0
    elif (score >=0.05) and (score < 0.15):
        return 1
    elif (score >=0.15) and (score < 0.25):
        return 2
    elif (score >=0.25) and (score < 0.35):
        return 3
    elif (score >=0.35) and (score < 0.45):
        return 4
    elif (score >=0.45) and (score < 0.55):
        return 5
    elif (score >=0.55) and (score < 0.65):
        return 6
    elif (score >=0.65) and (score < 0.75):
        return 7
    elif (score >=0.75) and (score < 0.85):
        return 8
    elif (score >=0.85) and (score < 0.95):
        return 9
    elif (score >=0.95) and (score <= 1):
        return 10
    
    

# takes in ds
def build_label_ds(album_path, ds):
    
    # extract the features we want
    #     Metacritic Critic Score (Metacritic Reviews), 
    #     Metacritic User Score (Metacritic User Reviews),
    #     AOTY Critic Score (AOTY Critic Reviews), 
    #     AOTY User Score (AOTY User Reviews)
    albums = os.listdir(album_path)
    # define list to hold all np.arrays for each song
    total_scores = []
    total_scores_values = []

    albums_ls = [] # to hold the albums used in the extra data

    for i in tqdm(range(len(albums)), desc='loading scores...', position=0, leave=True):
        album = albums[i]
        if (os.path.isdir(os.path.join(album_path, album))) and (len(os.listdir(os.path.join(album_path, album))) >= 1): # if it's a valid directory
            albums_ls.append(album)
            album_row = ds.loc[ds['Album']==album]
            aotycs = album_row['AOTY Critic Score'].to_list()[0]
            aotycr = album_row['AOTY Critic Reviews'].to_list()[0]
            aotyus = album_row['AOTY User Score'].to_list()[0]
            aotyur = album_row['AOTY User Reviews'].to_list()[0]

            # now compute weighted mean; need to normalize score!
            num_reviews = aotycr + aotyur
            weighted_mean = ((aotycr / num_reviews)*aotycs + (aotyur / num_reviews) * aotyus) / 100
            total_scores_values.append(weighted_mean)
         
            # convert to np.array
            cold_vec = np.zeros(11)
            # find class of score
            star = find_star(weighted_mean)
            hot_vec = cold_vec[star]=1 # all 0s except for 1 1 @ index corresponding to score
            total_scores.append(np.array(hot_vec))
    
    #first split 85-15
    init_split_index = int(.85*len(total_scores))
    tv_scores = total_scores[:init_split_index]
    extra_scores = total_scores[init_split_index:]
    extra_albums = albums_ls[init_split_index:]
    tv_scores_values = total_scores_values[:init_split_index]

    # split tv 80-20
    index = int(len(tv_scores)*0.8)
    train_y_list = tv_scores[:index]
    val_y_list = tv_scores[index:]
    train_scores_values = tv_scores_values[:index]

    train_y_ds = np.array(train_y_list)
    val_y_ds = np.array(val_y_list)
    extra_y_ds = np.array(extra_scores)

    print(val_y_ds.shape)

    # add extra albums to dataframe to save
    extra_albums_df = pd.DataFrame()
    extra_albums_df['album'] = extra_albums

    #save!!
    print('saving!')
    np.save(os.path.join(TRAIN_DIR, 'train_y_ds.npy'), train_y_ds)
    np.save(os.path.join(TRAIN_DIR, 'val_y_ds.npy'), val_y_ds)
    np.save(os.path.join(TRAIN_DIR, 'extra_y_ds.npy'), extra_y_ds)
    extra_albums_df.to_csv(os.path.join(TRAIN_DIR, 'extra_albums.csv'))

    # make histogram
    make_hist_scores(total_scores_values, train_scores_values, MAIN_DIR)

# extra data visualization functions
# functions to make histogram--------------
def make_hist_songs(input, output):
    num_songs = []
    for subpath in os.listdir(input):
        total_path = os.path.join(input, subpath)
        if os.path.isdir(total_path):
            num_songs.append(len(os.listdir(total_path)))

    print('min', min(num_songs), 'max', max(num_songs), 'median', np.median(num_songs))
    # plot a histogram
    plt.figure(figsize=(10, 5))
    plt.hist(num_songs, color='magenta', bins=100, alpha=0.5, edgecolor='black', linewidth=2)
    plt.xlabel('Number of songs per album', fontsize=16)
    plt.ylabel('Number of albums', fontsize=16)
    plt.title('Distribution of album songs', fontsize=18)
    plt.savefig(os.path.join(output, 'song_hist.jpeg'))

make_hist_songs(SPEC_DIR, MAIN_DIR)

def make_hist_scores(scores_all, scores_train, output):
    print('min score:', min(scores_all), 'max score:', max(scores_all), 'median score:', np.median(scores_all))
    plt.figure(figsize=(10, 5))
    counts, edges, bars = plt.hist(scores_all, color='magenta', bins=[0.6, .65, .75, .85, .95, 1], alpha=0.5, edgecolor='black', linewidth=2)
    plt.bar_label(bars)
    plt.xlabel('Score', fontsize=16)
    plt.ylabel('Number of albums', fontsize=16)
    plt.title('Distribution of all scores', fontsize=18)
    plt.savefig(os.path.join(output, 'scores_all.jpeg'))

    print('min score train:', min(scores_train), 'max score train:', max(scores_train), 'median score train:', np.median(scores_train))
    plt.figure(figsize=(10, 5))
    counts2, edges2, bars2 = plt.hist(scores_train, color='magenta', bins=[0.6, .65, .75, .85, .95, 1], alpha=0.5, edgecolor='black', linewidth=2)
    plt.bar_label(bars2)
    plt.xlabel('Score', fontsize=16)
    plt.ylabel('Number of albums', fontsize=16)
    plt.title('Distrubution of scores for training', fontsize=18)
    plt.savefig(os.path.join(output, 'scores_train.jpeg'))

# def get_score_dist(scores, output):
#     # get # of counts for each 