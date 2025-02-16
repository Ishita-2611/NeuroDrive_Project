import serial
import time
import csv

# Set up serial connection
ser = serial.Serial('COM3', 115200)  # Adjust COM port for your system

# Change the label according to the command you are collecting
LABEL = 'focus'  # Example: 'focus', 'relax', 'left', 'right', 'blink'

# File to save the data
filename = f'eeg_data_{LABEL}.csv'

# Open CSV file to save the data
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['CH1', 'CH2', 'CH3', 'CH4', 'Label'])

    print(f"Collecting EEG data for command: {LABEL}")
    print("Focus on the task. Data will be collected for 30 seconds.")

    start_time = time.time()
    duration = 30  # Collect data for 30 seconds

    while time.time() - start_time < duration:
        line = ser.readline().decode('utf-8').strip()
        values = line.split(',')
        if len(values) == 4:
            try:
                # Convert to integers
                values = [int(v) for v in values]
                values.append(LABEL)
                writer.writerow(values)
                print(values)
            except ValueError:
                pass

print(f"Data collection for {LABEL} completed. Saved to {filename}")