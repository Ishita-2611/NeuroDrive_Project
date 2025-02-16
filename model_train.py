import pandas as pd
import json
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load EEG data from JSON file
json_filename = 'eeg_data_focus.json'  # Change based on the collected data
with open(json_filename, 'r') as file:
    eeg_json = json.load(file)

# Convert JSON to DataFrame
data = []
for timestamp, values in eeg_json["direction"].items():
    row = [timestamp, values["Ch1"], values["Ch2"], values["Ch3"], values["Ch4"], values["Label"]]
    data.append(row)

# Create DataFrame
df = pd.DataFrame(data, columns=["Timestamp", "CH1", "CH2", "CH3", "CH4", "Label"])

# Drop Timestamp as it's not needed for training
df.drop(columns=["Timestamp"], inplace=True)

# Features and Labels
X = df[['CH1', 'CH2', 'CH3', 'CH4']]
y = df['Label']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the trained model
model_filename = 'eeg_model.pkl'
joblib.dump(model, model_filename)
print(f"Model saved as '{model_filename}'")
