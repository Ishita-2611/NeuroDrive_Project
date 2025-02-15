from brainflow.board_shim import BoardShim, BrainFlowInputParams
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch

# Configure BrainFlow parameters
params = BrainFlowInputParams()
params.serial_port = "COM3"  # Change based on your system

# Initialize Board (Replace `2` with your board ID if different)
board = BoardShim(2, params)

# Start EEG session
board.prepare_session()
board.start_stream()
print("Collecting EEG data...")

# Collect data for 30 seconds
time.sleep(30)

# Stop and retrieve data
board.stop_stream()
data = board.get_board_data()
board.release_session()

# Convert to DataFrame and save
df = pd.DataFrame(data)
df.to_csv("eeg_data.csv", index=False)
print("Data saved to eeg_data.csv")

### STEP 1: Load the collected EEG data
df = pd.read_csv("eeg_data.csv")
print("EEG Data Loaded:", df.shape)

# Assuming first N rows are EEG channels (adjust based on your device)
eeg_channels = df.iloc[:4, :]  # Adjust according to the number of EEG channels

### STEP 2: Apply Bandpass Filter to Remove Noise
def bandpass_filter(data, lowcut=0.5, highcut=50, fs=250, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# Filter all EEG channels
filtered_eeg = eeg_channels.apply(lambda x: bandpass_filter(x, 0.5, 50, 250), axis=1)

### STEP 3: Compute Power Spectral Density (PSD)
def compute_psd(data, fs=250):
    freqs, psd = welch(data, fs=fs, nperseg=256)
    return freqs, psd

freqs, psd_values = compute_psd(filtered_eeg.iloc[0, :])  # Compute PSD for first EEG channel

### STEP 4: Visualization of EEG Signals
plt.figure(figsize=(10, 4))
plt.plot(filtered_eeg.iloc[0, :])
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Filtered EEG Signal (First Channel)")
plt.show()

# Plot PSD
plt.figure(figsize=(10, 4))
plt.semilogy(freqs, psd_values)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power Spectral Density")
plt.title("Power Spectral Density of EEG Signal")
plt.show()
