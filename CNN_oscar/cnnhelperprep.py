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

            # get random song
            song_index = int(len(songs)*np.random.random())
            song = songs[song_index]

            if (song.endswith('.png')) or (song.endswith('jpeg')): # confirm we're loading images
                img = cv2.imread(os.path.join(album_path, album, song))
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY
                #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
                img = cv2.resize(img, (img_width, img_height))

                
                # print(np.array(img).shape)
                # print(np.array(img))
                all_albums_spec_ls.append(np.array(img))
                # visualize
                # plt.figure(figsize=(10,3))
                # plt.imshow(img)
                # plt.show()
                # print(img.shape)
        



            # superspec cut

            # for j in tqdm(range(len(songs)), desc='inner song loop p.1...', position=1, leave=False):
            #     song = songs[j]
            #     if j >= 11:
            #         break

            #     if (song.endswith('.png')) or (song.endswith('jpeg')): # confirm we're loading images
            #         img = cv2.imread(os.path.join(album_path, album, song))
            #         #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY
            #         #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            #         img = cv2.resize(img, (img_width, img_height))

                    
            #         # print(np.array(img).shape)
            #         # print(np.array(img))
            #         albums_spec_ls.append(np.array(img))

            #         # NEED TO CHECK WE HAVENT EXCEEDED NUMBER OF ALLOWED SPECTROGRAMS
            #         # use histogram to determine median number; append arrays of 0s for those that don't have enough

            #         #print(albums_spec_ls)
                
            #     if (len(songs) < 11) and (j==len(songs)-1): # if on last index and has below 11 songs
            #         for k in tqdm(range(11-len(songs)), desc='padding deficient album...', position=1, leave=False):
            #             #print(img_height)
            #             albums_spec_ls.append(np.zeros(img.shape, dtype='uint8')) # 3 for 3 colors
            #             #print(albums_spec_ls)
            #             #print(np.zeros((img_height, img_width, 3), dtype='float32').shape)
                
                     
            # # concatenate the spectrograms horizontally!
            # #print(albums_spec_ls)
            # super_spectrogram = np.concatenate(albums_spec_ls, axis=1)

            # #visualize
            # # plt.figure(figsize=(10,3))
            # # plt.imshow(super_spectrogram)
            # # plt.show()
            # # print(super_spectrogram.shape)

            # all_albums_spec_ls.append(super_spectrogram)

            # end cut---------------------------------------


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
         
            # # convert to np.array
            # vec = np.zeros(11)
            # # find class of score
            # star = find_star(weighted_mean)
            # vec[star]=1 # all 0s except for 1 1 @ index corresponding to score
            #total_scores.append(vec)
    
    num_classes = 4 # number of stars we want
    global stars # make it global so we can access it later
    stars = find_classes(total_scores_values, num_classes)
    print('stars:', stars)

    # use this list of tuples to define find star function to then get 1-hot vectors
    for score in total_scores_values:
        # initialize 1 hot vector
        vec = np.zeros(num_classes)
        for i, star in enumerate(stars):
            if (score >= star[0]) and (score < star[1]): # if we're within target range
                vec[i]=1
        # append np.array
        total_scores.append(np.array(vec))     
    
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

    print(train_y_ds.shape)

    # add extra albums to dataframe to save
    extra_albums_df = pd.DataFrame()
    extra_albums_df['album'] = extra_albums

    #save!!
    print('saving!')
    np.save(os.path.join(TRAIN_DIR, 'train_y_ds.npy'), train_y_ds)
    np.save(os.path.join(TRAIN_DIR, 'val_y_ds.npy'), val_y_ds)
    np.save(os.path.join(TRAIN_DIR, 'extra_y_ds.npy'), extra_y_ds)
    extra_albums_df.to_csv(os.path.join(TRAIN_DIR, 'extra_albums.csv'))

    # # make histogram
    # make_hist_scores(total_scores_values, train_scores_values, MAIN_DIR)

# extra function to find the distribution of songs for labeling-----
def find_classes(total_scores, num_classes):
    num_in_class = int(len(total_scores) / num_classes)
    class_tuples = []
    scores_sorted = sorted(total_scores)
    # print(total_scores)
    # print(scores_sorted)
    for i in range(num_classes): # need this to not have -1
        scores_clipped = scores_sorted[i*num_in_class: (i+1)*num_in_class+1] # want in this range of indices
        class_tuples.append((scores_clipped[0], scores_clipped[-1]))
        print('num objects in class', len(scores_clipped))
    return class_tuples # save as tuples so we can know what scores


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