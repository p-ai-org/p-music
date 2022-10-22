# python file to generate spectrograms given a file of mp3
# @oscars47

# imports-----------
# defaults
import os, pydub
from os import path
import numpy as np

# audio specific
from pydub import AudioSegment
import matplotlib.pyplot as plt
from IPython.display import Audio

# machine learning
import tensorflow as tf
import tensorflow_io as tfio

# prepare and load data-----
# assume we have already downloaded our mp3 files. we may need to convert into wav.
def convert_mp3_wav(path_name):
    for subpath in os.listdir(path_name):
        if ".mp3" in subpath:
            # assign files
            input_file = path.join(path_name, subpath)
            # create new subdirectory if does not already exist to store .wav files
            if not(path.isdir(path.join(path_name, 'output'))):
                os.mkdir(path.join(path_name, 'output'))
            output_file = path.join(path_name, 'output', subpath+'.wav')

            # convert mp3 file to wav file
            sound = AudioSegment.from_mp3(input_file)
            sound = sound.set_channels(1)
            sound.export(output_file, format="wav")

# spectrogram convert functions--------

# helper function to generate a single spectrogram
# pass path to waveform and label to save figure
def generate_spectrogram(file_path, label, nfft, window, stride):
    
    # read in song as AudioIOTensor
    song_test = tfio.audio.AudioIOTensor(file_path)

    #read contents of file by slicing and removing last dimension
    song_slice = song_test[100:]
    song_tensor = tf.squeeze(song_slice)

    # visualize raw audio wave
    tensor = tf.cast(song_tensor, tf.float32) / 32768.0    

    # apply fade
    fade = tfio.audio.fade(tensor, fade_in=1000, fade_out=2000, mode='logarithmic')

    
    # convert to spectrogram
    # nnft: number of fast fourier transforms; 10,000 seems to work well
    # window: size of window?; if window is too small you will not be able to see it
    # stride: number of "hops" between windows?; not really sure what this means
    # defaults: nfft=10000, window=4000, stride=2000
    spectrogram = tfio.audio.spectrogram(
        fade, nfft=nfft, window=window, stride=stride
    )
    # save resulting image
    plt.imshow(tf.math.log(spectrogram).numpy())
    plt.axis('off')
    plt.savefig(label+'.jpeg')

# master spectrogram generation function given input path, output path, and other parameters for the spectrograms
def get_spectrograms(path_name, outpath, nfft=10000, window=4500, stride=3500):
    # set cwd to outpath
    os.chdir(outpath)
    
    # convert all mp3 to mono-channel .wav
    convert_mp3_wav(path_name)

    #generate spectrograms for each ouput wav from above
    for i, subpath in enumerate(os.listdir(path_name+'/output/')):
        #print(subpath)
        if '.wav' in subpath:
            file_path = path.join(path_name+'/output/', subpath)
            # label is subpathup to first period
            label = subpath.split('.')[0]+'_spec_'+str(nfft)+'_'+str(window)+'_'+str(stride)
            generate_spectrogram(file_path, label, nfft, window, stride)

        percent = round((i/len(os.listdir(path_name+'/output/')))*100, 3)
        print ('progress: ' + str(percent) + '%', end="\r")