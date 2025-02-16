import serial
import joblib

# Load trained model
model = joblib.load('eeg_model.pkl')

# Connect to Maker UNO
ser = serial.Serial('COM4', 115200)

while True:
    line = ser.readline().decode('utf-8').strip()
    values = line.split(',')

    if len(values) == 4:
        try:
            values = [int(v) for v in values]
            prediction = model.predict([values])
            print(f"Predicted Command: {prediction[0]}")
        except ValueError:
            pass