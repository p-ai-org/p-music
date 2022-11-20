# file to generate training and validation datasets
# @oscars47

import os, cv2 # note to install cv2 run "git config pull.rebase false"
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

MAIN_DIR = '/home/oscar47/Desktop/P-ai'
TRAIN_DIR = os.path.join(MAIN_DIR, 'train_data') # to store out .npy files

# get spec dataset
def build_spec_ds(album_path, img_height, img_width):
    albums = os.listdir(album_path)[:10]
    all_albums_spec_ls = [] # init list to hold the subarrays of aubarrays per album per song

    for i in tqdm(range(len(albums)), desc='loading albums (upper)...', position=0, leave=True):
        album = albums[i]
        if os.path.isdir(os.path.join(album_path, album)): # if it's a valid directory
            songs = os.listdir(os.path.join(album_path, album))
            albums_spec_ls = [] # list to hold song np.arrays for a given album
            for j in tqdm(range(len(songs)), desc='inner song loop...', position=1, leave=False):
                song = songs[j]
                if j >= 11:
                    break

                if (song.endswith('.png')) or (song.endswith('jpeg')): # confirm we're loading images
                    img = cv2.imread(os.path.join(album_path, album, song))
                    #b, g, r = cv2.split(img) # split colors
                    #img = r
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
                    img = cv2.resize(img, (img_width, img_height))

                    #
                    #print(np.array(img).shape)
                    albums_spec_ls.append(np.array(img)) # we want only the r channel
                    #print(np.array(img))

                    # NEED TO CHECK WE HAVENT EXCEEDED NUMBER OF ALLOWED SPECTROGRAMS
                    # use histogram to determine median number; append arrays of 0s for those that don't have enough
                
                if (len(songs) < 11) and (j==len(songs)-1): # if on last index and has below 11 songs
                    for k in tqdm(range(11-len(songs)), desc='padding deficient album...', position=1, leave=False):
                        #print(img_height)
                        albums_spec_ls.append(np.zeros(np.array(img).shape)) # 3 for 3 colors
                        #print(np.zeros((img_height, img_width, 3), dtype='float32').shape)
                
                     
            # convert the list to np.array and append to main list
            all_albums_spec_ls.append(np.array(albums_spec_ls))

    #first split 85-15
    init_split_index = int(.85*len(all_albums_spec_ls))
    tv_albums_spec = all_albums_spec_ls[:init_split_index]
    extra_albums_spec = all_albums_spec_ls[init_split_index:]
            
    # split tv 80-20
    index = int(len(tv_albums_spec)*0.8)
    train_img_list = all_albums_spec_ls[:index]
    val_img_list = all_albums_spec_ls[index:]

   # for ls in train_img_list:
    #    print(ls.shape)
   
    train_x_ds = np.array(train_img_list, dtype='float32')
    val_x_ds = np.array(val_img_list, dtype='float32')

    extra_x_ds = np.array(extra_albums_spec, dtype='float32')

    # preprocess here
    train_x_ds /= 255 # rescale by 255 bc rgb
    val_x_ds /= 255
    extra_x_ds /= 255
    
    #save!!
    print('saving!')
    np.save(os.path.join(TRAIN_DIR, 'train_x_ds.npy'), train_x_ds)
    np.save(os.path.join(TRAIN_DIR, 'val_x_ds.npy'), val_x_ds)
    np.save(os.path.join(TRAIN_DIR, 'extra_x_ds.npy'), extra_x_ds)

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
        if os.path.isdir(os.path.join(album_path, album)): # if it's a valid directory
            album_row = ds.loc[ds['Album']==album]
            aotycs = album_row['AOTY Critic Score'].to_list()[0]
            aotycr = album_row['AOTY Critic Reviews'].to_list()[0]
            aotyus = album_row['AOTY User Score'].to_list()[0]
            aotyur = album_row['AOTY User Reviews'].to_list()[0]

            # now compute weighted mean; need to normalize score!
            num_reviews = aotycr + aotyur
            weighted_mean = ((aotycr / num_reviews)*aotycs + (aotyur / num_reviews) * aotyus) / 100
            # append!
            
            # now convert to np.array and add to total_scores in array
            total_scores.append([np.array(weighted_mean)])
    
    #first split 85-15
    init_split_index = int(.85*len(total_scores))
    tv_scores = total_scores[:init_split_index]
    extra_scores = total_scores[init_split_index:]

    # split tv 80-20
    index = int(len(tv_scores)*0.8)
    train_y_list = tv_scores[:index]
    val_y_list = tv_scores[index:]

    train_y_ds = np.array(train_y_list)
    val_y_ds = np.array(val_y_list)
    extra_y_ds = np.array(extra_scores)

    #save!!
    print('saving!')
    np.save(os.path.join(TRAIN_DIR, 'train_y_ds.npy'), train_y_ds)
    np.save(os.path.join(TRAIN_DIR, 'val_y_ds.npy'), val_y_ds)
    np.save(os.path.join(TRAIN_DIR, 'extra_y_ds.npy'), extra_y_ds)


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
    