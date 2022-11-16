import os 
from PIL import Image

#let us declare the path where our spectrogram is located
spectrogram_path = '/test/the 59th street bridge song'

#now let's get the spectrogram
os.chdir(spectrogram_path)
spectrogram = Image.open('spectrogram_test_1.PNG')
print(spectrogram.size)
spectrogram = Image.open('spectrogram_test_2.PNG')
print(spectrogram.size)
