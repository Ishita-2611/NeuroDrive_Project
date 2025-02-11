import serial
import numpy as np
from scipy import signal
import pandas as pd
import time
import pickle

from collections import deque 

# Setup serial connections
EEG_PORT = "/dev/ttyUSB0"  # Change based on your EEG module port
CAR_PORT = "/dev/ttyUSB1"  # Change based on your car control module
BAUD_RATE = 115200

eeg_ser = serial.Serial(EEG_PORT, BAUD_RATE, timeout=1)
car_ser = serial.Serial(CAR_PORT, BAUD_RATE, timeout=1)

# Load the trained model & scaler
with open("model.pkl", "rb") as f:
    clf = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Setup filters
def setup_filters(sampling_rate=512):
    b_notch, a_notch = signal.iirnotch(50.0 / (0.5 * sampling_rate), 30.0)
    b_bandpass, a_bandpass = signal.butter(4, [0.5 / (0.5 * sampling_rate), 30.0 / (0.5 * sampling_rate)], 'band')
    return b_notch, a_notch, b_bandpass, a_bandpass

b_notch, a_notch, b_bandpass, a_bandpass = setup_filters()

# Function to filter EEG data
def process_eeg_data(data):
    data = signal.filtfilt(b_notch, a_notch, data)
    data = signal.filtfilt(b_bandpass, a_bandpass, data)
    return data

# Extract EEG features
def calculate_features(segment, sampling_rate=512):
    f, psd_values = signal.welch(segment, fs=sampling_rate, nperseg=len(segment))
    bands = {"alpha": (8, 13), "beta": (14, 30), "theta": (4, 7), "delta": (0.5, 3)}
    features = {}
    for band, (low, high) in bands.items():
        idx = np.where((f >= low) & (f <= high))
        features[f"E_{band}"] = np.sum(psd_values[idx])
    features["alpha_beta_ratio"] = features["E_alpha"] / features["E_beta"] if features["E_beta"] > 0 else 0
    return features

# Buffer for EEG data
buffer = deque(maxlen=512)

print("Starting EEG-based car control...")

# Main loop
while True:
    try:
        raw_data = eeg_ser.readline().decode("utf-8").strip()
        if raw_data:
            eeg_value = float(raw_data)
            buffer.append(eeg_value)

            if len(buffer) == 512:  # Process after collecting enough data
                buffer_array = np.array(buffer)
                processed_data = process_eeg_data(buffer_array)
                features = calculate_features(processed_data)

                # Convert to DataFrame for ML model
                df = pd.DataFrame([features])
                X_scaled = scaler.transform(df)
                prediction = clf.predict(X_scaled)[0]  # Predicted movement

                print(f"Predicted Movement: {prediction}")

                # Send command to car
                movement_commands = {
                    0: "FORWARD",
                    1: "LEFT",
                    2: "RIGHT",
                    3: "BRAKE",
                    4: "REVERSE",
                    5: "OVERTAKE",
                    6: "BACKWARD"
                }

                command = movement_commands.get(prediction, "STOP")
                car_ser.write((command + "\n").encode())  # Send to car

                buffer.clear()  # Reset buffer for next cycle

    except Exception as e:
        print(f"Error: {e}")
        continue