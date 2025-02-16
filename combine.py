import json

# List of EEG data JSON files
files = [
    'eeg_data_focus_9e7b30e6.json',
    'eeg_data_left_19fb23ea.json',
    'eeg_data_relax_b2467bf2.json',
    'eeg_data_right_4d0c952b.json'
]

# Initialize JSON structure
eeg_json = {}

# Load and merge JSON files
for file in files:
    with open(file, 'r') as json_file:
        data = json.load(json_file)

        for label, timestamps in data.items():
            if label not in eeg_json:
                eeg_json[label] = {}  # Initialize label category

            eeg_json[label].update(timestamps)  # Merge timestamp data

# Save the combined dataset as a JSON file
json_filename = 'eeg_combined_data.json'
with open(json_filename, 'w') as json_file:
    json.dump(eeg_json, json_file, indent=4)

print(f"✅ Combined dataset saved as '{json_filename}'")
