import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load JSON Data
with open('eeg_combined_data.json', 'r') as json_file:
    data = json.load(json_file)

# Convert JSON to DataFrame
records = []
for label, timestamps in data.items():
    for timestamp, values in timestamps.items():
        records.append({
            "CH1": values["Ch1"],
            "CH2": values["Ch2"],
            "CH3": values["Ch3"],
            "CH4": values["Ch4"],
            "Label": label  # Use label as target variable
        })

# Convert to DataFrame
df = pd.DataFrame(records)

# Features and Labels
X = df[['CH1', 'CH2', 'CH3', 'CH4']]
y = df['Label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.4f}")

# Save model
joblib.dump(model, 'eeg_model.pkl')
print("✅ Model saved as 'eeg_model.pkl'")
