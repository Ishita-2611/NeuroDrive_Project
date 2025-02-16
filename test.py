import serial
import joblib
import numpy as np

# Load trained model
model = joblib.load('eeg_model.pkl')

# Connect to EEG device (adjust COM port as needed)
ser = serial.Serial('COM4', 115200)

print("🔹 Listening for EEG data...")

while True:
    line = ser.readline().decode('utf-8').strip()
    values = line.split(',')

    if len(values) == 4:
        try:
            # Convert values to integers
            values = np.array([int(v) for v in values]).reshape(1, -1)
            
            # Predict using trained model
            prediction = model.predict(values)
            print(f"🔮 Predicted Command: {prediction[0]}")
        except ValueError:
            print("⚠️ Invalid data received, skipping...")
            continue
