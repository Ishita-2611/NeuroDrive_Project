import json

# Load JSON Data
with open('eeg_combined_data.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize new structured JSON
structured_data = {}

# Iterate over the data
for label, timestamps in data.items():  # label = focus, relax, right, left
    if label not in structured_data:
        structured_data[label] = {
            "Ch1": [],
            "Ch2": [],
            "Ch3": [],
            "Ch4": []
        }

    for timestamp, values in timestamps.items():
        # Append channel values under corresponding label
        structured_data[label]["Ch1"].append(values["Ch1"])
        structured_data[label]["Ch2"].append(values["Ch2"])
        structured_data[label]["Ch3"].append(values["Ch3"])
        structured_data[label]["Ch4"].append(values["Ch4"])

# Save the new structured JSON
json_filename = 'eeg_structured_data.json'
with open(json_filename, 'w') as json_file:
    json.dump(structured_data, json_file, indent=4)

print(f"✅ Restructured dataset saved as '{json_filename}'")
