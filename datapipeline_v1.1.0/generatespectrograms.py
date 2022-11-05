# python file to generate spectrograms given a file of mp3
# @oscars47

# imports-----------
# defaults
import os, librosa
from os import path
import numpy as np
import skimage.io

# for converting mp3 to wav for spectrogram generation
from pydub import AudioSegment

# define variables for use with our model-------
# _HOP_LENGTH = 512 # number of samples per time-step
# _N_MELS = 128 # number of bins in spectrogram --> height of image
# _TIME_STEPS = 384 # number of time steps --> width of image


_HOP_LENGTH = 1000 # number of samples per time-step
_N_MELS = 512 # number of bins in spectrogram --> height of image
_TIME_STEPS = 1000 # number of time steps --> width of image

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
# https://stackoverflow.com/questions/56719138/how-can-i-save-a-librosa-spectrogram-plot-as-a-specific-sized-image helped a lot

# helper function to rescale np.array to be normalized
def scaler(X, min = 0.0, max = 1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (max - min) + min
    return X_scaled

# function to actually generate spectrogram given librosa object and other params
def get_spectrogram(y, sr, out, hop_length, n_mels):
    # use the log-mel spec for best performance: visualizing DB instead of amplitude
    mels = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, 
                                            n_fft = hop_length*2, hop_length=hop_length)
    # convert to log; add small number so no log of 0
    mels = np.log(mels + 1e-9)

    # want min-max scale within 8-but range
    img = scaler(mels, 0, 255).astype(np.uint8)
    # put low frequencies at bottom of image
    img = np.flip(img, axis=0)
    # invert colors so black = more energy
    img = 255 - img

    # now save it as a png
    skimage.io.imsave(out, img)

# master spectrogram generation function given input path, output path, and other parameters for the spectrograms
# max duration for this config is 60s -- hence clipped
def get_spectrograms_master_clipped(path_name, outpath):
    # change cwd
    os.chdir(outpath)
    
    # convert all mp3 to mono-channel .wav
    convert_mp3_wav(path_name)

    #generate spectrograms for each ouput wav from above
    for i, subpath in enumerate(os.listdir(path_name+'/output/')):
        #print(subpath)
        if '.wav' in subpath:
            file_path = path.join(path_name+'/output/', subpath)

            # y is our librosa object; the sr is sampling rate of y
            #y, sr = librosa.load(file_path, offset=1.0, duration=duration, sr =22050) # duration is length of clip'
            y, sr = librosa.load(file_path, offset=1.0, sr =22050)

            # extract fixed length window
            start_sample = 0 # start at the beginning
            length_samples = _TIME_STEPS * _HOP_LENGTH
            window = y[start_sample: start_sample + length_samples] 
            #window=y # for complete song, include complete y

            # convert to png
            # label is subpathup to first period
            #label = subpath.split('.')[0]+'_spec_'+str(_HOP_LENGTH)+'_'+str(_N_MELS)+'_'+str(_TIME_STEPS) + '_' + str(duration)+ '.png'
            label = subpath.split('.')[0]+'_spec_'+str(_HOP_LENGTH)+'_'+str(_N_MELS)+'_'+str(_TIME_STEPS) + '.png'

            get_spectrogram(y=window, sr=sr, out = label, n_mels = _N_MELS, hop_length = _HOP_LENGTH)
            #print('wrote file', label)

        # percent = round((i/len(os.listdir(path_name+'/output/')))*100, 3)
        # print ('progress: ' + str(percent) + '%', end="\r")

def get_spectrograms_master_all(path_name, outpath):
    # change cwd
    os.chdir(outpath)
    
    # convert all mp3 to mono-channel .wav
    convert_mp3_wav(path_name)

    #generate spectrograms for each ouput wav from above
    for i, subpath in enumerate(os.listdir(path_name+'/output/')):
        #print(subpath)
        if '.wav' in subpath:
            file_path = path.join(path_name+'/output/', subpath)

            # y is our librosa object; the sr is sampling rate of y
            #y, sr = librosa.load(file_path, offset=1.0, duration=duration, sr =22050) # duration is length of clip'
            y, sr = librosa.load(file_path, offset=1.0, sr =22050)

            # extract fixed length window
            start_sample = 0 # start at the beginning
            length_samples = _TIME_STEPS * _HOP_LENGTH
            #window = y[start_sample: start_sample + length_samples] 
            window=y # for complete song, include complete y

            # convert to png
            # label is subpathup to first period
            #label = subpath.split('.')[0]+'_spec_'+str(_HOP_LENGTH)+'_'+str(_N_MELS)+'_'+str(_TIME_STEPS) + '_' + str(duration)+ '.png'
            label = subpath.split('.')[0]+'_spec_'+str(_HOP_LENGTH)+'_'+str(_N_MELS)+'_'+str(_TIME_STEPS) + '_ALL.png'

            get_spectrogram(y=window, sr=sr, out = label, n_mels = _N_MELS, hop_length = _HOP_LENGTH)
            #print('wrote file', label)