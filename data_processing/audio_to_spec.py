import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import os,sys
import ffmpeg



# Load the first 1.2 seconds of the WAV file
data, sample_rate = librosa.load('test.wav', sr=None, duration=5)

# Generate a mel-spectrogram
S = librosa.feature.melspectrogram(y=data, sr=sample_rate, n_mels=128, fmax=8000)

# Convert the mel-spectrogram to decibels for visualization
S_dB = librosa.power_to_db(S, ref=np.max)

# Plot the mel-spectrogram
plt.figure(figsize=(10, 4))
librosa.display.specshow(S_dB, sr=sample_rate, x_axis='time', y_axis='mel', fmax=8000)
plt.colorbar(format='%+2.0f dB')
plt.title('Mel-spectrogram')
plt.tight_layout()
plt.show()