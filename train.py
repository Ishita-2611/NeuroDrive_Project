import serial
import time
import csv
import json

# Set up serial connection (Adjust port & baud rate as per your EEG device)
ser = serial.Serial('COM3', 115200)  

# Change the label according to the command you are collecting
LABEL = 'focus'  # Example: 'focus', 'relax', 'left', 'right', 'blink'

# File names
csv_filename = f'eeg_data_{LABEL}.csv'
json_filename = f'eeg_data_{LABEL}.json'

# Open CSV file to save the data
with open(csv_filename, 'w', newline='') as csvfile, open(json_filename, 'w') as jsonfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'CH1', 'CH2', 'CH3', 'CH4', 'Label'])  # CSV header

    eeg_json = {"direction": {}}  # JSON structure
    
    print(f"Collecting EEG data for command: {LABEL}")
    print("Focus on the task. Data will be collected for 30 seconds.")

    start_time = time.time()
    duration = 30  # Collect data for 30 seconds

    while time.time() - start_time < duration:
        line = ser.readline().decode('utf-8').strip()  # Read serial input
        values = line.split(',')

        if len(values) == 4:  # Ensure 4-channel data
            try:
                # Convert to integers
                values = [int(v) for v in values]
                timestamp = f"ts{int(time.time() * 1000)}"  # Unique timestamp (milliseconds)

                # Save to CSV
                writer.writerow([timestamp] + values + [LABEL])

                # Save to JSON
                eeg_json["direction"][timestamp] = {
                    "Ch1": values[0],
                    "Ch2": values[1],
                    "Ch3": values[2],
                    "Ch4": values[3],
                    "Label": LABEL
                }

                print(f"{timestamp}: {values}")

            except ValueError:
                pass  # Ignore faulty readings

    # Write final JSON data to file
    json.dump(eeg_json, jsonfile, indent=4)

print(f"Data collection for '{LABEL}' completed.")
print(f"CSV saved as: {csv_filename}")
print(f"JSON saved as: {json_filename}")
