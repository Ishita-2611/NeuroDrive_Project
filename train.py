import serial
import time
import csv
import json
import uuid

# Set up serial connection (Adjust port & baud rate as per your EEG device)
ser = serial.Serial('COM4', 115200)

# Unique identifier for each person (Change manually or assign dynamically)
PERSON_ID = str(uuid.uuid4())[:8]  # Short unique ID (first 8 characters)

# Change the label according to the command you are collecting
LABEL = input("Enter the EEG label (e.g., focus, relax, left, right): ").strip().lower()

# File names (Include person ID and label for distinction)
csv_filename = f'eeg_data_{LABEL}_{PERSON_ID}.csv'
json_filename = f'eeg_data_{LABEL}_{PERSON_ID}.json'

# Open CSV file to save the data
with open(csv_filename, 'w', newline='') as csvfile, open(json_filename, 'w') as jsonfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Person_ID', 'Timestamp', 'CH1', 'CH2', 'CH3', 'CH4'])  # CSV header

    eeg_json = {LABEL: {}}  # JSON structure with only the label name

    print(f"Collecting EEG data for '{LABEL}' (Person ID: {PERSON_ID})")
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
                writer.writerow([PERSON_ID, timestamp] + values)

                # Save to JSON (Organized under the dynamically entered LABEL)
                eeg_json[LABEL][timestamp] = {
                    "Person_ID": PERSON_ID,
                    "Ch1": values[0],
                    "Ch2": values[1],
                    "Ch3": values[2],
                    "Ch4": values[3]
                }

                print(f"{timestamp}: {values}")

            except ValueError:
                pass  # Ignore faulty readings

    # Write final JSON data to file
    json.dump(eeg_json, jsonfile, indent=4)

print(f"✅ Data collection for '{LABEL}' completed (Person ID: {PERSON_ID})")
print(f"📁 CSV saved as: {csv_filename}")
print(f"📁 JSON saved as: {json_filename}")
