import os
from downloadsongs_MARWAN_VERS import *
from generatespectrograms import *

# choose song name
song_name = "the 59th street bridge song"
# define song path
song_path = '/Users/oscarscholin/Desktop/Pomona/Junior_Year/P-ai/test'

# create new directory for song
t_path = os.path.join(song_path, song_name)
if not(os.path.exists(t_path)):
    os.makedirs(t_path)

# download the song
download_song(song_name, t_path)

# generate spectrogram
get_spectrograms_master_clipped(t_path, t_path)
get_spectrograms_master_all(t_path, t_path)